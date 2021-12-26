from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.purchase.models import *
from apps.sales.models import *


class PurchaseReportFilter(FilterSet):
    category = NumberFilter(field_name='goods__category', label='商品分类')
    creator = NumberFilter(field_name='sales_order__creator', label='创建人')
    start_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseGoods
        fields = ['category', 'creator', 'start_date', 'end_date']


class SalesReportFilter(FilterSet):
    category = NumberFilter(field_name='goods__category', label='商品分类')
    creator = NumberFilter(field_name='sales_order__creator', label='创建人')
    start_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesGoods
        fields = ['category', 'creator', 'start_date', 'end_date']


__all__ = [
    'PurchaseReportFilter', 'SalesReportFilter',
]
