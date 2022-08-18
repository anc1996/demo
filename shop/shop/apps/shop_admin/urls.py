from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from shop_admin.views import statistical,UsersView



urlpatterns = [
    # 用户注册，反向解析写法：users.register
    re_path(r'^authorizations/$', obtain_jwt_token),
    # 数据统计-用户总量
    re_path(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    # 数据统计-当日增用户统计
    re_path(r'^statistical/day_increment/$',statistical.UserDayCountView.as_view()),
    # 数据统计-当日活跃用户统计
    re_path(r'^statistical/day_active/$',statistical.UserActiveCountView.as_view()),
    # 数据统计-当日下单用户量统计
    re_path(r'^statistical/day_orders/$',statistical.UserOrderCountView.as_view()),
    # 数据统计-当月每天注册的用户量
    re_path(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 数据统计-当日每天用户访问商品的量
    re_path(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # 用户管理
    re_path(r'^users/$', UsersView.UserView.as_view()),
]