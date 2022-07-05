from django.shortcuts import render
from django.views import View
import random,logging
# Create your views here.
from .libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
from . import constants
from shop.utils.response_code import RETCODE
from celery_tasks.send_sms_code.tasks import ccp_send_sms_code
from .libs.yuntongxun.ccp_sms import CCP



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
        """保存图形验证"""
        redis_conn=get_redis_connection('VerifyCode')
        # setnx(self, name: KeyT, value: EncodableT) -> ResponseT:
        redis_conn.setex('img_%s'%uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)
        # 响应图形验证码
        return HttpResponse(image,content_type='image/jpg')

class SMSCodeView(View):
    """短信验证码"""
    def get(self,request,mobile):
        """
        :param request:
        :param mobile:手机号
        :return:JSON
        """
        # 接受参数
        image_code_client=request.GET.get('image_code')
        uuid=request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client,uuid]):
            return HttpResponseForbidden('缺少参数')

        # 创建连接redis对象
        redis_conn=get_redis_connection('VerifyCode')

        """判断发送短信验证码是否频繁"""
        # 提取发送验证码的标记
        send_flag=redis_conn.get('send_flag_%s'% mobile)
        if send_flag:
            return JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信验证码频繁'})
        # 提取图形验证码
        image_code_server=redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图形验证码已失效'})
        print(type(image_code_server))
        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        image_code_server=image_code_server.decode()# 将btyes转成字符串类型
        if image_code_client.lower()!=image_code_server.lower(): # 验证码转小写
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码错误'})
        # 生成短信验证码,随机6位数
        sms_code='%06d' % random.randint(0,999999)
        logger.info('mobile:%s,sms_code:%s'%(mobile,sms_code)) # 手动输出日志，导出验证码

        # 创建redis管道
        pl=redis_conn.pipeline()
        # 将命令添加到队列中
        # 保存短信验证码
        pl.setex('sms_%s' % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        """避免频繁发送短信验证码"""
        # 保存发送验证码的标记
        pl.setex('send_flag_%s'% mobile,constants.SEND_SMS_CODE_INTERVAL,1)
        # 执行
        pl.execute()

        # 发送短信验证码
        # 单例类发送短信验证码，过期时间5分钟，测试的短信模板编号为1
        print(type(constants.SEND_SMS_TEMPLATE_ID))
        # CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID) # 注释，\
        # 用celery执行
        ret=ccp_send_sms_code.delay(mobile, sms_code) # 千万不要忘记写delay，异步任务
        # 响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信短信验证码成功'})

# 创建日志输出器
logger=logging.getLogger('django')