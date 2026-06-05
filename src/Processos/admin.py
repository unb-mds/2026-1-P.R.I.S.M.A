from django.contrib import admin

from Processos.models import ProcessoLegislativo, TermoMonitorado

# Register your models here.
from Processos.services import sincronizar_processo_on_demand

@admin.register(ProcessoLegislativo)
class ProcessoLegislativoAdmin(admin.ModelAdmin):
    list_display = ('id_externo', 'origem_camara_ou_senado', 'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual')
    search_fields = ('id_externo', 'origem_camara_ou_senado', 'numero', 'ano', 'ementa', 'tipo_proposicao', 'status_atual')

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