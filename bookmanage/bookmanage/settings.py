"""
Django settings for bookmanage project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# __file__ 表示绝对路径,的上层路径的上层路径
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pmpr6j$8!t_&+%xroh_fu6igglynrbioyfze1ey66e9iq_afcv'

# SECURITY WARNING: don't run with debug turned on in production!
# 如果项目没有部署到远程服务器，且DEBUG = True(线下模式，允许调试)，
# 默认有ALLOWED_HOSTS = [‘localhost’, ‘127.0.0.1’, ‘[::1]’]，即默认允许本地主机访问django后台
# 开发者进行调试用的
DEBUG = True
ALLOWED_HOSTS = []



# Application definition
# 安装/注册 子应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book.apps.BookConfig',
    'login.apps.LoginConfig',# login.apps.LoginConfig = login
    'pay.apps.PayConfig'
    # '子应用名'
    # 子应用名.apps.子应用名Config
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF 是我们工程的url的配置的入口
# # 默认是 工程名.urls
# 可以修改,但是默认我们不修改
ROOT_URLCONF = 'bookmanage.urls'

# 和模板相关的配置信息
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # dirs 设置模板路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bookmanage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# sqlite 主要是一个嵌入式的关系型数据库
# 主要是在 移动端使用
# sqlite 属于小型的关系型数据库

# 中型的数据库: mysql(甲骨文)  sqlserver(微软的),
# 大型的数据库: oracle ,DB2
DATABASES = {
    'default': {
        # engine 引擎
        # sqlite3
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': BASE_DIR / 'db.sqlite3',
      
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '103.81.85.134',  # 主机
        'PORT': '3306',  # 端口号
        'USER': 'root',  # 用户名
        'PASSWORD': 'qwe123',  # 密码
        'NAME': 'manage_book',  # 指定数据库
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#语言
LANGUAGE_CODE = 'zh-hans'

# 时区
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# django是如何区分 静态资源和动态资源的呢?
# 就是通过 STATIC_URL
# 我们在访问静态资源 http://ip:port + STATIC_URL + 文件名
# django就会认为我们在访问静态资源,这个时候会去静态资源文件夹中进行匹配
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 告知系统静态文件在哪里
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]