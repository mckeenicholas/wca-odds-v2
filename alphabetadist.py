from threading import Thread
import numpy as np
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from competitionsimulator import CompetitionSimulator
from competitor import Competitor
from formats import event_formats


class AlphaBetaSimulation(CompetitionSimulator):

    def __init__(self, db_wrapper):
        CompetitionSimulator.__init__(self, db_wrapper)
        self.competitors = []
        self.event = None

    def prepare_data(
        self, event: str, competitors: list[str], halflife: str = "180 days"
    ):
        self.competitors = []
        self.event = event

        data = self.db_wrapper.query(event, competitors)
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
                results=results,
                weighted_results=weighted_series,
                dnf_rate=dnf_rate,
            )

            self.competitors.append(competitor)

    def run_simulation(self, count: int):
        num_competitors = len(self.competitors)

        threads = [
            Thread(target=self._simulation_thread, args=(competitor, count, True))
            for competitor in self.competitors
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        all_results = np.stack([c.generated_results for c in self.competitors])

        sorted_indices = np.argsort(all_results, axis=0)

        win_indices = sorted_indices[0, :]
        podium_indices = sorted_indices[: min(num_competitors, 3), :].flat

        win_by_person = np.bincount(win_indices, minlength=num_competitors)
        podium_by_person = np.bincount(podium_indices, minlength=num_competitors)

        competitor_ids = [competitor.id for competitor in self.competitors]

        data = {
            "id": competitor_ids,
            "win": win_by_person / count,
            "podium": podium_by_person / count,
        }

        return pd.DataFrame(data).sort_values(by="win", ascending=False)

    def _simulation_thread(self, competitor, count: int, use_dnf=False):
        mean = competitor.weighted_results.mean().iloc[-1]
        stdev = competitor.weighted_results.std().iloc[-1]

        shape = (mean**2) / (stdev**2)
        scale = (stdev**2) / mean

        num_attempts = event_formats[self.event]["num_attempts"]
        format = event_formats[self.event]["default_format"]

        random_values = np.random.gamma(shape, scale, (count, num_attempts)).astype(int)

        if use_dnf:
            mask = np.random.rand(*random_values.shape)
            replace_indices = np.where(mask < competitor.dnf_rate)

            random_values[replace_indices] = np.iinfo(np.int32).max

        sorted_by_instance = np.sort(random_values, axis=1)

        if format == "a":
            trimmed = sorted_by_instance[:, 1:4]
            results = np.mean(trimmed, axis=1)
        elif format == "m":
            results = np.mean(sorted_by_instance, axis=1)
        else:
            results = sorted_by_instance[:, 0]

        competitor.generated_results = results
