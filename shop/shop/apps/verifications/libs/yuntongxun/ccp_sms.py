# -*- coding:utf-8 -*-

# import ssl
# ssl._create_default_https_context =ssl._create_stdlib_context # 解决Mac开发环境下，网络错误的问题

from verifications.libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da881ad97540181ba09d9b90215'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '6202374657f446eab2da5fcbc09f0029'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf070881ad8ad40181ba1b34f5025f'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'app.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(_serverIP, _serverPort, _softVersion)
#     rest.setAccount(_accountSid, _accountToken)
#     rest.setAppId(_appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     print(result)

# 单例设计模式，单例模式确保某个类有且仅有一个实例，而且自行实例化并向整个系统提供这个实例
class CCP(object):
    """发送短信验证码的单例类"""
    # 定义单例的初始化方法
    def __new__(cls, *args, **kwargs):
        # 。__new__方法用于创建对象并返回对象,__new__方法是静态方法，而__init__是实例方法。
        """
        :param args:
        :param kwargs:
        :return: 单例对象
        """
        # 判断单例是否存在:_instatance属性中存储的就是单例
        if not hasattr(cls,'_instatance'):   #hasattr: This is done by calling getattr(obj, name) and catching AttributeError.
            # 如果单例不存在，初始化单例
            cls._instance=super(CCP,cls).__new__(cls,*args,**kwargs)
            # 初始化REST SDK
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        # 返回单例
        return cls._instance

    def send_template_sms(self,to,datas,tempId):
        # 发送短信验证码的方法
        """
        :param to:手机号码
        :param datas:内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        :param tempId: 模板Id,测试模板id位1
        :return:成功：0；失败：-1
        """
        result=self._instance.rest.sendTemplateSMS(to,datas,tempId)
         # 短信验证码发送有延迟
        print(result)
        if(result.get('statusCode')=='000000'):
            return 0
        else:
            return -1


if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    # sendTemplateSMS('15775023056', ['123456', 5], 1)

    # 单例类发送短信验证码，测试的短信模板编号为1
    CCP().send_template_sms('15775023056',['123456', 5], 1)