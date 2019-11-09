"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

import user_operation
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.authtoken import views
from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls

from goods.views import GoodsListViewSet, CategoryViewset, BannerViewset, IndexCategoryViewset, HotSearchsViewset
from trade.views import ShoppingCartViewset, OrderViewset

from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset,add

from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from users.views import SmsCodeViewset, UserViewset

from trade.views import AlipayView

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置category的url
router.register(r'categorys', CategoryViewset, base_name="categorys")
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")

# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")

# 配置购物车的url
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 配置收货地址
router.register(r'address', AddressViewset, base_name="address")

# 用户收藏
router.register(r'userfavs', UserFavViewset, base_name='userfavs')

# 配置订单的url
router.register(r'orders', OrderViewset, base_name="orders")

# 配置首页轮播图的url
router.register(r'banners', BannerViewset, base_name="banners")

# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^login/$', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    # 一定要去掉$
    url(r'docs/', include_docs_urls(title="暮学生鲜")),
    url(r'alipay/return/', AlipayView.as_view(), name="alipay"),
    url(r'index', TemplateView.as_view(template_name="index.html"), name="index"),
    # 第三方登录
    url('', include('social_django.urls', namespace='social')),
]
