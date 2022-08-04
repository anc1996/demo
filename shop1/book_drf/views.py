from django.http import JsonResponse
from django.views import View


from books.models import BookInfo
from book_drf.serializer import BookSerializer
# Create your views here.
class Books(View):


    def get(self,request):
        # 1、查询所有图书对象
        books=BookInfo.objects.all()
        bookserializer=BookSerializer(books,many=True)
        return JsonResponse(bookserializer.data, safe=False)



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
