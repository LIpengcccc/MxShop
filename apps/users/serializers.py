# encoding: utf-8
"""
@author:lipeng
@time:2019/10/22  15:48
"""
# users/serializers.py

import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from goods.serializers import GoodsSerializer
from user_operation.models import UserFav
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''

    # 通过商品id获取收藏的商品，需要嵌套商品的序列化
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 生成对象时会自动去验证
    # 函数名必须：validate + 验证字段名
    def validate_mobile(self, mobile):
        """
        手机号码验证
        """
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # 60s内只能发送一次
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # UserProfile中没有code字段，这里需要自定义一个code序列化字段
    # write_only只输入不输出
    code = serializers.CharField(required=True, max_length=4, min_length=4, write_only=True,
                                 error_messages={
                                     # "required"针对字段名称都没有，才有效
                                     # "blank": "针对输入为空",
                                     "blank": "该字段不能为空",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 label="验证码")
    # 验证用户名是否存在
    # help_text = "用户名",
    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, help_text="密码", label="密码",
    )

    # 密码加密保存
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # initial_data 前端传来原始的数据
        # 按时间排序
        # get容易出问题，多条数据就容易出错
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # 作用于所有字段之上
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
