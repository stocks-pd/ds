from django.http import HttpResponse
from stonks_model.src.models.api.api_model import ApiBaseStonksModel
from .models import ProphetParam


def predict(request, tiker, periods):
    api_model = ApiBaseStonksModel()

    params = ProphetParam.objects.latest("find_date").get_params()

    data = api_model.preprocessing(api_model.get_data_from_api(tiker.upper(), api_model.api_key))

    api_model.fit(data, params)

    predict = api_model.predict(periods)

    return HttpResponse(predict)


def fit(request):
    api_model = ApiBaseStonksModel
    return HttpResponse("123")
    # model = LearnStonksModel("POOL")
    # model.get_best_prediction()
    # return HttpResponse(True)
