"""bookmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path,re_path
from book.views import index
"""
1.urlpatterns 是固定写法. 它的值是列表
2.我们在浏览器中输入的路径和会 urlpatterns中的每一项顺序进行匹配
    如果匹配成功,则直接引导到相应的模块.
    如果匹配不成功(把urlpatterns中的每一个都匹配过了),则直接返回404.
3.urlpatterns中的元素 是 url
    url的第一个参数是: 正则
            r 转义
            ^ 严格的开始
            $ 严格的结尾

4.我们在浏览器中输入的路由 中 哪些部分参与正则匹配?
    http://ip:port/path/?key=value
    我们的http://ip:port/ 和 get、post参数不参与正则匹配

5. 如果和当前的某一项匹配成功,则引导到子应用中继续匹配
    如果匹配成功,则停止匹配返回相应的视图
    如果匹配不成功,则继承和后边的工程中的url的每一项继续匹配,直到匹配每一项,

6.
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^',include('book.urls')),
    # re_path(r'^index/$',index)
    re_path(r'^',include('pay.urls'))
]
