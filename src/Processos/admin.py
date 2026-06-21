from django.contrib import admin

from Processos.models import ProcessoLegislativo, TermoMonitorado, Movimentacao

# Register your models here.
@admin.register(ProcessoLegislativo)
class ProcessoLegislativoAdmin(admin.ModelAdmin):
    list_display = ('id_externo', 'origem_camara_ou_senado', 'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual')
    search_fields = ('id_externo', 'origem_camara_ou_senado', 'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual')

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('processo', 'data_evento', 'comissao_atual')
    search_fields = ('processo__numero', 'descricao', 'comissao_atual')

@admin.register(TermoMonitorado)
class TermoMonitoradoAdmin(admin.ModelAdmin):
    list_display = ('palavra_chave', 'users_list')
    search_fields = ('palavra_chave', 'users__username')

    def users_list(self, obj):
        return ", ".join([u.username for u in obj.users.all()])
    users_list.short_description = 'Users'