from django.contrib.auth.mixins import  LoginRequiredMixin
from django.http import JsonResponse

from shop.utils.response_code import  RETCODE
class LoginRequiredJSONMixin(LoginRequiredMixin):
    """自定义判断用户是否登录扩展类，返回JSON数据"""

    # 子类继承LoginRequiredMixin的handle_no_permission方法重写
    # 如果用户未登录，对应怎样的操作
    def handle_no_permission(self):
        """直接响应JSON数据"""
        return JsonResponse({'code':RETCODE.SESSIONERR,'errmsg':'用户未登录'})



