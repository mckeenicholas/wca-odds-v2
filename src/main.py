# from csvparser import CSVParser
from request_info import get_competitors
from psqlconnection import PSQLConnection
from dbwrapper import DBWrapper
from argparse import ArgumentParser
from competitionsimulator import CompetitionSimulator
from alphabetadist import AlphaBetaSimulation
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    username = os.getenv("PSQL_USERNAME")
    password = os.getenv("PSQL_PASSWORD")

    parser = ArgumentParser(
        prog="WCA Odds calculator",
        description="Find a competitor's chance of winning official WCA Competitions",
    )

    parser.add_argument("competitionId")
    parser.add_argument("event")
    parser.add_argument("-d", "--database", default="psql")
    parser.add_argument(
        "-n",
        "--num_simulations",
        default=1000000,
        type=int,
        help="Number of simulations to run",
    )
    args = parser.parse_args()

    competitors = get_competitors(args.competitionId, args.event)

    db_connection: DBWrapper
    if args.database == "psql":
        db_connection = PSQLConnection(
            dbname="wca_results",
            username=username,
            password=password,
            connect_args={"options": "-csearch_path=wca_results"},
        )
    elif args.database == "python":
        raise NotImplementedError

    # del competitors[0]

    odds = True

    results_calculator: CompetitionSimulator = AlphaBetaSimulation(db_connection)
    results_calculator.prepare_data(args.event, competitors)

    results = results_calculator.run_simulation(args.num_simulations)

    max_name_length = results["name"].str.len().max() + 2
    header_name = "Name".ljust(max_name_length)

    print(f"Results for {args.event}:")
    print(f"{header_name} | Win     | Podium")
    print(f"{'-' * max_name_length} + ------- + -------")

    for _, row in results.iterrows():
        win = f"{row['win'] * 100:.2f}%" if row["win"] > 0.01 else "<0.01%"
        podium = f"{row['podium'] * 100:.2f}%" if row["podium"] > 0.01 else "<0.01%"
        name = row["name"].ljust(max_name_length)
        print(f"{name} | {win.ljust(7)} | {podium.ljust(7)}")


if __name__ == "__main__":
    main()
