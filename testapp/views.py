from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.auth.hashers import check_password
import requests

# Create your views here.
url = 'http://localhost:8080'
headers = {'Content-Type': 'application/json'}
data = {'key': 'value'}


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
def create_user(request):
    if request.method == 'POST':
        registerData = request.data.POST
        for register in registerData['register']:
            steamId = register['steamid']
            # picTure = register['picture']
            userName = register['username']
            phoneNumber = register['phone_number']
            emAil = register['email']
            passWord = register['password']
        if models.User.objects.filter(phone_number=phoneNumber).exists():
            error_message = 'Registration failed. Please check your input.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            models.User.objects.create(steam_id=steamId, username=userName,
                                       phone_number=phoneNumber, email=emAil, password=passWord)
            response_data = {'message': 'Registration successful'}
            return Response(response_data, status=200)
            # 返回一个保存成功的标识


def user_login(request):
    if request.method == 'POST':
        userData = request.data.POST
        for user in userData['login']:
            phoneNumber = user['phone_number']
            passWord = user['password']
        if models.User.objects.filter(phone_number=phoneNumber).exists():
            user = User.objects.get(phone_number=phoneNumber)
            password_match = check_password(passWord, user.password)
            if password_match:
                response_data = {'message': 'login successful'}
                return Response(response_data, status=200)
            else:
                error_message = 'login failed. Please check your password.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            error_message = 'login failed. Please check your phone number.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)