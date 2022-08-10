from rest_framework.viewsets import ViewSet
from rest_framework.views import Response

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
"""

'''
ViewSet继承自APIView，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等。
在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。

'''
class Books(ViewSet):
    """获取所有图书"""
    # 自定义方法名，代替get方法,在urls路由匹配对应方法名
    def list(self, request):
        # 1、查询所有图书对象
        print(request.query_params)
        books = BookInfo.objects.all().filter(is_delete=False)
        bookserializer = BookSerializer(books, many=True)
        return Response(bookserializer.data)


    """保存图书"""
    # 自定义方法名，代替post方法,在urls路由匹配对应方法名
    def create(self, request):
        # 请求体获取数据
        data_dict = request.data
        # 2、验证数据
        bookserializer = BookSerializer(data=data_dict)  # 字节转化data类型
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True)  # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)

    def retrieve(self,request,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=400)
        bookserializer = BookSerializer(book)
        return Response(bookserializer.data)


class BookView(ViewSet):
    """查询单一数据"""

    def get(self, request, pk):
        # 1、查询数据对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=400)
        bookserializer = BookSerializer(book)
        return Response(bookserializer.data)

    """更新单一图书"""

    def update(self, request, pk):
        # 1、获取数据
        book_dict = request.data
        # 2、验证数据库是否有数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'error': '数据库已存在'}, status=404)
        # 3、验证数据
        bookserializer = BookSerializer(book, data=book_dict)
        bookserializer.is_valid()
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return Response(bookserializer.data)

    



