from apscheduler.schedulers.background import BackgroundScheduler # 使用它可以使你的定时任务在后台运行
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import time
from scheduler import views
from collections import OrderedDict
from django.template import loader
import os
from django.conf import settings


from contents.utils import get_categories
from contents.models import *

# Create your views here.
'''
date：在您希望在某个特定时间仅运行一次作业时使用
interval：当您要以固定的时间间隔运行作业时使用
cron：以crontab的方式运行定时任务
minutes：设置以分钟为单位的定时器
seconds：设置以秒为单位的定时器
'''



scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
@register_job(scheduler, "interval",id='test',replace_existing=True,seconds=300)
def test_job():
    # 定时每5秒执行一次
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
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
    html_text = template.render(context)
    # 4、将首页html字符串写入到指定目录，命名'index.html'
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)

# 启动定时器
scheduler.start()
