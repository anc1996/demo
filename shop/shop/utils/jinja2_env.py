from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage # 静态文件的存储


def jinja2_environment(**options):
    # 1.创建 Environment实例
    env = Environment(**options)
    # 2.指定(更新) jinja2的函数指向django的指定过滤器
    env.globals.update({
        # 自定义语法’{{ url('路由的命名空间') }} {{ static('相对路径') }}
        'static': staticfiles_storage.url, # 静态文件的前缀
        'url': reverse,# 反向解析
    })
    # 3.返回Environment实例
    return env


"""
确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句 
"""