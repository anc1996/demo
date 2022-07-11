from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache,caches # cache这个对象等价于 caches['default'] 。
import logging
from shop.utils.response_code import RETCODE
from .constants import province_city_REDIS_EXPIRES

from .models import Area
# Create your views here.
# 创建日志
logger=logging.getLogger('areas')

class AreasView(View):
    """省市区三级联动"""

    def get(self,request):
        # 根据get请求参数，判断当前是查询省份数据还是市区，
        cache1=caches['ProvinceCity']
        area_id=request.GET.get('area_id')
        if not area_id:
            # 获取并判断是否有省级缓存数据
            province_list=cache1.get('province_list')
            if not province_list:
                # 查询省级数据
                try:
                    province_model_list=Area.objects.filter(parent__isnull=True) # 返回集合
                    province_list=[]
                    for province_model in province_model_list:
                        province_list.append({'id': province_model.id, 'name': province_model.name})
                    # 存储省份列表缓存数据:默认存储到别名为"default"
                    cache1.set('province_list', province_list, province_city_REDIS_EXPIRES)
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'code':RETCODE.DBERR,"errmsg":'查询省份数据错误'})
            context = {'code': RETCODE.OK, "errmsg": 'OK', "province_list": province_list}
            return JsonResponse(context)
        else:
            # 查询市和区的数据
            sub_data=cache1.get('sub_area_'+area_id)
            if not sub_data:# redis没有，查询mysql
                try:
                    parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级模型
                   #  sub_model_list=parent_model.area_set.all(),由于模型的定义数据参数related_name='subs'
                    sub_model_list = parent_model.subs.all()
                    # 序列化市或区数据
                    sub_list = []
                    for sub_model in sub_model_list:
                        sub_list.append({'id': sub_model.id, 'name': sub_model.name})
                        """
                        {
                          "code":"0",
                          "errmsg":"OK",
                          "sub_data":{
                              "id":130000,
                              "name":"河北省",
                              "subs":[
                                  {
                                      "id":130100,
                                      "name":"石家庄市"
                                  },
                                  ......
                              ]
                        """
                    # 储存市或区缓存数据
                    sub_data={
                                  "id":parent_model.id,
                                   'name':parent_model.name,
                                   'subs':sub_list
                              }
                    # 存储市或县列表缓存数据:默认存储到别名为"default"
                    cache1.set('sub_area_' + area_id, sub_data, 3600)
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'code':RETCODE.DBERR,"errmsg":'查询省份数据错误'})
            # 响应城市或区JSON数据
            context = {'code': RETCODE.OK, "errmsg": 'OK', "sub_data": sub_data}
            return JsonResponse(context)

