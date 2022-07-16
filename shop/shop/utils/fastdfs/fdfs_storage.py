from django.core.files.storage import Storage
from django.conf import  settings


class FastDFSStorage(Storage):
    """自定义文件存储系统"""

    def __init__(self, fdfs_base_url=None):
        # Django 必须能以无参数实例化你的存储系统。
        # if not fdfs_base_url:
        #     self.fdfs_base_url = settings.FDFS_BASE_URL
        # self.fdfs_base_url=fdfs_base_url
        self.fdfs_base_url=fdfs_base_url or settings.FDFS_BASE_URL

    '''
    在你的存储类中，除了其他自定义的方法外，还必须实现 _open() 以及 _save() 等
    其他适合你的存储类的方法。关于这些方法，详情请查看下面的信息。
    
    另外，如果你的类提供了本地文件存储，它必须重写 path() 方法。您的存储类必须是 deconstructible，以便在迁移中的字段上使用它时可以序列化。
    只要你的字段有自己的参数 serializable，你可以使用django.utils.deconstruct.deconstructible 类装饰器（这是 Django 在 FileSystemStorage 上使用的）。
    '''

    def _open(self,name, mode='rb'):
        """
它将被 Storage.open() 调用，前者才是存储类用来打开文件的真正机制，
        这个方法必须要返回一个 文件 对象。尽管在大多数时候，
        你想要这个方法返回一个继承于特定逻辑的后台存储系统的子类。
        :name:文件路径
        :param mode:文件打开方式
        :return:因为当前不是去打开某个文件，所有这个方法不用。
        """
        pass

    def _save(self,name, content):
        """
        被称为 Storage.save()。这个 name 会早已经历 get_valid_name() 和 get_available_name()，并且 content 将会成为 File 对象自身。
        应该返回保存的文件名的实际名称（通常是传入“name”，但如果内存需要改变文件名，则返回新名称）。
        :param name:文件路径
        :param content:文件二进制内容
        :return:None，因为当前不是用来保存的文件名的实际名称
        """
        pass

    def url(self,name):
        """
        返回可以访问 name 引用的文件内容的URL。对于不支持通过 URL 访问的存储系统，这将引发 NotImplementedError。
        :param name:文件相对路径
        :return: 返回文件的全路径，http://***.**.**.**:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        """
        return self.fdfs_base_url+name