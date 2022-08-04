# 开发环境的配置文件

"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os,sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR:',os.path.dirname(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2gn%-!a%xgkw=o1m$dat8!ry)3vfp)cu)k-%n88i1v_@kykp0_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.freelearn.top','127.0.0.1']


# Application definition
# 查看导包路径
# print(sys.path)

# 追加导包路径指向apps,以便于注册应用做的更加简便。
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

INSTALLED_APPS = [
    # 第一次迁移会读取这里的子应用，然后通通都迁移
    'django.contrib.admin',
    # 分装整套用户认证系统
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'haystack',# 全文检索
    # 'django_crontab', # 定时任务,定时刷新首页
    "django_apscheduler",# 定时任务
    'scheduler',# 首页定时更新

    # 注册apps下子应用的user，用户模块
    'users',# 用户模块
    'contents',# 首页广告模块
    'verifications',# 验证码模块
    'oauth',# 第三方登录
    'areas',# 省市区三级联动
    'goods',# 商品模块
    'carts',# 购物车
    'orders',# 订单
    'payment',# 支付

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

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    # jinja2模板
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja模板
        'DIRS': [os.path.join(BASE_DIR, 'templates')]  # 配置模板文件加载路径
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            # 'environment':'jinja2.Environment',  #默认的
            'environment': 'shop.utils.jinja2_env.jinja2_environment',  # 指定jinja2的环境
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    # django模板
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

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# 配置mysql数据库
DATABASES = {
    'default': {# 写
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '103.81.85.134',  # 主机
        'PORT': '3306',  # 端口号
        'USER': 'wenming',  # 用户名
        'PASSWORD': '123456',  # 密码
        'NAME': 'shop',  # 指定数据库
    },
    'slave': {# 读
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': BASE_DIR / 'db.sqlite3',
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '103.81.85.134',  # 主机
            'PORT': '3307',  # 端口号
            'USER': 'root',  # 用户名
            'PASSWORD': 'qwe123',  # 密码
            'NAME': 'shop',  # 指定数据库
        }
}

# caches 缓存,配置redis数据库，分库缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://103.81.85.134:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123"
        }
    },
    # 存放session数据
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://103.81.85.134:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123"
        }
    },
    # 存储验证码VerifyCode
    "VerifyCode": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://103.81.85.134:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123"
        }
    },
    # 存储验证码VerifyCode
        "ProvinceCity": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://103.81.85.134:6379/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "qwe123"
            }
        },
    # 存储用户浏览记录history
        "history": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://103.81.85.134:6379/4",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "qwe123"
            }
        },
    # 存储用户浏览记录history
    "carts": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://103.81.85.134:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123"
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

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

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# 指定加载静态文件路由的前缀
# 配置收集静态文件存放的目录
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

STATIC_URL = '/static/'
# 告知系统静态文件在哪里
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'static'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 配置工程日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            # asctime。默认情况下，它的格式为“2003-07-0816:49:45,896”
            # levelname。消息的文本日志记录级别(‘ DEBUG’、‘ INFO’、‘ WARING’、‘ ERROR’、‘ CRITAL’)。
            # module：模块(文件名的名称部分)。
            # lineno：行号
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/shop.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024, # 300*1024*1024 B字节
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        'carts': {  # 定义了一个名为carts的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        'areas': {  # 定义了一个名为carts的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        'goods': {  # 定义了一个名为carts的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
        'verifications': {  # 定义了一个名为carts的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的一般的系统信息,DEBUG：排查故障时使用的低级别系统信息
        },
    }
}

#Django用户模型类是通过全局配置项 AUTH_USER_MODEL 决定的
# 指定自定义用户的模型类  值的语法：'子应用.用户模型类'，用户认证系统中的用户模型类
AUTH_USER_MODEL = "users.User"

# 多用户登录，指定自定义用户认证后端要使用的认证后端列表在 AUTHENTICATION_BACKENDS 配置中指定。
# 这应该是一个指向知道如何验证的 Python 类的 Python 路径名列表。这些类可以是 Python 路径上的任何地方。
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']

# 判断用户是否登录，指定未登录用户重定向的地址
LOGIN_URL="/login/"

# QQ登录参数
QQ_CLIENT_ID = '101863920'
QQ_CLIENT_SECRET = '3797609485bd149b4f2e7efb48315b74'
QQ_REDIRECT_URI = 'http://www.freelearn.top/oauth_callback'

# 配置邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.qq.com' # 发邮件主机
EMAIL_PORT = 25 # 发邮件端口
EMAIL_HOST_USER = '834195283@qq.com' # 授权的邮箱
EMAIL_HOST_PASSWORD = 'nkkcrwntbszabcae' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = 'shop<834195283@qq.com>' # 发件人抬头

# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://127.0.0.1:8000/emails/verification/'

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE='shop.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS相关参数
FDFS_BASE_URL = 'http://103.81.85.134:8888/'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://103.81.85.134:9200/', # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'shop', # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引,配置项保证了在Django运行起来后，有新的数据产生时，Haystack仍然可以让Elasticsearch实时生成新数据的索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 控制每页显示数量
HAYSTACK_SEARCH_RESULTS_PER_PAGE=12

# 支付宝
ALIPAY_APPID = '2021000121630764'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'

# # 定时器
# CRONJOBS = [
#     # 每1分钟生成一次首页静态文件
#     ('*/1 * * * *', 'contents.crons.generate_static_index_html', '>> '+os.path.join(os.path.dirname(BASE_DIR),'logs/crontab.log')),
# ]
#
# # 定时器指定中文编码格式
# CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# mysql读写分离路由
DATABASE_ROUTERS = ['shop.utils.db_router.MasterSlaveDBRouter']
# 配置收集静态文件存放的目录
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'collect_static')
