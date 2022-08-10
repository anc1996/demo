from rest_framework.viewsets import ReadOnlyModelViewSet

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

ReadOnlyModelViewSet
继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin。
"""


class Books(ReadOnlyModelViewSet):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer
    # 由于ModelViewSet继承ModelMixin的list、retrieve方法,不需要写
