from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import Response

from books.models import BookInfo
from book_drf.serializer import BookSerializer

# Create your views here.

class Books(GenericViewSet):
    """获取所有图书"""
    """获取所有图书"""
    # 1、要指定当前类视图使用的查询数据
    queryset = BookInfo.objects.all()
    # 2、要指定当前视图使用的序列化器
    # serializer_class = BookSerializer

    # 通过get_serializer_class方法返回应该用于序列化器的类。
    # 我们可以重写父类的get_serializer_class方法
    # 默认为返回序列化器 _ class 属性。
    def get_serializer_class(self):
        if self.action=='searchall':
            return BookSerializer
        else:
            return BookSerializer

    @action(methods=['get'],detail=False)
    # 自定义方法名，代替get方法,在urls路由匹配对应方法名
    def searchall(self, request):
        # 1、查询所有图书对象
        # 1、返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回queryset属性，可以重写
        # 获取查询集中的所有数据
        print(self.action) # action属性提取的是方法名,这里显示是searchall
        books = self.get_queryset()
        # 2、返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。
        # 使用指定序列化器，获取序列化对象
        bookserializer = self.get_serializer(books, many=True) # 调用get_serializer_class的函数
        return Response(bookserializer.data)

    """创建新的图书"""
    @action(methods=['post'],detail=False)
    # 自定义方法名，代替post方法,在urls路由匹配对应方法名
    def createone(self, request):
        # 请求体获取数据
        data_dict = request.data
        # 2、验证数据
        bookserializer = self.get_serializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True)  # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)

    # 获取单一图书
    @action(methods=['get'], detail=True)
    def getone(self, request, pk):
        try:
            # get_object(self) 返回详情视图所需的模型类数据对象，
            # 默认使用lookup_field参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=400)
        bookserializer = self.get_serializer(book)
        return Response(bookserializer.data)

    """更新单一图书"""
    @action(methods=['put'], detail=True)
    def refresh(self, request, pk):
        # 1、获取数据
        book_dict = request.data
        # 2、验证数据库是否有数据
        try:
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '数据库已存在'}, status=404)
        # 3、验证数据
        bookserializer =self.get_serializer(book, data=request.data)
        bookserializer.is_valid(raise_exception=True)
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return Response(bookserializer.data)

    # 删除数据
    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        try:
            book = self.get_object()  # 从查询集获取指定的单一数据对象
        except BookInfo.DoesNotExist:
            return Response({'error': '数据库已存在'}, status=404)
        book.delete()
        return Response({'ok': '删除成功'}, status=200)






