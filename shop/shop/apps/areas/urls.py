from django.urls import re_path
from .views import *

urlpatterns = [
    # 提供qq登录扫描页面
    re_path(r'^areas/$',AreasView.as_view()),

]