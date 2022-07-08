# 1、启动celery服务
```ssh
cd celery_tasks
celery -A celery_tasks.main worker -l info  

## -A指对应的应用程序, 其参数是项目中 Celery实例的位置。
## worker指这里要启动的worker。
## -l指日志等级，比如info等级。
```

