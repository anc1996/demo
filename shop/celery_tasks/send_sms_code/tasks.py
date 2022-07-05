# 定义任务
from celery_tasks.send_sms_code.yuntongxun.ccp_sms import CCP
from . import constants
from celery_tasks.main import celery_app

# 使用装饰器异步任务，保证celery识别任务
@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param self:
    :param mobile:手机号
    :param sms_code:短信验证码
    :return:成功 0；失败 -1
    """
    send_ret=CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
    return send_ret