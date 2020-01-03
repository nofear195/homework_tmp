# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:27:43 2019
https://medium.com/@daniel820710/%E5%88%A9%E7%94%A8keras%E5%BB%BA%E6%A7%8Blstm%E6%A8%A1%E5%9E%8B-%E4%BB%A5stock-prediction-%E7%82%BA%E4%BE%8B-1-67456e0a0b
@author: user
"""

import pandas as pd
import numpy as np

np.random.seed(10)
# load data
spy = pd.read_csv("SPY_1993.12.1_2019.12.1.csv")

spy["Date"] = pd.to_datetime(spy["Date"])
spy["year"] = spy["Date"].dt.year
spy["month"] = spy["Date"].dt.month
spy["date"] = spy["Date"].dt.day
spy["day"] = spy["Date"].dt.dayofweek

# normalize data
spy = spy.drop(["Date"], axis =1)
spy_norm = spy.apply(lambda x : (x - np.mean(x)) / (np.max(x) - np.min(x)))

# split train data and test data

#msk = np.random.rand(len(spy_norm)) < 0.8
train_spy = spy_norm[:5273]
test_spy = spy_norm[5274:]

# build train data
def buildTrain(train, pastDay=30, futureDay=5):
  X_train, Y_train = [], []
  for i in range(train.shape[0]-futureDay-pastDay):
    X_train.append(np.array(train.iloc[i:i+pastDay]))
    Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Adj Close"]))
  return np.array(X_train), np.array(Y_train)

X_train, Y_train = buildTrain(train_spy, 30, 1)
X_test, Y_test = buildTrain(test_spy, 30,1)


from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.layers.recurrent import LSTM

model = Sequential()

model.add(LSTM(32, input_shape = (30,10)))
model.add(Dropout(0.2))
model.add(Dense(units = 256, activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(units = 256, activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(units = 1, activation = 'linear'))
model.summary()

model.compile(loss="mse",optimizer = "adam")


#from keras.models import load_model
#load_model("snp500_LSTM_model.h5")

train_history = model.fit(X_train,Y_train,
                          batch_size=128,
                          epochs=100,
                          verbose=2,
                          validation_split = 0.2)


import matplotlib.pyplot as plt
def show_train_history(train_history,train,validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title('Train History')
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    
show_train_history(train_history,'loss','val_loss')

scores = model.evaluate(X_test,Y_test, verbose=2)
print("scores :",scores)

model.save("snp500_LSTM_model.h5")
print("Saved model")