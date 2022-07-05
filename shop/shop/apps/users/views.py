from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden,HttpResponse,JsonResponse
import re
from django.urls import reverse
from django.db import DatabaseError
from django.contrib.auth import login
from django_redis import get_redis_connection
from shop.utils.response_code import RETCODE
from .models import User

# Create your views here.
''' 提供用户注册页面,判断用户名是否重复注册,判断手机号是否重复注册'''
class RegisterView(View):
    "用户注册"
    def get(self,request):
        '提供用户注册页面'
        return render(request,'register.html')

    def post(self,request):
        '''
          实现用户注册内部逻辑
        :param request: 请求对象
        :return: 注册结果
        '''
        # 接收参数：表单参数
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile=request.POST.get('mobile')
        allow = request.POST.get('allow')
        sms_code_client=request.POST.get('sms_code')

        # 校验参数:前后端校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全。前后端校验逻辑要相同。
        # 判断参数是否齐全，all([list]):会去校验列表中元素是否存在空值，若为空，false
        if not all([username,password,password2,mobile,allow]):
            return HttpResponseForbidden('如果缺少必传参数，响应错误信息，403')
        # 用户名是5-20个字符，[a-zA-Z0-9_-]
        if not re.match('^[a-zA-Z0-9_-]{5,20}$',username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否相同，且密码是否是8-20个字符
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        if password!=password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')
        # 判断用户是否勾选了协议
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议')
        # 判断短信验证码是否输入正确验证码
        redis_conn=get_redis_connection('VerifyCode')
        sms_code_server=redis_conn.get('sms_%s' % mobile).decode()
        if sms_code_server is None:
            return render(request,'register.html', {'sms_code_errmsg': '短信验证码失效'})
        if sms_code_server!=sms_code_client:
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})


        # 保存注册数据，是注册业务的核心。
        try:
            user=User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return render(request,'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request,user)
        '''响应结果：重定向首页'''
        # redirect
        # print(reverse('contents:index'))  # /
        return redirect(reverse('contents:index'))


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用username查询对应的记录的条数
        count=User.objects.filter(username=username).count()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self,request,mobile):
        """
        :param request:请求对象
        :param mobile:手机号
        :return:JSON
        """
        count=User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})