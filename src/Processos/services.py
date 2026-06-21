import datetime
import json
import logging
import time

import requests
from django.utils import timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from Processos.models import ProcessoLegislativo, Movimentacao

CAMARA_API_BASE = "https://dadosabertos.camara.leg.br/api/v2"
SENADO_API_BASE = "https://legis.senado.leg.br/dadosabertos"
SENADO_PROCESSO_BASE = f"{SENADO_API_BASE}/processo"
SENADO_HEADERS = {"Accept": "application/json"}
CAMARA_PAGE_SIZE = 100
DEFAULT_DATA_INICIO = "2000-01-01"
DEFAULT_ANO_INICIO = 2000
REQUEST_TIMEOUT = 30
BULK_INSERT_SIZE = 1000
RATE_LIMIT_DELAY = 0.2  # 200ms entre chamadas individuais de detalhes

logger = logging.getLogger(__name__)

def _build_session():
    """Cria sessão HTTP com retry automático e exponential backoff."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s entre retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

_SESSION = _build_session()

def _parse_date(value: str):
    if not value:
        return None
    try:
        if "T" in value:
            return datetime.datetime.fromisoformat(value).date()
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None

def _parse_datetime(value: str):
    if not value:
        return None
    try:
        if "T" in value:
            parsed = datetime.datetime.fromisoformat(value)
        else:
            parsed = datetime.datetime.fromisoformat(f"{value}T00:00:00")
    except ValueError:
        return None

    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed

def _get_json(url, params=None, headers=None):
    """Faz GET e retorna JSON. Retorna None em caso de falha."""
    try:
        response = _SESSION.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        logger.warning("Falha na requisicao %s: %s", url, exc)
        return None

    if response.status_code != 200:
        logger.warning("Resposta %s para %s", response.status_code, url)
        return None

    try:
        return response.json()
    except ValueError:
        logger.warning("JSON invalido para %s", url)
        return None

def _coerce_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def _extract_ano_camara(ano_raw, data_apresentacao):
    ano_str = str(ano_raw or "")
    if ano_str and ano_str != "0":
        return ano_str
    if data_apresentacao:
        return str(data_apresentacao.year)
    return ""

def _gerar_notificacao_atualizacao(processo, movimentacao):
    from Usuarios.models import Notificacao
    usuarios = processo.users.all()
    for user in usuarios:
        Notificacao.objects.create(
            user=user,
            processo=processo,
            tipo='ATUALIZACAO',
            mensagem=f"Nova movimentação no processo {processo.numero}/{processo.ano}: {movimentacao.descricao}"
        )

# ============================================================================
# API da Câmara dos Deputados
# ============================================================================

def buscar_todas_proposicoes_camara(termo: str = None, ano: int = None, data_inicio: str = None):
    """
    Busca as proposições na API de Dados Abertos da Câmara, lidando com a paginação.
    Se 'termo' for None, busca todas as proposições do 'ano' (se fornecido).
    """
    url = f"{CAMARA_API_BASE}/proposicoes"
    params = {
        "itens": CAMARA_PAGE_SIZE,  # Recomendado pela doc da camara (maximo 100 por pagina)
        "ordem": "DESC",
        "ordenarPor": "ano",
    }
    if ano:
        params["ano"] = ano
    if termo:
        params["keywords"] = termo
    if data_inicio:
        params["dataInicio"] = data_inicio

    todas_proposicoes = []

    while url:
        payload = _get_json(url, params=params)
        if not payload:
            break

        todas_proposicoes.extend(payload.get("dados", []))
        links = payload.get("links", [])
        next_link = next((link["href"] for link in links if link.get("rel") == "next"), None)

        if next_link:
            url = next_link
            params = None  # Os params ja vem embutidos na URL 'next'.
        else:
            url = None

    return todas_proposicoes

def buscar_detalhe_camara(id_externo: str):
    payload = _get_json(f"{CAMARA_API_BASE}/proposicoes/{id_externo}")
    if not payload:
        return {}
    return payload.get("dados", {})

def buscar_tramitacoes_camara(id_externo: str):
    payload = _get_json(f"{CAMARA_API_BASE}/proposicoes/{id_externo}/tramitacoes")
    if not payload:
        return []
    return payload.get("dados", [])

def atualizar_detalhes_camara(processo: ProcessoLegislativo, incluir_tramitacoes: bool = True):
    dados = buscar_detalhe_camara(processo.id_externo)
    if not dados:
        return False

    status = dados.get('statusProposicao', {})
    processo.descricao_tramitacao = status.get('descricaoTramitacao')
    processo.descricao_situacao = status.get('descricaoSituacao')
    processo.status_atual = (
        status.get('descricaoSituacao')
        or status.get('descricaoTramitacao')
        or processo.status_atual
    )
    processo.orgao_atual = status.get('siglaOrgao')
    processo.url_orgao_atual = status.get('uriOrgao')
    processo.regime = status.get('regime')
    processo.apreciacao = status.get('apreciacao')
    processo.despacho = status.get('despacho')
    processo.data_status = _parse_datetime(status.get('dataHora'))
    processo.uri_ultimo_relator = status.get('uriUltimoRelator')

    processo.url_autores = dados.get('uriAutores')
    processo.url_inteiro_teor = dados.get('urlInteiroTeor')
    processo.url_detalhe = dados.get('uri') or processo.url_detalhe
    processo.ementa_detalhada = dados.get('ementaDetalhada')
    processo.keywords = dados.get('keywords')
    processo.descricao_tipo = dados.get('descricaoTipo')
    data_apresentacao = _parse_date(dados.get('dataApresentacao')) or processo.data_apresentacao
    processo.data_apresentacao = data_apresentacao

    if dados.get('numero') is not None:
        processo.numero = str(dados.get('numero'))

    ano_value = _extract_ano_camara(dados.get('ano'), data_apresentacao)
    if ano_value:
        processo.ano = ano_value

    processo.tipo_proposicao = dados.get('siglaTipo') or processo.tipo_proposicao
    processo.ementa = dados.get('ementa') or processo.ementa

    processo.dados_extra_json = json.dumps(dados, ensure_ascii=True)
    if incluir_tramitacoes:
        tramitacoes = buscar_tramitacoes_camara(processo.id_externo)
        processo.tramitacao_json = json.dumps(tramitacoes, ensure_ascii=True)
        
        # Extrair Movimentacao
        for tramitacao in tramitacoes:
            data_hora_str = tramitacao.get('dataHora')
            if not data_hora_str:
                continue
                
            data_evento = _parse_datetime(data_hora_str)
            
            descricao = tramitacao.get('despacho') or tramitacao.get('descricaoTramitacao') or "Movimentação registrada"
            comissao = tramitacao.get('siglaOrgao')
            
            mov, created = Movimentacao.objects.get_or_create(
                processo=processo,
                data_evento=data_evento,
                descricao=descricao,
                defaults={
                    'comissao_atual': comissao
                }
            )
            if created:
                _gerar_notificacao_atualizacao(processo, mov)

    processo.detalhes_atualizados_em = timezone.now()
    processo.save()
    return True

# ============================================================================
# API do Senado Federal
# ============================================================================

def buscar_todos_processos_senado(ano=None):
    """
    Busca TODOS os processos em tramitação ou de um determinado ano na nova API do Senado.
    """
    params = {}
    if ano:
        params['ano'] = ano
        
    payload = _get_json(SENADO_PROCESSO_BASE, headers=SENADO_HEADERS, params=params)
    if not payload:
        logger.warning("Falha ao buscar processos do Senado na nova API")
        return []
    if isinstance(payload, list):
        return payload
    return payload.get("dados", payload.get("processos", []))

def buscar_detalhe_senado(id_processo: str):
    """
    Busca detalhes de um processo na nova API do Senado.
    """
    url = f"{SENADO_PROCESSO_BASE}/{id_processo}"
    payload = _get_json(url, headers=SENADO_HEADERS)
    if not payload:
        return {}
    return payload

def _mapear_processo_senado_da_listagem(proc: dict) -> dict:
    data_apresentacao = _parse_date(proc.get('dataApresentacao'))
    ano_raw = proc.get('ano') or proc.get('Ano')
    ano_str = str(ano_raw) if ano_raw else ""
    if not ano_str and data_apresentacao:
        ano_str = str(data_apresentacao.year)

    identificacao = proc.get('identificacao', '')
    sigla = proc.get('sigla') or proc.get('Sigla', '')
    numero = proc.get('numero') or proc.get('Numero', '')
    if not numero and identificacao:
        parts = identificacao.split()
        if len(parts) >= 2:
            num_part = parts[-1].split('/')[0] if '/' in parts[-1] else parts[-1]
            try:
                int(num_part)
                numero = num_part
            except ValueError:
                pass

    tramitando_str = proc.get('tramitando', '')
    tramitando = True if tramitando_str == 'Sim' else (False if tramitando_str == 'Não' else None)

    def _trunc(v, max_len=255):
        if not v:
            return ""
        return str(v)[:max_len]

    return {
        'numero': _trunc(numero),
        'ano': _trunc(ano_str),
        'ementa': proc.get('ementa', ''),
        'tipo_proposicao': _trunc(sigla),
        'status_atual': _trunc(proc.get('situacaoAtual', '')),
        'autor': _trunc(proc.get('autoria', '')),
        'descricao_identificacao': _trunc(identificacao),
        'data_apresentacao': data_apresentacao,
        'url_detalhe': None,
        'id_processo_senado': _trunc(proc.get('id', ''), 50),
        'tipo_conteudo': _trunc(proc.get('tipoConteudo', '')),
        'tipo_documento': _trunc(proc.get('tipoDocumento', '')),
        'tramitando': tramitando,
        'apelido': _trunc(proc.get('apelido', ''), 500),
        'casa_identificadora': _trunc(proc.get('casaIdentificadora', ''), 10),
        'norma_gerada': _trunc(proc.get('normaGerada', '')),
        'objetivo': _trunc(proc.get('objetivo', ''), 100),
    }

def _fetch_and_create_movimentacoes_senado(processo):
    try:
        url = f"https://legis.senado.leg.br/dadosabertos/materia/movimentacoes/{processo.id_externo}"
        response = _SESSION.get(url, headers={'Accept': 'application/json'}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            materia = data.get('MovimentacaoMateria', {}).get('Materia', {})
            autuacoes = materia.get('Autuacoes', {}).get('Autuacao', [])
            
            if isinstance(autuacoes, dict):
                autuacoes = [autuacoes]
                
            for autuacao in autuacoes:
                informes = autuacao.get('InformesLegislativos', {}).get('InformeLegislativo', [])
                if isinstance(informes, dict):
                    informes = [informes]
                    
                for informe in informes:
                    data_hora_str = informe.get('Data')
                    if not data_hora_str:
                        continue
                        
                    data_evento = _parse_datetime(data_hora_str)
                    
                    descricao = informe.get('Descricao') or "Movimentação registrada"
                    local = informe.get('Local', {})
                    comissao = local.get('SiglaLocal') or local.get('NomeLocal')
                    
                    mov, created = Movimentacao.objects.get_or_create(
                        processo=processo,
                        data_evento=data_evento,
                        descricao=descricao,
                        defaults={
                            'comissao_atual': comissao
                        }
                    )
                    if created:
                        _gerar_notificacao_atualizacao(processo, mov)
    except Exception as e:
        logger.error(f"Erro ao sincronizar movimentações do Senado para {processo.id_externo}: {e}")

def atualizar_detalhes_senado(processo: ProcessoLegislativo, incluir_tramitacoes: bool = True):
    id_processo = processo.id_processo_senado
    if not id_processo:
        logger.warning("Processo %s sem id_processo_senado, impossível buscar detalhes", processo.id_externo)
        return False

    detalhes = buscar_detalhe_senado(id_processo)
    if not detalhes:
        return False

    processo.status_atual = detalhes.get('situacaoAtual') or processo.status_atual

    conteudo = detalhes.get('conteudo', {})
    if conteudo:
        ementa_conteudo = conteudo.get('ementa')
        if ementa_conteudo:
            processo.ementa = ementa_conteudo
        processo.tipo_conteudo = conteudo.get('tipo') or processo.tipo_conteudo

    ementa_raiz = detalhes.get('ementa')
    if ementa_raiz and not conteudo.get('ementa'):
        processo.ementa = ementa_raiz

    documento = detalhes.get('documento', {})
    if documento:
        data_apres = _parse_date(documento.get('dataApresentacao'))
        if data_apres:
            processo.data_apresentacao = data_apres

        processo.indexacao = documento.get('indexacao') or processo.indexacao
        url_doc = documento.get('url')
        if url_doc:
            processo.url_inteiro_teor = url_doc

        autorias = documento.get('autoria', [])
        if autorias and isinstance(autorias, list):
            autores_str = ', '.join(
                f"{a.get('autor', '')} ({a.get('siglaPartido', '')}/{a.get('uf', '')})"
                if a.get('siglaPartido') else a.get('autor', '')
                for a in autorias
            )
            processo.autor = autores_str

    processo.tipo_documento = detalhes.get('tipoDocumento') or processo.tipo_documento
    processo.casa_identificadora = detalhes.get('casaIdentificadora') or processo.casa_identificadora
    processo.objetivo = detalhes.get('objetivo') or processo.objetivo
    processo.apelido = detalhes.get('apelido') or processo.apelido
    processo.norma_gerada = detalhes.get('normaGerada') or processo.norma_gerada

    identificacao = detalhes.get('identificacao', '')
    if identificacao:
        processo.descricao_identificacao = identificacao

    sigla = detalhes.get('sigla')
    if sigla:
        processo.tipo_proposicao = sigla

    desc_sigla = detalhes.get('descricaoSigla')
    if desc_sigla:
        processo.descricao_tipo = desc_sigla

    numero = detalhes.get('numero')
    if numero is not None:
        processo.numero = str(numero)

    ano = detalhes.get('ano')
    if ano is not None:
        processo.ano = str(ano)

    data_situacao = _parse_datetime(detalhes.get('dataSituacaoAtual'))
    if data_situacao:
        processo.data_status = data_situacao

    tramitando_str = detalhes.get('tramitando', '')
    if tramitando_str:
        processo.tramitando = tramitando_str == 'Sim'

    processo.dados_extra_json = json.dumps(detalhes, ensure_ascii=True, default=str)

    if incluir_tramitacoes:
        processo.tramitacao_json = json.dumps(detalhes, ensure_ascii=True, default=str)
        _fetch_and_create_movimentacoes_senado(processo)

    processo.detalhes_atualizados_em = timezone.now()
    processo.save()
    return True

# ============================================================================
# Funções genéricas
# ============================================================================

def atualizar_detalhes_processo(processo: ProcessoLegislativo, incluir_tramitacoes: bool = True):
    if processo.origem_camara_ou_senado == 'CAMARA':
        return atualizar_detalhes_camara(processo, incluir_tramitacoes=incluir_tramitacoes)
    if processo.origem_camara_ou_senado == 'SENADO':
        return atualizar_detalhes_senado(processo, incluir_tramitacoes=incluir_tramitacoes)
    return False

# ============================================================================
# Sincronização incremental e utilidades
# ============================================================================

def sincronizar_processos_legislativos(data_inicio: str = DEFAULT_DATA_INICIO, ano_inicio: int = DEFAULT_ANO_INICIO):
    novos_processos_criados = 0
    processos_camara_atualizados = set()
    processos_senado_atualizados = set()

    logger.info("Iniciando sincronização da Câmara dos Deputados...")
    proposicoes_camara = buscar_todas_proposicoes_camara(None, data_inicio=data_inicio)
    
    for prop in proposicoes_camara:
        id_externo = str(prop.get('id', ''))
        if not id_externo:
            continue

        data_apresentacao = _parse_date(prop.get('dataApresentacao'))
        ano_str = _extract_ano_camara(prop.get('ano'), data_apresentacao)

        processo, created = ProcessoLegislativo.objects.get_or_create(
            id_externo=id_externo,
            origem_camara_ou_senado='CAMARA',
            defaults={
                'numero': str(prop.get('numero', '')),
                'ano': ano_str,
                'ementa': prop.get('ementa', ''),
                'tipo_proposicao': prop.get('siglaTipo', ''),
                'status_atual': '',
                'data_apresentacao': data_apresentacao,
                'url_detalhe': prop.get('uri'),
            }
        )
        if created:
            novos_processos_criados += 1

        if id_externo not in processos_camara_atualizados:
            atualizar_detalhes_camara(processo, incluir_tramitacoes=True)
            processos_camara_atualizados.add(id_externo)
            time.sleep(RATE_LIMIT_DELAY)

    logger.info("Iniciando sincronização do Senado Federal...")
    todos_processos_senado = buscar_todos_processos_senado(ano=ano_inicio)

    for proc in todos_processos_senado:
        codigo_materia = str(proc.get('codigoMateria', ''))
        if not codigo_materia:
            continue

        defaults = _mapear_processo_senado_da_listagem(proc)

        processo, created = ProcessoLegislativo.objects.get_or_create(
            id_externo=codigo_materia,
            origem_camara_ou_senado='SENADO',
            defaults=defaults,
        )
        if created:
            novos_processos_criados += 1
        else:
            if not processo.id_processo_senado and defaults.get('id_processo_senado'):
                processo.id_processo_senado = defaults['id_processo_senado']
                processo.save(update_fields=['id_processo_senado'])

        if codigo_materia not in processos_senado_atualizados and processo.id_processo_senado:
            atualizar_detalhes_senado(processo, incluir_tramitacoes=True)
            processos_senado_atualizados.add(codigo_materia)
            time.sleep(RATE_LIMIT_DELAY)

    return novos_processos_criados

def popular_banco_carga_inicial(ano_inicio=2024):
    total_antes = ProcessoLegislativo.objects.count()
    buffer = []
    
    proposicoes_camara = buscar_todas_proposicoes_camara(ano=ano_inicio)
    for prop in proposicoes_camara:
        id_externo = str(prop.get('id', ''))
        data_apresentacao = _parse_date(prop.get('dataApresentacao'))
        ano_str = _extract_ano_camara(prop.get('ano'), data_apresentacao)
        numero_str = str(prop.get('numero', ''))
        
        if not id_externo:
            continue

        buffer.append(
            ProcessoLegislativo(
                id_externo=id_externo,
                origem_camara_ou_senado='CAMARA',
                numero=numero_str,
                ano=ano_str,
                ementa=prop.get('ementa', ''),
                tipo_proposicao=prop.get('siglaTipo', ''),
                status_atual='',
                data_apresentacao=data_apresentacao,
                url_detalhe=prop.get('uri')
            )
        )

        campos_atualizacao_camara = [
            'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual', 
            'data_apresentacao', 'url_detalhe'
        ]

        if len(buffer) >= BULK_INSERT_SIZE:
            ProcessoLegislativo.objects.bulk_create(
                buffer,
                update_conflicts=True,
                update_fields=campos_atualizacao_camara,
                unique_fields=['id_externo', 'origem_camara_ou_senado'],
                batch_size=BULK_INSERT_SIZE,
            )
            buffer.clear()

    if buffer:
        ProcessoLegislativo.objects.bulk_create(
            buffer,
            update_conflicts=True,
            update_fields=campos_atualizacao_camara,
            unique_fields=['id_externo', 'origem_camara_ou_senado'],
            batch_size=BULK_INSERT_SIZE,
        )
        buffer.clear()

    todos_processos_senado = buscar_todos_processos_senado()
    for proc in todos_processos_senado:
        codigo_materia = str(proc.get('codigoMateria', ''))
        if not codigo_materia:
            continue

        ano_proc = proc.get('ano')
        if ano_proc and isinstance(ano_proc, int) and ano_proc < ano_inicio:
            continue

        defaults = _mapear_processo_senado_da_listagem(proc)
        tramitando_val = defaults.pop('tramitando', None)

        buffer.append(
            ProcessoLegislativo(
                id_externo=codigo_materia,
                origem_camara_ou_senado='SENADO',
                tramitando=tramitando_val,
                **defaults,
            )
        )

        campos_atualizacao_senado = [
            'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual', 'autor',
            'descricao_identificacao', 'data_apresentacao', 'url_detalhe',
            'id_processo_senado', 'tipo_conteudo', 'tipo_documento', 'tramitando',
            'apelido', 'casa_identificadora', 'norma_gerada', 'objetivo'
        ]

        if len(buffer) >= BULK_INSERT_SIZE:
            ProcessoLegislativo.objects.bulk_create(
                buffer,
                update_conflicts=True,
                update_fields=campos_atualizacao_senado,
                unique_fields=['id_externo', 'origem_camara_ou_senado'],
                batch_size=BULK_INSERT_SIZE,
            )
            buffer.clear()

    if buffer:
        ProcessoLegislativo.objects.bulk_create(
            buffer,
            update_conflicts=True,
            update_fields=campos_atualizacao_senado,
            unique_fields=['id_externo', 'origem_camara_ou_senado'],
            batch_size=BULK_INSERT_SIZE,
        )

    total_depois = ProcessoLegislativo.objects.count()
    return total_depois - total_antes

def sincronizar_processo_on_demand(processo: ProcessoLegislativo) -> bool:
    """
    Sincroniza um único processo legislativo sob demanda.
    Sempre faz a consulta na API, ignorando cache, para garantir a atualização.
    """
    agora = timezone.now()
    
    logger.info(f"Processo {processo.id_externo} desatualizado. Buscando novas tramitações na API...")
    try:
        if processo.origem_camara_ou_senado == 'CAMARA':
            atualizar_detalhes_camara(processo, incluir_tramitacoes=True)
        else:
            atualizar_detalhes_senado(processo, incluir_tramitacoes=True)
            
        processo.detalhes_atualizados_em = agora
        processo.save(update_fields=['detalhes_atualizados_em'])
        return True
    except Exception as e:
        logger.error(f"Erro ao atualizar sob demanda o processo {processo.id_externo}: {e}")
        return False

def previsao_tempo_conclusao(processo):
    """
    Serviço simples para previsão de tempo de conclusão do processo.
    """
    progresso = getattr(processo, 'progresso_percentual', 0)
    if progresso == 100:
        return 0
    elif progresso == 75:
        return 30
    elif progresso == 50:
        return 60
    elif progresso == 25:
        return 180
    else:
        return 365
