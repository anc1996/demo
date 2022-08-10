import datetime
import json
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse


from books.models import BookInfo

# Create your views here.


class BooksView(View):
    """查询所有图书"""
    def get(self,request):
        books=BookInfo.objects.all()
        book_list=[]
        # 返回图书，
        for book in books:
            if not book.is_delete:
                book_list.append({
                    'id':book.id,
                    'name':book.name,
                    'pub_date':book.pub_date,
                    'readcount':book.readcount,
                    'commentcount':book.commentcount,
                })
        return JsonResponse(book_list,safe=False)

    """保存图书"""
    def post(self,request):
        # 请求体获取数据
        # 验证数据
        name=request.POST.get('name')
        pub_date=request.POST.get('pub_date')
        readcount=request.POST.get('readcount')
        commentcount=request.POST.get('commentcount')
        if not(all([name,pub_date])):
            return JsonResponse({'error':'如果缺少必传参数，响应错误信息，403'},status=400)
        book=BookInfo.objects.create(name=name,pub_date=pub_date,readcount=readcount,commentcount=commentcount)
        context={
                    'id':book.id,
                    'name':book.name,
                    'pub_date':book.pub_date,
                    'readcount':book.readcount,
                    'commentcount':book.commentcount,
                }
        return JsonResponse(context)


class BookView(View):


    """查询单一数据"""
    def get(self,request,pk):
        # 1、查询数据对象
        try:
            book=BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '当前数据不存在'}, status=400)
        context = {
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount,
            'commentcount': book.commentcount,
        }
        return JsonResponse(context)

    """更新单一图书"""
    def put(self,request,pk):

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)
        if not (all([book_dict.get('name'), book_dict.get('pub_date')])):
            return JsonResponse({'error': '如果缺少必传参数，响应错误信息，403'}, status=400)
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)
        book.name=book_dict.get('name')
        book.readcount=book_dict.get('readcount')
        book.commentcount=book_dict.get('commentcount')
        book.pub_date =book_dict.get('pub_date')
        book.save()
        context = {
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date,
            'readcount': book.readcount,
            'commentcount': book.commentcount,
        }
        return JsonResponse(context)


    """删除单一图书"""
    def delete(self,reuqest,pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({'error': '如果缺少必传参数，响应错误信息，404'}, status=404)
        book.is_delete=True
        book.save()
        return JsonResponse({})