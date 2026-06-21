from django.contrib import admin
from .models import User, Notificacao

admin.site.register(User)

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('user', 'processo', 'tipo', 'lida', 'data_criacao')
    list_filter = ('tipo', 'lida', 'data_criacao')
    search_fields = ('user__username', 'processo__numero', 'mensagem')
