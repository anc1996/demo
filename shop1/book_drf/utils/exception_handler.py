from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError
from rest_framework.response import Response

# 配置全局数据库异常捕获
def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response