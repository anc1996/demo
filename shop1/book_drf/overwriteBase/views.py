

from rest_framework.response import Response

from book_drf.overwriteBase import serializer
from book_drf.overwriteBase import generic

class BookView(generic):
    queryset = [{'name':'散花','id':1},{'id':2,'name':'悲惨世界'}]

    def post(self,request):
        # 1、获取数据
        data_dict = request.data
        # 2、验证数据
        bookserializer=self.get_serializer(data=data_dict)
        # bookserializer = serializer(data=data_dict)  # 字节转化data类型
        bookserializer.is_valid()  # 验证方法
        # 3、保存数据
        bookserializer.save()
        # 返回构建对象，这里的对象为data=book，然后序列化返回
        return bookserializer.data