from dbwrapper import DBWrapper
from pandas.core.api import DataFrame as DataFrame


class CSVParser(DBWrapper):

    def __init__(self, results_path: str, comp_path) -> DataFrame:
        raise NotImplementedError

    def query(self, event: str, names: list[str], length=365) -> DataFrame:
        raise NotImplementedError
