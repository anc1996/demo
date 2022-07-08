from django.urls import re_path
from .views import *

urlpatterns = [
    # 提供qq登录扫描页面
    re_path(r'^qq/login/$',QQAuthURLView.as_view()),
    # 处理登陆后的回调函数
    re_path(r'^oauth_callback/$',QQAuthUserView.as_view()),
]