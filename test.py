from stonksModel import StonksPrediction

model = StonksPrediction("POOL")

model.fit(0.1, 1, 90)

model.predict()

print(model.get_metrix())

model.print_predict_with_real_data()