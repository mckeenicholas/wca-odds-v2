from abc import ABC, abstractmethod
from pandas.core.api import DataFrame as DataFrame


class DBWrapper(ABC):
    """
    Abstract base class for database wrappers.

    Defines the interface for querying data from a database.

    Attributes
    ----------
    None

    Methods
    -------
    query(query: str, args: tuple[str]) -> DataFrame
        Abstract method to execute a query and return results as a pandas DataFrame.
    """

    @abstractmethod
    def query(self, query: str, args: tuple[str]) -> DataFrame:
        """
        Execute a query and return results as a pandas DataFrame.

        Parameters
        ----------
        query : str
            SQL query to execute.
        args : tuple[str]
            Arguments to pass to the query.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the query results.
        """
        pass
