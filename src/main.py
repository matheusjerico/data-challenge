import uvicorn
from fastapi import FastAPI
from model.database import MySQLDatabase, insert_csv_data_into_database
from model.data_processing import DataProcesing
from utils.variables import db_config

app = FastAPI()
db = MySQLDatabase(
    db=db_config["db"],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
)
insert_csv_data_into_database(db=db)
dp = DataProcesing(db_config=db_config, db=db)


@app.get("/health")
def health_check():
    """
    Endpoint to check if the API is up and running
    """
    return {"Health Check": "ok"}


@app.get("/similar-trips")
def similar_trips():
    """
    Endpoint to calculate trips with similar origin, destination,
    and time of day should be grouped together.
    The number of trips in each group should be counted.
    """

    df = dp._get_data(table_name="trips")
    df = dp.process_similar_trips(df=df)
    return df.to_dict(orient="records")


@app.get("/weekly-trips")
def weekly_trips():
    """
    Endpoint to calculate the number of trips per week and region.
    """

    df = dp._get_data(table_name="trips")
    df = dp.weekly_trips_for_region(df=df)
    return df.to_dict(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
