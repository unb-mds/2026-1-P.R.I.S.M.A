from django.core.management.base import BaseCommand
from Processos.models import ProcessoLegislativo

class Command(BaseCommand):
    help = 'Limpa todos os processos legislativos do banco de dados (Câmara e Senado)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando deleção de todos os processos legislativos...'))
        
        try:
            total_deletados, detalhes = ProcessoLegislativo.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Limpeza concluída! Foram deletados {total_deletados} registros.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao tentar limpar o banco: {str(e)}'))