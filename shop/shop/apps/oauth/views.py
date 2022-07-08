from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import  OAuthQQ
from django.http import JsonResponse,HttpResponseServerError
import logging
# 引入配置文件参数dev
from django.conf import settings
from shop.utils.response_code import RETCODE
class QQAuthURLView(View):
    """
    提供QQ登录页面网址
    链接：https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=appid&redirect_uri=(注册appid时填写的主域名下的地址)&state=next
    """
    def get(self,request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next=request.GET.get('next')
        print(type(next))
        # 创建工具对象

        # 生产QQ登录扫描页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        # QQ第一步：获取Authorization Code
        login_url = oauth.get_qq_url()
        # 响应结果
        return JsonResponse({'code':RETCODE.OK,'errmsg':'OK','login_url':login_url})

# 创建日志输出器
logger=logging.getLogger('django')
class QQAuthUserView(View):
    """qq扫码登录后的回调处理"""
    def get(self,request):
        # 获取回调后的code码
        code=request.GET.get('code')
        if code is None:
            return HttpResponseServerError('获取code失败')
        """
        QQ第二步：通过Authorization Code获取Access Token
            https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&
            client_id=appid&client_secret=appkey&code=(URL中带上AuthorizationCODE)&redirect_uri=(注册appid时填写的主域名下的地址)
        """
        # 创建工具对象
        oauth=OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token=oauth.get_access_token(code)
            """QQ第三步：通过access_token获取openid"""
            openid=oauth.get_open_id(access_token)
        except Exception as e:
            logger.error('错误信息:%s'%e)
            return HttpResponseServerError('OAuth2.0认证失败')

        # 使用openid 该qq用户是否绑定过美多商城的用户
        pass
