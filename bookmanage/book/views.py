from django.shortcuts import render
from  django.http import  HttpRequest,HttpResponse
from book.models import BookInfo,PeopleInfo
from django.db.models import *
# Create your views here.
"""
视图
1.就是python函数
2.函数的第一个参数就是 请求  和请求相关的 它是 HttpRequest的实例对象
3.我们必须要返回一个相应   相应是 HttpResponse的实例对象/子类实例对象
"""

def index(request):
    name = '志玲姐姐 '
    # request, template_name, context=None
    # 参数1: 当前的请求
    # 参数2: 模板文件
    # 参数3:context 传递参数
    print('request请求:', request)
    # 实现业务逻辑
    # 1.先把所有书籍查询出来
    # select * from bookinfo
    # ORM
    books=BookInfo.objects.all()
    # books = [BookInfo(),BookInfo()]
    # 2.组织数据
    context={'name':name,'books':books}
    for book in books:
        print('书籍：',book)
    # 3.将组织号的数据传递给模板
    return render(request,'index.html',context=context)
    # return HttpResponse('index')

'''
    缓存:
'''