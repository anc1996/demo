from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.urls import reverse
from django.views import View

import json
# Create your views here.
def index(request):
    """
      reverse  就是通过 name 来动态获取路径(路由)
      如果没有设置namespace 则可以通过name来获取 reverse(name)
      如果有设置namespace 则可以通过namespace:name来获取 reverse(namespace:name)

      # 登陆成功之后需要跳转到首页
      # 注册成功之后需要跳转到首页
      """
    # return redirect('/home/')
    # return redirect(path)


    # 注册成功之后需要跳转到首页
    # return redirect('/home/')
    # return redirect(path)

    # redirect跳转页面
    # 如果没有设置namespace,则可以通过name来获取reverse(name)
    # path=reverse('index')
    # 路由是动态获取的,设置了namespance 这个时候就需要通过 namespace:name 来获取路由
    url=reverse('book:index')

    print(url)


    return HttpResponse('index')

def detail2(request,category_id,book_id):
    '''
     http://127.0.0.1:8000/10/100
    :param request:
    :param category_id:
    :param book_id:
    :return:
    '''
    print(category_id, book_id)
    print(request)
    context = {'category_id': category_id, 'book_id': book_id}
    return HttpResponse(context.items())

def detail(request,category_name,book_id):
    print('request请求:',category_name,book_id)
    print(request)
    ###########################GET 查询字符串#################################
    """
    http://127.0.0.1:8000/math/100?username=it&password=123&username=python&password=web
    定义视图接受参数，category_name=math，book_id=100
    以? 作为一个分隔
    ?前边 表示 路由
    ?后边 表示 get方式传递的参数 称之为 查询字符串
    ?key=value&key=value...
    我们在登陆的时候会输入用户名和密码 理论上 用户名和密码都应该以POST方式进行传递
    只是为了让大家好理解,我们接下来
    用 get方式来传递用户名和密码,QueryDict类型的对象用来处理同一个键带有多个值的情况
    get('键',默认值)   如果键不存在则返回None值，可以设置默认值进行后续处理
    """
    query_params=request.GET
    print(query_params) # <QueryDict: {'username': ['it'], 'password': ['123']}>
    # QueryDict 以普通的字典形式来获取 一键多值的是时候 只能获取最后的那一个值
    # 我们想获取 一键一值的化 就需要使用 QueryDict 的get方法
    username=query_params['username']
    password=query_params.get('password') # 注意：用 get方式，如果一个键同时拥有多个值将获取最后的那一个值，这里获取了web值
    # 比如   /1/1?username=it&password=123&username=python&password=web
    print('get请求',username,password)
    print('-------')
    # 我们想获取一键多值的化就需要使用QueryDict的getlist方法
    username=query_params.getlist('username') # 返回list列表
    password=query_params.getlist('password')
    context = {'category_id': category_name, 'book_id': book_id,'username':username,'password':password}
    print('get请求列表',username,password)
    return HttpResponse(context.items())


def detail1(request):
    ###########################POST 表单数据#################################
    '''
    :param request:
    :return:
    范例：post请求 http://127.0.0.1:8000/post/
    参数 number：17688888888
    '''
    data=request.POST
    print(request)
    print(data)
    context={'request':request,'data':data}
    return HttpResponse(context.items())

def post_json(request):
    ###########################POST json数据#################################
    """
    范例：http://127.0.0.1:8000/post_json
    JSON 是双引号
    {
        "name":"itcast",
        "password":"cdde"
    }
    """
    data=request.POST
    print(data)  # 没有数据
    body=request.body
    print(body)
    body_decode=body.decode()# JSON形式的字符串
    print(body_decode)
    """
    导入 import json
    json
    json.dumps   将字典转换为 JSON形式的字符串
    json.loads   将JSON形式的字符串转换为字典
    """
    data_dic=json.loads(body_decode)
    print(data_dic)
    return HttpResponse(data_dic.items())

def meta(request):
    ###########################请求头#################################
    '''
    范例：http://127.0.0.1:8000/meta
    参数 number：17688888888
    :param request:
    :return:

    '''
    # 可以通过request.META属性获取请求头headers中的数据，request.META为字典类型
    request_meta=request.META # 返回请求头所以参数。
    print(request_meta)
    '''
    CONTENT_LENGTH– The length of the request body (as a string).
    CONTENT_TYPE– The MIME type of the request body.
    HTTP_ACCEPT– Acceptable content types for the response.
    HTTP_ACCEPT_ENCODING– Acceptable encodings for the response.
    HTTP_ACCEPT_LANGUAGE– Acceptable languages for the response.
    HTTP_HOST– The HTTP Host header sent by the client.
    HTTP_REFERER– The referring page, if any.
    HTTP_USER_AGENT– The client’s user-agent string.
    QUERY_STRING– The query string, as a single (unparsed) string.
    REMOTE_ADDR– The IP address of the client.
    REMOTE_HOST– The hostname of the client.
    REMOTE_USER– The user authenticated by the Web server, if any.
    REQUEST_METHOD– A string such as"GET"or"POST".
    SERVER_NAME– The hostname of the server.
    SERVER_PORT– The port of the server (as a string).
    '''
    content_type=request_meta['CONTENT_TYPE']
    SERVER_PORT=request_meta['SERVER_PORT']
    SERVER_PROTOCOL=request_meta['SERVER_PROTOCOL']
    CONTENT_LENGTH=request_meta['CONTENT_LENGTH']
    '''
    method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    user：请求的用户对象。
    path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    encoding：一个字符串，表示提交的数据的编码方式。
    如果为None则表示使用浏览器的默认设置，一般为utf-8。
    这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    FILES：一个类似于字典的对象，包含所有的上传文件。
    '''
    context_dict={'request.META':{'CONTENT_LENGTH':CONTENT_LENGTH,'content_type':content_type,'SERVER_PORT':SERVER_PORT,'SERVER_PROTOCOL':SERVER_PROTOCOL},
                  'HttpRequest对象属性':{'request.method': request.method, 'request.path': request.path,'request.encoding':request.encoding}
                  }
    context_json=json.dumps(context_dict)
    return HttpResponse(context_json)

def response1(reuqest):
    ###########################HttpResponse#################################
    '''
    范例：http://127.0.0.1:8000/meta
    :param reuqest:
    :return:
    '''
    data = {'name': 'itcast'} #只有name
    # HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
    # content       传递字符串 ,但不能传递对象,字典等数据
    # statue        HTTP status code must be an integer from 100 to 599. 只能使用系统规定的
    # content_type  是一个MIME类型
    #               语法形式是: 大类/小类
    #           text/html   text/css    text/javascript
    #           application/json
    #           image/png   image/gif   image/jpeg
    return HttpResponse(data,status=200,content_type='application/json')

def jsonresponse(request):
    '''
    范例：http://127.0.0.1:8000/jsonresponse
    若要返回json数据，可以使用JsonResponse来构造响应对象，作用：
    帮助我们将数据转换为json字符串
    设置响应头Content - Type为application / json
    '''
    data = {'name': 'itcast'}
    return JsonResponse(data)

def tiaozhuan(request):
    ###########################跳转页面#################################
    '''
    范例：http://127.0.0.1:8000/tiaozhuan
    :param request: 
    :return: 
    '''
    # 需求是跳转到首页
    # 通过reverse 这个名字来找到路径
    path = reverse('book:index')
    return redirect(path)

"""
面试题:
    你是如何理解cookie的? / 你谈一谈cookie/

    1. 概念
    2. 流程 (大体流程,从http角度分析)
    3. 在开发过程中哪里使用了
    4. 你在开发过程中遇到什么印象深刻的地方

保存在客户端的数据叫做 cookie
    1.cookie是保存在客户端
    2.cookie是基于域名(IP)的

    0.概念
    1.流程(原理)

        第一次请求过程
        ① 我们的浏览器第一次请求服务器的时候,不会携带任何cookie信息
        ② 服务器接收到请求之后,发现 请求中没有任何cookie信息
        ③ 服务器设置一个cookie.这个cookie设置响应中
        ④ 我们的浏览器接收到这个相应之后,发现相应中有cookie信息,浏览器会将cookie信息保存起来

        第二次及其之后的过程
        ⑤ 当我们的浏览器第二次及其之后的请求都会携带cookie信息
        ⑥ 我们的服务器接收到请求之后,会发现请求中携带的cookie信息,这样的话就认识是谁的请求了

    2.看效果

    3.从http协议角度深入掌握cookie的流程(原理)

        第一次
            ① 我们是第一次请求服务器,不会携带任何cookie信息,请求头中没有任何cookie信息
            ② 服务器会为响应设置cookie信息.响应头中有set_cookie信息

        第二次及其之后的
            ③ 我们第二次及其之后的请求都会携带cookie信息,请求头中有cookie信息
            ④(可选) 在当前我们的代码中,没有再在相应头中设置cookie,所以响应头中没有set_cookie信息
            
            
保存在服务器的数据叫做 session
"""

def set_cookie(request):
    """
    范例:http://127.0.0.1:8000/set_cookie/?username=zhangsan
     # 第一次请求过程
     # ① 我们的浏览器第一次请求服务器的时候,不会携带任何cookie信息
     # ② 服务器接收到请求之后,发现 请求中没有任何cookie信息
     # ③ 服务器设置一个cookie.这个cookie设置在resopnse_headers响应头中响应信息
     # ④ 我们的浏览器接收到这个相应之后,发现相应中有cookie信息,浏览器会将cookie信息保存起来
     """
    # 1. 先判断有没有cookie信息
    # 先假设就是没有
    # 2.获取用户名
    # HttpResponse.set_cookie(cookie名, value=cookie值, max_age=cookie有效期)
        # key,value
        # max_age 单位是秒
        # 时间是 从服务器接收到这个请求时间 + 秒数 计算之后的时间
    username = request.GET.get('username')
    print(username)
    # 3. 因为我们假设没有cookie信息,我们服务器就要设置cookie信息
    response = HttpResponse(username)

    # key,value
    response.set_cookie('username', username,max_age=3600) # max_age=3600,有效期一小时

    # 删除cookie的2种方式
    # response.delete_cookie(key)
    # response.set_cookie(key,value,max_age=0)

    # 4.返回相应
    return response

def get_cookie(request):
    """
    范例:http://127.0.0.1:8000/get_cookie/
    # 第二次及其之后的过程
    # ⑤ 当我们的浏览器第二次及其之后的请求都会携带cookie信息
    # ⑥ 我们的服务器接收到请求之后,会发现请求中携带的cookie信息,这样的话就认识是谁的请求了
    """
    cookies=request.COOKIES
    print(cookies)
    username=cookies.get('username','没有cookies信息')
    context={'get_cookie':username}
    print(username)
    print('----')
    return HttpResponse(context.items())


"""
    问题1: 我换了浏览器,还能获取到 session信息吗? 不可以
    问题2: 我不换浏览器,删除session id ,则获取不到session数据
    问题3: 再去执行 set_sesison 的时候 会重新生成session id

保存在服务器的数据叫做 session
    session需要依赖于cookie
    如果浏览器禁用了cookie,则session不能实现

    0.概念
    1.流程

        第一次请求:
            ① 我们第一次请求的时候可以携带一些信息(用户名/密码) cookie中没有任何信息
            ② 当服务器接收到这个请求之后,进行用户名和密码的验证,验证没有问题可以设置session信息
            ③ 在设置session信息的同时(session信息保存在服务器端).服务器会在响应头中设置一个sessionid的cookie信息(由服务器自己设置的,不是我们设置的)
            ④ 客户端(浏览器)在接收到响应之后,会将cookie信息保存起来 (保存 sessionid的信息)

        第二次及其之后的请求:
            ⑤ 第二次及其之后的请求都会携带 session id信息
            ⑥ 当服务器接收到这个请求之后,会获取到 sessionid 信息,然后进行验证,验证成功,则可以获取 session信息(session信息保存在服务器端)

    2.效果
    3.从原理(http)角度

        第一次请求:
            ① 第一次请求,在请求头中没有携带任何cookie信息
            ② 我们在设置session的时候,session会做2件事.
                #第一件：　将数据保存在数据库中
                #第二件：　设置一个cookie信息，这个cookie信息是以　sessionid为key  value为 xxxxx
                cookie肯定会以响应的形式在相应头中出现

        第二次及其之后的:
            ③ 都会携带 cookie信息,特别是 sessionid


"""
def set_session(request):
    '''
         范例:http://127.0.0.1:8000/set_cookie?username=itenginger&password=123
        第一次请求:
            ① 我们第一次请求的时候可以携带一些信息(用户名/密码) cookie中没有任何信息
            ② 当服务器接收到这个请求之后,进行用户名和密码的验证,验证没有问题可以设置session信息
            ③ 在设置session信息的同时(session信息保存在服务器端).服务器会在响应头中设置一个sessionid的cookie信息(由服务器自己设置的,不是我们设置的)
            ④ 客户端(浏览器)在接收到响应之后,会将cookie信息保存起来 (保存 sessionid的信息)
    '''

    print(request.COOKIES)
    # 2.对用户名和密码进行验证
    # 假设认为 用户名和密码正确
    user_id = 6666
    print(type(request.session))
    # 3.设置session信息
    # 设置session的时候其实 session做了2件事
    # 第一件：　将数据保存在数据库中
    # 第二件：　设置一个ｃｏｏｋｉｅ信息，这个ｃｏｏｋｉｅ信息是以　sessionid为key
    request.session['user_id']=user_id  # request.session  理解为字典
    request.session['name']='itcast'
    # 4. 返回响应
    return  HttpResponse(request.session['user_id'])


def get_session(request):
    """
        范例:http://127.0.0.1:8000/get_session/
        第二次及其之后的请求:
            ⑤ 第二次及其之后的请求都会携带 session id信息
            ⑥ 当服务器接收到这个请求之后,会获取到sessionid信息,然后进行验证,验证成功,则可以获取session信息(session信息保存在服务器端)
            可通过数据库查找session的信息。
    """
    # 1. 请求都会携带 session id信息
    print(request.COOKIES)
    # 2. 会获取到sessionid信息,然后进行验证,如果验证成功,可以获取 session信息
    # request.session 字典
    # user_id = request.session['user_id']
    user_id = request.session.get('user_id')
    name=request.session.get('name')
    context={'user_id':user_id,'name':name}
    print(user_id,name)
    #
    # 3.返回响应
    return HttpResponse(context.items())

"""
登陆页面
    GET 请求是获取 登陆的页面
    POST 请求是 验证登陆 (用户名和密码是否正确)
"""

# 我想由2个视图 变为 1个视图
def login(request):
    '''
    范例:http://127.0.0.1:8000/login
    :param request:
    :return:
    '''
    # 我们需要区分业务逻辑
    if request.method=='GET':# GET 请求是获取登陆的页面
        return render('get请求')
    else:#POST 请求是验证登陆 (用户名和密码是否正确)
        return redirect('首页')

"""
面向对象

    类视图 是采用的面向对象的思路

    1.定义类试图
        ① 继承自 View  (from django.views import View)
        ② 不同的请求方式 有不同的业务逻辑
            类试图的方法 就直接采用 http的请求方式的名字 作为我们的函数名.例如: get,post,put,delete
        ③  类试图的方法的第二个参数 必须是请求实例对象
            类试图的方法 必须有返回值 返回值是HttpResopnse及其子类

    2.类试图的url引导
    
    
"""
class BookView(View):

    # http_method_names = ["get","post","put","patch","delete","head","options","trace",]
    # 范例:http://127.0.0.1:8000/loginbook
    def get(self,request):
        """处理GET请求，返回注册页面"""
        username = request.COOKIES.get('username')
        if username is None:
            print('username is None')
        return HttpResponse('get')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        username = request.COOKIES.get('username')
        if username is None:
            print('username is None')
        return HttpResponse('post')

    def put(self, request):
        username = request.COOKIES.get('username')
        if username is None:
            print('username is None')
        return HttpResponse('put')
    def delete(self,request):
        username = request.COOKIES.get('username')
        if username is None:
            print('username is None')
        return HttpResponse('delete')

"""
个人中心页面      --  必须登陆才能显示
GET 方式 展示 个人中心
POST 实现个人中心信息的修改
定义类视图
导入from django.contrib.auth.mixins import LoginRequiredMixin
"""
from django.contrib.auth.mixins import LoginRequiredMixin

class CenterView(LoginRequiredMixin,View): # 多继承，先找LoginRequiredMixin的方法，如果没有找view
    # 范例:http://127.0.0.1:8000/center
    # LoginRequiredMixi判断是否验证用户已登录
    def get(self,request):
        return HttpResponse('个人中心展示')

    def post(self, request):
        return HttpResponse('个人中心修改')


#############################模板############################################

class HomeView(View):
    '''
    范例:http://127.0.0.1:8000/home
    '''
    def get(self,request):
        # 1.获取数据
        username=request.GET.get('username')
        # 2.组织数据
        context={
            'username': username,
            'age': 14,
            'birthday': datetime.now(),
            'friends': ['tom', 'jack', 'rose'],
            'money': {
                '2019': 12000,
                '2020': 18000,
                '2021': 25000,
            },
            'desc': '<script>alert("这是脚本")</script>'  # 脚本，留意
        }
        return render(request,'index-jinja2.html',context=context)

class detailView(View):
    '''
    范例:http://127.0.0.1:8000/detail
    '''
    def get(self, request):
        return render(request,'detail.html')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        return HttpResponse('post')