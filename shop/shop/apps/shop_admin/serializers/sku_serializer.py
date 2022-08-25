from django.db import transaction
from rest_framework import serializers

from goods.models import SKUSpecification, SKU, GoodsCategory
from celery_tasks.static_file.tasks import get_detail_html

class SKUSpecificationSerialzier(serializers.ModelSerializer):
    """
      SKU具体规格表序列化器
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()
    class Meta:
        model = SKUSpecification # SKUSpecification中sku外键关联了SKU表
        fields=("spec_id",'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """
      sku表的序列化器
    """
    # 指定所关联的选项信息 关联嵌套返回
    specs = SKUSpecificationSerialzier(read_only=True, many=True)
    # 指定分类信息
    category_id = serializers.IntegerField()
    # 关联嵌套返回
    category = serializers.StringRelatedField(read_only=True)
    # 指定所关联的spu表信息
    spu_id = serializers.IntegerField()
    # 关联嵌套返回
    spu = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SKU  # SKU表中category外键关联了GoodsCategory分类表。spu外键关联了SPU商品表
        fields='__all__'

    def create(self, validated_data):
        specs = self.context['request'].data.get('specs') # specs前端返回的是list类型，当前list
        # 开启事务
        with transaction.atomic():
            try:
                # 设置保存点
                save_point = transaction.savepoint()
                # 保存sku表
                sku=SKU.objects.create(**validated_data)
                # 保存sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.create(spec_id=spec['spec_id'],option_id=spec['option_id'],sku=sku)
            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:
                # 提交
                transaction.savepoint_commit(save_point)
                # 生成详情页的静态页面
                get_detail_html.delay(sku.id)
                return sku

    def update(self, instance, validated_data):
        # 获取规格信息
        specs = self.context['request'].data.get('specs') # specs前端返回的是list类型，当前list
        # 因为sku表中没有specs字段，所以在保存的时候需要删除validated_data中specs数据
        with transaction.atomic():
            try:
                # 设置保存点
                save_point = transaction.savepoint()
                # 修改sku表
                SKU.objects.filter(id=instance.id).update(**validated_data)
                # 修改sku具体规格表
                for spec in specs:
                    if SKUSpecification.objects.filter(sku=instance).count():
                        SKUSpecification.objects.filter(sku=instance).update(**spec)
                    else:
                        SKUSpecification.objects.create(spec_id=spec['spec_id'], option_id=spec['option_id'], sku=sku)
            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:
                # 提交
                transaction.savepoint_commit(save_point)
                # 生成详情页的静态页面
                get_detail_html.delay(sku_id=instance.id)
                return instance



class SKUCategorieSerializer(serializers.ModelSerializer):
    """
          商品分类序列化器
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"