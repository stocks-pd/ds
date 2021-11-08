from models.stonksModel import StonksModel

model = StonksModel("POOL")

model.fit(150, 0.1, 1)
model.predict()
print(model.get_metrix())
# model.print_prophet_predict()
model.print_predict_with_real_data()
# model.get_best_prediction()
