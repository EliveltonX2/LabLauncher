# catalog/templatetags/query_transforms.py

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Esta tag customizada pega todos os parâmetros GET da URL atual,
    e atualiza (ou adiciona) os parâmetros passados.

    Isso é útil para manter os filtros de busca ao mudar de página na paginação.
    """
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()