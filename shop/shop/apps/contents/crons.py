from collections import OrderedDict
from django.template import loader
import os
from django.conf import settings

from contents.utils import get_categories
from contents.models import *
# 2.什么是页面静态化
# 将动态渲染生成的页面结果保存成html文件，放到静态文件服务器中。
# 用户直接去静态服务器，访问处理好的静态html文件。



def generate_static_index_html():
    """
    生成静态的主页html文件
    """
# 步骤：
    # 1、查询首页相关数据
    """1、查询并展示商品分类"""
    channel_group_list = get_categories()

    """2、查询首页广告数据"""
    # 第一步：查询所有广告类别
    contents = OrderedDict()
    contentCategory_list = ContentCategory.objects.all()
    for contentCategory in contentCategory_list:
        # 查询未下架的广告并排序
        content_list = contentCategory.content_set.filter(status=True).order_by('sequence')
        contents[contentCategory.key] = content_list
        # 第二步：使用广告类别查询出该类别对应的广告内容
    context = {'categories': channel_group_list, 'contents': contents}

    # 2、获取首页模板文件
    template = loader.get_template('index.html')  # 此函数使用给定名称加载模板并返回 Template 对象。
    # 3、渲染首页html字符串,如果提供了 context ，则必须是 dict。如果未提供，则引擎将使用空上下文渲染模板。
    html_text=template.render(context)
    # 4、将首页html字符串写入到指定目录，命名'index.html'
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)