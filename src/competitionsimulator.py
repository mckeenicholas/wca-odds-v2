from abc import ABC, abstractmethod
import pandas as pd
from dbwrapper import DBWrapper


class CompetitionSimulator(ABC):

    def __init__(self, db_wrapper: DBWrapper):
        self.db_wrapper = db_wrapper

    @abstractmethod
    def prepare_data(self, data: dict[str, pd.DataFrame], halflife: str = "180 days"):
        pass

    @abstractmethod
    def run_simulation(self, count):
        pass
