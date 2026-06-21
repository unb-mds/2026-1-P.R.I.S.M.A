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

    @property
    def dias_na_comissao_atual(self):
        from django.utils import timezone
        ultima_movimentacao = self.movimentacoes.order_by('-data_evento').first()
        if ultima_movimentacao and ultima_movimentacao.data_evento:
            return (timezone.now() - ultima_movimentacao.data_evento).days
        return 0

    @property
    def dias_totais_tramitacao(self):
        from django.utils import timezone
        primeira_movimentacao = self.movimentacoes.order_by('data_evento').first()
        if primeira_movimentacao and primeira_movimentacao.data_evento:
            return (timezone.now() - primeira_movimentacao.data_evento).days
        return 0

class Movimentacao(models.Model):
    processo = models.ForeignKey(ProcessoLegislativo, on_delete=models.CASCADE, related_name='movimentacoes')
    data_evento = models.DateTimeField()
    descricao = models.TextField()
    comissao_atual = models.CharField(max_length=255, blank=True, null=True)

class TermoMonitorado(models.Model):
    palavra_chave = models.CharField(max_length=255, unique=True)
    processos = models.ManyToManyField(
        'ProcessoLegislativo',
        related_name='termos_monitorados',
        blank=True,
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='termos_monitorados',
        blank=True,
    )