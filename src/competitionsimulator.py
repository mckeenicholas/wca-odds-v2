from abc import ABC, abstractmethod
from pandas.core.api import DataFrame as DataFrame
from dbwrapper import DBWrapper


class CompetitionSimulator(ABC):
    """
    Abstract base class for simulating competition results.

    Attributes
    ----------
    db_wrapper : DBWrapper
        Database wrapper instance used for data retrieval.

    Methods
    -------
    __init__(self, db_wrapper: DBWrapper)
        Initializes the CompetitionSimulator with a database wrapper instance.

    prepare_data(self, data: dict[str, DataFrame], halflife: str = "180 days")
        Abstract method to prepare data for simulation.

    run_simulation(self, count)
        Abstract method to run the simulation for a given number of times.
    """

    def __init__(self, db_wrapper: DBWrapper):
        """
        Initializes the CompetitionSimulator with a database wrapper instance.

        Parameters
        ----------
        db_wrapper : DBWrapper
            Database wrapper instance used for data retrieval.

        Returns
        -------
        None
        """
        self.db_wrapper = db_wrapper

    @abstractmethod
    def prepare_data(self, data: dict[str, DataFrame], halflife: str = "180 days"):
        """
        Abstract method to prepare data for simulation.

        Parameters
        ----------
        data : dict[str, DataFrame]
            Dictionary mapping data keys to pandas DataFrames containing simulation data.
        halflife : str, optional
            Halflife for exponential weighted moving average (default is '180 days').

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def run_simulation(self, count):
        """
        Abstract method to run the simulation for a given number of times.

        Parameters
        ----------
        count : int
            Number of simulations to run.

        Returns
        -------
        None
        """
        pass
