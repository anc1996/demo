from django.urls import re_path
from .views import *

urlpatterns = [
    # 首页广告，反向解析写法：IndexView.register
    re_path(r'^$',IndexView.as_view(),name='index'),
]