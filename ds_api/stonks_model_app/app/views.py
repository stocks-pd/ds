import requests
import json
from django.utils import timezone
from django.http import HttpResponse
from ..models.api.api_model import ApiBaseStonksModel
from .models import ProphetParams
from ..app_settings import *
from django.shortcuts import render
from googletrans import Translator


def index(request):
    par = ProphetParams.objects.create()
    stocks = []
    for s in STOCKS_TIKERS[:10]:
        stock = requests.get(FMP_STOCK_INFO.format(s, FMP_KEY[FMP_KEY_INDEX])).json()
        if not stock:
            continue

        try:
            stock = stock[0]

            stocks.append(
                {'company_name': stock.get('companyName'),
                 'price': stock.get('price'),
                 'ticker': s,
                 'absolute_price_change': round(stock.get('changes'), 2),
                 'relative_price_change': round(stock.get('changes') / stock.get('price'), 2)})
        except KeyError:
            continue
    return render(request, 'list/list.html', {'stocks_table': stocks})


def detail(request, ticker):
    translator = Translator()
    ticker = ticker.upper()
    info = requests.get(FMP_STOCK_INFO.format(ticker, FMP_KEY[FMP_KEY_INDEX])).json()
    # description = translator.translate(info[0]['description'], dest='ru', src='en').text
    description = info[0]['description']
    country = info[0]['country']
    # sector = translator.translate(info[0]['sector'], dest='ru', src='en').text
    sector = info[0]['sector']
    # industry = translator.translate(info[0]['industry'], dest='ru', src='en').text
    industry = info[0]['industry']
    historical_price = requests.get(FRMP_HISTORICal_DATA.format(ticker, FMP_KEY[FMP_KEY_INDEX])).json().get(
        'historical')
    forecast, accuracy = get_predict_by_tiker(ticker, "YEAR")
    if accuracy <= 10:
        accuracy = '<span class="good_accuracy">' + str(100 - accuracy) + '%</span>'
    elif accuracy <= 30:
        accuracy = '<span class="normal_accuracy">' + str(100 - accuracy) + '%</span>'
    else:
        accuracy = '<span class="bad_accuracy">' + str(100 - accuracy) + '%</span>'
    return render(request, 'detail/detail.html', {
        'ticker': ticker,
        'description_part1': description[:500],
        'description_part2': description[500:],
        'country': country,
        'sector': sector,
        'industry': industry,
        'historical_price': historical_price,
        'forecast': forecast,
        'accuracy': accuracy
    })


def predict(request):
    ticker = request.GET.get("ticker", "").upper()
    periods = request.GET.get("periods", "").upper()
    predict = get_predict_by_tiker(ticker, periods)
    return HttpResponse(predict)


def fit(request):
    # api_model = ApiBaseStonksModel
    return HttpResponse("123")
    # model = LearnStonksModel("POOL")
    # model.get_best_prediction()
    # return HttpResponse(True)


# def update_recommendations(request):
#     url = FMP_TIKER_LABELS.format(FMP_KEY)
#     r = requests.get(url)
#     tikers = r.json()
#     predicts = []
#     for i in range(5):
#         predicts.append(get_predict_by_tiker(tikers[i], 90, True))
#     predict.sort(key=lambda l: l.get("yhat"))
#     date_time = timezone.now()
#     best_rec = Recommendations(date=date_time, **predict[0])
#     return HttpResponse(tikers)


def get_predict_by_tiker(ticker, periods, to_rec=False):
    api_model = ApiBaseStonksModel()
    params = ProphetParams.objects.latest('find_date')
    params = params.get_params()
    data = api_model.get_data_from_api(ticker, ALPHA_KEY)
    data = api_model.preprocessing(data)
    return api_model.fit_predict_transform(data, params, periods, to_rec)


def update_parameters(request):
    api_model = ApiBaseStonksModel()
    params = api_model.double_selection_hyperparameters("POOL")
    return HttpResponse(params)
