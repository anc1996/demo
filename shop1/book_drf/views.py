import json

from django.http import JsonResponse, HttpResponse
from django.views import View


from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.
class Books(View):


    def get(self,request):
        # 1、查询所有图书对象
        books=BookInfo.objects.all().filter(is_delete=False)
        bookserializer=BookSerializer(books,many=True)
        return JsonResponse(bookserializer.data, safe=False)

    """保存图书"""

    def post(self, request):
        # 请求体获取数据
        # 验证数据
        # x-www-form-urlencoded;charset=UTF-8
        if request.POST.get('name') is not None:
            name = request.POST.get('name')
            pub_date = request.POST.get('pub_date')
            readcount = request.POST.get('readcount')
            commentcount = request.POST.get('commentcount')
            data_dict={'name':name,'pub_date':pub_date,'readcount':readcount,'commentcount':commentcount}
        else:
            # 前端json请求
            data=request.body.decode()
            data_dict=json.loads(data)
        # 2、验证数据
        bookserializer=BookSerializer(data=data_dict)
        # raise_exception=True,REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。
        bookserializer.is_valid(raise_exception=True) # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return JsonResponse(bookserializer.data)


class BookView(View):

    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=400)
        bookserializer = BookSerializer(book)
        return JsonResponse(bookserializer.data)

    """更新单一图书"""

    def put(self, request, pk):
        # 1、获取数据
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)
        # 2、验证数据库是否有数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'error':'数据库已存在'},status=404)
        # 3、验证数据
        bookserializer = BookSerializer(book,data=book_dict)
        bookserializer.is_valid()
        # 4、更新数据
        bookserializer.save()
        # 6、返回结果
        return JsonResponse(bookserializer.data)


