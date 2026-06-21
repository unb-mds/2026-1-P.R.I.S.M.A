from django.core.management.base import BaseCommand
import logging
from Processos.services import popular_banco_carga_inicial, buscar_todas_proposicoes_camara, buscar_todos_processos_senado, _mapear_processo_senado_da_listagem
from Processos.models import ProcessoLegislativo
import time
from datetime import datetime

logger = logging.getLogger('Processos.services')

class Command(BaseCommand):
    help = 'Popula o banco com TODOS os processos históricos, iterando por ano, com proteção contra falhas.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ano_inicio', 
            type=int, 
            default=2000, 
            help='Ano inicial para iniciar a busca histórica'
        )
        parser.add_argument(
            '--ano_fim', 
            type=int, 
            default=datetime.now().year, 
            help='Ano final para a busca histórica'
        )

    def handle(self, *args, **options):
        ano_inicio = options['ano_inicio']
        ano_fim = options['ano_fim']
        
        self.stdout.write(self.style.WARNING(f'Iniciando carga histórica do ano {ano_inicio} até {ano_fim}... (Isso levará horas)'))
        
        BULK_INSERT_SIZE = 500

        campos_atualizacao_camara = [
            'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual', 
            'data_apresentacao', 'url_detalhe'
        ]
        campos_atualizacao_senado = [
            'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual', 'autor',
            'descricao_identificacao', 'data_apresentacao', 'url_detalhe',
            'id_processo_senado', 'tipo_conteudo', 'tipo_documento', 'tramitando',
            'apelido', 'casa_identificadora', 'norma_gerada', 'objetivo'
        ]

        total_geral_inseridos = 0

        for ano in range(ano_inicio, ano_fim + 1):
            self.stdout.write(self.style.SUCCESS(f'\n--- Processando Ano: {ano} ---'))
            
            # 1. Senado
            self.stdout.write(f'[{ano}] Buscando processos do Senado...')
            processos_senado = buscar_todos_processos_senado(ano=ano)
            self.stdout.write(f'[{ano}] Senado encontrou {len(processos_senado)} processos.')
            
            buffer_senado = []
            for proc in processos_senado:
                codigo_materia = str(proc.get('codigoMateria', ''))
                if not codigo_materia:
                    continue

                defaults = _mapear_processo_senado_da_listagem(proc)
                tramitando_val = defaults.pop('tramitando', None)

                buffer_senado.append(
                    ProcessoLegislativo(
                        id_externo=codigo_materia,
                        origem_camara_ou_senado='SENADO',
                        tramitando=tramitando_val,
                        **defaults,
                    )
                )

                if len(buffer_senado) >= BULK_INSERT_SIZE:
                    unicos_senado = {}
                    for obj in buffer_senado:
                        unicos_senado[obj.id_externo] = obj
                    buffer_senado_filtrado = list(unicos_senado.values())

                    ProcessoLegislativo.objects.bulk_create(
                        buffer_senado_filtrado,
                        update_conflicts=True,
                        update_fields=campos_atualizacao_senado,
                        unique_fields=['id_externo', 'origem_camara_ou_senado'],
                        batch_size=BULK_INSERT_SIZE,
                    )
                    buffer_senado.clear()
            
            # Deduplicar o buffer do senado pelo id_externo antes de inserir o resto
            if buffer_senado:
                unicos_senado = {}
                for obj in buffer_senado:
                    unicos_senado[obj.id_externo] = obj
                buffer_senado_filtrado = list(unicos_senado.values())

                ProcessoLegislativo.objects.bulk_create(
                    buffer_senado_filtrado,
                    update_conflicts=True,
                    update_fields=campos_atualizacao_senado,
                    unique_fields=['id_externo', 'origem_camara_ou_senado'],
                    batch_size=BULK_INSERT_SIZE,
                )
            
            # 2. Câmara
            self.stdout.write(f'[{ano}] Buscando proposições da Câmara...')
            
            proposicoes_camara = buscar_todas_proposicoes_camara(ano=ano)
            self.stdout.write(f'[{ano}] Câmara encontrou {len(proposicoes_camara)} proposições.')

            buffer_camara = []
            for prop in proposicoes_camara:
                id_externo = str(prop.get('id', ''))
                ano_str = str(prop.get('ano', ''))
                
                # Conversão de data
                data_apresentacao = None
                dt_apresentacao_str = prop.get('dataApresentacao')
                if dt_apresentacao_str:
                    try:
                        dt = datetime.fromisoformat(dt_apresentacao_str)
                        data_apresentacao = dt.date()
                    except ValueError:
                        pass
                
                numero_str = str(prop.get('numero', ''))
                
                if not id_externo:
                    continue

                buffer_camara.append(
                    ProcessoLegislativo(
                        id_externo=str(id_externo)[:255],
                        origem_camara_ou_senado='CAMARA',
                        numero=str(numero_str)[:255],
                        ano=str(ano_str)[:255],
                        ementa=prop.get('ementa', ''),
                        tipo_proposicao=str(prop.get('siglaTipo', ''))[:255],
                        status_atual='',
                        data_apresentacao=data_apresentacao,
                        url_detalhe=str(prop.get('uri', ''))[:500] if prop.get('uri') else None
                    )
                )

                if len(buffer_camara) >= BULK_INSERT_SIZE:
                    unicos_camara_lote = {}
                    for obj in buffer_camara:
                        unicos_camara_lote[obj.id_externo] = obj
                    buffer_camara_filtrado_lote = list(unicos_camara_lote.values())

                    ProcessoLegislativo.objects.bulk_create(
                        buffer_camara_filtrado_lote,
                        update_conflicts=True,
                        update_fields=campos_atualizacao_camara,
                        unique_fields=['id_externo', 'origem_camara_ou_senado'],
                        batch_size=BULK_INSERT_SIZE,
                    )
                    buffer_camara.clear()
            
            # Deduplicar o buffer da câmara pelo id_externo antes de inserir
            if buffer_camara:
                unicos_camara = {}
                for obj in buffer_camara:
                    unicos_camara[obj.id_externo] = obj
                buffer_camara_filtrado = list(unicos_camara.values())

                ProcessoLegislativo.objects.bulk_create(
                    buffer_camara_filtrado,
                    update_conflicts=True,
                    update_fields=campos_atualizacao_camara,
                    unique_fields=['id_externo', 'origem_camara_ou_senado'],
                    batch_size=BULK_INSERT_SIZE,
                )

            self.stdout.write(self.style.SUCCESS(f'[{ano}] Processamento do ano {ano} concluído! Salvos: Senado={len(processos_senado)}, Câmara={len(proposicoes_camara)}'))
            total_geral_inseridos += len(processos_senado) + len(proposicoes_camara)
            
            # Pequena pausa para evitar sobrecarga excessiva nas APIs caso processe muito rápido
            time.sleep(2)

        self.stdout.write(self.style.SUCCESS(f'\nCarga Histórica finalizada. Aproximadamente {total_geral_inseridos} registros processados/atualizados.'))
