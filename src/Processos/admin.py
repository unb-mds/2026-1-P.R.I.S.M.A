from django.contrib import admin

from Processos.models import ProcessoLegislativo, TermoMonitorado

# Register your models here.
from Processos.services import sincronizar_processo_on_demand

@admin.register(ProcessoLegislativo)
class ProcessoLegislativoAdmin(admin.ModelAdmin):
    list_display = ('id_externo', 'origem_camara_ou_senado', 'tipo_proposicao', 'numero_ano', 'data_apresentacao', 'ementa_curta', 'status_atual')
    search_fields = ('id_externo', 'numero', 'ano', 'ementa', 'tipo_proposicao', 'autor', 'status_atual')
    list_filter = ('origem_camara_ou_senado', 'ano', 'tipo_proposicao', 'status_atual', 'orgao_atual', 'autor')
    
    readonly_fields = ('detalhes_atualizados_em', 'tramitacao_json', 'dados_extra_json')

    fieldsets = (
        ('Identificação Geral', {
            'fields': ('id_externo', 'origem_camara_ou_senado', 'numero', 'ano', 'tipo_proposicao', 'descricao_tipo', 'data_apresentacao', 'casa_iniciadora', 'autor')
        }),
        ('Informações e Ementa', {
            'fields': ('ementa', 'ementa_detalhada', 'keywords', 'indexacao', 'descricao_identificacao')
        }),
        ('Status e Tramitação', {
            'fields': ('status_atual', 'data_status', 'orgao_atual', 'regime', 'apreciacao', 'descricao_tramitacao', 'descricao_situacao', 'despacho')
        }),
        ('Links e Referências', {
            'fields': ('url_detalhe', 'url_inteiro_teor', 'url_autores', 'url_orgao_atual', 'uri_ultimo_relator')
        }),
        ('Especificidades do Senado', {
            'fields': ('id_processo_senado', 'tipo_conteudo', 'tipo_documento', 'tramitando', 'apelido', 'casa_identificadora', 'norma_gerada', 'objetivo')
        }),
        ('Dados de Sistema (Somente Leitura)', {
            'fields': ('detalhes_atualizados_em', 'dados_extra_json', 'tramitacao_json')
        }),
    )

    def numero_ano(self, obj):
        if obj.numero and obj.ano:
            return f"{obj.numero}/{obj.ano}"
        return obj.numero or obj.ano or "-"
    numero_ano.short_description = 'Número/Ano'

    def ementa_curta(self, obj):
        if obj.ementa and len(obj.ementa) > 80:
            return obj.ementa[:80] + "..."
        return obj.ementa or "-"
    ementa_curta.short_description = 'Ementa'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        No momento em que o usuário do admin clica para visualizar ou editar
        um processo específico, engatilhamos o Lazy Update (Atualização sob Demanda).
        Isso preenche os campos vazios em tempo real.
        """
        try:
            obj = self.get_object(request, object_id)
            if obj:
                # Chama a engine de inteligência de cache (1 hora)
                sincronizar_processo_on_demand(obj)
        except Exception:
            pass
            
        return super().change_view(request, object_id, form_url, extra_context)

@admin.register(TermoMonitorado)
class TermoMonitoradoAdmin(admin.ModelAdmin):
    list_display = ('palavra_chave', 'users_list')
    search_fields = ('palavra_chave', 'users__username')

    def users_list(self, obj):
        return ", ".join([u.username for u in obj.users.all()])
    users_list.short_description = 'Users'