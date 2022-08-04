from django.urls import re_path

from .views import *
urlpatterns = [

    re_path(r'^books/$', BooksView.as_view()),
    # 获取图书按钮
    re_path(r'^books/(?P<pk>\d+)/$', BookView.as_view()),
]
