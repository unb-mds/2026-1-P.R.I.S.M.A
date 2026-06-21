from django.db import models
from django.conf import settings

class ProcessoLegislativo(models.Model):
    id_externo = models.CharField(max_length=255, unique=True)
    origem_camara_ou_senado = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    ano = models.CharField(max_length=255)
    ementa = models.TextField()
    tipo_proposicao = models.CharField(max_length=255)
    status_atual = models.CharField(max_length=255)

class TermoMonitorado(models.Model):
    palavra_chave = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='termos_monitorados',
        blank=True,
    )