import sqlalchemy
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from dbwrapper import DBWrapper


class PSQLConnection(DBWrapper):

    def __init__(
        self,
        dbname: str,
        host: str = "localhost",
        username: str = "root",
        password: str = "",
        connect_args={},
    ) -> None:
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{username}:{password}@{host}/{dbname}",
            connect_args=connect_args,
        )

    def query(self, event: str, names: list[str], length=365) -> dict[str, DataFrame]:
        query = r"""
        SELECT value1, value2, value3, value4, value5, TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD') AS date 
        FROM Results 
        JOIN Competitions ON id = competitionId
        WHERE personId = %s AND eventId = %s AND (CURRENT_DATE - TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD')) < %s
        ORDER BY (CURRENT_DATE - TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD')) DESC;
        """

        results = {}

        for id in names:
            results[id] = pd.read_sql_query(
                sql=query, con=self.engine, params=(id, event, length)
            )

        return results
