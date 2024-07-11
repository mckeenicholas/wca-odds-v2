import sqlalchemy
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from dbwrapper import DBWrapper


class PSQLConnection(DBWrapper):
    """
    A class representing a PostgreSQL database connection.

    Attributes
    ----------
    engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy engine for database connection.

    Methods
    -------
    __init__(self, dbname, host='localhost', username='root', password='', connect_args={})
        Initializes a PostgreSQL connection.

    query(self, event, names, length=365)
        Executes a query to retrieve results from the database.
    """

    def __init__(
        self,
        dbname: str,
        host: str = "localhost",
        username: str = "root",
        password: str = "",
        connect_args={},
    ) -> None:
        """
        Initializes a PostgreSQL connection.

        Parameters
        ----------
        dbname : str
            The name of the database to connect to.
        host : str, optional
            The host address of the database (default is 'localhost').
        username : str, optional
            The username for database authentication (default is 'root').
        password : str, optional
            The password for database authentication (default is '').
        connect_args : dict, optional
            Additional connection arguments for SQLAlchemy engine.

        Returns
        -------
        None
        """
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{username}:{password}@{host}/{dbname}",
            connect_args=connect_args,
        )

    def query(self, event: str, names: list[str], length=365) -> dict[str, DataFrame]:
        """
        Executes a query to retrieve results from the database.

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
