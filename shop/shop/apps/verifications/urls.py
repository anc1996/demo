from django.urls import re_path
from .views import *

urlpatterns = [
    # 首页广告，反向解析写法：IndexView.register
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',ImageCodeView.as_view()),
    # 短信验证码
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/',SMSCodeView.as_view()),
]