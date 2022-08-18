import re

from rest_framework.serializers import ModelSerializer

from shop_admin import serializers
from users.models import User


class UserSerializer(ModelSerializer):
    # 查看用户序列号器
    class Meta:
        model=User
        fields=('id','username','mobile','email')


class UserAddSerializer(ModelSerializer):
    # 增加用户序列号器
    class Meta:
        model=User
        fields=('id','username','mobile','email','password') # id 默认是read-only，不参与序列号操作
        #  username字段增加长度限制，password字段只参与保存，不在返回给前端，增加write_only选项参数
        extra_kwargs = {
            'username': {'max_length': 20,'min_length': 5},
            'password': {'max_length': 20,'min_length': 8,'write_only': True},
        }
    # 单一验证
    def validate_mobile(self,vaule):
        if re.match(r'^1[3-9]\d{9}$', vaule):
            raise serializers.ValidationError('手机号格式不匹配')
        return vaule



    # 由于父类没有加密密码，重写ModelSerializer的create方法
    def create(self, validated_data):
        # 保存用户数据并对密码加密
        # 方法一
        user = User.objects.create_user(**validated_data)
        return user

        # 方法二：
        # user=super().create(validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        # return user
