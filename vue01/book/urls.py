from django.urls import re_path
from  book.views import *
urlpatterns = [
#index/
    # url的第一参数是:正则
    # url的第二参数是:视图函数名
    #pay/order/
    re_path(r'^login/$', LoginView.as_view()),
    re_path(r'^recevieview/$', RecevieView.as_view()),
]
