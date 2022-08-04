from django.urls import re_path

from .views import *
urlpatterns = [

    re_path(r'books/$', Books.as_view()),
    re_path(r'book/(?P<pk>\d+)/$', BookView.as_view()),
]
