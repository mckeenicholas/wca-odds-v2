from threading import Thread
from multiprocessing import Pool
import numpy as np
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from competitionsimulator import CompetitionSimulator
from competitor import Competitor
from formats import event_formats
from time import perf_counter
from multi_sim import multi_simulation_thread


class AlphaBetaSimulation(CompetitionSimulator):

    def __init__(self, db_wrapper):
        CompetitionSimulator.__init__(self, db_wrapper)
        self.competitors = []
        self.event = None

    def prepare_data(
        self, event: str, competitors: list[dict[str, str]], halflife: str = "180 days"
    ):
        self.competitors = []
        self.event = event

        name_mappings = {i["id"]: i["name"] for i in competitors}

        data = self.db_wrapper.query(event, name_mappings.keys())
        num_attempts = event_formats[self.event]["num_attempts"]

        for id, df in data.items():
            date_label = pd.to_datetime(df.iloc[:, num_attempts])
            results = df.iloc[:, :5]

            total_attempts = results.shape[0] * results.shape[1]

            if total_attempts == 0:
                continue

            averages = results[results > 0].mean(axis=1)
            dnf_count = (results < 0).to_numpy().sum()
            dnf_rate = 0 if total_attempts == 0 else dnf_count / total_attempts
            df = pd.Series(averages)

            weighted_series = pd.Series.ewm(
                df, span=averages.shape[0], times=date_label, halflife=halflife
            )

            competitor = Competitor(
                id=id,
                name=name_mappings[id],
                results=results,
                weighted_results=weighted_series,
                dnf_rate=dnf_rate,
            )

            self.competitors.append(competitor)

    def run_simulation(self, count: int):
        start_t = perf_counter()
        num_competitors = len(self.competitors)

        args = [
            (comp.weighted_results, comp.dnf_rate, self.event, count)
            for comp in self.competitors
        ]

        with Pool() as pool:
            results = pool.starmap(multi_simulation_thread, args)

            all_results = np.stack([result for result in results])

        sorted_indices = np.argsort(all_results, axis=0)

        win_indices = sorted_indices[0, :]
        podium_indices = sorted_indices[: min(num_competitors, 3), :].flat

        win_by_person = np.bincount(win_indices, minlength=num_competitors)
        podium_by_person = np.bincount(podium_indices, minlength=num_competitors)

        competitor_names = [competitor.name for competitor in self.competitors]

        data = {
            "name": competitor_names,
            "win": win_by_person / count,
            "podium": podium_by_person / count,
        }

        end_t = perf_counter()

        print(f"Comleted {count} simulations in {end_t-start_t:2f} seconds")

        return pd.DataFrame(data).sort_values(by="win", ascending=False)
