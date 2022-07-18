from django.urls import re_path
from .views import *

urlpatterns = [
    # 商品列表页
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$',ListView.as_view(),name='list'),
    # 热销排行
    re_path(r'^hot/(?P<category_id>\d+)/$',HotGoodsView.as_view()),
]