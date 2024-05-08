import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import json

# 读取数据
data = pd.read_csv('C:\\Users\\Windows\\Desktop\\456.csv', usecols=['date', 'price', 'quantity_on_sale'])
data['date'] = pd.to_datetime(data['date'])

# 创建dataframe对象
dataframe = data.set_index('date')

# 数据预处理
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataframe[['price']].values)

# 构建数据集
def create_dataset(dataset, look_back=1):
 dataX, dataY = [], []
 for i in range(len(dataset)-look_back-1):
     a = dataset[i:(i+look_back), 0]
     dataX.append(a)
     dataY.append(dataset[i + look_back, 0])
 return np.array(dataX), np.array(dataY)

# 构建输入特征X和输出Y
look_back = 3
trainX, trainY = create_dataset(dataset, look_back)

# 调整输入数据的格式
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

# 构建LSTM双变量模型
model = Sequential()
model.add(LSTM(64, input_shape=(1, trainX.shape[2])))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=200, batch_size=1, verbose=2)

# 使用模型进行预测
def predict_next_five_days(model, dataset, look_back=1, scaler=None):
 last_data = dataset[-look_back:]
 prediction = []
 for i in range(5):
     X = np.array(last_data[-look_back:]).reshape(1, 1, look_back)
     pred = model.predict(X)
     last_data = np.append(last_data, pred)
     prediction.append(pred[0, 0])
 prediction = scaler.inverse_transform(np.array(prediction).reshape(-1, 1))
 return prediction

# 预测未来五天的价格
future_prediction = predict_next_five_days(model, dataset, look_back, scaler)

# 生成未来五天的日期
forecast_dates = [dataframe.index[-1] + timedelta(days=(i+1)) for i in range(5)]

# 将预测结果添加到数据框中
forecast = pd.DataFrame(future_prediction, index=forecast_dates, columns=['price'])

# 将预测结果转换为JSON格式
forecast_json = forecast.reset_index().to_json(orient='records', date_format='iso')
forecast_data = json.loads(forecast_json)

# 将预测结果添加到JSON对象中
output_json = {
   "future_predictions": forecast_data
}

# 打印JSON格式的输出
print(json.dumps(output_json, indent=2))

# 合并历史数据和预测数据
combined_data = pd.concat([dataframe, forecast])
# 绘制历史数据和预测数据
plt.figure(figsize=(12, 6))
plt.plot(combined_data.index, combined_data['price'], label='Historical Data', color='b')
plt.plot(forecast.index, forecast['price'], label='Predicted Data', color='r', linestyle='solid')
plt.title('Historical Data')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# 设置x轴刻度和标签
x_ticks = pd.date_range(start=combined_data.index[0], end=forecast.index[-1], freq='D')  # 设置每天为刻度
plt.xticks(x_ticks, rotation=90)  # 设置x轴刻度位置和标签，并旋转标签

plt.show()