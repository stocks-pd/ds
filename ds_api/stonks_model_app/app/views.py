import requests
from django.utils import timezone
from django.http import HttpResponse
from ..models.api.api_model import ApiBaseStonksModel
from .models import ProphetParam, Recommendations
from ..app_settings import *
from django.shortcuts import render
import pandas as pd


def index(request):
    stock_tikers = requests.get(FMP_TIKER_LABELS.format(FMP_KEY[2])).json()
    stocks = []
    for s in stock_tikers[:10]:
        stock = requests.get(FMP_STOCK_INFO.format(s, FMP_KEY[2])).json()
        if not stock:
            continue
        stock = stock[0]
        company_name = stock.get('companyName')[:18] + "..." if len(stock.get('companyName')) > 21 else stock.get(
            'companyName')
        stocks.append(
            {'url': stock.get('image'), 'company_name': company_name, 'price': stock.get('price'), 'tiker': s,
             'absolute_price_change': round(stock.get('changes'), 2),
             'relative_price_change': round(stock.get('changes') / stock.get('price'), 2)})
    return render(request, 'main/detail_with_list.html', {'stocks': stocks})


def predict(request, tiker, periods):
    predict = get_predict_by_tiker(tiker, periods)
    return HttpResponse(predict)


def fit(request):
    # api_model = ApiBaseStonksModel
    return HttpResponse("123")
    # model = LearnStonksModel("POOL")
    # model.get_best_prediction()
    # return HttpResponse(True)


def update_recommendations(request):
    url = FMP_TIKER_LABELS.format(FMP_KEY)
    r = requests.get(url)
    tikers = r.json()
    predicts = []
    for i in range(5):
        predicts.append(get_predict_by_tiker(tikers[i], 90, True))
    predict.sort(key=lambda l: l.get("yhat"))
    date_time = timezone.now()
    best_rec = Recommendations(date=date_time, **predict[0])
    return HttpResponse(tikers)


def get_predict_by_tiker(tiker, periods, to_rec=False):
    api_model = ApiBaseStonksModel()
    params = ProphetParam.objects.latest("find_date").get_params()
    data = api_model.preprocessing(api_model.get_data_from_api(tiker.upper(), api_model.api_key))
    return api_model.fit_predict_transform(data, params, periods, to_rec)


def update_parameters(request):
    api_model = ApiBaseStonksModel()
    params = api_model.double_selection_hyperparameters("POOL")
    print(params)
    return HttpResponse(params)
