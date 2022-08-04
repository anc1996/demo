from rest_framework import  serializers

# 如果需要序列化的数据中包含有其他关联对象，则对关联对象数据的序列化需要指明。
class PeopleInfoSerializer(serializers.Serializer):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name=serializers.CharField(label='名字',max_length=20)
    description = serializers.CharField(max_length=200, allow_null=True, label='描述信息')
    # PrimaryKeyRelatedField，此字段将被序列化为关联对象的主键。
    # 包含read_only=True参数时，该字段将不能用作反序列化使用
    # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # 此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    book=serializers.StringRelatedField()
    is_delete = serializers.BooleanField(default=False, label='逻辑删除')

# 自定义序列化器
class BookSerializer(serializers.Serializer):
    # 序列化返回字段

    """注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。"""
    id=serializers.IntegerField(label='ID', read_only=True)
    name=serializers.CharField(label='名称',max_length=20)
    pub_date=serializers.DateField(label='发布日期',required=False)
    readcount=serializers.IntegerField(label='阅读量', required=False)
    commentcount=serializers.IntegerField(label='评论量', required=False)
    is_delete=serializers.BooleanField(label='逻辑删除',required=False)
    # 返回所关联的人物id
    # peopleinfo_set=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    # 返回关联人物模型类__str__方法值
    # peopleinfo_set=serializers.StringRelatedField(read_only=True,many=True)
    # 返回人物模型类的对象所有属性，
    # 每个BookInfo对象关联的英雄HeroInfo对象可能有多个，只是在声明关联字段时，多补充一个many=True参数即可。
    peopleinfo_set=PeopleInfoSerializer(many=True)

