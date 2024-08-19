import json
import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.users.models import User

"""
判断用户名是否重复
"""


class UsernameCountView(View):
    def get(self, request):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'code': 400, 'errmsg': 'No usernames provided'})
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if allow not in ['0', '1']:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})
        allow_int = int(allow)
        if allow_int == 0:
            return JsonResponse({'code': 400, 'errmsg': '注册失败，请勾选同意'})
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        count = User.objects.filter(username=username).count()
        if count != 0:
            return JsonResponse({'code': 400, 'errmsg': '用户名已存在'})
        # 数据入库
        user = User(username=username, password=password, mobile=mobile)
        user.save()
        userid = User.objects.get(username=username).id
        return JsonResponse(
            {'code': 200, 'errmsg': '注册成功，用户ID为%s' % userid})


class LoginView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        count = User.objects.filter(username=username).count()
        if count != 0:
            password_right = User.objects.get(username=username).password
            if password == password_right:
                user = User.objects.get(username=username)
                user.state = 1
                user.save()
                return JsonResponse({'code': 200, 'errmsg': '登录成功'})
            else:
                return JsonResponse({'code': 400, 'errmsg': '登录失败，账号或密码错误'})
        elif count == 0:
            return JsonResponse({'code': 400, 'errmsg': '登录失败，账号或密码错误'})


class LoginStateView(View):
    def get(self, request):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'code': 400, 'errmsg': 'No usernames provided'})
        count = User.objects.filter(username=username).count()
        if count == 0:
            return JsonResponse({'code': 400, 'errmsg': '用户不存在'})
        else:
            state = User.objects.get(username=username).state
            if state == 0:
                return JsonResponse({'code': 200, 'errmsg': '用户离线'})
            if state == 1:
                return JsonResponse({'code': 200, 'errmsg': '用户在线'})


class LogoutView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        allow = body_dict.get('allow')
        if not all([username, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if allow not in ['0', '1']:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})
        allow_int = int(allow)
        if allow_int == 0:
            return JsonResponse({'code': 400, 'errmsg': '注销失败，请勾选同意'})
        count = User.objects.filter(username=username).count()
        if count == 0:
            return JsonResponse({'code': 400, 'errmsg': '注销失败，用户不存在'})
        state = User.objects.get(username=username).state
        if state == 0:
            return JsonResponse({'code': 400, 'errmsg': '注销失败，不可重复注销'})
        else:
            user = User.objects.get(username=username)
            user.state = 0
            user.save()
            return JsonResponse({'code': 200, 'errmsg': '注销成功'})
