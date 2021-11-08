from models.stonksModel import StonksModel



# model.fit(150, 1, 1, 3)
# model.predict(252)
# print(model.get_metrix())
# model.print_predict_with_real_data()
if __name__ == '__main__':
    model = StonksModel("POOL")
    model.get_best_prediction()





