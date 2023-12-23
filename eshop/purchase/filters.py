# filters.py

import django_filters
from purchase.models import Order


class OrderFilter(django_filters.FilterSet):
    supplier_name = django_filters.CharFilter(
        field_name='supplier__name', lookup_expr='icontains')
    item_name = django_filters.CharFilter(
        field_name='line_items__item_name', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['supplier_name', 'item_name']
