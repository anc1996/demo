from django.urls import re_path
from .views import *

urlpatterns = [
    # 用户注册，反向解析写法：users.register
    re_path(r'^register',RegisterView.as_view(),name='register'),
    # 判断用户名是否重复注册
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',UsernameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',MobileCountView.as_view()),
    # 用户登录
    re_path(r'^login/$',LoginView.as_view(),name='login'),
    # 用户退出登录
    re_path(r'^logout/$',LogoutView.as_view(),name='logout'),
    # 用户中心
    re_path(r'^info/$',UserInfoView.as_view(),name='info'),
]