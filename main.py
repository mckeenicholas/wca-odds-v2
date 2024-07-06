from simulate import run_simulations
from request_info import get_competitors
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="WCA Odds calculator",
        description="Find a competitor's chance of winning official WCA Competitions",
    )

    parser.add_argument("competitionId")
    parser.add_argument("event")

    args = parser.parse_args()

    competitors = get_competitors(args.competitionId, args.event)

    df = run_simulations(competitors)
    print(df)


if __name__ == "__main__":
    main()
