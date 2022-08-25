# celery的入口
from celery import Celery
import os

# 为celery使用django配置文件进行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.dev'

# 创建celery实例，对应生产者
celery_app=Celery('producer')
# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.send_sms_code',
                               'celery_tasks.email','celery_tasks.static_file'
                               ])
#
## 消费者为celery，启动进程

