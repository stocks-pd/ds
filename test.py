from stonksModel import StonksPrediction

model = StonksPrediction("POOL")

model.fit(50, 0.1, 1)
print(model.get_metrix())
model.print_predict_with_real_data()
# model.get_best_prediction()
