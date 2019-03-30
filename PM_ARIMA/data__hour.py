import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller,kpss,arma_order_select_ic
import matplotlib.dates as mdates

import numpy as np
from statsmodels.tsa.arima_model import ARMA

def arma_p_q():
    data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018-9-12.csv")
    plt.plot(data1)


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white',figsize=(10,5))
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction Data')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def arma_predict(number):
    data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018.csv", index_col="date")
    dta = np.array(data1["PM2.5"], dtype=np.float)
    model = ARMA(dta, order=(2, 2)).fit(disp=0, method='css')
    predict_data = model.predict(len(data1)-number,len(data1))
    RMSE = np.sqrt(((predict_data-data1["PM2.5"][len(data1)-number-1:])**2).sum()/(number+1))
    plot_results(predict_data, data1["PM2.5"][len(data1)-number-1:])
    print(RMSE)

data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018-9-12.csv")
a=adfuller(data1["PM2.5"])
print(a)





plt.show()






