class BaseSerialier(object):
    """
        基础序列化器
    """

    def __init__(self, instance=None, data=None):
        self.instance = instance
        self._data = data


    def validated_data(self, attrs):
        """
            多个字段验证方法
        :param attrs:
        :return:
        """
        pass

    def is_valid(self):
        """
            验证
        :return:
        """
        data=self.validated_data(attrs=self.data)
        self._data=data

    def save(self,**kwargs):
        """
            保存更新方法
        :return:
        """
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def update(self, instance, validate_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validate_data):
        raise NotImplementedError('`create()` must be implemented.')


    @property
    def data(self):
        return self._validated_data


    @property
    def errors(self):
        # 返回错误信息
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors
