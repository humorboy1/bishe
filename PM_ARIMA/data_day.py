import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller,arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
from statsmodels.tsa.arima_model import ARMA


def drop_columns(file_path):  # 删除多余的列只保留date,type,hour,chengdu这四列
    data = pd.read_csv(file_path, encoding="utf-8")
    new_data = pd.DataFrame(columns=["date", "hour", "type", "chengdu"])
    new_data["date"] = data["date"]
    new_data["hour"] = data["hour"]
    new_data["type"] = data["type"]
    new_data["chengdu"] = data["成都"]
    return new_data


def data_pro():  # 把数据转换为标准格式column为，date,PM2.5
    new_data = pd.DataFrame(columns=["date", "PM2.5"])
    file_store_path = "C:\\Users\\Administrator\\Desktop\\2018.csv"
    for i in os.listdir("C:\\Users\\Administrator\\Desktop\\pmdata\\2018"):
        # print(i)
        data = drop_columns("C:\\Users\\Administrator\\Desktop\\pmdata\\2018\\"+i)
        date_value = list(data["date"].drop_duplicates())[0]
        hour_list = list(data["hour"].drop_duplicates())
        if 23 in hour_list:
            pm_value = list(data.loc[data["type"] == "PM2.5_24h"].loc[data["hour"] == 23]['chengdu'])[0]
        elif 22 in hour_list:
            pm_value = list(data.loc[data["type"] == "PM2.5_24h"].loc[data["hour"] == 22]['chengdu'])[0]
        elif 21 in hour_list:
            pm_value = list(data.loc[data["type"] == "PM2.5_24h"].loc[data["hour"] == 21]['chengdu'])[0]
        elif 20 in hour_list:
            pm_value = list(data.loc[data["type"] == "PM2.5_24h"].loc[data["hour"] == 20]['chengdu'])[0]
        else:
            pm_value = 90
        s1 = pd.Series([date_value, pm_value], index=["date","PM2.5"])
        new_data = new_data.append(s1,ignore_index=True)
    new_data.to_csv(file_store_path,index=False)


def data_merge():  # 合并数据到一个csv里面
    dfs = []
    df1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2016.csv")
    dfs.append(df1)
    df2 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2017.csv")
    dfs.append(df2)
    df3 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018.csv")
    dfs.append(df3)
    dfs = pd.concat(dfs,ignore_index=True)
    dfs.to_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\total_data.csv", index=False)


def draw_acf_pacf():
    data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018-9-12.csv")
    data1["date"] = pd.to_datetime(data1["date"])
    xdata = data1["PM2.5"]
    f = plt.figure(facecolor='white')
    ax1 = f.add_subplot(211)
    plot_acf(xdata, lags=31, ax=ax1)
    ax2 = f.add_subplot(212)
    plot_pacf(xdata, lags=31, ax=ax2)
    plt.show()


def arma_p_q():
    data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018-9-12.csv")
    data1["date"] = pd.to_datetime(data1["date"])
    xdata = data1["PM2.5"]
    bic_matrix = []  # bic矩阵
    for p in range(5):
        tmp = []
        for q in range(5):
            try:  # 存在部分报错，所以用try来跳过报错。
                tmp.append(ARMA(xdata, (p, q)).fit().bic)
            except:
                tmp.append(None)
        bic_matrix.append(tmp)
    bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值

    p, q = bic_matrix.stack().astype('float64').idxmin()  # 先用stack展平，然后用idxmin找出最小值位置。
    print(u'BIC最小的p值和q值为：%s、%s' % (p, q))   # 这个函数的原理是，根据设定的maxLag，通过循环输入p和q值，选出拟合后BIC最小的p、q值。

    # a = arma_order_select_ic(xdata, max_ma=5, max_ar=5)  #自动选取
    # print(a.bic_min_order)
    d = adfuller(data1["PM2.5"], autolag='AIC')  #平稳性检验
    print(d)


def arma_predict_test(number):
    data1 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pmdata\\2018-9-12.csv", index_col="date")
    dta = np.array(data1["PM2.5"], dtype=np.float)
    model = ARMA(dta, order=(1, 1)).fit(disp=0, method='css')
    predict_data = model.predict(len(data1)-number,len(data1))
    RMSE = np.sqrt(((predict_data-data1["PM2.5"][len(data1)-number-1:])**2).sum()/(number+1))
    print(RMSE)
    plot_results(predict_data, data1["PM2.5"][len(data1)-number-1:])


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white',figsize=(10,5))
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction Data')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def arma_forecast(number):
    data1 = pd.read_csv("2018-9-12.csv", index_col="date")
    dta = np.array(data1["PM2.5"], dtype=np.float)
    model = ARMA(dta, order=(1, 1)).fit(disp=0, method='css')
    a=model.forecast(steps=number)
    b=[int(i) for i in a[0]]
    print(b)


arma_predict_test(50)








