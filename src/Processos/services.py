import datetime
import json
import logging

import requests
from django.utils import timezone

from Processos.models import ProcessoLegislativo


CAMARA_API_BASE = "https://dadosabertos.camara.leg.br/api/v2"
SENADO_API_BASE = "https://legis.senado.leg.br/dadosabertos"
SENADO_HEADERS = {"Accept": "application/json"}
CAMARA_PAGE_SIZE = 100
DEFAULT_DATA_INICIO = "2000-01-01"
DEFAULT_ANO_INICIO = 2000
REQUEST_TIMEOUT = 15
BULK_INSERT_SIZE = 1000

logger = logging.getLogger(__name__)


def _build_session():
    return requests.Session()


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
    for attempt in range(2):
        timeout = REQUEST_TIMEOUT if attempt == 1 else None
        try:
            response = _SESSION.get(url, params=params, headers=headers, timeout=timeout)
        except requests.RequestException as exc:
            logger.warning("Falha na requisicao %s (tentativa %s/2): %s", url, attempt + 1, exc)
            if attempt == 0:
                continue
            return None

        if response.status_code != 200:
            logger.warning("Resposta %s para %s", response.status_code, url)
            return None

        try:
            return response.json()
        except ValueError:
            logger.warning("JSON invalido para %s", url)
            return None

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


def buscar_todas_proposicoes_camara(termo: str = None, data_inicio: str = "2000-01-01"):
    """
    Busca as proposições na API de Dados Abertos da Câmara, lidando com a paginação.
    Se 'termo' for None, busca todas as proposições desde 'data_inicio'.
    """
    url = f"{CAMARA_API_BASE}/proposicoes"
    params = {
        "dataInicio": data_inicio,
        "itens": CAMARA_PAGE_SIZE,  # Recomendado pela doc da camara (maximo 100 por pagina)
        "ordem": "DESC",
        "ordenarPor": "ano",
    }
    if termo:
        params["keywords"] = termo

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


def buscar_materias_senado(termo: str = None, ano: int = None):
    """
    Busca materias na API de Dados Abertos do Senado.
    Se 'termo' for None e 'ano' for passado, busca todas do ano.
    """
    url = f"{SENADO_API_BASE}/materia/pesquisa/lista"
    params = {}
    if termo:
        params["palavraChave"] = termo
    if ano:
        params["ano"] = ano

    payload = _get_json(url, params=params, headers=SENADO_HEADERS)
    if not payload:
        return []

    return (
        payload
        .get("PesquisaBasicaMateria", {})
        .get("Materias", {})
        .get("Materia", [])
    )


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


def buscar_detalhe_senado(id_externo: str):
    payload = _get_json(f"{SENADO_API_BASE}/materia/{id_externo}", headers=SENADO_HEADERS)
    if not payload:
        return {}
    return payload.get("DetalheMateria", {}).get("Materia", {})


def buscar_tramitacoes_senado(id_externo: str):
    payload = _get_json(
        f"{SENADO_API_BASE}/materia/movimentacoes/{id_externo}",
        headers=SENADO_HEADERS,
    )
    if not payload:
        return {}
    return payload


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

    processo.detalhes_atualizados_em = timezone.now()
    processo.save()
    return True


def atualizar_detalhes_senado(processo: ProcessoLegislativo, incluir_tramitacoes: bool = True):
    materia = buscar_detalhe_senado(processo.id_externo)
    if not materia:
        return False

    identificacao = materia.get('IdentificacaoMateria', {})
    dados_basicos = materia.get('DadosBasicosMateria', {})
    origem = materia.get('OrigemMateria', {})
    decisao_destino = materia.get('DecisaoEDestino', {})
    decisao = decisao_destino.get('Decisao', {})

    processo.status_atual = decisao.get('Descricao') or processo.status_atual
    processo.data_status = _parse_datetime(decisao.get('Data'))
    processo.despacho = decisao.get('Descricao') or processo.despacho

    processo.autor = dados_basicos.get('Autor')
    processo.ementa = dados_basicos.get('EmentaMateria') or processo.ementa
    processo.indexacao = dados_basicos.get('IndexacaoMateria')
    processo.casa_iniciadora = dados_basicos.get('CasaIniciadoraNoLegislativo')
    processo.data_apresentacao = _parse_date(dados_basicos.get('DataApresentacao')) or processo.data_apresentacao

    processo.descricao_identificacao = identificacao.get('DescricaoIdentificacao')
    processo.descricao_tipo = identificacao.get('DescricaoSubtipoMateria') or processo.descricao_tipo

    numero = identificacao.get('NumeroMateria') or identificacao.get('Numero')
    if numero is not None:
        processo.numero = str(numero)

    ano = identificacao.get('AnoMateria') or identificacao.get('Ano')
    if ano is not None:
        processo.ano = str(ano)

    sigla = (
        identificacao.get('SiglaSubtipoMateria')
        or identificacao.get('SiglaMateria')
        or identificacao.get('Sigla')
    )
    if sigla:
        processo.tipo_proposicao = sigla

    url_detalhe = origem.get('UrlDetalheMateria') or origem.get('UrlMateria')
    if url_detalhe:
        processo.url_detalhe = url_detalhe

    processo.dados_extra_json = json.dumps(materia, ensure_ascii=True)
    if incluir_tramitacoes:
        tramitacoes = buscar_tramitacoes_senado(processo.id_externo)
        processo.tramitacao_json = json.dumps(tramitacoes, ensure_ascii=True)

    processo.detalhes_atualizados_em = timezone.now()
    processo.save()
    return True


def atualizar_detalhes_processo(processo: ProcessoLegislativo, incluir_tramitacoes: bool = True):
    if processo.origem_camara_ou_senado == 'CAMARA':
        return atualizar_detalhes_camara(processo, incluir_tramitacoes=incluir_tramitacoes)
    if processo.origem_camara_ou_senado == 'SENADO':
        return atualizar_detalhes_senado(processo, incluir_tramitacoes=incluir_tramitacoes)
    return False

def sincronizar_processos_legislativos(
    data_inicio: str = DEFAULT_DATA_INICIO,
    ano_inicio: int = DEFAULT_ANO_INICIO,
):
    """
    Sincroniza processos legislativos sem depender de termos monitorados.
    """
    novos_processos_criados = 0
    processos_camara_atualizados = set()
    processos_senado_atualizados = set()
    # === 1. API Camara ===
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

    # === 2. API Senado ===
    ano_atual = datetime.datetime.now().year
    for ano in range(ano_inicio, ano_atual + 1):
        materias_senado = _coerce_list(buscar_materias_senado(termo=None, ano=ano))

        for mat in materias_senado:
            id_externo = str(mat.get('Codigo', ''))
            if not id_externo:
                continue

            processo, created = ProcessoLegislativo.objects.get_or_create(
                id_externo=id_externo,
                origem_camara_ou_senado='SENADO',
                defaults={
                    'numero': str(mat.get('Numero', '')),
                    'ano': str(mat.get('Ano', '')),
                    'ementa': mat.get('Ementa', ''),
                    'tipo_proposicao': mat.get('Sigla', ''),
                    'status_atual': 'Apresentada',
                    'autor': mat.get('Autor', ''),
                    'descricao_identificacao': mat.get('DescricaoIdentificacao', ''),
                    'data_apresentacao': _parse_date(mat.get('Data')),
                    'url_detalhe': mat.get('UrlDetalheMateria'),
                }
            )
            if created:
                novos_processos_criados += 1

            if id_externo not in processos_senado_atualizados:
                atualizar_detalhes_senado(processo, incluir_tramitacoes=True)
                processos_senado_atualizados.add(id_externo)

    return novos_processos_criados

def popular_banco_carga_inicial(ano_inicio=2024):
    """
    Ignora os termos e baixa TODOS os processos legislativos das APIs da Câmara e Senado
    a partir do 'ano_inicio' até o ano atual.
    """
    total_antes = ProcessoLegislativo.objects.count()
    ano_atual = datetime.datetime.now().year
    buffer = []
    
    # === 1. Câmara (permite puxar a partir de uma data paginando tudo) ===
    data_inicio = f"{ano_inicio}-01-01"
    proposicoes_camara = buscar_todas_proposicoes_camara(termo=None, data_inicio=data_inicio)
    
    for prop in proposicoes_camara:
        id_externo = str(prop.get('id', ''))
        data_apresentacao = _parse_date(prop.get('dataApresentacao'))
        
        # Câmara envia algumas proposições (como Pareceres) com ano=0.
        # Vamos tentar extrair pelo `dataApresentacao` quando isso ocorrer
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

        if len(buffer) >= BULK_INSERT_SIZE:
            ProcessoLegislativo.objects.bulk_create(
                buffer,
                ignore_conflicts=True,
                batch_size=BULK_INSERT_SIZE,
            )
            buffer.clear()

    # === 2. Senado (melhor puxar ano a ano para não estourar payload/timeout) ===
    for ano in range(ano_inicio, ano_atual + 1):
        materias_senado = _coerce_list(buscar_materias_senado(termo=None, ano=ano))
            
        for mat in materias_senado:
            id_externo = str(mat.get('Codigo', ''))
            
            if not id_externo:
                continue

            buffer.append(
                ProcessoLegislativo(
                    id_externo=id_externo,
                    origem_camara_ou_senado='SENADO',
                    numero=str(mat.get('Numero', '')),
                    ano=str(mat.get('Ano', '')),
                    ementa=mat.get('Ementa', ''),
                    tipo_proposicao=mat.get('Sigla', ''),
                    status_atual="Apresentada",  # A listagem do senado nao traz a situacao atual.
                    autor=mat.get('Autor', ''),
                    descricao_identificacao=mat.get('DescricaoIdentificacao', ''),
                    data_apresentacao=_parse_date(mat.get('Data')),
                    url_detalhe=mat.get('UrlDetalheMateria')
                )
            )

            if len(buffer) >= BULK_INSERT_SIZE:
                ProcessoLegislativo.objects.bulk_create(
                    buffer,
                    ignore_conflicts=True,
                    batch_size=BULK_INSERT_SIZE,
                )
                buffer.clear()

    if buffer:
        ProcessoLegislativo.objects.bulk_create(
            buffer,
            ignore_conflicts=True,
            batch_size=BULK_INSERT_SIZE,
        )

    total_depois = ProcessoLegislativo.objects.count()
    return total_depois - total_antes
