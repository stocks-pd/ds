import pandas as pd


class IModel:
    def get_hyperparameters(self) -> dict:
        pass

    def get_param_grid(self) -> list:
        pass

    def make_future_dataframe(self, periods: int, freq: str, include_history: bool) -> pd.DataFrame:
        pass
