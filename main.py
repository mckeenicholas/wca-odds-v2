from csvparser import CSVParser
from request_info import get_competitors
from psqlconnection import PSQLConnection
from dbwrapper import DBWrapper
import passwords
from argparse import ArgumentParser
from competitionsimulator import CompetitionSimulator
from alphabetadist import AlphaBetaSimulation


def main():

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
        default=1000,
        type=int,
        help="Number of simulations to run",
    )
    args = parser.parse_args()

    competitors = get_competitors(args.competitionId, args.event)

    db_connection: DBWrapper
    if args.database == "psql":
        db_connection = PSQLConnection(
            dbname="wca_results",
            username=passwords.PSQL_USERNAME,
            password=passwords.PSQL_PASSWORD,
            connect_args={"options": "-csearch_path=wca_results"},
        )
    elif args.database == "python":
        raise NotImplementedError

    results_calculator: CompetitionSimulator = AlphaBetaSimulation(db_connection)
    results_calculator.prepare_data(args.event, competitors)

    results = results_calculator.run_simulation(args.num_simulations)

    print(results)


if __name__ == "__main__":
    main()
