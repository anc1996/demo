from django.http import HttpResponse
"""
中间件的作用: 每次请求和相应的时候都会调用
中间件的定义
中间件的使用: 我们可以判断每次请求中是否携带了cookie中某些信息
"""
def simple_middleware(get_response):
    # One-time configuration and initialization.
    # 这里是 中间件第一次调用执行的地方
    print('这里是 中间件1第一次调用执行的地方')
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        username = request.COOKIES.get('username')
        # if username is None:
        #     print('username is None')
        #     return HttpResponse('哥们,你没有登陆哎')
        print('这里是 请求前')
        response = get_response(request)
        print('这里就 响应后/请求后')
        # Code to be executed for each request/response after
        # the view is called.
        return response
    return middleware

def simple_middleware2(get_response):
    # print('init2222')
    print('这里是 中间件2第一次调用执行的地方')
    def middleware(request):
        # username = request.COOKIES.get('username')
        # if username is None:
        #     print('username is None')
        #     return HttpResponse('哥们,你没有登陆哎')
        # 这里是 请求前
        print('before request simple_middleware2')
        response=get_response(request)
        #这里就 响应后/请求后
        print('after request/response simple_middleware2')
        return response
    return middleware

