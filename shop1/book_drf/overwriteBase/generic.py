class GenericAPIView(object):

    # -应该用于从这个视图返回对象的查询集。通常，您必须设置此属性，或者重写 get_queryset ()方法。
    # 如果要重写一个视图方法，重要的是要调用get_queryset()，而不是直接访问这个属性，因为 queryset 只计算一次，这些结果将缓存用于所有后续请求。
    queryset = None
    # 应该用于验证和反序列化输入以及序列化输出的序列化器类。
    # 通常，您必须设置此属性，或者重写get_serializer_class()方法。
    serializer_class = None
    
    # 应该用于执行单个模型实例的对象查找的模型字段。
    # 默认为“ pk”。注意，在使用超链接 API 时，如果需要使用自定义值，则需要确保 API 视图和序列化器类都设置了查找字段。
    lookup_field = 'pk'

    #应该用于对象查找的URL关键字参数。
    # URL_conf 应该包含与此值对应的关键字参数。
    # 如果取消此设置，则默认为使用与 lookup_field 相同的值。
    lookup_url_kwarg=None
    
    # 返回应该用于列表视图的查询集，并且应该用作详细视图中查找的基础。
    def get_queryset(self):
        queryset = self.queryset
        return queryset

    # 返回应用于详细信息视图的对象实例。默认情况下使用lookup_field参数筛选基本查询集。
    def get_object(self):
        for instanse in self.queryset:
            if instanse.id==1:
                return instanse

    def get_serializer(self, *args, **kwargs):
        # 添加参数来调用,并将类初始化为序列化的对象
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        # 返回要用于序列化器的类。serializer_class
        return self.serializer_class

