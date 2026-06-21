import requests
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from .models import Movimentacao

def sync_processo_on_demand(processo):
    """
    Função on-demand para atualizar as informações de um Processo Legislativo.
    Sempre faz a consulta na API da Câmara ou do Senado para garantir que os
    dados apresentados estejam 100% atualizados conforme a necessidade de consulta.
    """
    origem = processo.origem_camara_ou_senado.lower()
    if 'camara' in origem or 'câmara' in origem:
        _sync_camara_api(processo)
    elif 'senado' in origem:
        _sync_senado_api(processo)

def _sync_camara_api(processo):
    try:
        url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{processo.id_externo}/tramitacoes"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dados = response.json().get('dados', [])
            
            for tramitacao in dados:
                data_hora_str = tramitacao.get('dataHora')
                if not data_hora_str:
                    continue
                    
                data_evento = parse_datetime(data_hora_str)
                if data_evento and is_naive(data_evento):
                    data_evento = make_aware(data_evento)
                
                descricao = tramitacao.get('despacho') or tramitacao.get('descricaoTramitacao') or "Movimentação registrada"
                comissao = tramitacao.get('siglaOrgao')
                
                Movimentacao.objects.get_or_create(
                    processo=processo,
                    data_evento=data_evento,
                    descricao=descricao,
                    defaults={
                        'comissao_atual': comissao
                    }
                )
    except Exception as e:
        print(f"Erro ao sincronizar API da Câmara para {processo.id_externo}: {e}")

def _sync_senado_api(processo):
    try:
        url = f"https://legis.senado.leg.br/dadosabertos/materia/movimentacoes/{processo.id_externo}"
        response = requests.get(url, headers={'Accept': 'application/json'}, timeout=10)
        
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
                        
                    data_evento = parse_datetime(data_hora_str)
                    if data_evento and is_naive(data_evento):
                        data_evento = make_aware(data_evento)
                    
                    descricao = informe.get('Descricao') or "Movimentação registrada"
                    local = informe.get('Local', {})
                    comissao = local.get('SiglaLocal') or local.get('NomeLocal')
                    
                    Movimentacao.objects.get_or_create(
                        processo=processo,
                        data_evento=data_evento,
                        descricao=descricao,
                        defaults={
                            'comissao_atual': comissao
                        }
                    )
    except Exception as e:
        print(f"Erro ao sincronizar API do Senado para {processo.id_externo}: {e}")


