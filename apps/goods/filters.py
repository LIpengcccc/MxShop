# -*- coding: utf-8 -*-
from django.db.models import Q

__author__ = 'bobby'

import django_filters

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', help_text="最低价格", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    top_category = django_filters.NumberFilter(method='top_category_filter', label="分类id父级")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    # 'is_hot', 'is_new'
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', "name", "is_hot","is_new"]
