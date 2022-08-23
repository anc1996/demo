# 定义任务
from celery_tasks.send_sms_code.yuntongxun.ccp_sms import CCP
from . import constants
from celery_tasks.main import celery_app

# 使用装饰器异步任务，保证celery识别任务
# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
@celery_app.task(bind=True,name='ccp_send_sms_code',retry_backoff=2,max_retries=4)
def ccp_send_sms_code(self,mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param self:
    :param mobile:手机号
    :param sms_code:短信验证码
    :return:成功 0；失败 -1
    """
    try:
        send_ret=CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        # 触发错误重试：最多3次
        raise self.retry(exec=e,max=2)
    return send_ret