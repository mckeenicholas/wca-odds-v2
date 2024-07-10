from abc import ABC, abstractmethod
from pandas.core.api import DataFrame as DataFrame


class DBWrapper(ABC):

    @abstractmethod
    def query(self, query: str, args: tuple[str]) -> DataFrame:
        pass
