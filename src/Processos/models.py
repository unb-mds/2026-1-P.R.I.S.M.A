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

    # Campos de IA
    estimativa_dias_conclusao = models.IntegerField(null=True, blank=True)
    porcentagem_conclusao = models.FloatField(null=True, blank=True)
    sla_status_ia = models.CharField(max_length=50, null=True, blank=True, help_text="Status do SLA classificado pela IA (Ex: Normal, Atenção, Estagnado)")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id_externo", "origem_camara_ou_senado"],
                name="unique_id_externo_origem",
            )
        ]

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

    @property
    def progresso_percentual(self):
        if self.porcentagem_conclusao is not None:
            return self.porcentagem_conclusao
            
        status = (self.status_atual or '').lower()
        if any(palavra in status for palavra in ['sancionad', 'promulgad', 'transformad', 'vetad', 'arquivad', 'retirad']):
            return 100
        elif 'aprovad' in status:
            return 75
        elif 'plenário' in status or 'plenario' in status:
            return 50
        elif 'comissão' in status or 'comissao' in status:
            return 25
        else:
            return 10

    @property
    def previsao_conclusao_dias(self):
        if self.estimativa_dias_conclusao is not None:
            return self.estimativa_dias_conclusao
            
        progresso = self.progresso_percentual
        if progresso == 100:
            return 0
        elif progresso == 75:
            return 30
        elif progresso == 50:
            return 60
        elif progresso == 25:
            return 180
        else:
            return 365

class Movimentacao(models.Model):
    processo = models.ForeignKey(ProcessoLegislativo, on_delete=models.CASCADE, related_name='movimentacoes')
    data_evento = models.DateTimeField()
    descricao = models.TextField()
    comissao_atual = models.CharField(max_length=255, blank=True, null=True)

    @property
    def dias_gastos(self):
        next_mov = self.processo.movimentacoes.filter(data_evento__gt=self.data_evento).order_by('data_evento').first()
        if next_mov and next_mov.data_evento:
            return (next_mov.data_evento - self.data_evento).days
        else:
            from django.utils import timezone
            return (timezone.now() - self.data_evento).days

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