from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound,JsonResponse
# 分页器（先规定每页多少文字，然后确定多少页）
# 数据库中的记录就是文字，我们需要考虑在分页时每页的条数，然后得出多少页
from django.core.paginator import Paginator,EmptyPage

from contents.utils import get_categories,get_breadcrumb
from .models import GoodsCategory,SKU
from shop.utils.response_code import RETCODE
# Create your views here.
"""
1、提供商品列表页
2、商品热销排行
"""
class ListView(View):
    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        # 校验参数，category_id为三级id
        try:
            category=GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return HttpResponseNotFound('GoodsCategory does not exist')
        except GoodsCategory.MultipleObjectsReturned:
            return HttpResponseNotFound('不是查找三级分类')

        """分页和排序：category_id查询sku，一查多。"""
        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')
        # 按照排序规则查询该分类商品SKU信息，排序的属性必须是模型类的
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'
            sort_field = 'create_time'
        # skus=SKU.objects.filter(category=category,is_launched=True)
        skus=category.sku_set.filter(is_launched=True).order_by(sort_field)

        # 创建分页器
        # Paginator('要分页的数据','每页记录的条数')
        paginator = Paginator(skus, 10)
        try:
            # 获取每页商品数据
            page_skus = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        # 查询商品分类
        channel_group_list = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 构造上下文
        context={'categories':channel_group_list,
                 'breadcrumb':breadcrumb,
                 'page_skus':page_skus,
                 'total_page':total_page,
                 'sort':sort,
                'page_num':page_num,
                 'category_id':category_id
                 }
        return render(request, 'list.html',context)

class HotGoodsView(View):
    """商品热销排行"""
    def get(self,request,category_id):
        """提供商品热销排行JSON数据"""
        # 根据销量倒序,并且是上架的状态前2位。
        skus=SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]
        '''{
            "code": "0",
            "errmsg": "OK",
            "hot_skus": [
                {
                    "id": 6,
                    "default_image_url": "http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRbI2ARekNAAFZsBqChgk3141998",
                    "name": "Apple iPhone 8 Plus (A1864) 256GB 深空灰色 移动联通电信4G手机",
                    "price": "7988.00"
                },
              ...
            ]
        }'''
        # 序列化
        hot_skus = []
        for sku in skus:
            hot_skus.append(
                {'id':sku.id,'default_image_url':sku.default_image.url,
                 'name':sku.name,'price':sku.price}
            )
        return JsonResponse({"code": RETCODE.OK,"errmsg": "OK","hot_skus":hot_skus})