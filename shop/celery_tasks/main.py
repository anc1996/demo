# celery的入口
from celery import Celery

# 创建celery实例，对应生产者
celery_app=Celery('producer')
# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.send_sms_code'])



