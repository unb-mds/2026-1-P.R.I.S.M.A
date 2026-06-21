from django.core.management.base import BaseCommand
import logging
from Processos.models import ProcessoLegislativo
from Processos.services import CAMARA_API_BASE, SENADO_PROCESSO_BASE, SENADO_HEADERS, _get_json
from datetime import datetime
import requests

class Command(BaseCommand):
    help = 'Audita a quantidade de processos por ano na API versus no Banco de Dados para garantir 100% de cobertura.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ano_inicio', 
            type=int, 
            default=2020, 
            help='Ano inicial para a auditoria'
        )
        parser.add_argument(
            '--ano_fim', 
            type=int, 
            default=datetime.now().year, 
            help='Ano final para a auditoria'
        )

    def handle(self, *args, **options):
        ano_inicio = options['ano_inicio']
        ano_fim = options['ano_fim']
        
        self.stdout.write(self.style.WARNING(f'Iniciando auditoria do ano {ano_inicio} até {ano_fim}...\n'))
        
        # Formato de tabela
        header = f"{'ANO':<6} | {'CAMARA (API)':<15} | {'CAMARA (DB)':<15} | {'STATUS C.':<10} | {'SENADO (API)':<15} | {'SENADO (DB)':<15} | {'STATUS S.':<10}"
        self.stdout.write(header)
        self.stdout.write("-" * len(header))

        for ano in range(ano_inicio, ano_fim + 1):
            # 1. Contagem Senado na API
            params_senado = {'ano': ano}
            payload_senado = _get_json(SENADO_PROCESSO_BASE, headers=SENADO_HEADERS, params=params_senado)
            
            if isinstance(payload_senado, list):
                processos_senado = payload_senado
            elif isinstance(payload_senado, dict):
                processos_senado = payload_senado.get("dados", payload_senado.get("processos", []))
            else:
                processos_senado = []

            # Filtrar únicos reais que seriam salvos no DB
            unique_ids_senado = set(str(p.get("codigoMateria", "")) for p in processos_senado if p.get("codigoMateria"))
            total_api_senado_unique = len(unique_ids_senado)

            # 2. Contagem Senado no Banco
            ids_senado_list = list(unique_ids_senado)
            encontrados_senado = ProcessoLegislativo.objects.filter(
                origem_camara_ou_senado='SENADO',
                id_externo__in=ids_senado_list
            ).count()
            
            total_db_senado = ProcessoLegislativo.objects.filter(ano=str(ano), origem_camara_ou_senado='SENADO').count()
            status_senado = "OK" if encontrados_senado == total_api_senado_unique and total_api_senado_unique > 0 else "DEFASADO"

            # 3. Contagem Câmara na API (Bordas)
            total_api_camara = 0
            status_camara = "DEFASADO"
            try:
                # Pegar total bruto (inflado) e IDs da primeira pagina
                params_str = f"ano={ano}&itens=100&ordem=DESC&ordenarPor=ano"
                camara_url_first = f"{CAMARA_API_BASE}/proposicoes?{params_str}&pagina=1"
                resp_first = requests.get(camara_url_first, timeout=15)
                
                if resp_first.status_code == 200:
                    total_api_camara = int(resp_first.headers.get('x-total-count', 0))
                    dados_first = resp_first.json().get('dados', [])
                    ids_to_check = [str(p.get('id')) for p in dados_first if p.get('id')]
                    
                    if total_api_camara > 0:
                        import math
                        last_page = math.ceil(total_api_camara / 100)
                        
                        # Pegar IDs da última página
                        if last_page > 1:
                            camara_url_last = f"{CAMARA_API_BASE}/proposicoes?{params_str}&pagina={last_page}"
                            resp_last = requests.get(camara_url_last, timeout=15)
                            if resp_last.status_code == 200:
                                dados_last = resp_last.json().get('dados', [])
                                ids_to_check.extend([str(p.get('id')) for p in dados_last if p.get('id')])
                                
                    # 4. Contagem Câmara no Banco
                    total_db_camara = ProcessoLegislativo.objects.filter(ano=str(ano), origem_camara_ou_senado='CAMARA').count()

                    # 5. Avaliação por amostragem
                    ids_to_check = list(set(ids_to_check))
                    encontrados = ProcessoLegislativo.objects.filter(
                        origem_camara_ou_senado='CAMARA',
                        id_externo__in=ids_to_check
                    ).count()
                    
                    if encontrados == len(ids_to_check) and total_db_camara > 0:
                        status_camara = "OK"
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao contar Câmara na API: {e}"))
                total_db_camara = ProcessoLegislativo.objects.filter(ano=str(ano), origem_camara_ou_senado='CAMARA').count()

            # Colorir status
            c_status_cam = self.style.SUCCESS(status_camara) if status_camara == "OK" else self.style.ERROR(status_camara)
            c_status_sen = self.style.SUCCESS(status_senado) if status_senado == "OK" else self.style.ERROR(status_senado)

            # Para exibir melhor o número "único" do Senado, mostramos o unique e não o inflado.
            linha = f"{ano:<6} | {total_api_camara:<15} | {total_db_camara:<15} | {c_status_cam:<10} | {total_api_senado_unique:<15} | {total_db_senado:<15} | {c_status_sen:<10}"
            self.stdout.write(linha)
            
        self.stdout.write("\n" + "-" * len(header))
        self.stdout.write(self.style.WARNING("Auditoria concluída. Se houver defasagem, rode o comando 'carga_historica' para o ano correspondente."))
