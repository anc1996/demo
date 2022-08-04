from rest_framework import  serializers

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
