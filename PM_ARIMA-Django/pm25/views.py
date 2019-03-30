#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARMA
# Create your views here.
import json


def index(request):
    return render(request,"home.html")


def test(request, par):
    return HttpResponse(par)


def arma_forecast(request,day_num):
    data1 = pd.read_csv("pm25/2018-9-12.csv", index_col="date")
    dta = np.array(data1["PM2.5"], dtype=np.float)
    model = ARMA(dta, order=(1, 1)).fit(disp=0, method='css')
    a = model.forecast(steps=int(day_num))
    data = [int(i) for i in a[0]]
    return HttpResponse(json.dumps(data))
