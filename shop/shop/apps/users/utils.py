# 自定义用户认证的后端：实现多账号登录
from django.contrib.auth.backends import ModelBackend
import re
from .models import User

def get_user_by_account(account):
    """
    通过账号获取账号
    :param account:用户名或者手机号
    :return:user
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # username为手机号
            user = User.objects.get(mobile=account)
        else:
            # username为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户客户端"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写用户认证的方法
        :param request:
        :param username:用户名或者手机号
        :param password:密码明文
        :param kwargs:额外参数
        :return:user
        """
        # 校验username参数是否是用户名还是手机号
        # 使用账号查询用户
        user=get_user_by_account(username)
        # 如果可以查询到用户，以便于需要校验密码是否正确
        if user and user.check_password(password):
            return user
        else:
            return None



