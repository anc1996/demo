from django.urls import re_path

from . import views
from book_drf.BasicViewSet import viewset, genericviewset
from book_drf.extendedAPIView import modelmixinview, childmixinview
from book_drf.BasicAPIView import apiview, gapiview
from book_drf.ExtendedViewSet import modelviewset,ReadonlyModelviewset
from .DefineViewSet import defineviewset
from rest_framework.routers import SimpleRouter,DefaultRouter


urlpatterns = [
    # 普通序列化视图操作
    re_path(r'^books/$', views.Books.as_view()),
    re_path(r'^book/(?P<pk>\d+)/$', views.BookView.as_view()),
    # APIView是REST framework提供的所有视图的基类，继承自Django的View父类。
    re_path(r'^apibooks/$', apiview.Books.as_view()),
    re_path(r'^apibooks/(?P<pk>\d+)/$', apiview.BookView.as_view()),
    # GenericAPIView，继承自APIVIew，增加了对于列表视图和详情视图可能用到的通用支持方法。
    re_path(r'^gapiview/$', gapiview.Books.as_view()),
    re_path(r'^gapiview/(?P<pk>\d+)/$', gapiview.BookView.as_view()),
    # GenericAPIView搭配一个或多个Mixin扩展类。
    re_path(r'^modelmixinview/$', modelmixinview.Books.as_view()),
    re_path(r'^modelmixinview/(?P<pk>\d+)/$', modelmixinview.BookView.as_view()),
    # 继承GenericAPIView与多个Mixin扩展类的子类视图。
    re_path(r'^childmixinview/$', childmixinview.Books.as_view()),
    re_path(r'^childmixinview/(?P<pk>\d+)/$', childmixinview.BookView.as_view()),
    # ViewSet继承自APIView,它可以需要我们自己实现action方法。
    re_path(r'^viewset/$', viewset.Books.as_view({'get': 'list', 'post': 'create','put':'update'})),
    re_path(r'^viewset/(?P<pk>\d+)/retrieve/$', viewset.Books.as_view({'get': 'retrieve'})),
    # GenericViewSet,继承自GenericAPIView与ViewSetMixi。作用也与GenericAPIVIew类似，它可以需要我们自己实现action方法。
    re_path(r'^GenericViewSet/$', genericviewset.Books.as_view({'get': 'list', 'post': 'create','put': 'update','delete':'destory'})),
    re_path(r'^genericViewSet/(?P<pk>\d+)/retrieve/$', genericviewset.Books.as_view({'get': 'retrieve'})),
    # # ModelViewSet,继承自GenericAPIVIew与5个Mixin扩展类的子类视图集，它可以需要我们自己实现action方法。
    # re_path(r'^ModelViewSet/$', modelviewset.Books.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^ModelViewSet/(?P<pk>\d+)/retrieve/$', modelviewset.Books.as_view({'get': 'retrieve'})),
    # # ReadOnlyModelViewSet,,继承自GenericAPIVIew与2个只能读取扩展类的子类视图集，它可以需要我们自己实现action方法。
    # re_path(r'^ReadonlyModelviewset/$', ReadonlyModelviewset.Books.as_view({'get': 'list'})),
    # re_path(r'^ReadonlyModelviewset/(?P<pk>\d+)/retrieve/$', ReadonlyModelviewset.Books.as_view({'get': 'retrieve'})),
]
# 自动生成路由，要结合视图集才能使用。
# 创建SimpleRouter路由对象
router1=SimpleRouter()
router=DefaultRouter()  #DefaultRouter,继承SimpleRouter
# 第一个参数：Prefix-用于这组路由的 URL 前缀。
# 第二个参数：Viewset-viewset 类。
"""
DefaultRouter与SimpleRouter的区别是，DefaultRouter会多附带一个默认的API根视图，返回一个包含所有列表视图的超链接响应数据。
"""
# Basename base_name路由名称的前缀。如果取消设置，则基于视图集的 queryset 属性自动生成 basename，如果视图集有一个这样的属性的话
router.register('ModelViewSet',modelviewset.Books,basename='ModelViewSet')  # ModelViewSet
router.register('ReadonlyModelviewset',ReadonlyModelviewset.Books,basename='ReadonlyModelviewset') # ReadOnlyModelViewSet
# 类中额外自定义的方法
router.register('DefineViewSet',defineviewset.Books,basename='DefineViewSet') # DefineViewSet
print(router.urls)
urlpatterns+=router.urls

