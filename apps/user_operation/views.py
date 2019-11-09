from django.shortcuts import render, redirect

# Create your views here.

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from users.serializers import UserFavDetailSerializer
from utils.permissions import IsOwnerOrReadOnly
from .serializers import UserFavSerializer, UserDetailSerializer, LeavingMessageSerializer, AddressSerializer


class UserFavViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()

    # IsAuthenticated 要求登录
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    serializer_class = UserFavSerializer

    # auth使用来做用户认证的
    # JSONWebTokenAuthentication JWT认证
    # SessionAuthentication api登陆认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 搜索的字段,默认是主键，但主键删除会变，所以要这样干，让查询的换成goods_id
    lookup_field = 'goods_id'

    # 搜索的字段

    # queryset = UserFav.objects.all()
    # 重载上面这个方法

    def get_queryset(self):
        # 只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    # 动态选择serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    # def perform_create(self, serializer):
    #
    #     return serializer.save()
    #    # 这里instance相当于UserFav model，通过它找到goods
    # goods = instance.goods
    # goods.fav_num += 1
    # goods.save()


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """

    # 权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 认证方式
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    # 只能看到自己的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    # ModelViewSet 继承上面所有
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


def add(request):
    url =request
    return redirect()
