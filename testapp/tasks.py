from background_task import background
import itertools
import logging
import re
import time
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from .models import *
import requests
from testapp import models

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# def get_image(session, url):
#    try:
#        response = session.get(url)
#        response.raise_for_status()  # 检查响应状态码，如果不是200会抛出异常
#        return response.content
#    except requests.RequestException as e:
#        logging.error(f"Failed to fetch image from {url}: {e}")
#        return None

def get_history_price(session, goods_id):
    url = f"https://buff.163.com/api/market/goods/price_history/buff?game=csgo&goods_id={goods_id}&currency=CNY&days=180&buff_price_type=2&_=1682951672714"
    try:
        response = session.get(url)
        response.raise_for_status()  # 检查响应状态码，如果不是200会抛出异常
        data = response.json()
        if 'data' in data and 'price_history' in data['data']:
            return data['data']['price_history']
        else:
            raise ValueError('Invalid JSON format or missing data')
    except requests.RequestException as e:
        logging.error(f"Failed to fetch price history for goods ID {goods_id}: {e}")
        return None
    except (KeyError, ValueError) as e:
        logging.error(f"Error processing JSON data for goods ID {goods_id}: {e}")
        return None


def get_items(session):
    page = 1
    goodsData = {}
    goodsPrice = {}
    priceDay = {}
    while True:
        url = f"https://buff.163.com/api/market/goods?game=csgo&page_num={page}&use_suggestion=0&_=1682951638925"
        try:
            response = session.get(url)
            response.raise_for_status()  # 检查响应状态码，如果不是200会抛出异常
            data = response.json()['data']
            items = data['items']
            for item in itertools.islice(items, 6):
                short_name = item['short_name']
                logging.info(f'正在爬取 {short_name}')
                icon_url = item['goods_info']['icon_url']
                # icon = get_image(session, icon_url)
                if icon_url:
                    i = 0
                    for record in get_history_price(session, item['id']):
                        goodsUrl = icon_url
                        # sheet[f'A{index}'] = sheet.add_image(image, f'A{index}')
                        goodsName = short_name
                        # sheet[f'C{index}'] = item['sell_reference_price']
                        goodsAbradability = ''.join(re.findall('\((.*?)\)', item['name']))
                        priceDay[i] = datetime.fromtimestamp(int(str(record[0])[:-3])).strftime("%Y-%m-%d %H:%M:%S")
                        goodsPrice[i] = record[1]
                        goodsId = item['id']
                        sellNumber = item['sell_num']
                        i += 1
                    goodsDataArray = [goodsUrl, goodsName, goodsAbradability, priceDay, goodsPrice, goodsId,
                                      sellNumber]
                    key = f'Product_{goodsId}'
                    goodsData[key] = goodsDataArray

                time.sleep(3)
            time.sleep(2)
            page += 1
            if page > 1:
                break
        except requests.RequestException as e:
            logging.error(f"Failed to fetch items from page {page}: {e}")
            time.sleep(5)  # 等待一段时间后重试
        except (KeyError, ValueError) as e:
            logging.error(f"Error processing JSON data for page {page}: {e}")
            time.sleep(5)  # 等待一段时间后重试
    return goodsData


def spiders():
    session = requests.session()
    session.headers = {
        'authority': 'buff.163.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': '_ntes_nuid=045cbd10cba196cf51a1a7761ef504ff; Device-Id=e6Oxt0HKqjJJq4xFgkfR; _ntes_nnid=045cbd10cba196cf51a1a7761ef504ff,1695470791036; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=DPh5ptnrMU478ZxEM6y6EBXoQq1J4qodS5MrTDs9RwilybvYyrnuZzKLvYJQid5nC6arMyZrbwtVBhy2buxisFCUDLHxLv.aR_1ie7o5qh3z_lyGQV9of3hY5bGJQuxl2lMimVzlOm_EvLGgjKuP.qgvSF3hMSQ1AdKHhslrmBS6kFtlqzAvFO7cl4rB.6qDC2P8qaIcnwAXkDxS.XK0J1TaI0wik78EPjjXUCMsDFyPc; S_INFO=1715231249|0|0&60##|18016234568; P_INFO=18016234568|1715231249|1|netease_buff|00&99|null&null&null#taiwan&710000#10#0|&0|null|18016234568; qr_code_verify_ticket=f18iLzr91e6997a3fc07863cf0353369eaa9; remember_me=U1092033227|DWPsykMxWLNegUJ3YuvjXscukVGjXXwV; session=1-52FUWqwTYqhBgQgheIBqhp5IrT-GCBiJ0fbUh4n6BBYJ2044298643; csrf_token=IjNkMTcwYmQwZjUyNDUwMWQ3NTQyMDY0OTU5MjMzZTUxMzBhZmFmMDgi.GR3sTQ.YSdBl7VVc2L4HKB3YRjo0zAd5TM',
        'referer': 'https://buff.163.com/market/csgo',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    goodsData = get_items(session)
    return goodsData


def saveJson(goodsData):
    saveData = {}
    saveData["product_info"] = goodsData
    with open('saveData.json', 'w') as file:
        json.dump(saveData, file)


def saveLSTMJson(goodsData):
    saveData = {}
    saveData["product_info"] = goodsData
    with open('LSTM.json', 'w') as file:
        json.dump(saveData, file)


def readJson():
    with open('sendData.json', 'r') as file:
        jsonData = json.load(file)
        for i in jsonData['product_info'].keys():
            pictureUrl = jsonData['product_info'][i][0]
            goodsName = jsonData['product_info'][i][1]
            goodsAbradability = jsonData['product_info'][i][2]
            goodsId = jsonData['product_info'][i][5]
            sellNumber = jsonData['product_info'][i][6]
            sellDays = jsonData['product_info'][i][3]
            goodsPrice = jsonData['product_info'][i][4]
            good_exists = models.JewelryType.objects.filter(name=goodsName, wear_and_tear=goodsAbradability).exists()
            if not good_exists:
                models.JewelryType.objects.create(name=goodsName, wear_and_tear=goodsAbradability, image=pictureUrl,
                                                  jewelry_id=goodsId)
            for j in sellDays.keys():
                #加一个自动覆盖来覆盖预测数据，
                #加一个自动删除控制在37条。
                day = sellDays[j]
                price = goodsPrice[j]
                sale_exists = models.Jewelry.objects.filter(jewelry_id=goodsId, date=day).exists()
                if not sale_exists:
                    models.Jewelry.objects.create(jewelry_id=goodsId, date=day, price=price, units_sold=sellNumber)


def readLSTMJson():
    with open('LSTM.json', 'r') as file:
        jsonData = json.load(file)
        for i in jsonData['product_info'].keys():

            jewelry_id = i
            for j in jsonData['product_info'][i]:
                date = j['index']
                price = j['price']
                good_exists = Jewelry.objects.filter(date=date, jewelry_id=jewelry_id).exists()
                if not good_exists:
                    Jewelry.objects.create(date=date, price=price, units_sold='',
                                           jewelry_id=jewelry_id)
                else:
                    good = Jewelry.objects.get(date=date, jewelry_id=jewelry_id)
                    good.price = price
                    good.save()

def spider_task():
    saveJson(spiders())


def spider_read():
    readJson()


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


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


def LSTM():
    goods = JewelryType.objects.values_list('jewelry_id', flat=True)
    output_json = {}
    for good_id in goods:
        prices = Jewelry.objects.filter(jewelry_id=good_id)
        data_log = []
        price_log = []
        quantity_log = []
        for price in prices:
            # 需要引入日期判断，如果是今天之前的日期，且价格数据与current价格一致，则读取。
            if price.quantity != '':
                data_log.append(price.date)
                price_log.append(price.price)
                quantity_log.append(price.units_sold)
            data = pd.DataFrame({
                'date': data_log,
                'price': price_log,
                'quantity_on_sale': quantity_log
            })
            dataframe = data.set_index('date')
            # 数据预处理
            scaler = MinMaxScaler(feature_range=(0, 1))
            dataset = scaler.fit_transform(dataframe[['price']].values)
            # 构建数据集
            # 构建输入特征X和输出Y
            look_back = 14  # 增加为14次的数据
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
            output_json[good_id]: forecast_data

    return output_json


def LSTM_task():
    saveLSTMJson(LSTM())


@background(schedule=timedelta(hours=24))
def my_background_task():
    spider_task()
    spider_read()
    LSTM_task()
    # 在后台执行的任务代码
