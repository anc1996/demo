from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotFound,JsonResponse,HttpResponseForbidden,HttpResponseServerError
from django.utils import timezone
from datetime import datetime
# 分页器（先规定每页多少文字，然后确定多少页）
# 数据库中的记录就是文字，我们需要考虑在分页时每页的条数，然后得出多少页
from django.core.paginator import Paginator,EmptyPage
import logging

from contents.utils import get_categories,get_breadcrumb
from .models import GoodsCategory,SKU,GoodsVisitCount
from shop.utils.response_code import RETCODE
# Create your views here.
"""
1、提供商品列表页
2、商品热销排行
"""
# 创建日志输出器
logger=logging.getLogger('goods')

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

class DetailView(View):
    """商品详情页"""
    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, '404.html')
        # 查询商品分类
        channel_group_list = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        # 获取当前显示商品的所有规格，例如sku=2
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            # 添加该规格的所有选项 ，sku-key对应规格id为[1，3，7]
            sku_key.append(spec.option.id)

        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # spec_sku_map --> {(1,4,7):1,(1,3,7):2}


        # 获取当前商品的这一类所有的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options


        # 构造上下文
        context={
            'categories': channel_group_list,
            'breadcrumb': breadcrumb,
            'sku':sku,
            'specs':goods_specs,
        }


        return render(request, 'detail.html',context)


class DetailVisitView(View):
    """详情页分类商品访问量"""

    def post(self, request, category_id):
        """记录分类商品访问量
            如果访问记录存在，说明今天不是第一次访问，不新建记录，访问量直接累加。
            如果访问记录不存在，说明今天是第一次访问，新建记录并保存访问量。
        """
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return HttpResponseForbidden('缺少category_id必传参数')
        # 获取今天的日期
        t = timezone.localtime()

        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        today_date = datetime.strptime(today_str, '%Y-%m-%d')# 时间字符串转时间对象。
        # datetime.strftime() 时间对象转字符串
        try:
            counts_data = GoodsVisitCount.objects.get(category=category,date=today_date)
        except GoodsVisitCount.DoesNotExist:
            # 如果该类别的商品在今天没有过访问记录，就新建一个访问记录
            counts_data = GoodsVisitCount()
            counts_data.category = category
        counts_data.count += 1
        try:
            counts_data.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError('统计失败')
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


