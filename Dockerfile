# create docker file using python and pandas for data processing
FROM python:3.10-slim-buster

# set working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt .

# Install python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    manpages-dev \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install -r requirements.txt

# copy the source code
COPY src src
COPY data src/data

# set working directory
WORKDIR /app/src

# env var
ENV MYSQL_DATABASE="db"
ENV MYSQL_USER="user"
ENV MYSQL_PASSWORD="password"
ENV MYSQL_HOST="127.0.0.1"
ENV DATA_PATH="../data/trips.csv"

# run the command
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
