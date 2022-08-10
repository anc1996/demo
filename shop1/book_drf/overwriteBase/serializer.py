from book_drf.overwriteBase.serializers import BaseSerialier

class BookSerializer(BaseSerialier):
    def validated_data(self, attrs):
        print('多个字段验证成功')
        return attrs

    def create(self, validate_data):
        print('保存数据')

    def update(self, instance, validate_data):
        print('更新数据')

