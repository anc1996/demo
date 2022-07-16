from django.shortcuts import render,reverse
from django.views import View
from collections import OrderedDict

from goods.models import *
from contents.models import *
# Create your views here.
class IndexView(View):
    '''
    首页广告
    '''
    def get(self,request):
        '''提供首页广告页面'''
        # {
        #     "1": {
        #         "channels": [
        #             {"id": 1, "name": "手机", "url": "http://shouji.jd.com/"},
        #             {"id": 2, "name": "相机", "url": "http://www.itcast.cn/"}
        #         ],
        #         "sub_cats": [
        #             {
        #                 "id": 38,
        #                 "name": "手机通讯",
        #                 "sub_cats": [
        #                     {"id": 115, "name": "手机"},
        #                     {"id": 116, "name": "游戏手机"}
        #                 ]
        #             },
        #             {
        #                 "id": 39,
        #                 "name": "手机配件",
        #                 "sub_cats": [
        #                     {"id": 119, "name": "手机壳"},
        #                     {"id": 120, "name": "贴膜"}
        #                 ]
        #             }
        #         ]
        #     },
        #     "2": {
        #         "channels": [],
        #         "sub_cats": []
        #     }
        # }

        # 准备商品分类的字典
        channel_group_list = OrderedDict()
        # 查询所有的商品频道，1比1对应37个一级类别
        good_channels=GoodsChannel.objects.order_by('group_id','sequence')
        # 遍历所有频道
        for channel in good_channels:
            # 获取当前频道所在的组
            channel_group_id =channel.group_id
            # 构造数据基本框架，共11组的频道组
            if channel_group_id not in channel_group_list:
                channel_group_list[channel_group_id]={'channels':[],'sub_cats':[]}
            category1=channel.category # 当前频道的一级类别
            # {"id": 1, "name": "手机", "url": "http://shouji.jd.com/"},
            channel_group_list[channel_group_id]['channels'].append(
                {"id":category1.id,"name":category1.name,"url":channel.url})

            '''
            构建当前类别的子类别
                {           "id": 38,
                            "name": "手机通讯",
                            "sub_cats": [
                                {"id": 115, "name": "手机"},
                                {"id": 116, "name": "游戏手机"}
                            ]
                },
            '''
            # 查询二级
            for category2 in category1.subs.all():
                    # 在面向对象过程中增加sub_cats属性
                    category2.sub_cats=[] # 给二级类别添加一个保存三级类别的列表
                    # 查询三级类别
                    for category3 in category2.subs.all():
                        category2.sub_cats.append(category3)
                    # 将二级类别添加到一级类别sub_cat钟
                    channel_group_list[channel_group_id]['sub_cats'].append(category2)


        """查询首页广告数据"""
        # 第一步：查询所有广告类别
        contents=OrderedDict()
        contentCategory_list=ContentCategory.objects.all()
        for contentCategory in contentCategory_list:
            # 查询未下架的广告并排序
            content_list=contentCategory.content_set.filter(status=True).order_by('sequence')
            contents[contentCategory.key]=content_list
            # 第二步：使用广告类别查询出该类别对应的广告内容

        context={'categories':channel_group_list,'contents':contents}
        # print(reverse('contents:index'))
        return render(request,'index.html',context)

