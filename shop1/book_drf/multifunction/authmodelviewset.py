from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from books.models import BookInfo
from book_drf.serializer import BookSerializer

# Create your views here.

"""
使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数据
ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。

3）ModelViewSet
继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin、
    CreateModelMixin、UpdateModelMixin、DestoryModelMixin。
"""


class Books(ModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # authentication_classes = (BasicAuthentication,SessionAuthentication) # 基本认证，由于全局有配置
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户,覆盖全局的权限IsAuthenticated

    # 只会扼杀未经身份验证的用户。传入请求的 IP 地址用于生成一个唯一的密钥，以便对其进行节流。
    throttle_classes = [AnonRateThrottle] #setting限流了100次

    # 指定过滤字段
    filterset_fields=['name','readcount']

    # SearchFilter 类支持基于搜索的简单单个查询参数，并且基于 Django 管理员的搜索功能。
    # http://**?search=russell
    filter_backends = [SearchFilter]
    search_fields = ['name', 'readcount']
    # search_fields = ['=username', '=email']
        # '^' Starts-with search.
        # '=' Exact matches.
        # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
        # '$' Regex search.

    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要写










