from django.urls import re_path
from .views import *

urlpatterns = [
    # 支付功能
    re_path(r'^payment/(?P<order_id>\d+)/$',PaymentView.as_view()),
    # 支付状态
    re_path(r'^payment/status/$',PaymentStatusView.as_view()),
]