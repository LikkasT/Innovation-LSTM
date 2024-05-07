import itertools
import re
import time
import requests
import openpyxl
from openpyxl.drawing.image import Image
from datetime import datetime
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_image(session, url):
   try:
       response = session.get(url)
       response.raise_for_status()  # 检查响应状态码，如果不是200会抛出异常
       return response.content
   except requests.RequestException as e:
       logging.error(f"Failed to fetch image from {url}: {e}")
       return None

def get_history_price(session, goods_id):
   url = f"https://buff.163.com/api/market/goods/price_history/buff?game=csgo&goods_id={goods_id}&currency=CNY&days=30&buff_price_type=2&_=1682951672714"
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

def get_items(session, sheet, index):
   page = 1
   while True:
       url = f"https://buff.163.com/api/market/goods?game=csgo&page_num={page}&use_suggestion=0&_=1682951638925"
       try:
           response = session.get(url)
           response.raise_for_status()  # 检查响应状态码，如果不是200会抛出异常
           data = response.json()['data']
           items = data['items']
           for item in itertools.islice(items,6):
               short_name = item['short_name']
               logging.info(f'正在爬取 {short_name}')
               icon_url = item['goods_info']['icon_url']
               icon = get_image(session, icon_url)
               if icon:
                   for record in get_history_price(session, item['id']):
                       image = Image(BytesIO(icon))
                       image.width = 50
                       image.height = 30
                       sheet[f'A{index}'] = sheet.add_image(image, f'A{index}')
                       sheet[f'B{index}'] = short_name
                       sheet[f'C{index}'] = item['sell_reference_price']
                       sheet[f'D{index}'] = ''.join(re.findall('\((.*?)\)', item['name']))
                       sheet[f'E{index}'] = datetime.fromtimestamp(int(str(record[0])[:-3])).strftime("%Y-%m-%d %H:%M:%S")
                       sheet[f'F{index}'] = record[1]
                       sheet[f'G{index}'] = item['id']
                       sheet[f'H{index}'] = item['sell_num']
                       index += 1
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
def spiders():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    index = 2
    sheet['A1'] = '图片'
    sheet['B1'] = '名称'
    sheet['C1'] = '价格'
    sheet['D1'] = '磨损度'
    sheet['E1'] = '日期'
    sheet['F1'] = '价格'
    sheet['G1'] = 'ID'
    sheet['H1'] = '在售数量'
    session = requests.session()
    session.headers = {
        'authority': 'buff.163.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': '_ntes_nnid=aa59d9de485f50b3d3840e305e698909,1685641317623; _ntes_nuid=aa59d9de485f50b3d3840e305e698909; Device-Id=HVXBUzZrbMzDc2YH04oW; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=RypXfqEJCL557vPRYsVCk8fBqCyOhctH9aIEsf89mIfD490e4zw3CZFN0ecW_TxwotHzb4Cz9ByuDA4I93s_lmokRN.sN0YHK5n_vg7xEAPhh6aFo7I2h.YOMRRPTpGdCjiHVGVsBx4Q2sXQ.Kf.7BZp4jFcIVsesX.otm1gVPBQb0b7Rr.LuWqoBKxNLCukm9srIeihnqqtIXaz.CiO5NKvbNmSTzY2pp5XWNyvF0Ctp; S_INFO=1715065120|0|0&60##|18016234568; P_INFO=18016234568|1715065120|1|netease_buff|00&99|null&null&null#shh&null#10#0|&0||18016234568; remember_me=U1076171504|yT4jHZMy7ekogeJ2GcHuGYBwsFDy4z41; session=1-R7OHVLQY1enK1JeuMfRbZVGe8V_1Ah4SCY628wxyoBSE2028703144; csrf_token=ImVhN2I4ZWMwZTdiYmU2NjRlMmUzZDgyNzJkMzgwZGU5ZTNkZGQ3MDAi.GRtiwg.z5RDPaqNbAmet1OfW0uSdPwv7Eo',
        'referer': 'https://buff.163.com/market/csgo',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    get_items(session, sheet, index)
    workbook.save('数据.xlsx')