import pandas_datareader as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas.plotting._converter as pandacnv
import csv
import pandas
pandacnv.register()

#to get the data


#
def to_csv(stock_num):
    start = dt.datetime.now() + dt.timedelta(-500)
    end = dt.datetime.today()
    try:
        df = web.DataReader(stock_num,'yahoo',start,end)
    except:
        row_data = 0
        date = 0
        return row_data,date
    else:
        df.to_csv('stock.csv')

        row_data = []
        with open("stock.csv", 'r') as csvfile:
            csvFileReader = csv.reader(csvfile)
            next(csvFileReader)
            for row in csvFileReader:
                data = []
                data.append(round(float(row[1]),1)) #open price
                data.append(round(float(row[5]),1)) #close price
                data.append(round(float(row[3]),1)) #high price
                data.append(round(float(row[2]),1)) #low price
                row_data.append(data)
        file = pandas.read_csv('stock.csv')
        date = []
        for i in file['Date']:
            date.append(i)
        return row_data,date

