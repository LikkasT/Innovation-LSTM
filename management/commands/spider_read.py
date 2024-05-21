import itertools
import json
import logging
import re
import time
from datetime import datetime

import requests
from django.core.management.base import BaseCommand
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
                day = sellDays[j]
                price = goodsPrice[j]
                sale_exists = models.Jewelry.objects.filter(jewelry_id=goodsId, date=day).exists()
                if not sale_exists:
                    models.Jewelry.objects.create(jewelry_id=goodsId, date=day, price=price, units_sold=sellNumber)





def spider_task():
    while True:
        saveJson(spiders())

def spider_read():
    while True:
        readJson()

class Command(BaseCommand):
    help = 'Starts a task that runs synchronously in the background.'

    def handle(self, *args, **options):
        spider_task()
        spider_read()



# python manage.py spider_read