from django.http import HttpResponse
from stonks_model.src.models.api.api_model import ApiStonksModel
from .models import ProphetParam


def predict(request, tiker, periods):
    api_model = ApiStonksModel(tiker)
    params = ProphetParam.objects.latest("find_date").get_params()
    api_model.fit(params)
    predict = api_model.predict(periods)
    return HttpResponse(predict)


def fit(request):
    api_model = ApiStonksModel
    return HttpResponse("123")
    # model = LearnStonksModel("POOL")
    # model.get_best_prediction()
    # return HttpResponse(True)
