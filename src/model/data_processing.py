import pandas as pd
from logger import logger
from sqlalchemy import create_engine
from model.database import MySQLDatabase


class DataProcesing:
    """
    Read data from MySQL database and process it
    """

    def __init__(self, db_config: dict = None, db: MySQLDatabase = None):
        """
        Initialize the class
        """
        self.db = db.db
        self.engine = create_engine(
            f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}/{db_config["db"]}',  # noqa: E501
            pool_recycle=3600,
        )

    def _get_data(self, table_name: str = None):
        """
        Get data from MySQL database

        Args:
            table_name (str): table name

        Returns:
            df (DataFrame): data frame

        """
        logger.info(
            "[DataProcessing] [_get_data]"
            f"Getting data from {table_name} table"
        )
        df = pd.read_sql(f"SELECT * FROM {table_name}", self.db)
        return df

    def process_similar_trips(self, df: pd.DataFrame = None):
        """
        This function is reponsible to answer the question:
        Trips with similar origin, destination, and time
        of day should be grouped together.
        The number of trips in each group should be counted.

        Args:
            df (DataFrame): data frame

        Returns:
            df (DataFrame): processed data frame

        """
        logger.info(
            "[DataProcessing] [process_similar_trips]"
            "Processing similar trips"
        )
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["hour"] = df["datetime"].dt.round("H").dt.hour
        df["origin_coord"] = df["origin_coord"].str.extract(
            "(\d*\.?\d+ \d*\.?\d+)"  # noqa: W605
        )
        df["destination_coord"] = df["destination_coord"].str.extract(
            "(\d*\.?\d+ \d*\.?\d+)"  # noqa: W605
        )
        df[["origin_coord_x", "origin_coord_y"]] = df[
            "origin_coord"
        ].str.split(" ", n=1, expand=True)
        df[["destination_coord_x", "destination_coord_y"]] = df[
            "destination_coord"
        ].str.split(" ", n=1, expand=True)
        df = df.astype(
            {
                "origin_coord_x": "float",
                "origin_coord_y": "float",
                "destination_coord_x": "float",
                "destination_coord_y": "float",
            }
        )
        df["origin_coord_x"] = df["origin_coord_x"].round(decimals=0)
        df["origin_coord_y"] = df["origin_coord_y"].round(decimals=0)
        df["destination_coord_x"] = df["destination_coord_x"].round(decimals=0)
        df["destination_coord_y"] = df["destination_coord_y"].round(decimals=0)
        df = df.astype(
            {
                "origin_coord_x": "str",
                "origin_coord_y": "str",
                "destination_coord_x": "str",
                "destination_coord_y": "str",
            }
        )
        df["origin_coord"] = df["origin_coord_x"].str.cat(
            df["origin_coord_y"], sep=" "
        )
        df["destination_coord"] = df["destination_coord_x"].str.cat(
            df["destination_coord_y"], sep=" "
        )
        df2 = (
            df.groupby(["origin_coord", "destination_coord", "hour"])
            .size()
            .reset_index(name="counts")
        )

        df2.to_sql(
            "similar_trips",
            con=self.engine,
            if_exists="replace",
        )
        return df2

    def weekly_trips_for_region(self, df: pd.DataFrame = None):
        """
        This function is reponsible to answer the question:
        Develop a way to obtain the weekly average number of trips
        for an area, defined by a region.

        Args:
            df (DataFrame): data frame

        Returns:
            df (DataFrame): processed data frame

        """
        logger.info(
            "[DataProcessing] [weekly_trips_for_region]"
            "Processing weekly trips for region"
        )
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["week_of_year"] = df["datetime"].dt.week
        df2 = (
            df.groupby(["region", "week_of_year"])
            .size()
            .reset_index(name="counts")
        )
        df2.to_sql(
            "weekly_trips_for_region",
            con=self.engine,
            if_exists="replace",
        )
        return df2
