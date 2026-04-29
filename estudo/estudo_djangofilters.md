## Visão geral

O **Django Filter** (pacote django-filter) é uma biblioteca que fornece uma forma declarativa, segura e reutilizável de construir filtros de consulta (`QuerySet`) a partir de parâmetros HTTP. Ele é amplamente usado junto ao Django e integra-se de forma nativa ao Django REST Framework para APIs.

A ideia central é mapear parâmetros de requisição (GET/QueryParams) para condições de banco, evitando lógica manual repetitiva e reduzindo risco de erros.

---

# 1. Conceitos fundamentais

### FilterSet

É a classe principal. Funciona como um “Form” para filtros.

import django_filters
from .models import Produto

class ProdutoFilter(django_filters.FilterSet):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria']

Isso gera automaticamente filtros básicos baseados nos campos do modelo.

---

### Integração com QuerySet

def lista_produtos(request):
    f = ProdutoFilter(request.GET, queryset=Produto.objects.all())
    return render(request, 'template.html', {'filter': f})

* `request.GET` → parâmetros
* `queryset` → base de dados inicial
* `f.qs` → queryset filtrado

---

# 2. Tipos de filtros

## 2.1 Filtros básicos

| Tipo      | Classe             |
| --------- | ------------------ |
| Texto     | `CharFilter`     |
| Número   | `NumberFilter`   |
| Booleano  | `BooleanFilter`  |
| Data      | `DateFilter`     |
| Data/Hora | `DateTimeFilter` |

Exemplo:

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    preco = django_filters.NumberFilter()

---

## 2.2 Lookup expressions

Controlam como a query será feita no banco.

nome = django_filters.CharFilter(lookup_expr='icontains')
preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')
preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')

### Principais lookup_expr:

| Lookup    | Descrição                |
| --------- | -------------------------- |
| exact     | Igual                      |
| iexact    | Igual case-insensitive     |
| contains  | Contém                    |
| icontains | Contém (case-insensitive) |
| gt / gte  | Maior que / maior ou igual |
| lt / lte  | Menor que / menor ou igual |
| in        | Lista                      |
| range     | Intervalo                  |
| isnull    | Nulo                       |

---

## 2.3 Filtros relacionais

categoria = django_filters.ModelChoiceFilter(
    queryset=Categoria.objects.all()
)

Para múltiplos valores:

categoria = django_filters.ModelMultipleChoiceFilter(
    queryset=Categoria.objects.all()
)

---

## 2.4 Filtros customizados (method)

Permite lógica arbitrária:

class ProdutoFilter(django_filters.FilterSet):
    nome_custom = django_filters.CharFilter(method='filtrar_nome')

    def filtrar_nome(self, queryset, name, value):
        return queryset.filter(nome__icontains=value)

---

# 3. Filtros avançados

## 3.1 RangeFilter

preco = django_filters.RangeFilter()

Query:

?preco_min=10&preco_max=100

---

## 3.2 DateFromToRangeFilter

data = django_filters.DateFromToRangeFilter()

---

## 3.3 BaseInFilter

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

ids = NumberInFilter(field_name='id', lookup_expr='in')

Query:

?id=1,2,3

---

## 3.4 OrderingFilter

ordenacao = django_filters.OrderingFilter(
    fields=(
        ('preco', 'preco'),
        ('nome', 'nome'),
    )
)

Uso:

?ordering=preco
?ordering=-preco

---

# 4. Integração com Django REST Framework

## Configuração

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

---

## Uso em ViewSets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProdutoFilter

Ou direto:

filterset_fields = ['nome', 'preco']

---

# 5. Performance e otimização

## Problemas comuns

### 1. N+1 queries

Filtros com relacionamentos podem gerar consultas extras.

Solução:

queryset = Produto.objects.select_related('categoria')

ou

queryset = Produto.objects.prefetch_related('tags')

---

### 2. Índices no banco

Filtros frequentes devem ter índices:

class Produto(models.Model):
    nome = models.CharField(max_length=100, db_index=True)

---

### 3. Evitar filtros desnecessários

if value:
    queryset = queryset.filter(...)

---

# 6. Segurança

O django-filter evita SQL Injection porque:

* Usa ORM do Django
* Não concatena SQL manualmente
* Valida tipos automaticamente

Mas atenção:

* Nunca use filtros baseados em input direto sem validação em métodos customizados

---

# 7. Customização de formulários

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

---

# 8. Validação e limpeza de dados

Filtros usam sistema de forms do Django:

f.is_valid()
f.form.cleaned_data

---

# 9. Composição dinâmica de filtros

Você pode gerar filtros dinamicamente:

class DynamicFilter(django_filters.FilterSet):
    class Meta:
        model = Produto
        fields = '__all__'

Ou modificar em runtime:

filterset = ProdutoFilter(data=request.GET, queryset=qs)

---

# 10. Casos avançados reais

## 10.1 Filtro com múltiplos critérios combinados

def filtrar_complexo(self, queryset, name, value):
    return queryset.filter(
        Q(nome__icontains=value) | Q(descricao__icontains=value)
    )

---

## 10.2 Filtro baseado no usuário

def __init__(self, *args, user=None, **kwargs):
    super().__init__(*args, **kwargs)
    if user:
        self.queryset = self.queryset.filter(usuario=user)

---

## 10.3 Filtros condicionais

def filter_queryset(self, queryset):
    qs = super().filter_queryset(queryset)
    if not self.request.user.is_staff:
        qs = qs.filter(publico=True)
    return qs

---

# 11. Integração com front-end

* Query params padrão:

/api/produtos?nome=abc&preco_min=10

* Funciona com:
  * React
  * Vue
  * Angular
  * HTMX

---

# 12. Comparação com alternativas

| Abordagem                   | Prós                | Contras                            |
| --------------------------- | -------------------- | ---------------------------------- |
| Django Filter               | Declarativo, rápido | Menos flexível que lógica manual |
| Query manual                | Total controle       | Verboso e propenso a erro          |
| Search frameworks (Elastic) | Alta performance     | Complexidade                       |

# 13. Boas práticas

* Use `FilterSet` sempre que possível
* Separe lógica complexa em métodos
* Use índices no banco
* Evite filtros pesados sem paginação
* Combine com `select_related`

# 14. Quando NÃO usar django-filter

* Queries extremamente complexas (ex: analytics)
* Quando precisa de busca full-text avançada → usar ElasticSearch
* Quando lógica depende de múltiplas tabelas com agregações complexas

# 15. Exemplo completo (produção)

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte')
    categoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all())
    ordenar = django_filters.OrderingFilter(fields=('preco', 'nome'))

    class Meta:
        model = Produto
        fields = ['nome', 'categoria']

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all().select_related('categoria')
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProdutoFilter

# 16. Conclusão técnica

O django-filter atua como uma camada declarativa sobre o ORM do Django, permitindo:

* Redução de boilerplate
* Segurança embutida
* Integração direta com DRF
* Alta extensibilidade via métodos customizados
