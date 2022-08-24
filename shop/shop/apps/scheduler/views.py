from datetime import datetime, time

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.redis import RedisJobStore
from collections import OrderedDict

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.template import loader
import os
from django.conf import settings


from contents.utils import get_categories
from contents.models import *

def test_job():
    # 定时每5秒执行一次
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
    print(settings.STATICFILES_DIRS)
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
'''
APScheduler basic concepts:
    triggers:触发器包含调度逻辑。每个作业都有自己的触发器，该触发器确定下一次运行作业的时间。在初始配置之外，触发器是完全无状态的。
    job stores:job stores存放计划的工作。默认作业存储只是将作业保存在内存中，而其他作业存储在各种类型的数据库中.作业存储绝不能在计划程序之间共享。
    executors:executors负责运行作业。它们通常是通过将作业中指定的可调用内容提交给线程或进程池来实现这一点的。当作业完成时，executors通知schedulers，
              然后schedulers发出适当的事件。
    schedulers：schedulers与休眠区绑定一起。应用程序中通常只运行一个计划程序。应用程序开发人员通常不直接处理
                作业存储（job stores）、执行器（executors）或触发器（triggers）。
                相反，调度程序提供适当的接口来处理所有这些。作业存储器和执行器的配置是通过调度程序完成的，添加、修改和删除作业也是如此。
'''

'''
choosing a scheduler:
    BlockingScheduler:当进程中只有schedulers在运行时使用
    BackoundScheduler:当您不使用以下任何框架时使用，并希望scheduler在应用程序内部的后台运行
    AsyncIOScheduler: 在应用程序使用异步模块时使用
    TornadoScheduler:在Tornado IOLoop.上运行的调度程序。

APScheduler 有三种内置的触发器（triggers）类型:
    data:当您希望在某个时间点只运行作业一次时使用
    interval:当您希望以固定的时间间隔运行作业时使用
    cron:当您希望在一天中的特定时间周期性地运行作业时使用

Starting the scheduler:
        
    
'''



# Create your views here.
'''
date：在您希望在某个特定时间仅运行一次作业时使用
interval：当您要以固定的时间间隔运行作业时使用
cron：以crontab的方式运行定时任务
minutes：设置以分钟为单位的定时器
seconds：设置以秒为单位的定时器
'''



# id：指定作业的唯一ID
# name：指定作业的名字
# trigger：apscheduler定义的触发器，用于确定Job的执行时间，根据设置的trigger规则，计算得到下次执行此job的时间， 满足时将会执行
# executor：apscheduler定义的执行器，job创建时设置执行器的名字，根据字符串你名字到scheduler获取到执行此job的 执行器，执行job指定的函数
# max_instances：执行此job的最大实例数，executor执行job时，根据job的id来计算执行次数，根据设置的最大实例数来确定是否可执行
# next_run_time：Job下次的执行时间，创建Job时可以指定一个时间[datetime],不指定的话则默认根据trigger获取触发时间
# misfire_grace_time：Job的延迟执行时间，例如Job的计划执行时间是21:00:00，但因服务重启或其他原因导致21:00:31才执行，如果设置此key为40,则该job会继续执行，否则将会丢弃此job
# coalesce：Job是否合并执行，是一个bool值。例如scheduler停止20s后重启启动，而job的触发器设置为5s执行一次，因此此job错过了4个执行时间，如果设置为是，则会合并到一次执行，否则会逐个执行
# func：Job执行的函数
# args：Job执行函数需要的位置参数
# kwargs：Job执行函数需要的关键字参数




executors = {
    'default': ThreadPoolExecutor(20), # 一个名为“ default”的 ThreadPoolExecator，其 worker 计数为20
    'processpool': ProcessPoolExecutor(5) # 一个名为“ processpool”的 ProcessPoolExecator，其 worker 计数为5
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
jobstores = {
    'redis': RedisJobStore(
        db=10,
        jobs_key="apschedulers.default_jobs",
        run_times_key="apschedulers.default_run_times",
        host="42.112.30.108",
        port=6466,
        password="qwe987"
    ),
}
scheduler= BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler.add_job(test_job,'interval', minutes=5,id='my_job_id',misfire_grace_time =4)
def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print(
            "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}".format(
                event.code,
                event.job_id,
                event.jobstore
            ))
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()