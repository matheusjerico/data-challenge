import os

db_config = {
    "db": os.environ.get("MYSQL_DATABASE", "db"),
    "user": os.environ.get("MYSQL_USER", "user"),
    "password": os.environ.get("MYSQL_PASSWORD", "password"),
    "host": os.environ.get("MYSQL_HOST", "localhost"),
}
