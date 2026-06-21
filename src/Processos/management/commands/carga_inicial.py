from django.core.management.base import BaseCommand
from Processos.services import popular_banco_carga_inicial

class Command(BaseCommand):
    help = 'Popula o banco com TODOS os processos da Câmara e Senado a partir do ano definido (default 2024)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ano', 
            type=int, 
            default=2024, 
            help='Ano inicial para buscar todas as proposições'
        )

    def handle(self, *args, **options):
        ano = options['ano']
        self.stdout.write(self.style.WARNING(f'Iniciando carga maciça das APIs a partir do ano {ano}... (Isso pode demorar bastante)'))
        
        try:
            novos = popular_banco_carga_inicial(ano)
            self.stdout.write(self.style.SUCCESS(f'Carga inicial concluída com sucesso! {novos} processos criados.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante a carga inicial: {str(e)}'))