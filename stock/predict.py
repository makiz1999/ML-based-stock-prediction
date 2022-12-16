import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return np.array(dataX), np.array(dataY)

def predict(stock):
	print("Downloading start")
	data = yf.download(tickers=stock, period='1000d', interval='1d')
	close = data['Close']
	print("Downloading stop")

	scaler = MinMaxScaler(feature_range=(0, 1))
	close_scaled = scaler.fit_transform(np.array(close).reshape(-1, 1))

	# split data into test-train
	train = close_scaled[:len(close_scaled) - 1]
	test = close_scaled[len(close_scaled) - 1:]

	time_step = 20
	Xtrain, Ytrain = create_dataset(train, time_step)
	Xtrain = Xtrain.reshape(Xtrain.shape[0], Xtrain.shape[1], 1)
	Xtest = close_scaled[len(close_scaled) - 20:]
	Xtest = Xtest.reshape(1, 20, 1)

	print("Initializing model")

	model = Sequential()
	model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
	model.add(LSTM(50, return_sequences=True))
	model.add(LSTM(50))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')

	print("Fit data")

	history = model.fit(Xtrain, Ytrain, epochs=200, batch_size=64, verbose=1)

	print("Predicting")

	test_predict = model.predict(Xtest)

	test_predict = scaler.inverse_transform([np.append(Xtest, test_predict)])
	y_index = test_predict[0].tolist()

	x_index = close.index[-20:].strftime("%d %b %Y ").tolist()
	x_index.append('Today')

	return x_index, y_index