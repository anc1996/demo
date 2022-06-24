from django.shortcuts import render
from  django.http import  HttpRequest,HttpResponse
from book.models import BookInfo,PeopleInfo
from django.db.models import *
from django.core.paginator import Paginator
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

"""
类似于 ipython的东西可以用来操作数据库
python manage.py shell
"""

#############################新增数据#####################################
# 方式1
# 要在python manage.py shell环境里，手动调用save方法
book=BookInfo(name='Python入门',pub_date='2000-01-01')
# 需要手动调用save方法
book.save()

# 方式2  要在python manage.py shell环境里，
# 直接入库
# objects 模型的管理类
# 我们对模型的 增删改查 都找它
# 会把新生成的对象返回给我们
BookInfo.objects.create(name='java',pub_date='2010-1-1')

#############################修改(更新)数据#####################################
# 方式1
# 1.先查询数据
# select * from bookinfo where id=1
book1=BookInfo.objects.get(id=1)   #book: <BookInfo: 射雕英雄传>
#2. 直接修改实例的属性
book1.readcount=20
#3.调用save方法
book1.save()


# 方式2  直接更新
# filter 过滤
BookInfo.objects.filter(id=1).update(
    readcount=150,
    commentcount=300
)  # 成功返回：1


##############################删除数据#####################################
#方式1
# 1. 先查询出数据
book2=BookInfo.objects.get(id=5)
#2.调用删除方法
book2.delete()

#方式2
BookInfo.objects.filter(id=6).delete()

###############################基本查询#####################################


# get  得到某一个数据
# all  获取所有的
# count 个数

#select * from bookinfo where id=1
# 返回一个单一对象
book3=BookInfo.objects.get(id=1)
#查询id 不存在的数据会抛出异常
try:
    book=BookInfo.objects.get(id=100)   # raise self.model.DoesNotExist

except BookInfo.DoesNotExist:
    pass

# 返回所有结果,返回所有结果的列表
boolist=BookInfo.objects.all()

# count
count=BookInfo.objects.all().count()
count=BookInfo.objects.count()


###############################filter,get,exclude#####################################
"""
    select * from bookinfo where 条件语句
    相当于 where查询
    
    filter          : 筛选/过滤 返回 n个结果 (n = 0/1/n)
    get             :           返回1个结果
    exclude         : 排除掉符合条件剩下的结果  相当于 not
    
    语法形式:
        以filter(字段名__运算符=值) 为例
"""

# 查询编号为1的图书
book=BookInfo.objects.get(id=1)  #get返回单一对象
books=BookInfo.objects.filter(id=1) #filter返回的是一个列表
books=BookInfo.objects.filter(id__exact=1) #exact：表示判等。精确值
print(book[0])

# 查询书名包含'湖'的图书
# name_contains包含
books=BookInfo.objects.filter(name__contains='湖')
# name__endswith以’湖‘结尾的书名
books=BookInfo.objects.filter(name__endswith='湖')


# 查询书名以'部'结尾的图书
books=BookInfo.objects.filter(name__endswith='部')

# 查询书名为空的图书
books=BookInfo.objects.filter(name__isnull=True)
# 查询编号为1或3或5的图书
books=BookInfo.objects.filter(id__in=[1,3,5])

# 查询编号大于3的图书,
# gt:greater than   gte:greater than or equal to
# lt:less than      lte:less than or equal to
# e:equal
books=BookInfo.objects.filter(id__gt=3)
# 查询编号不等于3的图书
books=BookInfo.objects.exclude(id=3)# 返回列表
# 查询编号等于3的图书
books=BookInfo.objects.filter(id__exact=3)

# 查询1980年发表的图书
books=BookInfo.objects.filter(pub_date__year='1980')

# 查询1990年1月1日后发表的图书
books=BookInfo.objects.filter(pub_date__gt='1990-1-1')

###############################F(了解)#####################################
# 使用F对象，被定义在django.db.models中,语法如下：F(属性名)
"""
首先导入包：from django.db.models import F
F对象的语法形式:filter(字段名__运算符=F('字段名'))
"""
# 查询阅读量大于等于评论量的图书。
books=BookInfo.objects.filter(readcount__gte=F('commentcount'))
#查询阅读量大于等于评论量2倍的图书
books=BookInfo.objects.filter(readcount__gte=F('commentcount')*2)



###############################Q对象(了解)#####################################

# 如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符，要导入：from django.db.models import Q
# 语法如下：Q(属性名__运算符=值)
"""
    Q(字段名__运算符=值)
    或  Q()|Q() ..
    并且 Q()&Q() ..
    not  ~Q()
"""
# 需要查询id大于2 或者 阅读量大于20的书籍
books=BookInfo.objects.filter(Q(id__gt=2)|Q(readcount__gt=20))
# 查询阅读量大于20的图书
books=BookInfo.objects.filter(Q(readcount__gt=20))
# 查询书籍id不为3
books=BookInfo.objects.filter(~Q(id=3))

# 多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字。
# 需要查询id大于2 并且阅读量大于20的书籍
#方式1
# filter().filter()
books=BookInfo.objects.filter(id__gt=2).filter(readcount__gt=20)
#方式2
# filter(条件,条件)
books=BookInfo.objects.filter(id__gt=2,readcount__gt=20)

###############################聚合函数(了解)#####################################
# 首先导入from django.db.models import Avg,Sum
# 使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg平均，Count数量，Max最大，Min最小，Sum求和，
# 语法形式是: aggragte(Xxx('字段'))
# 当前数据的阅读总量
book_dist=BookInfo.objects.aggregate(Sum('readcount')) #返回字典：{'readcount__sum': 214}
# 当前数据的阅读平均量
book_dist=BookInfo.objects.aggregate(Avg('readcount'))
# 当前数据的数量
book_dist=BookInfo.objects.aggregate(Count('id'))
# 当前数据的最大数量
book_dist=BookInfo.objects.aggregate(Max('readcount'))
#当前数据的最小数量
book_dist=BookInfo.objects.aggregate(Min('readcount'))


###############################排序#####################################
# 使用order_by对结果进行排序,返回列表
# 默认升序
books=BookInfo.objects.all().order_by('readcount')
# 降序
books=BookInfo.objects.all().order_by('-readcount')


###############################关联查询#####################################
"""
书籍和人物的关系是   1:n
    书籍 中没有任何关于人物的字段
    人物 中有关于书籍的字段 book 外键

语法形式

    通过书籍查询人物信息(已知主表数据,关联查询从表数据)
    主表模型(实例对象).关联模型类名小写_set.all()
    通过人物查询书籍信息( 已知 从表数据,关联查询主表数据)
    从表模型(实例对象).外键
    
    
"""


# 查询书籍为'天龙八部'的所有人物信息
book=BookInfo.objects.filter(name='天龙八部') #返回的是列表，不是对象
# 通过书籍查询任务信息
people=book[0].peopleinfo_set.all()
people_book=people[0].book_id

# 查询书籍为1的所有人物信息
book = BookInfo.objects.get(id=1)
people=book.peopleinfo_set.all()

#查询人物为1的书籍信息
#1. 查询任务
person=PeopleInfo.objects.get(id=1)
#2.根据人物关联查询书籍
'''通过人物查询书籍信息（已知从表数据，关联查询主表数据)
'''
book_name=person.book.name
book_count=person.book.readcount


"""
     我们需要的是书籍信息,已知条件是人物信息
    我们需要的是主表数据, 已知条件是从表信息

    filter(关联模型类名小写__字段__运算符=值)

"""
# 查询图书，要求图书人物为"郭靖"
book=BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
book=BookInfo.objects.filter(peopleinfo__name='郭靖')
# 查询图书，要求图书中人物的描述包含"八"
person=BookInfo.objects.filter(peopleinfo__description__contains='八')
'''
    我们需要的是 人物信息,已知条件是 书籍信息
    我们需要是是 从表数据,已知条件是 主表信息
    
    filter(外键__字段__运算符=值)
    注意：如果没有"__运算符"部分，表示等于。
'''
# 查询书名为“天龙八部”的所有人物
person=PeopleInfo.objects.filter(book__name='天龙八部')
person=PeopleInfo.objects.filter(book__name__exact='天龙八部')
# 查询图书阅读量大于30的所有人物
person=PeopleInfo.objects.filter(book__readcount__gt=80)


###############################查询集#####################################
'''
Django的ORM中存在查询集的概念。
查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。
当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：
    all()：返回所有数据。
    filter()：返回满足条件的数据。
    exclude()：返回满足条件之外的数据。
    order_by()：对结果进行排序。
特性：1、惰性执行  2、缓存
    
'''
#默认升序
books = BookInfo.objects.filter(readcount__gt=30).order_by('pub_date')
#默认降序
books = BookInfo.objects.filter(readcount__gt=30).order_by('-pub_date')

#当执行如下语句时，并未进行数据库查询，只是创建了一个查询集books
books = BookInfo.objects.all()

#缓存方法
books=BookInfo.objects.all()
bookid_list=[book.id for book in books]
# 限制查询集
books = BookInfo.objects.all()[0:2]

#######################分页##############################
# from django.core.paginator import Paginator

books= BookInfo.objects.all()
#object_list        结果集 /列表
#  per_page         每页多少条记录
#object_list, per_page
p=Paginator(list(books),2)
#共多少条
p_count=p.count
#获取第几页的数据
books_page=p.page(1)
books_1=books_page.object_list  #[<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>]
#获取分页数据
total_page=p.num_pages