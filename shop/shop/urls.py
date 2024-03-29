"""shop URL Configuration

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
from django.urls import path,re_path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 在include 的第二个参数中添加一个 namespace,避免不同应用中的路由使用了相同的名字发生冲突，使用命名空间区别开。
    # 这样的话 我们的name 就变为了 namespace:name
    # namespace 习惯上使用 子应用的名字

    # include((pattern_list, app_namespace), namespace=None)
        # 参数:
        # module -- URLconf 模块（或模块名称）
        # namespace (str) -- 包含的 URL 条目的实例命名空间。
        # pattern_list -- 可迭代的 path() 和／或 re_path() 实例。
        # app_namespace (str) -- 被包含的 URL 条目的应用命名空间

    # users
    re_path(r'^',include(('users.urls','users'),namespace='users')),
    # contents
    re_path(r'^', include(('contents.urls', 'contents'), namespace='contents')),
    # verifications
    re_path(r'^',include('verifications.urls')),
    # oauth
    re_path(r'^',include('oauth.urls')),
    # areas
    re_path(r'^',include('areas.urls')),
    # goods
    re_path(r'^',include(('goods.urls','goods'), namespace='goods')),
    # haystack
    re_path(r'^search/',include('haystack.urls')),
    # carts
    re_path(r'^',include(('carts.urls','goods'), namespace='carts')),
    # orders
    re_path(r'^',include(('orders.urls','orders'), namespace='orders')),
    # payment
    re_path(r'^',include(('payment.urls','payment'), namespace='payment')),
    # scheduler
    re_path(r'^',include('scheduler.urls')),
    # shop_admin
    re_path(r'^shop_admin/', include('shop_admin.urls')),

]
