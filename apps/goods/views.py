from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Goods, GoodsCategory, Banner, HotSearchWords
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer, \
    HotWordsSerializer
from .filters import GoodsFilter
from rest_framework.authentication import TokenAuthentication

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, ):
    """
    商品列表页,分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    pagination_class = GoodsPagination
    # Token设置,局部接口token设置
    # authentication_classes = (TokenAuthentication,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    # search_fields = ('=name', 'goods_brief', 'goods_desc')
    # =是精确匹配
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # 完全等于
    # filterset_fields = ('name', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
     list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


class HotSearchsViewset(CacheResponseMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer