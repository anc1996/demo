from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

from books.models import BookInfo
from book_drf.serializer import BookSerializer

# Create your views here.


class PageNum(LimitOffsetPagination):

    '''
    这种分页样式反映了查找多个数据库记录时使用的语法。客户端包括“limit”和“offset”查询参数。
    limit指示在数据库要返回的项目的最大数目，这相当于其他样式中的 page_size。
    offset指示在数据库查询相对于完整的未分页项的起始位置。
    '''
    # default_limit指示在客户端未在查询参数中提供限制时使用的限制。默认为与 PAGE_SIZE 设置键相同的值。
    default_limit = 2
    # limit_query_param,指示“limit”查询参数的名称。默认为 'limit'。
    limit_query_param='limit'
    # offset_query_param 指示“offset”查询参数的名称。默认为 'offset'。
    offset_query_param='offset'
    max_limit=400

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
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户,覆盖全局的权限IsAuthenticated

    # 只会扼杀未经身份验证的用户。传入请求的 IP 地址用于生成一个唯一的密钥，以便对其进行节流。
    throttle_classes = [AnonRateThrottle,] # setting限流了100次

    # 在类视图中设置filter_backends，使用rest_framework.filters.OrderingFilter过滤器，
    # REST framework会在请求的查询字符串参数中检查是否包含了ordering参数，如果包含了ordering参数，
    # 则按照ordering参数指明的排序字段对数据集进行排序。
    filter_backends = [OrderingFilter,]
    # 显式指定视图应该允许对任何模型字段或查询集聚合进行排序。
    # http://127.0.0.1:8000/book_drf/orderfilter/?ordering=-readcount
    ordering_fields = '__all__'

    # 指定分页器
    pagination_class = PageNum
    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要写













