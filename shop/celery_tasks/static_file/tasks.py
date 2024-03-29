
import sys
# sys.path.insert(0, '../')

import django
import os
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.dev'
from django.shortcuts import render
from django.template import loader
from django.conf import settings
from celery_tasks.main import celery_app

from goods.models import SKU
from contents.utils import get_categories
from goods.utils import get_breadcrumb


# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
# 创建日志输出器
@celery_app.task(bind=True,name='get_detail_html',retry_backoff=3,max_retries=4) # name给任务起别名
def get_detail_html(self,sku_id):
    # 获取当前sku的信息
    sku = SKU.objects.get(id=sku_id)
    # 查询商品频道分类
    channel_group_list = get_categories()
    # 查询面包屑导航
    breadcrumb = get_breadcrumb(sku.category)

    # 构建当前商品的规格键
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
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
    # 获取spu
    spu=sku.spu
    # 获取当前商品的规格信息
    goods_specs = spu.specs.order_by('id')
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
    context = {
        'categories': channel_group_list,
        'breadcrumb': breadcrumb,
        'category_id': sku.category_id,
        'sku': sku,
        'spu': spu,
        'specs': goods_specs,
    }

    response = render(None, 'detail.html', context)
    file_path = os.path.join(settings.BASE_DIR, 'static/detail/%d.html' % sku.id)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response.content.decode())

