from abc import ABC, abstractmethod
from pandas.core.api import DataFrame as DataFrame


class DBWrapper(ABC):

    @abstractmethod
    def query(self, event: str, names: list[str], length=365) -> DataFrame:
        pass
