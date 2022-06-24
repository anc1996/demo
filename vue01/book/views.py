from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
# Create your views here.
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self, request):
        pass

class RecevieView(View):

    def get(self,request):
        # 1.接收参数
        data = request.GET
        username=data.get('username')
        password = data.get('password')
        return JsonResponse({'info':{'username':username,'password':password}})

    def post(self,request):
        # data = request.POST
        data=json.loads(request.body.decode())# 由于发送是ajax请求
        username = data.get('username')
        password = data.get('password')
        return JsonResponse({'info': {'username': username, 'password': password}})