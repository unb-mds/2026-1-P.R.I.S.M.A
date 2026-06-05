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
                total_api_senado = len(payload_senado)
            elif isinstance(payload_senado, dict):
                total_api_senado = len(payload_senado.get("dados", payload_senado.get("processos", [])))
            else:
                total_api_senado = 0

            # 2. Contagem Senado no Banco
            total_db_senado = ProcessoLegislativo.objects.filter(ano=str(ano), origem_camara_ou_senado='SENADO').count()

            # 3. Contagem Câmara na API
            # Usando requisição direta com itens=1 e pegando o header X-Total-Count para ser rápido
            total_api_camara = 0
            try:
                camara_url = f"{CAMARA_API_BASE}/proposicoes?ano={ano}&itens=1"
                resp = requests.get(camara_url, timeout=15)
                if resp.status_code == 200:
                    total_api_camara = int(resp.headers.get('x-total-count', 0))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao contar Câmara na API: {e}"))

            # 4. Contagem Câmara no Banco
            total_db_camara = ProcessoLegislativo.objects.filter(ano=str(ano), origem_camara_ou_senado='CAMARA').count()

            # 5. Avaliação
            status_camara = "OK" if total_api_camara == total_db_camara else "DEFASADO"
            status_senado = "OK" if total_api_senado == total_db_senado else "DEFASADO"

            # Colorir status
            c_status_cam = self.style.SUCCESS(status_camara) if status_camara == "OK" else self.style.ERROR(status_camara)
            c_status_sen = self.style.SUCCESS(status_senado) if status_senado == "OK" else self.style.ERROR(status_senado)

            linha = f"{ano:<6} | {total_api_camara:<15} | {total_db_camara:<15} | {c_status_cam:<10} | {total_api_senado:<15} | {total_db_senado:<15} | {c_status_sen:<10}"
            self.stdout.write(linha)
            
        self.stdout.write("\n" + "-" * len(header))
        self.stdout.write(self.style.WARNING("Auditoria concluída. Se houver defasagem, rode o comando 'carga_historica' para o ano correspondente."))
