"""
Django settings for MxShop project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

from apps.utils.alipay import AliPay

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=)q5ir()%87*ao=5y0d!glf1ogs3hcbyksbccivml-f2n57c2f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserProfile'

# Application definition


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users.apps.UsersConfig',
    'apps.goods.apps.GoodsConfig',
    'apps.trade.apps.TradeConfig',
    'apps.user_operation.apps.UserOperationConfig',
    'DjangoUeditor',
    'crispy_forms',
    'django_filters',
    'xadmin',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'social_django',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MxShop.urls'

# 跨域处理
CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 第三方登录
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'users.views.CustomBackend',
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',

)

WSGI_APPLICATION = 'MxShop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mxshop",
        'USER': 'root',
        'PASSWORD': "123456",
        'HOST': "106.54.54.226",
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 和中间键一样，只要一个验证就会加到request中
# 问题全局token，局部控制实现
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',

        # 'rest_framework.authentication.TokenAuthentication',
        # jwt
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    # 限速设置
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',  # 未登陆用户
        'rest_framework.throttling.UserRateThrottle'  # 登陆用户
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/minute',  # 每分钟可以请求两次
        'user': '3000/minute'  # 每分钟可以请求五次
    }
}

# 缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3000  # 5s过期，时间自己可以随便设定
}




import datetime

# 有效期限
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 也可以设置seconds=20
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # JWT跟前端保持一致，比如“token”这里设置成JWT
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片网设置
APIKEY = "52f5c9723e5cb5eef56d12d8ab8062f4"

# 支付宝相关的key
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')

alipay_pro = AliPay(
    appid="2016101500696091",
    app_notify_url="https://www.helloly.wang/alipay/return/",
    app_private_key_path=private_key_path,
    alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    debug=True,  # 默认False,
    return_url="https://www.helloly.wang/alipay/return/"
)
alipay_dev = AliPay(
    appid="2016101500696091",
    app_notify_url="http://127.0.0.1:8000/alipay/return/",
    app_private_key_path=private_key_path,
    alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    debug=True,  # 默认False,
    return_url="http://127.0.0.1:8000/alipay/return/"
)



# 第三方登录，里面的值是你的开放平台对应的值
SOCIAL_AUTH_WEIBO_KEY = '3317834272'
SOCIAL_AUTH_WEIBO_SECRET = '7d24b3503a0f17d581fbcb8a8369ddf2'

SOCIAL_AUTH_QQ_KEY = 'xxxxxxx'
SOCIAL_AUTH_QQ_SECRET = 'xxxxxxx'

SOCIAL_AUTH_WEIXIN_KEY = 'xxxxxxx'
SOCIAL_AUTH_WEIXIN_SECRET = 'xxxxxxx'

# 登录成功后跳转到首页
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'


# redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}