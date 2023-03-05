import pymysql
import csv
from logger import logger
import os


class MySQLDatabase:
    """Database class"""

    def __init__(
        self,
        host: str = None,
        user: str = None,
        password: str = None,
        db: str = None,
    ):
        """
        Initialize database connection

        Args:
            host (str): host name
            user (str): user name
            password (str): password
            db (str): database name

        Returns:
            None

        """
        logger.info(
            "Initializing database connection"
            f"host={host}, user={user}, password={password}, db={db}"
        )
        self.db = pymysql.connect(
            host=host, user=user, password=password, db=db
        )
        self.cursor = self.db.cursor()

    def create_table_trips(self):
        """Create table trips"""

        self.cursor.execute("DROP TABLE IF EXISTS trips")
        self.cursor.execute(
            "CREATE TABLE trips(region VARCHAR(255), origin_coord VARCHAR(255), destination_coord VARCHAR(255), datetime VARCHAR(255), datasource VARCHAR(255))"  # noqa: E501
        )

    def insert_data_trips(self, csv_file: str):
        """
        Insert data into table trips

        Args:
            csv_file (str): csv file path

        Returns:
            None

        """

        csv_data = csv.reader(open(csv_file))
        next(csv_data)
        for row in csv_data:
            self.cursor.execute(
                "INSERT INTO trips(region,origin_coord,destination_coord,datetime,datasource) VALUES(%s, %s, %s, %s, %s)",  # noqa: E501
                row,
            )

        self.db.commit()
        self.cursor.close()


def insert_csv_data_into_database(db: MySQLDatabase):
    """
    This function is used to insert CSV file into MYSQL database
    """
    logger.info("Inserting data into database")
    db.create_table_trips()
    db.insert_data_trips(
        csv_file=os.environ.get("DATA_PATH", "../data/trips.csv")
    )
