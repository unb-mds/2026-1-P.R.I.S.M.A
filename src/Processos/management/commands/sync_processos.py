from django.core.management.base import BaseCommand

from Processos.services import sincronizar_processos_legislativos

class Command(BaseCommand):
    help = 'Sincroniza os processos legislativos na base da Camara e Senado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-inicio',
            default='2000-01-01',
            help='Data inicial (YYYY-MM-DD) para sincronizacao da Camara',
        )
        parser.add_argument(
            '--ano',
            type=int,
            default=2000,
            help='Ano inicial para sincronizacao do Senado',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando integração com Serviços da Câmara e Senado...'))

        try:
            novos = sincronizar_processos_legislativos(
                data_inicio=options['data_inicio'],
                ano_inicio=options['ano'],
            )
            self.stdout.write(self.style.SUCCESS(f'Sincronização concluída com sucesso! {novos} processos criados.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante a sincronização: {str(e)}'))