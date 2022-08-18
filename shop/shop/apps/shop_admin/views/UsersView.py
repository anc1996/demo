from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

from shop_admin.serializers import User_serializer
from users.models import User

class PageNum(PageNumberPagination):

    #默认值与 PAGE_SIZE 设置键相同。 如果设置了，则settings.py重写 PAGE_SIZE 。
    # page_size显示<max_page_size
    page_size = 5
    # 指定查询参数的名称，该参数允许客户端根据每个请求设置页面大小。
    # 默认为“无”，表示客户端可能无法控制请求的页面大小。
    page_size_query_param = 'pagesize'
    # 指示所请求的页面大小的最大允许值。只有当 page_size_query_param 也被设置时，此属性才有效。
    max_page_size =10

    # 重写分页返回方法，按照指定的字段进行分页数据返回
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # 总数量
            'lists': data,  # 用户数据
            'page' : self.page.number, # 当前页数
            'pages' : self.page.paginator.num_pages, # 总页数
            'pagesize':self.page_size  # 后端指定的页容量
        })



class UserView(ListCreateAPIView):
    """用户管理"""
    # 权限指定
    permission_classes = [IsAdminUser]

    # 1、要指定当前类视图使用的查询数据
    # 重写get_queryset方法，根据前端是否传递keyword值返回不同查询结果
    def get_queryset(self):
        """查询数据"""
        # 获取前端传递的keyword值
        keyword = self.request.query_params.get('keyword')
        if keyword is None or keyword is '':
            return User.objects.all()
        else:
            return User.objects.filter(username__contains=keyword)

    # 2、要指定当前视图使用的序列化器
    # serializer_class =User_serializer.UserSerializer
    def get_serializer_class(self):
        # 请求方式是GET，则是获取用户数据返回UserSerializer
        if self.request.method == 'GET':
            return User_serializer.UserSerializer
        else:
            # POST请求，完成保存用户，返回UserAddSerializer
            return User_serializer.UserAddSerializer

    # 3、指定分页器，会调用ModelMixin的list方法
    pagination_class = PageNum



    #