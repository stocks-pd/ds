import pandas as pd


class IModel:
    def get_hyperparameters(self) -> dict:
        pass

    @staticmethod
    def get_param_grid(estimators_dict: dict, train_data: pd.DataFrame, test_data: pd.DataFrame) -> list:
        pass

    def make_future_dataframe(self, periods: int, freq: str, include_history: bool) -> pd.DataFrame:
        pass
