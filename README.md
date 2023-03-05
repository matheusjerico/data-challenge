# Data Challenge for JobSity - Data Enginner

The description for this data challange can be found [here](https://www.github.com/matheusjerico/data-challenge). Is a PDF file.

## Mandatory Features

- [DONE] There must be an automated process to ingest and store the data.
    - When the API start, it will load CSV file into MySQL database.
- [DONE] Trips with similar origin, destination, and time of day should be grouped together.
    - The API will group trips by origin, destination and time of day. Return the data as a dictionary and save It as `similar_trips` table into MySQL database. Endpoint `similar-trips`
- [DONE] Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box(given by coordinates) or by a region.
    - The API will return the weekly average number of trips for an area, defined by a bounding box or by a region. Return the data as a dictionary and save It as `weekly_trips_for_region` table into MySQL database. Endpoint `weekly-trips`
- [NOT DONE] Develop a way to inform the user about the status of the data ingestion without using a
polling solution.
- [DONE] Use a SQL database.

## Bonus features

- [DONE] Containerize your solution.
- [NOT DONE] Sketch up how you would set up the application using any cloud provider (AWS, Google
Cloud, etc).
- [DONE] Include a .sql file with queries to answer these questions:
    - From the two most commonly appearing regions, which is the latest datasource? (`sql/question_01.sql`)
    - What regions has the "cheap_mobile" datasource appeared in? (`sql/question_02.sql`)

## How to run

Use `Makefile` to run the project.

```bash
make docker-compose-up
```

## API Docs
We are using FastAPI to create the API. The docs can be found [here](http://localhost:8000/docs).

## API Endpoints
The API has two endpoints:
- `similar-trips`
- `weekly-trips`

## 🍜 License

[MIT](https://choosealicense.com/licenses/mit/).<br>
