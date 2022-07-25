from alipay import AliPay, AliPayConfig
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
import os,sys


from shop.utils.response_code import RETCODE
from shop.utils.views import LoginRequiredJSONMixin
from orders.models import OrderInfo
from payment.models import Payment
# Create your views here.

class PaymentView(LoginRequiredJSONMixin, View):
    """对接支付宝订单支付功能"""

    def get(self, request, order_id):
        # 查询要支付的订单
        """

        :param request:
        :param order_id:当前要支付的订单ID
        :return:JSON
        """
        user = request.user
        
        # 校验order_id
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return HttpResponseForbidden('订单信息错误')
        app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
        alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),

        f = open("".join(app_private_key_path), "r")
        app_private_key = f.read()
        f = open("".join(alipay_public_key_path), "r")
        alipay_public_key = f.read()
        # 创建对接支付宝的接口sdk，得到登录页的地址
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url,如果采用同步通知就不传
            app_private_key_string=app_private_key,
            alipay_public_key_string=alipay_public_key,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
        )

        # 如果你是 Python3 的用户，使用默认的字符串即可
        subject = "测试订单"

        # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="SHOP_%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )

        # order_string=alipay.client_api(
        #     "alipay.trade.page.pay",
        #     biz_content={
        #         "out_trade_no": order_id,# 订单编号
        #         "total_amount": str(order.total_amount), # 订单支付金额
        #         "subject": "SHOP%s" % order_id,
        #     },
        #     return_url=settings.ALIPAY_RETURN_URL,  # this is optional# 如果不是同步通知就不传
        # )
        # 响应登录支付宝连接
        # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string


        # # 查询订单状态
        # alipay.server_api(
        #     "alipay.trade.query",
        #     biz_content={
        #         "out_trade_no": "202101010000"
        #     }
        # )
        #
        # # 退款
        # alipay.server_api(
        #     "alipay.rade.refund",
        #     biz_content={
        #         "out_trade_no": "202101010000",
        #         "refund_amount": 12.34
        #     }
        # )

        alipay_url = settings.ALIPAY_URL + "?" + order_string
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})


class PaymentStatusView(View):
    """保存订单支付状态"""

    def get(self,request):
        # 获取前端传入的请求参数
        query_dict = request.GET
        data = query_dict.dict()
        # 获取并从请求参数中提取并移除sign
        signature = data.pop('sign')
        # 使用支付宝支付对象，调用验通知验证接口函数，得到验证结果
        app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
        alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),

        f = open("".join(app_private_key_path), "r")
        app_private_key = f.read()
        f = open("".join(alipay_public_key_path), "r")
        alipay_public_key = f.read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_string=app_private_key,
            alipay_public_key_string=alipay_public_key,
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 如果验证通过，需要将支付宝的支付状态进行处理
        # tradeStatus.TRADE_CLOSED 交易关闭 0
        # tradeStatus.TRADE_FINISHED 交易完结 0
        # tradeStatus.TRADE_SUCCESS 支付成功 1
        # tradeStatus.WAIT_BUYER_PAY 交易创建 0
        status=alipay.verify(data,signature=signature)
        if status:
            # 读取order_id
            order_id = data.get('out_trade_no')
            # 读取trade_no，支付宝的订单
            trade_id=data.get('trade_no')
            # 需要修改订单状态，将shop的订单和支付宝的订单保存一起
            Payment.objects.update_or_create(order_id=order_id,trade_id=trade_id)
            # 修改订单状态,由“待支付”改为“待评价”
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])
            # 响应结果
            context = {
                'trade_id': trade_id
            }
            return render(request, 'pay_success.html', context)
        else:
            # 订单支付失败，重定向到我的订单
            return HttpResponseForbidden('非法请求')

