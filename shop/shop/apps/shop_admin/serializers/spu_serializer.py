from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


class SPUOptineSerializer(serializers.ModelSerializer):
    """
      SPU规格选项序列化器
    """
    class Meta:
        model = SpecificationOption
        fields=('id','value')


class SPUSpecSerialzier(serializers.ModelSerializer):
    """
        规格序列化器
    """

    # 关联序列化返回SPU表数据
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField(read_only=True)
    # 关联序列化返回 规格选项信息,由于SpecificationOption的spec中关联options属性
    options = SPUOptineSerializer(read_only=True, many=True)  # 使用规格选项序列化器

    class Meta:
        model = SPUSpecification  # SPUSpecification中的外键spu关联了SPU商品表
        fields = "__all__"
