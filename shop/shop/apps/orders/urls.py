from django.urls import re_path
from .views import *

urlpatterns = [
    # 结算订单
    re_path(r'^orders/settlement/$',OrderSettlementView.as_view(),name='settlement'),
    # 提交订单
    re_path(r'^orders/commit/$',OrderCommitView.as_view()),
    # 提交订单成功
    re_path(r'^orders/success/$',OrderSuccessView.as_view()),
    # 展示订单
    re_path(r'^orders/info/(?P<page_num>\d+)/$',UserOrderInfoView.as_view(),name='info'),
]