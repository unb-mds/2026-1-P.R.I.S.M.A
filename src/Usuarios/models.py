from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
	processos_legislativos = models.ManyToManyField(
		'Processos.ProcessoLegislativo',
		related_name='users',
		blank=True,
	)

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('ESTAGNACAO', 'Alerta de Estagnação'),
        ('ATUALIZACAO', 'Atualização'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes'
    )
    processo = models.ForeignKey(
        'Processos.ProcessoLegislativo', on_delete=models.CASCADE, related_name='notificacoes', null=True, blank=True
    )
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        ordering = ['-data_criacao']

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    receber_alertas_estagnacao = models.BooleanField(default=True)
    dias_limite_estagnacao = models.IntegerField(default=30)
    receber_alertas_novas_movimentacoes = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
