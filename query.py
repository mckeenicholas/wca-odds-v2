from competitor import competitor
import sqlalchemy
import pandas as pd

num_attempts = {'333': 5,
                '555': 5}


def connect(host, username, password):
    return sqlalchemy.create_engine(f"postgresql://{username}:{password}@{host}/wca_results") 


def extract_results(engine, names: list[str], event: str, days=365, halflife='180 days'):
    query = r"""SELECT value1, value2, value3, value4, value5, TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD') AS date 
            FROM Results JOIN Competitions ON id = competitionId
            AND personId = %s AND eventId = %s AND (CURRENT_DATE - TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD')) < %s
            ORDER BY (CURRENT_DATE - TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD')) DESC;"""

    competitors = [None] * len(names)
    for i, name in enumerate(names):

        data = pd.read_sql_query(sql=query, con=engine, params=(name, event, days))

        date_label = pd.to_datetime(data.iloc[:, num_attempts[event]])
        results = data.iloc[:, :5]

        averages = results[results > 0].mean(axis=1)
        dnf_count = (results < 0).to_numpy().sum()

        dnf_rate = dnf_count / (results.shape[0] * results.shape[1])

        df = pd.Series(averages)

        weighted_series = pd.Series.ewm(df, span=averages.shape[0], times=date_label, halflife=halflife)

        comp = competitor(id=name, results=results, weighted_results=weighted_series, dnf_rate=dnf_rate)
        competitors[i] = comp

    return competitors