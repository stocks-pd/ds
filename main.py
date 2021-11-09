from models.learn.learn_stonks_model import LearnStonksModel

if __name__ == '__main__':
    model = LearnStonksModel("POOL")
    model.get_best_prediction()
