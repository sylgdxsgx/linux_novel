"""
Django settings for novel project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g&yepsxy$%lqup*$u^l4o5+6+qoj%^&9wmj7a11mp$u^9%f516'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#当DEBUG=FALSE时，需要配置ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['mprtest.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shufa',
    'app02',
    'Intf',
    'bootstrap3',
]

#为什么要注释掉csrf(“跨站请求伪造”)？？,不注释掉也可以，（通过在模板中添加令牌）
#那么，要在模板中，发送POST请求的位置添加{% csrf_token %}，发送 csrfmiddlewaretoken 字段
#当页面向 Django 服务器发送一个 POST 请求时，该字段的值为当前会话 ID 加上一个密钥的散列值。
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'novel.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'novel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE':'django.db.backends.mysql',
#         'HOST':'127.0.0.1',
#         'PORT':'3306',
#         'NAME':'guest',
#         'USER':'root',
#         'PASSWORD':'123456',
#         'OPTIONS':{
#             'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     },
#     'mysqldb': {
#         'ENGINE':'django.db.backends.mysql',
#         'HOST':'127.0.0.1',
#         'PORT':'3306',
#         'NAME':'guest',
#         'USER':'root',
#         'PASSWORD':'123456',
#         'OPTIONS':{
#             'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# DATABASE_ROUTERS = ['novel.database_router.DatabaseAppsRouter']

# DATABASE_APPS_MAPPING = {
#     'firstApp':'default',
#     'app02':'default',
#     'Intf':'default',
# }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#LOGIN_URL = '/app02/login'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'     #是指从浏览器访问时的地址前缀
STATIC_ROOT = os.path.join(BASE_DIR,'collected_static') #当你要发布时，分散的static文件将被收集到STATIC_ROOT中。
#指定额外的静态文件存储位置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]