from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Usuarios.models import User, Notificacao

class Command(BaseCommand):
    help = 'Gera alertas de estagnação para processos favoritados que estão parados há mais de 30 dias.'

    def handle(self, *args, **options):
        # Limite de 30 dias atrás
        limite_estagnacao = 30
        agora = timezone.now()

        # Pegamos apenas usuários que têm processos favoritados
        users_com_favoritos = User.objects.filter(processos_legislativos__isnull=False).distinct()
        
        alertas_criados = 0

        for user in users_com_favoritos:
            for processo in user.processos_legislativos.all():
                dias_parado = processo.dias_na_comissao_atual
                
                if dias_parado > limite_estagnacao:
                    # Verifica se já existe uma notificação de estagnação nos últimos 30 dias para evitar spam
                    data_corte = agora - timedelta(days=limite_estagnacao)
                    alerta_recente = Notificacao.objects.filter(
                        user=user,
                        processo=processo,
                        tipo='ESTAGNACAO',
                        data_criacao__gte=data_corte
                    ).exists()
                    
                    if not alerta_recente:
                        mensagem = f"O processo {processo.numero}/{processo.ano} está estagnado há mais de {limite_estagnacao} dias."
                        Notificacao.objects.create(
                            user=user,
                            processo=processo,
                            tipo='ESTAGNACAO',
                            mensagem=mensagem
                        )
                        alertas_criados += 1
                        self.stdout.write(self.style.SUCCESS(f'Alerta criado para usuário {user.username} - Processo {processo.numero}/{processo.ano}'))

        self.stdout.write(self.style.SUCCESS(f'Rotina finalizada. Total de alertas criados: {alertas_criados}'))
