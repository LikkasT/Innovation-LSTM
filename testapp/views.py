import json
from datetime import timedelta

import numpy as np
import pandas as pd
from django.contrib.auth.hashers import check_password
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from sklearn.preprocessing import MinMaxScaler

from .models import *


# Create your views here.


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
        if User.objects.filter(phone_number=phoneNumber).exists():
            error_message = 'Registration failed. Please check your input.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            User.objects.create(steam_id=steamId, username=userName,
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
        if User.objects.filter(phone_number=phoneNumber).exists():
            user = User.objects.get(phone_number=phoneNumber)
            password_match = check_password(passWord, user.password)
            if password_match:
                response_data = {'message': 'login successful', 'userid': user.user_id}
                return Response(response_data, status=200)
            else:
                error_message = 'login failed. Please check your password.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            error_message = 'login failed. Please check your phone number.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)


def user_modify(request):
    if request.method == 'POST':
        modifyData = request.data.POST
        for user in modifyData['modify']:
            userId = user['userid']
            steamId = user['steamid']
            #图片加个转码，存本地，暂定base64
            picTure = user['picture']
            userName = user['username']
            phoneNumber = user['phone_number']
            emAil = user['email']
            passWord = user['password']
            if User.objects.filter(userid=userId).exists():
                try:
                    user = User.objects.get(userid=userId)

                    # 修改用户信息
                    user.steamid = steamId
                    user.picture = picTure
                    user.username = userName
                    user.phone_number = phoneNumber
                    user.email = emAil
                    user.password = passWord

                    # 保存修改后的用户信息
                    user.save()
                    response_data = {'message': 'modify successful'}
                    return Response(response_data, status=200)
                except User.DoesNotExist:
                    error_message = 'bug.'
                    return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            else:
                error_message = 'user not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        userid = request.GET.get('userid')
        try:
            user = User.objects.get(userid=userid)
            response_data = {'message':
                {
                    'username': user.username,
                    'email': user.email,
                    'phoneNumber': user.phone_number,
                    'picture': user.picture,
                    'steamid': user.steamid,
                    'password': user.password,
                    'userid': user.userid
                }
            }
            return Response(response_data, status=200)
        except User.DoesNotExist:
            error_message = 'user not found.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)


#商品收藏页面，post函数包括了添加和删除，get函数返回{message:{collection1:商品id，collection2：商品id}}

def collection(request):
    message = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        userId = request.POST.get('userid')
        goodsId = request.POST.get('goodsId')
        if action == 'add':
            try:
                user = User.objects.get(userid=userId)
                user.favorite_jewelry_types = user.favorite_jewelry_types + goodsId + ','
                user.save()
                response_data = {'message': 'collection add successful'}
                return Response(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'user not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        elif action == 'delete':
            try:
                user = User.objects.get(userid=userId)
                user.favorite_jewelry_types = user.favorite_jewelry_types.replace(goodsId + ',', "")
            except User.DoesNotExist:
                error_message = 'user not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        elif action == 'show':
            page = request.POST.get('page')
            #page需要从0开始返回例如第1页为page0
            try:
                user = User.objects.get(userid=userId)  # 返回两个涨幅，
                elements = user.favorite_jewelry_types.split(',')  # 限制10条
                j = 1
                for i in elements:
                    if j > page*10:
                        message[f'collection{i}']['goodsId'] = elements[i]
                        goodsforin = Jewelry.objects.get(jewelry_id=elements[i])
                        message[f'collection{i}']['7days'] = goodsforin.with_price_increase(days=7)
                        message[f'collection{i}']['30days'] = goodsforin.with_price_increase(days=30)
                        goods = JewelryType.objects.get(jewelry_id=elements[i])
                        message[f'collection{i}']['image'] = goods.image
                        message[f'collection{i}']['name'] = goods.name
                    j = j+1
                    if j >= page*10+10:
                        break
                response_data = {'message': message}
                return Response(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'user not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        userId = request.GET.get('userid')
        try:
            user = User.objects.get(userid=userId)#返回两个涨幅，
            elements = user.favorite_jewelry_types.split(',')
            j = 0
            for i in elements:
                message[f'collection{i}']['goodsId'] = elements[i]
                goodsforin = Jewelry.objects.get(jewelry_id=elements[i])
                message[f'collection{i}']['7days'] = goodsforin.with_price_increase(days=7)
                message[f'collection{i}']['30days'] = goodsforin.with_price_increase(days=30)
                goods = JewelryType.objects.get(jewelry_id=elements[i])
                message[f'collection{i}']['image'] = goods.image
                message[f'collection{i}']['name'] = goods.name
                j = j + 1
                if j >= 10:
                    break
            response_data = {'message': message}
            return Response(response_data, status=200)
        except User.DoesNotExist:
            error_message = 'user not found.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
def perform_search(query):
    results = JewelryType.objects.filter(name__icontains=query)
    return results

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')

        results = perform_search(query)

        serializer = ItemSerializer(results, many=True)
        return Response(serializer.data)


    #交易排行，热榜返回10条


def goods_show(request):
    message = {}
    if request.method == 'GET':
        jewelry_name = request.GET.get('jewelry_name')
        try:
            goods = JewelryType.objects.filter(name=jewelry_name)
            for good in goods:
                message[good]['name'] = good.name
                message[good]['wear_and_tear'] = good.wear_and_tear
                message[good]['image'] = good.image
                message[good]['jewelry_id'] = good.jewelry_id
                price = Jewelry.objects.filter(jewelry_id=good.jewelry_id)
                message[good] = {'pricelog': []}
                data_log = []
                price_log = []
                quantity_log = []
                for price in price:
                    message[good]['price'].append(price)
                    data_log.append(price.date)
                    price_log.append(price.price)
                    quantity_log.append(price.units_sold)
                data = pd.DataFrame({
                    'date': data_log,
                    'price': price_log,
                    'quantity_on_sale': quantity_log
                })
                data['date'] = pd.to_datetime(data['date'])

                # 创建dataframe对象
                dataframe = data.set_index('date')

                # 数据预处理
                scaler = MinMaxScaler(feature_range=(0, 1))
                dataset = scaler.fit_transform(dataframe[['price']].values)

                # 构建数据集
                def create_dataset(dataset, look_back=1):
                    dataX, dataY = [], []
                    for i in range(len(dataset) - look_back - 1):
                        a = dataset[i:(i + look_back), 0]
                        dataX.append(a)
                        dataY.append(dataset[i + look_back, 0])
                    return np.array(dataX), np.array(dataY)

                # 构建输入特征X和输出Y
                look_back = 14  # 增加为14天的数据
                trainX, trainY = create_dataset(dataset, look_back)

                # 调整输入数据的格式
                trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

                # 构建更复杂的LSTM多变量模型
                model = Sequential()
                model.add(LSTM(64, input_shape=(1, look_back), return_sequences=True))
                model.add(Dropout(0.2))
                model.add(LSTM(64, return_sequences=False))
                model.add(Dropout(0.2))
                model.add(Dense(1))
                model.compile(loss='mean_squared_error', optimizer='adam')
                model.fit(trainX, trainY, epochs=300, batch_size=16, verbose=2)

                # 使用模型进行预测
                def predict_next_seven_days(model, dataset, look_back=14, scaler=None):  # 修改为14天的数据
                    last_data = dataset[-look_back:]
                    prediction = []
                    for i in range(7):
                        X = np.array(last_data).reshape(1, 1, look_back)
                        pred = model.predict(X)
                        last_data = np.append(last_data, pred)[-look_back:]
                        prediction.append(pred[0, 0])
                    prediction = scaler.inverse_transform(np.array(prediction).reshape(-1, 1))
                    return prediction

                # 预测未来七天的价格
                future_prediction = predict_next_seven_days(model, dataset, look_back, scaler)

                # 生成未来七天的日期
                forecast_dates = [dataframe.index[-1] + timedelta(days=(i + 1)) for i in range(7)]

                # 将预测结果添加到数据框中
                forecast = pd.DataFrame(future_prediction, index=forecast_dates, columns=['price'])

                # 将预测结果转换为JSON格式
                forecast_json = forecast.reset_index().to_json(orient='records', date_format='iso')
                forecast_data = json.loads(forecast_json)

                # 将预测结果添加到JSON对象中
                output_json = {
                    "future_predictions": forecast_data
                }
                response_data = {'message': message,'output_json': output_json}
                return Response(response_data, status=200)
        except JewelryType.DoesNotExist:
            error_message = 'good not found.'
            return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)


def trading_hot_list(request):
    message = {}
    if request.method == 'GET':
        data = Jewelry.objects.order_by('-units_sold').values('jewelry_id', 'units_sold')[:10]
        i = 1
        for item in data:
            try:
                JewelryType.objects.get(jewelry_id=item['jewelry_id'] )
                message[f'good{i}']['jewelry_id']=item['jewelry_id']
                message[f'good{i}']['units_sold']=item['units_sold']
                message[f'good{i}']['image']=item.image
                message[f'good{i}']['name']=item.name
                message[f'good{i}']['wear_and_tear']=item.wear_and_tear
            except JewelryType.DoesNotExist:
                error_message = 'data not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i+=1
        response_data = {'message': message}
        return Response(response_data, status=200)
    if request.method == 'POST':
        page = request.POST.get('page')
        data = Jewelry.objects.order_by('-units_sold').values('jewelry_id', 'units_sold')[page:page+10]
        i = 1
        for item in data:
            try:
                JewelryType.objects.get(jewelry_id=item['jewelry_id'])
                message[f'good{page*10+i}']['jewelry_id'] = item['jewelry_id']
                message[f'good{page*10+i}']['units_sold'] = item['units_sold']
                message[f'good{page*10+i}']['image'] = item.image
                message[f'good{page*10+i}']['name'] = item.name
                message[f'good{page*10+i}']['wear_and_tear'] = item.wear_and_tear
            except JewelryType.DoesNotExist:
                error_message = 'data not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
        response_data = {'message': message}
        return Response(response_data, status=200)


def earnings_ranking(request):
    message = {}
    if request.method == 'GET':
        data = Jewelry.objects.with_price_increase(days=7).order_by('price_increase')[:10]
        i = 1
        for item in data:
            try:
                JewelryType.objects.get(jewelry_id=item['jewelry_id'])
                message[f'good{i}']['jewelry_id'] = item['jewelry_id']
                message[f'good{i}']['price_increase'] = item['price_increase']
                message[f'good{i}']['image'] = item.image
                message[f'good{i}']['name'] = item.name
                message[f'good{i}']['wear_and_tear'] = item.wear_and_tear
            except JewelryType.DoesNotExist:
                error_message = 'data not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
    if request.method == 'POST':
        page = request.POST.get('page')
        days = request.POST.get('days')
        data = Jewelry.objects.with_price_increase(days=days).order_by('price_increase')[page:page+10]
        i = 1
        for item in data:
            try:
                JewelryType.objects.get(jewelry_id=item['jewelry_id'])
                message[f'good{page*10+i}']['jewelry_id'] = item['jewelry_id']
                message[f'good{page*10+i}']['price_increase'] = item['price_increase']
                message[f'good{page*10+i}']['image'] = item.image
                message[f'good{page*10+i}']['name'] = item.name
                message[f'good{page*10+i}']['wear_and_tear'] = item.wear_and_tear
            except JewelryType.DoesNotExist:
                error_message = 'data not found.'
                return Response({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
