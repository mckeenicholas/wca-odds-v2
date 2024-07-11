from dbwrapper import DBWrapper
from pandas.core.api import DataFrame as DataFrame
import pandas as pd
import os

sep = os.path.sep

JOINED_RESULTS_PATH = f"db{sep}results_dump{sep}results_joined.feather"


class CSVParser(DBWrapper):
    """
    A class implementing the DBWrapper interface for querying CSV data.

    Attributes
    ----------
    None

    Methods
    -------
    __init__(self, results_path: str=f"db{sep}results_dump{sep}Results.csv", comp_path: str=f"db{sep}results_dump{sep}Competitions.csv") -> None
        Initializes the CSVParser with paths to CSV files and updates the feather file if necessary.

    query(self, event: str, names: list[str], length: int=365) -> dict[str, DataFrame]
        Queries data from the joined feather file based on event and competitor names.

    _check_file_update(self, results_path: str, comp_path: str, feather_path: str) -> None
        Checks and updates the feather file if CSV files are modified.
    """

    def __init__(
        self,
        results_path: str = f"db{sep}results_dump{sep}Results.csv",
        comp_path: str = f"db{sep}results_dump{sep}Competitions.csv",
    ) -> None:
        """
        Initializes the CSVParser with default paths to CSV files and updates the feather file if necessary.

        Parameters
        ----------
        results_path : str, optional
            Path to the Results CSV file (default is 'db/results_dump/Results.csv').
        comp_path : str, optional
            Path to the Competitions CSV file (default is 'db/results_dump/Competitions.csv').

        Returns
        -------
        None
        """
        super().__init__()
        self._check_file_update(results_path, comp_path, JOINED_RESULTS_PATH)

    def query(
        self, event: str, names: list[str], length: int = 365
    ) -> dict[str, DataFrame]:
        """
        Queries data from the joined feather file based on event and competitor names.

        Parameters
        ----------
        event : str
            The event identifier for filtering results.
        names : list[str]
            List of person IDs to retrieve results for.
        length : int, optional
            Number of days to limit results by age (default is 365).

        Returns
        -------
        dict[str, DataFrame]
            A dictionary mapping person IDs to pandas DataFrames of query results.
        """
        try:
            results = pd.read_feather(JOINED_RESULTS_PATH)
            filtered_results = {}
            for name in names:
                res = results.query(r"eventId == @event and personId == @name")
                res = res[
                    [
                        "year",
                        "month",
                        "day",
                        "value1",
                        "value2",
                        "value3",
                        "value4",
                        "value5",
                    ]
                ]
                res["date"] = pd.to_datetime(res[["year", "month", "day"]])
                res.drop(columns=["year", "month", "day"], inplace=True)
                filtered_results[name] = res

            return filtered_results
        except Exception as e:
            print(f"Error querying data: {e}")
            return {}

    def _check_file_update(
        self, results_path: str, comp_path: str, feather_path: str
    ) -> None:
        """
        Checks and updates the feather file if the Results and Competitions CSV files are modified.

        Parameters
        ----------
        results_path : str
            Path to the Results CSV file.
        comp_path : str
            Path to the Competitions CSV file.
        feather_path : str
            Path to the joined feather file.

        Returns
        -------
        None
        """
        try:
            if os.path.exists(feather_path):
                feather_mod_time = os.path.getmtime(feather_path)
            else:
                feather_mod_time = None

            competitions_mod_time = os.path.getmtime(comp_path)
            results_mod_time = os.path.getmtime(results_path)

            if (
                feather_mod_time is None
                or competitions_mod_time > feather_mod_time
                or results_mod_time > feather_mod_time
            ):
                print("Results file out of date, updating (this could take a while)")
                competitions_df = pd.read_csv(comp_path)
                results_df = pd.read_csv(results_path)
                merged_df = pd.merge(
                    competitions_df, results_df, left_on="id", right_on="competitionId"
                )
                merged_df.to_feather(feather_path)
        except Exception as e:
            print(f"Error updating file: {e}")
