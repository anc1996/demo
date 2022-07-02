from django.shortcuts import render
from django.views import View
# Create your views here.
from .libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from . import constants
class ImageCodeView(View):
    """图形验证码"""
    def get(self,request,uuid):
        """
        :param request:
        :param uuid:通用唯一识别码，用于唯一标识该图形验证码属于哪个用户的
        :return:image/jpg
        """
        # 接收参数，校验参数

        '''实现主体业务逻辑，生成图形验证码，保持，并响应'''
        # 生成图形验证码
        text,image=captcha.generate_captcha()
        # 保存图形验证
        redis_conn=get_redis_connection('VerifyCode')
        # setnx(self, name: KeyT, value: EncodableT) -> ResponseT:
        redis_conn.setex('img_%s'%uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)
        # 响应图形验证码
        return HttpResponse(image,content_type='image/jpg')

class ImageCodeView(View):
    """短信验证码"""
    def get(self,request,mobile):
        """
        :param request:
        :param mobile:手机号
        :return:JSON
        """
        pass