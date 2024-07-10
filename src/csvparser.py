from dbwrapper import DBWrapper
from pandas.core.api import DataFrame as DataFrame
import pandas as pd
import os

JOINED_RESULTS_PATH = "db/results_dump/results_joined.feather"

class CSVParser(DBWrapper):

    def __init__(self, results_path: str="db/results_dump/Results.csv", comp_path="db/results_dump/Competitions.csv") -> DataFrame:
        self._check_file_update(results_path, comp_path, JOINED_RESULTS_PATH)

    def query(self, event: str, names: list[str], length=365) -> dict[str, DataFrame]:
        results = pd.read_feather(JOINED_RESULTS_PATH)
        filtered_results = {}
        for name in names:
            res = results.query(r"eventId == @event and personId == @name")
            res = res[['year', 'month', 'day', 'value1', 'value2', 'value3', 'value4', 'value5']]
            res['date'] = pd.to_datetime(res[['year', 'month', 'day']]) 
            res.drop(columns=['year', 'month', 'day'], inplace=True)
            
            filtered_results[name] = res

        return filtered_results

    def _check_file_update(self, results: str, comp: str, feather: str):
        if os.path.exists(feather):
            feather_mod_time = os.path.getmtime(feather)
        else:
            feather_mod_time = None

        competitions_mod_time = os.path.getmtime(comp)
        results_mod_time = os.path.getmtime(results)

        if feather_mod_time is None or competitions_mod_time > feather_mod_time or results_mod_time > feather_mod_time:
            print(f"Results file out of date, updating (this could take a while)")
            competitions_df = pd.read_csv(comp)
            results_df = pd.read_csv(results)

            merged_df = pd.merge(competitions_df, results_df, left_on="id", right_on="competitionId")
            merged_df.to_feather(feather)
            