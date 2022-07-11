# 1、启动celery服务
```ssh
cd celery_tasks
celery -A celery_tasks.main worker -l info  

## -A指对应的应用程序, 其参数是项目中 Celery实例的位置。
## worker指这里要启动的worker。
## -l指日志等级，比如info等级。
```


`celery -A celery_tasks.main worker -l info  -c 20`

默认是进程池方式，进程数以当前机器的CPU核数为参考，每个CPU开四个进程。
如何自己指定进程数：`celery worker -A proj --concurrency=4`
如何改变进程池方式为协程方式,但需要安装：`celery worker -A proj --concurrency=1000 -P eventlet -c 1000`

## 启用 Eventlet 池,`pip install eventlet`
```
celery -A celery_tasks.main worker -l info -P eventlet -c 1000
```