import django_filters
from django_filters.fields import Lookup

from .models import Item


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):

        if not value:
            return qs

        # For django-filter versions < 0.13, use lookup_type instead of lookup_expr
        self.lookup_expr = 'in'
        values = value.split(',')
        print(values)
        return super(ListFilter, self).filter(qs, values)


class ItemFilterSet(django_filters.FilterSet):
    marca = ListFilter(field_name='marca')
    tipo = ListFilter(field_name='tipo')
    year = ListFilter(field_name='year')
    label = ListFilter(field_name='label')

    price = django_filters.RangeFilter()
    km = django_filters.RangeFilter()

    class Meta:
        model = Item
        fields = ['marca', 'tipo', 'year', 'label', 'price', 'km']
