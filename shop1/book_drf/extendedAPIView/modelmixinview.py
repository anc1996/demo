from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin

from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.
"""
五个扩展类（配合GenericAPIview使用继承object）
CreateModelMixin：保存数据
ListModelMixin：获取多个数据对象
UpdateModelMixin：更新数据
DestroyModelMixin：删除数据
RetrieveModelMixin：获取单一数据
"""

class Books(GenericAPIView,CreateModelMixin,ListModelMixin):

    """
    GenericAPIView
    支持定义的属性：
    列表视图与详情视图通用：
        queryset 列表视图的查询集
        serializer_class 视图使用的序列化器
    列表视图使用：
        pagination_class 分页控制类
        filter_backends 过滤控制后端
    详情页视图使用：
        lookup_field 查询单一数据库对象时使用的条件字段，默认为'pk'
        lookup_url_kwarg 查询单一数据时URL中的参数关键字名称，默认与look_field相同

    """
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 交给扩展类ListModelMixin来写
    def get(self,request):
        return self.list(request)

    """保存图书"""

    # 交给扩展类CreateModelMixin来写
    def post(self, request):
       return self.create(request)


class BookView(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 方法一、
    """查询单一数据"""
    def get(self,request,pk):
        return self.retrieve(request,pk)

    """更新单一图书"""
    def put(self, request, pk):
        return self.update(request,pk)

    """删除图书"""
    def delete(self,request,pk):
        return self.destroy(request,pk)




