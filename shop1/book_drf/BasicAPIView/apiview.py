
from rest_framework.views import APIView
from rest_framework.response import Response

from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.


class Books(APIView):
    """
    APIView是REST framework提供的所有视图的基类，继承自Django的View父类。

    APIView与View的不同之处在于：
        传入到视图方法中的是REST framework的Request对象，而不是Django的HttpRequeset对象；
        视图方法可以返回REST framework的Response对象，视图会为响应数据设置（render）符合前端要求的格式；
        任何APIException异常都会被捕获到，并且处理成合适的响应信息；
        在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。
    支持定义的属性：
        authentication_classes 列表或元祖，身份认证类
        permissoin_classes 列表或元祖，权限检查类
        throttle_classes 列表或元祖，流量控制类
    """

    def get(self,request):
        # 1、查询所有图书对象
        print(request.query_params)
        books=BookInfo.objects.all().filter(is_delete=False)
        bookserializer=BookSerializer(books,many=True)
        return Response(bookserializer.data)

    """保存图书"""

    def post(self, request):
        # 请求体获取数据
        # 验证数据
        # x-www-form-urlencoded;charset=UTF-8
        data_dict=request.data
        # 2、验证数据
        bookserializer=BookSerializer(data=data_dict) # 字节转化data类型
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True) # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return Response(bookserializer.data)


class BookView(APIView):

    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'error': '当前数据不存在'}, status=400)
        bookserializer = BookSerializer(book)
        return Response(bookserializer.data)

    """更新单一图书"""
    def put(self, request, pk):
        # 1、获取数据
        book_dict=request.data
        # 2、验证数据库是否有数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'error':'数据库已存在'},status=404)
        # 3、验证数据
        bookserializer = BookSerializer(book,data=book_dict)
        bookserializer.is_valid()
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return Response(bookserializer.data)


