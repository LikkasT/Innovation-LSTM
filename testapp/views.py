import json
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .models import *
from .tasks import my_background_task
from django_q.tasks import async_task
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
        registerData = json.loads(request.body)

        # registerData = request.data.POST
        steamId = registerData['steamID']
        # picTure = register['picture']
        userName = registerData['userName']
        phoneNumber = registerData['phoneNumber']
        emAil = registerData['email']
        passWord = registerData['pass']
        if User.objects.filter(phone_number=phoneNumber).exists():
            error_message = 'Registration failed. Please check your input.'

            return JsonResponse({'error': error_message}, status=401)
        else:
            User.objects.create(steam_id=steamId, username=userName,
                                       phone_number=phoneNumber, email=emAil, password=passWord)
            user = User.objects.get(phone_number=phoneNumber)
            message = {'userID': user.user_id,
                       'userName': user.username,
                       'userEmail': user.email,
                       'userPhoneNumber': user.phone_number,
                       'userPass': user.password,
                       'userSteamID': user.steam_id,
                       'message': 'Registration successful'}

            return JsonResponse(message, status=200)
            # 返回一个保存成功的标识


def user_login(request):
    # 加个标识登录状态的参数
    if request.method == 'POST':
        userData = json.loads(request.body)
        phoneNumber = userData['phoneNumber']
        passWord = userData['password']
        if User.objects.filter(phone_number=phoneNumber).exists():
            user = User.objects.get(phone_number=phoneNumber)
            # password_match = check_password(passWord, user.password)
            # print(passWord)
            # print(user.password)
            if passWord == user.password:
                # id生成逻辑改成000001
                response_data = {'message': 'login successful',
                                 'userID': user.user_id,
                                 'userName': user.username,
                                 'userEmail': user.email,
                                 'userPhoneNumber': user.phone_number,
                                 'userPass': user.password,
                                 'userSteamID': user.steam_id,
                                 'userURL': '',
                                 'userBalance': 0}
                return JsonResponse(response_data, status=200)
            else:
                error_message = 'login failed. Please check your password.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            error_message = 'login failed. Please check your phone number.'
            return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)


def user_modify(request):
    if request.method == 'UPDATE':
        modifyData = json.loads(request.body)
        userId = modifyData['userid']
        steamId = modifyData['steamid']
        #图片加个转码，存本地，暂定base64
        # picTure = user['picture']
        userName = modifyData['username']
        phoneNumber = modifyData['phone_number']
        emAil = modifyData['email']
        passWord = modifyData['password']
        if User.objects.filter(userid=userId).exists():
            try:
                user = User.objects.get(userid=userId)
                if User.objects.filter(phone_number=phoneNumber).exists():
                    return JsonResponse({'error': 'phone number already exists'}, status=HTTP_400_BAD_REQUEST)
                else:
                    # 修改用户信息
                    user.steamid = steamId
                    # user.picture = picTure
                    user.username = userName
                    user.phone_number = phoneNumber
                    user.email = emAil
                    user.password = passWord
                    user.save()
                    response_data = {'message': 'modify successful'}
                    return JsonResponse(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'bug.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        else:
            error_message = 'user not found.'
            return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        userid = json.loads(request.body)
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
            return JsonResponse(response_data, status=200)
        except User.DoesNotExist:
            error_message = 'user not found.'
            return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)


#商品收藏页面，post函数包括了添加和删除，get函数返回{message:{collection1:商品id，collection2：商品id}}

def collection(request):
    message = {}
    if request.method == 'POST':
        txt = json.loads(request.body)
        action = txt['action']
        userId = txt['userid']
        goodsId = txt['goodsId']
        if action == 'add':
            try:
                user = User.objects.get(userid=userId)
                user.favorite_jewelry_types = user.favorite_jewelry_types + goodsId + ','
                user.save()
                response_data = {'message': 'collection add successful'}
                return JsonResponse(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'user not found.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        elif action == 'delete':
            try:
                user = User.objects.get(userid=userId)
                user.favorite_jewelry_types = user.favorite_jewelry_types.replace(goodsId + ',', "")
                response_data = {'message': 'collection delete successful'}
                return JsonResponse(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'user not found.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
        elif action == 'show':
            txt = json.loads(request.body)
            page = txt['page']
            #page需要从0开始返回例如第1页为page0,反向展示
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
                # {
                # collection1:
                #               {goodsId:xxx,
                #               7days:xxx,
                #               30days:xxx,
                #               image:xxx,
                #               name:xxx},
                # collection2:
                #               {goodsId:xxx,
                #               7days:xxx,
                #               30days:xxx,
                #               image:xxx,
                #               name:xxx},
                # }
                #
                return JsonResponse(response_data, status=200)
            except User.DoesNotExist:
                error_message = 'user not found.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        txt = json.loads(request.body)
        userId = txt['userid']
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
            return JsonResponse(response_data, status=200)
        except User.DoesNotExist:
            error_message = 'user not found.'
            return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)


def goods_show(request):
    # 历史价格和预测价格合在一个字典里/存一个表里
    # 每天更新一次覆盖数据库只保存37天
    message = {}
    if request.method == 'GET':
        txt = json.loads(request.body)
        jewelry_name = txt['jewelry_name']
        try:
            goods = JewelryType.objects.filter(name=jewelry_name)
            for good in goods:
                message[good] = {'priceLog': [],
                                 'predictLog': [],
                                 'predictDate': [],
                                 'priceDate': []}
                message[good]['name'] = good.name
                message[good]['wear_and_tear'] = good.wear_and_tear
                message[good]['image'] = good.image
                message[good]['jewelry_id'] = good.jewelry_id
                price = Jewelry.objects.filter(jewelry_id=good.jewelry_id)
                for price in price:
                    if price.units_sold == '':
                        message[good]['predictLog'].append(price.price)
                        message[good]['predictDate'].append(price.date)
                    else:
                        message[good]['priceLog'].append(price.price)
                        message[good]['priceDate'].append(price.date)
                response_data = {'message': message}
                return JsonResponse(response_data, status=200)
        except JewelryType.DoesNotExist:
            error_message = 'good not found.'
            return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)


def trading_hot_list(request):
    message = {}

    if request.method == 'GET':
        data = Jewelry.objects.order_by('-units_sold').values('jewelry_id', 'units_sold')[:10]
        count = JewelryType.objects.count()
        i = 1
        for item in data:
            try:
                JewelryType.objects.get(jewelry_id=item['jewelry_id'] )
                message[f'good{i}']['jewelry_id'] = item['jewelry_id']
                message[f'good{i}']['units_sold'] = item['units_sold']
                message[f'good{i}']['image'] = item.image
                message[f'good{i}']['name'] = item.name
                message[f'good{i}']['wear_and_tear'] = item.wear_and_tear
            except JewelryType.DoesNotExist:
                error_message = 'data not found.'
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
        response_data = {'message': message, 'count': count}
        return JsonResponse(response_data, status=200)
    if request.method == 'POST':
        txt = json.loads(request.body)
        page = txt['page']
        data = Jewelry.objects.order_by('-units_sold').values('jewelry_id', 'units_sold')[page:page+10]
        count = JewelryType.objects.count()
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
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
        response_data = {'message': message, 'count': count}
        return JsonResponse(response_data, status=200)


def earnings_ranking(request):
    message = {}
    if request.method == 'GET':
        data = Jewelry.objects.with_price_increase(days=7).order_by('price_increase')[:10]
        count = JewelryType.objects.count()
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
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
            response_data = {'message': message, 'count': count}
            return JsonResponse(response_data, status=200)
    if request.method == 'POST':
        txt = json.loads(request.body)
        page = txt['page']
        days = txt['days']
        data = Jewelry.objects.with_price_increase(days=days).order_by('price_increase')[page:page+10]
        count = JewelryType.objects.count()
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
                return JsonResponse({'error': error_message}, status=HTTP_400_BAD_REQUEST)
            i += 1
            response_data = {'message': message, 'count': count}
            return JsonResponse(response_data, status=200)

def history(request):
    #需要加个商品id外键
    if request.method == 'GET':
        message = {}
        txt = json.loads(request.body)
        param_value = request.GET.get('param_name', 'default_value')
        userID = txt['userID']
        if param_value != 'default_value':
            products = JewelryType.objects.filter(name__icontains=param_value)[:10]
            search = {'products': products, 'query': param_value}
        else:
            search = {'products': '', 'query': ''}
        if userID != '':
            try:
                record = Transaction.objects.filter(userid=userID)
                i = 1
                for records in record:
                    good = JewelryType.objects.get(jewelry_id=records.jewelry_id)
                    message[f'records{i}']['transaction_id'] = records.transaction_id
                    message[f'records{i}']['image'] = good.image
                    message[f'records{i}']['wear_and_tear'] = good.wear_and_tear
                    message[f'records{i}']['current_price'] = good.current_price
                    message[f'records{i}']['name'] = good.name
                    message[f'records{i}']['income'] = records.income
                    message[f'records{i}']['expense'] = records.expense
                    message[f'records{i}']['price'] = records.price
                    message[f'records{i}']['identifier'] = records.identifier
                    i += 1
                return JsonResponse({'message': message, 'search': search}, status=200)
            except Transaction.DoesNotExist:
                return JsonResponse({'message': '', 'search': search}, status=200)
        else:
            return JsonResponse({'message': '', 'search': search}, status=200)
    if request.method == 'POST':
        txt = json.loads(request.body)
        income = txt['income']#收益支出
        expense = txt['expense']#成交时价格
        price = txt['price']#卖出/买入时花费的价格
        identifier = txt['identifier']#交易类型
        jewelry_id = txt['jewelry_id']
        Transaction.objects.create(income=income, expense=expense,
                                   price=price, identifier=identifier, jewelry_id=jewelry_id)
        tran = Transaction.objects.order_by('-id').first()
        return JsonResponse({'success': 'create success', 'transaction_id': tran.transaction_id}, status=200)
    if request.method == 'DELETE':
        txt = json.loads(request.body)
        transaction_id = txt['transactionID']
        try:
            Transaction.objects.filter(transaction_id=transaction_id).delete()
            return JsonResponse({'success': 'delete success'}, status=200)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'wrong transactionID'}, status=HTTP_400_BAD_REQUEST)


def runback(request):
    if request.method == 'GET':
        result = async_task(my_background_task)
        print(result)





