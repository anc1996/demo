from django.urls import re_path,include
from .views import *

urlpatterns = [
    # 用户注册，反向解析写法：users.register
    re_path(r'^register',RegisterView.as_view(),name='register'),
]