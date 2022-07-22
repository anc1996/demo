from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from decimal import Decimal
from django.http import *
import json
from django.utils import timezone
from django.db import transaction

from shop.utils.views import LoginRequiredJSONMixin
from shop.utils.response_code import RETCODE
from orders.models import *
from users.models import Address
from goods.models import SKU
# Create your views here.
class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        # 接受参数
        user=request.user
        # 查询用户没有被删除的收货地址
        try:
            addresses=Address.objects.filter(user=user,is_deleted=False)
        except Exception as e:
            addresses=None

        # 查询购物车中被勾选的商品
        redis_conn=get_redis_connection('carts')
        # 获取字典中说要sku的id，包含购物车勾选与未勾选的商品
        redis_sku_dict=redis_conn.hgetall('carts_%s' % user.id)
        # 查询set数据,SMEMBERS key命令返回存储在 key 中的集合的所有的成员。 不存在的集合被视为空集合。
        set_selected_list = redis_conn.smembers('selected_%s' % user.id)
        # 构造购物车被勾选的商品数据
        cart_dict={}
        for sku_id in set_selected_list:
            cart_dict[int(sku_id)]=int(redis_sku_dict[sku_id])
        # 遍历cart_dict,取sku_id和count，同时获取商品详细信息
        sku_ids_list=cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids_list)
        total_count=0
        total_amount=Decimal(0.00) # Decimal更精确数字，用于存储金钱
        # 遍历skus给每个sku的模型对象补充count和amount属性
        for sku in skus:
            sku.count=cart_dict[sku.id]
            sku.amount=cart_dict[sku.id]*sku.price
            total_count+=sku.count
            total_amount+=sku.amount

        # 指定默认邮费
        freight=Decimal(10.00)
        # 构造上下文
        context={
            'addresses':addresses,
            'skus':skus,
            'total_count':total_count,
            'total_amount':total_amount,
            'freight':freight,
            'payment_amount':freight+total_amount,
        }
        return render(request, 'place_order.html',context)

class OrderCommitView(LoginRequiredJSONMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 接受参数
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')
        # 校验参数
        if not all([address_id, pay_method]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return HttpResponseForbidden('参数address_id错误')
        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return HttpResponseForbidden('参数pay_method错误')
        user=request.user

        # 从redis读取购物车中被勾选的商品信息
        # 查询购物车中被勾选的商品
        redis_conn=get_redis_connection('carts')
        # 获取字典中说要sku的id，包含购物车勾选与未勾选的商品
        redis_sku_dict=redis_conn.hgetall('carts_%s' % user.id)
        # 查询set数据,SMEMBERS key命令返回存储在 key 中的集合的所有的成员。 不存在的集合被视为空集合。
        set_selected_list = redis_conn.smembers('selected_%s' % user.id)
        # 构造购物车被勾选的商品数据
        cart_dict={}
        for sku_id in set_selected_list:
            cart_dict[int(sku_id)]=int(redis_sku_dict[sku_id])
        sku_ids_list = cart_dict.keys()
        # 获取订单编号:时间+用户id
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 事务的使用，开启一次，
        with transaction.atomic():
            '''保存订单基本信息一'''
            # 在事务中创建保存点来记录数据的特定状态，数据库出现错误时，可以回滚到数据保存点的状态
            save_id=transaction.savepoint()

            try:
                order=OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal(0.00),
                    freight=Decimal(10.00),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                            OrderInfo.ORDER_STATUS_ENUM['UNSEND'] # 选择alipay，待支付，否则待发货
                )
                '''保存订单商品信息多'''
                for sku_id in sku_ids_list:
                    # 每个商品都有多次下单的机会，
                    while True:
                        sku = SKU.objects.get(id=sku_id)  # 查询商品和库存信息，不能用缓存。
                        # 获取原始的库存和销量
                        origin_stock=sku.stock
                        origin_sales=sku.sales
                        # 获取要递交的订单商品的数量
                        sku_count = cart_dict[sku_id]
                        if sku_count > origin_stock:
                            return JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})
                        # 获取要递交的订单商品的数量
                        sku_count = cart_dict[sku_id]
                        # SKU减少库存，增加销量
                        new_stock=origin_stock-sku_count
                        new_sales=origin_sales-sku_count
                        # 乐观锁并发下单
                        result=SKU.objects.filter(id=sku_id,stock=origin_stock).update(stock=new_stock,sales=new_sales)
                        # 如果在更新数据时，原始数据变化了，返回0，表示资源抢夺,只要购买数量小于库存，重新跑一次。
                        if result==0:
                            continue

                        # 修改SPU销量
                        sku.spu.sales += sku_count
                        sku.spu.save()

                        OrderGoods.objects.create(
                            order=order,
                            sku = sku,
                            count = sku_count,
                            price = sku.price,
                        )

                        # 累加订单商品的数量和总价到订单基本信息表
                        order.total_count+=sku_count
                        order.total_amount+=sku_count*sku.price
                        # 下单成功，跳槽While循坏
                        break

                # 添加邮费和保存订单信息
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})

            # 提交明显的一次的事务
            transaction.savepoint_commit(save_id)

        # 清楚redis被挑选数据
        pl = redis_conn.pipeline()
        pl.hdel('carts_%s' % user.id, *set_selected_list)
        pl.srem('selected_%s' % user.id, *set_selected_list)
        pl.execute()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order_id})

class OrderSuccessView(LoginRequiredJSONMixin, View):
    """提交订单成功页面"""
    def get(self,request):
        """提供提交订单成功页面"""
        order_id=request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context)
