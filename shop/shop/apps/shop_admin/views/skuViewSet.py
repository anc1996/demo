from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop_admin.serializers.sku_serializer import SKUSerializer,SKUCategorieSerializer
from goods.models import SKU, GoodsCategory, SPU
from shop_admin.serializers.spu_serializer import SPUSpecSerialzier
from shop_admin.views.PageNum import PageNum

class SKUView(ModelViewSet):
    # 指定序列化器
    serializer_class =SKUSerializer
    # 指定分页器 进行分页返回
    pagination_class = PageNum

    # 权限指定
    permission_classes=[IsAdminUser]

    # 重写get_queryset方法，判断是否传递keyword查询参数
    def get_queryset(self):
          # 提取keyword
        keyword=self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name=keyword)

    @action(methods=['get'], detail=False)
    def categories(self,request):
        """
        获取三级分类的方法
        :param request:
        :return:
        """
        # 子节点没有id
        data=GoodsCategory.objects.filter(subs__id=None)
        serializer=SKUCategorieSerializer(data,many=True)
        return Response(serializer.data)

    def specs(self,request,pk):
        """
        获取spu_id的规格，以及规格选项信息
        :param request:
        :param pk:spu_id
        :return:
        """
        # 1、查询spu对象
        spu=SPU.objects.get(id=pk)
        # 2、查询spu所关联的规格表
        data=spu.specs.all()
        # 3、序列号返回规格信息
        serializer=SPUSpecSerialzier(data,many=True)
        return Response(serializer.data)
