from  book.views import *
from django.urls import re_path
urlpatterns = [
#index/
    # url的第一参数是:正则
    # url的第二参数是:视图函数名
    #pay/order/
    # name是url的别名，我们可以通过name找到这个路由
    re_path(r'^index/$',index,name='index'),

    # re_path(r'^(10)/(100)/$',detail2,name='detail2'),
    # 分组来获取正则中的数据
    # 根据位置来获取 url中的参数
    re_path(r'^(\d+)/(\d+)/$',detail2,name='detail2'),
    #http://127.0.0.1:8000/分类id/书籍id/
    #http://127.0.0.1:8000/category_id/book_id/
    # re_path(r'^(\d+)/(\d+)/',detail,name='detail'),#detail() takes 1 positional argument but 3 were given，正则表达式传递了参数，需要定义参数
# url(r'^(?P<category_id>\d+)/(?P<book_id>\d+)/$',detail),
    # 关键字参数--推荐大家使用关键字参数
    # 关键字参数，推荐使用
    re_path(r'^(?P<category_name>\D+)/(?P<book_id>\d+)/', detail, name='detail'),
    re_path(r'^post/',detail1,name='post1'),
    re_path(r'^post_json',post_json,name='post_json'),
    re_path(r'^meta',meta,name='meta'),
    re_path(r'^response',response1,name='response'),
    re_path(r'^jsonresponse',jsonresponse,name='jsonresponse'),
    re_path(r'^tiaozhuan',tiaozhuan,name='tiaozhuan'),
    re_path(r'^set_cookie/',set_cookie,name='set_cookie'),
    re_path(r'^get_cookie/',get_cookie,name='get_cookie'),
    re_path(r'^set_session/', set_session, name='set_session'),
    re_path(r'^get_session/', get_session, name='get_session'),

    # re_path的第一个参数是 正则
    # re_path的第二个参数是 视图函数名
    # re_path(r'^login',login,name='login'),
    re_path(r'^loginbook',BookView.as_view()),

    re_path(r'^home/$',HomeView.as_view()),
    re_path(r'^detail/$',detailView.as_view()),
    re_path(r'^center',CenterView.as_view()),
    re_path(r'^login/$',LoginView.as_view())
]
