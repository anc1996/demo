from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

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

    throttle_scope = 'contacts'


    # 由于ModelViewSet继承ModelMixin的list、update、retrieve、destory、create方法,不需要写










