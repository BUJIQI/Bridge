from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt  # 禁用 CSRF 验证，适用于开发环境
def register(request):
    if request.method == 'POST':
        # 获取前端发送的用户注册信息
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {
            'username':'success',
            'password':7777
        }
        '''
        # 向原网站的注册页面发送请求
        response = requests.post('https://target-website.com/api/register/', data={
            'username': username,
            'password': password
        })
        '''
        # 返回注册结果给前端
        return JsonResponse(data.json())

    else:
        return HttpResponse('.....')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取前端发送的登录信息
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {
            'username':'success',
            'password':7777
        }
        '''
        # 向原网站登录接口发送请求
        response = requests.post('https://target-website.com/api/login/', data={
            'username': username,
            'password': password
        })
        '''
        # 返回登录结果给前端
        return JsonResponse(response.json())
    else:
        return HttpResponse('.....')
