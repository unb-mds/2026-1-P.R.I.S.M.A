from django.db import models
from django.conf import settings

class ProcessoLegislativo(models.Model):
    id_externo = models.CharField(max_length=255)
    origem_camara_ou_senado = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    ano = models.CharField(max_length=255)
    ementa = models.TextField()
    tipo_proposicao = models.CharField(max_length=255)
    status_atual = models.CharField(max_length=255)
    data_apresentacao = models.DateField(null=True, blank=True)
    url_detalhe = models.URLField(max_length=500, null=True, blank=True)
    url_inteiro_teor = models.URLField(max_length=500, null=True, blank=True)
    url_autores = models.URLField(max_length=500, null=True, blank=True)
    orgao_atual = models.CharField(max_length=255, null=True, blank=True)
    url_orgao_atual = models.URLField(max_length=500, null=True, blank=True)
    uri_ultimo_relator = models.URLField(max_length=500, null=True, blank=True)
    regime = models.CharField(max_length=255, null=True, blank=True)
    apreciacao = models.CharField(max_length=255, null=True, blank=True)
    descricao_tramitacao = models.CharField(max_length=255, null=True, blank=True)
    descricao_situacao = models.CharField(max_length=255, null=True, blank=True)
    despacho = models.TextField(null=True, blank=True)
    ementa_detalhada = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    autor = models.CharField(max_length=255, null=True, blank=True)
    casa_iniciadora = models.CharField(max_length=255, null=True, blank=True)
    indexacao = models.TextField(null=True, blank=True)
    descricao_tipo = models.CharField(max_length=255, null=True, blank=True)
    descricao_identificacao = models.CharField(max_length=255, null=True, blank=True)
    data_status = models.DateTimeField(null=True, blank=True)
    detalhes_atualizados_em = models.DateTimeField(null=True, blank=True)
    tramitacao_json = models.TextField(null=True, blank=True)
    dados_extra_json = models.TextField(null=True, blank=True)

    # Campos adicionais da nova API do Senado (/dadosabertos/processo)
    id_processo_senado = models.CharField(max_length=50, null=True, blank=True,
                                          help_text="ID do processo na nova API do Senado")
    tipo_conteudo = models.CharField(max_length=255, null=True, blank=True,
                                     help_text="Ex: Norma Geral, Veto Constitucional")
    tipo_documento = models.CharField(max_length=255, null=True, blank=True,
                                      help_text="Ex: Medida Provisória, Projeto de Decreto Legislativo")
    tramitando = models.BooleanField(null=True, default=None,
                                     help_text="Se o processo está em tramitação")
    apelido = models.CharField(max_length=500, null=True, blank=True,
                               help_text="Nome popular da matéria")
    casa_identificadora = models.CharField(max_length=10, null=True, blank=True,
                                           help_text="SF, CN, CD")
    norma_gerada = models.CharField(max_length=255, null=True, blank=True,
                                    help_text="Lei gerada após aprovação")
    objetivo = models.CharField(max_length=100, null=True, blank=True,
                                help_text="Revisora, Iniciadora")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id_externo", "origem_camara_ou_senado"],
                name="unique_id_externo_origem",
            )
        ]

class TermoMonitorado(models.Model):
    palavra_chave = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='termos_monitorados',
        blank=True,
    )