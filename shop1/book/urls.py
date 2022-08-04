from django.urls import re_path

from .views import *
urlpatterns = [
    re_path(r'^$',IndexView.as_view()),
    # 登录
    re_path(r'^login/$',LoginView.as_view()),
    # 获取图书按钮
    # re_path(r'^book/(?P<pk>\d+)/$',BookView.as_view()),

]
