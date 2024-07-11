from argparse import ArgumentParser
from contextlib import contextmanager
from dotenv import load_dotenv
from time import perf_counter
from pandas.core.api import DataFrame as DataFrame
import os

from request_info import get_competitors
from psqlconnection import PSQLConnection
from csvparser import CSVParser
from dbwrapper import DBWrapper
from competitionsimulator import CompetitionSimulator
from alphabetadist import AlphaBetaSimulation


@contextmanager
def verbose_logging(verbose, message):
    """
    Context manager for verbose logging with timing.
    """
    if verbose:
        print(message)
        start_t = perf_counter()
    yield
    if verbose:
        end_t = perf_counter()
        print(f"Completed in {end_t - start_t:.2f} seconds")


def print_results(results: DataFrame, event: str) -> None:
    max_name_length = results["name"].str.len().max() + 2
    header_name = "Name".ljust(max_name_length)

    print(f"Results for {event}:")
    print(f"{header_name} | Win     | Podium")
    print(f"{'-' * max_name_length} + ------- + -------")

    for _, row in results.iterrows():
        win = f"{row['win'] * 100:.2f}%" if row["win"] > 0.01 else "<0.01%"
        podium = f"{row['podium'] * 100:.2f}%" if row["podium"] > 0.01 else "<0.01%"
        name = row["name"].ljust(max_name_length)
        print(f"{name} | {win.ljust(7)} | {podium.ljust(7)}")


def main():
    """
    Main function to calculate competitors' chances of winning WCA competitions.
    """

    parser = ArgumentParser(
        prog="WCA Odds Calculator",
        description="Find a competitor's chance of winning official WCA Competitions",
    )

    parser.add_argument("competitionId")
    parser.add_argument("event")
    parser.add_argument(
        "-d", "--database", default="psql", help="Database type: 'psql' or 'csv'"
    )
    parser.add_argument(
        "-n",
        "--num_simulations",
        default=1000000,
        type=int,
        help="Number of simulations to run",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    with verbose_logging(
        args.verbose, f"Getting competitor list for {args.competitionId}"
    ):
        competitors = get_competitors(args.competitionId, args.event)

    db_connection: DBWrapper
    if args.database == "psql":
        load_dotenv()
        username = os.getenv("PSQL_USERNAME")
        password = os.getenv("PSQL_PASSWORD")

        db_connection = PSQLConnection(
            dbname="wca_results",
            username=username,
            password=password,
            connect_args={"options": "-csearch_path=wca_results"},
        )
    elif args.database == "csv":
        db_connection = CSVParser()

    del competitors[0]

    results_calculator: CompetitionSimulator = AlphaBetaSimulation(db_connection)

    with verbose_logging(args.verbose, "Fetching competitor results"):
        results_calculator.prepare_data(args.event, competitors)

    with verbose_logging(args.verbose, f"Running {args.num_simulations} simulations"):
        results = results_calculator.run_simulation(args.num_simulations)

    print_results(results, args.event)


if __name__ == "__main__":
    main()
