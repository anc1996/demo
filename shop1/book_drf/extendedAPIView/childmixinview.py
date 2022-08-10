from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.
"""
五个扩展类如下：与配合GenericAPIview使用继承object的子类共9个。
CreateModelMixin：保存数据
ListModelMixin：获取多个数据对象
UpdateModelMixin：更新数据
DestroyModelMixin：删除数据
RetrieveModelMixin：获取单一数据

共9个扩展类的子类
1） CreateAPIView
提供 post 方法
继承自： GenericAPIView、CreateModelMixin
2）ListAPIView
提供 get 方法
继承自：GenericAPIView、ListModelMixin
3）RetireveAPIView
提供 get 方法
继承自: GenericAPIView、RetrieveModelMixin
4）DestoryAPIView
提供 delete 方法
继承自：GenericAPIView、DestoryModelMixin
5）UpdateAPIView
提供 put 和 patch 方法
继承自：GenericAPIView、UpdateModelMixin
6）RetrieveUpdateAPIView
提供 get、put、patch方法
继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin
7）RetrieveUpdateDestoryAPIView
提供 get、put、patch、delete方法
继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin
"""

# ListCreateAPIView继承GenericAPIView,CreateModelMixin,ListModelMixin
class Books(ListCreateAPIView):

    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 由于ListCreateAPIView有get、post方法,不需要写
    

# RetrieveUpdateDestroyAPIView继承GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
class BookView(RetrieveUpdateDestroyAPIView):
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    serializer_class = BookSerializer

    # 由于RetrieveUpdateDestroyAPIView有get、post、delete方法,不需要写




