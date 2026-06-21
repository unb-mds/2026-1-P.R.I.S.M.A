import django_filters
from .models import ProcessoLegislativo

class ProcessoFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_q', label="Pesquisa")
    ano = django_filters.CharFilter(lookup_expr='exact')
    numero = django_filters.CharFilter(lookup_expr='exact')
    tipo_proposicao = django_filters.CharFilter(lookup_expr='icontains')
    status_atual = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProcessoLegislativo
        fields = ['q', 'tipo_proposicao', 'status_atual', 'ano', 'numero']

    def filter_q(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(
            Q(ementa__icontains=value) | 
            Q(id_externo__icontains=value) | 
            Q(tipo_proposicao__icontains=value) | 
            Q(numero__icontains=value)
        )
