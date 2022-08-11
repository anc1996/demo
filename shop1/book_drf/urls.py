from django.urls import re_path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from . import views
from book_drf.BasicViewSet import viewset, genericviewset
from book_drf.extendedAPIView import modelmixinview, childmixinview
from book_drf.BasicAPIView import apiview, gapiview
from book_drf.ExtendedViewSet import modelviewset,ReadonlyModelviewset
from .DefineViewSet import defineviewset
from .multifunction import authmodelviewset,ScopedRThrottleview,orderfilterviewset
from .Pagination import PageNumberview,limitoffsetview

'''
Swagger：是一个规范和完整的框架，用于生成、描述、调用和可视化RESTful风格的Web服务。
总体目标是使客户端和文件系统源代码作为服务器以同样的速度来更新。
当接口有变动时，对应的接口文档也会自动更新。
Swagger优势：
1）Swagger可生成一个具有互动性的API控制台，开发者可快速学习和尝试API
2）Swagger可生成客户端SDK代码，用于不同平台上（Java、Python...）的实现
3）Swagger文件可在许多不同的平台上从代码注释中自动生成
4）Swagger有一个强大的社区，里面有许多强悍的贡献者
'''

schema_view = get_swagger_view(title='swagger API')

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
    re_path(r'^coreapi/', include_docs_urls(title='core api文档')),
    re_path(r'^swagger', schema_view),
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
router.register('DefineViewSet',defineviewset.Books,basename='DefineViewSet')  # DefineViewSet
router.register('multifunction',authmodelviewset.Books,basename='multifunction')  # 局部认证，匿名限流,search过滤，普通过滤
router.register('ScopedRate',ScopedRThrottleview.Books,basename='ScopedRate')  # 视图局部认证
router.register('orderfilter',orderfilterviewset.Books,basename='orderfilter')  # ordering对字段排序
router.register('pagenumber',PageNumberview.Books,basename='pagenumber')  # pagenumber分页器
router.register('limitoffset',limitoffsetview.Books,basename='limitoffset')  # limitoffsetview分页器
print(router.urls)

urlpatterns+=router.urls

