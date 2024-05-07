from django.shortcuts import render
import json
from models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def enroll(request):
    return render(request, 'enroll.html')


# 假设以下json文件是注册的前端传输文件
# {
#   "register": [
#     {
#       "steamId": "user1",
#       "email": "user1@example.com"
#     },
#     {
#       "steamId": "user2",
#       "email": "user2@example.com"
#     }
#   ]
# }
def create_user():
    with open('register.json', 'r') as file:
        jsonData = file.read()
        registerData = json.loads(jsonData)
        for register in registerData['register']:
            steamId = register['steamid']
            # picTure = register['picture']
            userName = register['username']
            phoneNumber = register['phone_number']
            emAil = register['email']
            passWord = register['password']
            if User.objects.filter(phone_number=phoneNumber).exists():
                return 0
                # 电话号码重复则返回一个报错信息
            else:
                User.objects.create(steam_id=steamId,  username=userName,
                                    phone_number=phoneNumber, email=emAil, password=passWord)
                return 1
                # 返回一个保存成功的标识
