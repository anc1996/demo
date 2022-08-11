from django.http import JsonResponse
from rest_framework import serializers
from django.db.transaction import atomic

from books.models import BookInfo
# 如果需要序列化的数据中包含有其他关联对象，则对关联对象数据的序列化需要指明。
class PeopleInfoSerializer(serializers.Serializer):
    GENDER_CHOICES = ((0, 'male'),(1, 'female'))
    # 1、一种方法字段选项验证
    id = serializers.IntegerField(label='ID', read_only=True)
    name=serializers.CharField(label='书名',max_length=20, help_text='书名')
    description = serializers.CharField(max_length=200, allow_null=True, label='描述信息', help_text='图书介绍')
    # PrimaryKeyRelatedField，此字段将被序列化为关联对象的主键。
    # 包含read_only=True参数时，该字段将不能用作反序列化使用
    # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # 此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    book=serializers.StringRelatedField()
    is_delete = serializers.BooleanField(default=False, label='逻辑删除')

def about_django(value):
    print('外面的函数验证')

# 自定义序列化器
class BookSerializer(serializers.Serializer):
    # 序列化返回字段

    """注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。"""
    id=serializers.IntegerField(label='ID', read_only=True)
    name=serializers.CharField(label='名称',max_length=20,validators=[about_django])
    pub_date=serializers.DateField(label='发布日期')
    readcount=serializers.IntegerField(label='阅读量', required=False,default=10)
    commentcount=serializers.IntegerField(label='评论量', required=False,default=0)
    is_delete=serializers.BooleanField(label='逻辑删除',required=False)
    # 返回所关联的人物id
    # peopleinfo_set=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    # 返回关联人物模型类__str__方法值
    # peopleinfo_set=serializers.StringRelatedField(read_only=True,many=True)
    # 返回人物模型类的对象所有属性，
    # 每个BookInfo对象关联的英雄HeroInfo对象可能有多个，只是在声明关联字段时，多补充一个many=True参数即可。
    peopleinfo_set=PeopleInfoSerializer(many=True,required=False)


    # 单一字段验证,固定方法,attrs的参数可以随便写,validate_<field_name>,对<field_name>字段进行验证，
    def validate_name(self,value):
        if 'django' in value.lower():
            raise serializers.ValidationError('图书是关于Django的')
        return value



    # 多个字段验证
    def validate(self, attrs):
        if attrs['readcount']<attrs['commentcount']:
            raise serializers.ValidationError('readcount<commentcount,可能存在假评论')
        return attrs

    # 保存数据
    def create(self, validated_data):
        # 字典拆包处理，
        book=BookInfo.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        # 更新数据
        instance.name=validated_data['name']
        instance.pub_date=validated_data['pub_date']
        instance.readcount=validated_data['readcount']
        instance.commentcount=validated_data['commentcount']
        instance.save()
        return instance




class BookModelSerializer(serializers.ModelSerializer):
    '''
    如果我们想要使用序列化器对应的是Django的模型类，DRF为我们提供了ModelSerializer模型类序列化器来帮助我们快速创建一个Serializer类。
    ModelSerializer与常规的Serializer相同，但提供了
        基于模型类自动生成一系列字段
        基于模型类自动为Serializer生成validators，比如unique_together
        包含默认的create()和update()的实现
    '''
    # 可以向 ModelSerializer 添加额外的字段，也可以通过在类上声明字段来覆盖默认字段，
    # 就像对 Serializer 类所做的那样。
    readcount=serializers.IntegerField(min_value=20)
    sms_code=serializers.CharField(max_length=6,min_length=6,validators=[about_django])

    class Meta:
        model=BookInfo   # 指定生成字段的模型类
        # fields=('name','readcount') # 指定模型类中生成的字段
        fields='__all__' # 指定模型类中生成所有的字段
        # exclude = ('is_delete',) # 指定模型类中除了is_delete字段生成的字段，
        # 可以通过read_only_fields指明只读字段，即仅用于序列化输出的字段
        read_only_fields = ('id', 'name',)
        # 对字段进行添加和修改
        extra_kwargs={'readcount': {'min_value': 10}}

    # 单一字段验证,固定方法,attrs的参数可以随便写,validate_<field_name>,对<field_name>字段进行验证，
    def validate_name(self, value):
        if 'django' in value.lower():
            raise serializers.ValidationError('图书是关于Django的')
        return value

    # 多个字段验证
    def validate(self, attrs):
        if attrs['readcount'] < attrs['commentcount']:
            raise serializers.ValidationError('readcount<commentcount,可能存在假评论')
        return attrs