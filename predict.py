import pandas as pd
import quandl
import math,datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import pandas_datareader as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas.plotting._converter as pandacnv
import csv
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from keras import Sequential
from keras.layers import LSTM, Dense, Activation,Dropout


pandacnv.register()
def predictation(stock_num):
    start = dt.datetime.now() + dt.timedelta(-500)
    end = dt.datetime.today()
    df = web.DataReader('AAPL','yahoo',start,end)

    df = df[['Open', 'High', 'Low', 'Adj Close', 'Volume']]
    df['HL_PCT'] = (df['High'] - df['Adj Close']) / df['Adj Close']
    df['PCT_change'] = (df['Adj Close'] - df['Open']) / df['Open']

    df_change = df[['Adj Close', 'HL_PCT', 'PCT_change', 'Volume']]

    forecast_col = 'Adj Close'

    df_change.fillna(-99999, inplace=True)

    forecast_out = 10

    df_change['label'] = df_change[forecast_col].shift(-forecast_out)
    df_change.dropna(inplace=True)
    print df_change.tail(50)

    X = np.array(df_change.drop(['label'], 1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out:]

    df_change.dropna(inplace=True)
    y = np.array(df_change['label'])
    y = np.array(df_change['label'])
    y = y[:-forecast_out]

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    clf_svm = svm.SVR(kernel='poly',degree=3)
    clf_svm.fit(X_train,y_train)
    accuracy = clf_svm.score(X_test, y_test)
    print accuracy

    clf2 = svm.SVR()
    clf2.fit(X,y)
    accuracy = clf2.score(X_test,y_test)

    model = Sequential()
    model.add(LSTM(input_dim=1,output_dim=50,return_sequences=True))
    model.add(Dropout(0.2))

    model.add((LSTM(100,return_sequences=False)))
    model.add(Dropout(0.2))

    model.add(Dense(output_dim=1))
    model.add(Activation('linear'))

    model.compile(loss='mse',optimizer='rmsprop')

    #model.fit(X_train,y_train,batch_size=512,nb_epoch=1,validation_split=0.05)

    forecast_set_linear = clf.predict(X_lately)
    forecast_set_SVR = clf_svm.predict(X_lately)
    forecast_set_rbf = clf2.predict(X_lately)
    result = []
    for i in forecast_set_linear:
        i = round(i,1)
        result.append(i)

    result2 = []
    for i in forecast_set_SVR:
        i = round(i,1)
        result2.append(i)

    result3 = []
    for i in forecast_set_rbf:
        i = round(i,1)
        result3.append(i)
    return result,result2,result3