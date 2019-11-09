# encoding: utf-8
"""
@author:lipeng
@time:2019/10/24  17:24
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, User, UserLeavingMessage, UserAddress


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    # email = serializers.EmailField(max_length=100, required=True,
    #                                error_messages={"required": "请输入合法邮箱"})

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserFavSerializer(serializers.ModelSerializer):
    # 使用当前用户的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]

        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    用户留言
        list
            获取留言
        create
            添加留言

        delete
            删除留言
    '''
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only:只返回，post时候可以不用提交，format：格式化输出
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")


