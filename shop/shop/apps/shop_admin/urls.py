from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from shop_admin.views import statistical,UsersView,SpecsViewSet,imageViewSet,skuViewSet

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
    # 商品管理-新增商品规格
    re_path(r'^goods/simple/$', SpecsViewSet.SpecsView.as_view({'get':'simple'})),
    # 商品管理-新增SKU图片
    re_path(r'^skus/simple/$', imageViewSet.ImagesView.as_view({'get': 'simple'})),
    # 商品管理-获取SPU商品规格信息
    re_path(r'^goods/(?P<pk>\d+)/specs/$', skuViewSet.SKUView.as_view({'get': 'specs'})),
]


# --规格表路由---
router=DefaultRouter()
# 商品管理-规格管理
router.register('goods/specs',SpecsViewSet.SpecsView,basename='specs')
# 商品管理-SKU图片管理
router.register('skus/images',imageViewSet.ImagesView,basename='images')
# 商品管理-SKU表管理
router.register('skus',skuViewSet.SKUView,basename='skus')
# print(router.urls)
urlpatterns+=router.urls