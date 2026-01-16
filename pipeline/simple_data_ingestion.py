#!/usr/bin/env python
# coding: utf-8
"""
NYC Taxi Data Ingestion Pipeline

This module ingests NYC taxi data from GitHub and loads it into a PostgreSQL database.
"""

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Configuration
CONFIG = {
    "year": 2021,
    "month": 1,
    "chunk_size": 100000,
    "table_name": "yellow_taxi_data",
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "db": "ny_taxi",
        "port": "5432",
    },
}

DATA_TYPES = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

PARSE_DATES = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def build_database_url() -> str:
    """Build PostgreSQL database URL from configuration."""
    db_config = CONFIG["database"]
    return (
        f"postgresql://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['db']}"
    )


def build_data_url(year: int, month: int) -> str:
    """Build the data URL for NYC taxi data."""
    url_prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    return f"{url_prefix}yellow_tripdata_{year}-{month:02d}.csv.gz"


def create_table(engine, table_name: str) -> None:
    """Create an empty table in the database with the correct schema."""
    df_sample = pd.read_csv(
        build_data_url(CONFIG["year"], CONFIG["month"]),
        dtype=DATA_TYPES,
        parse_dates=PARSE_DATES,
        nrows=0,
    )
    schema = pd.io.sql.get_schema(df_sample, name=table_name, con=engine)
    print("Generated schema:")
    print(schema)
    df_sample.to_sql(name=table_name, con=engine, if_exists="replace")


def ingest_data(engine, url: str, table_name: str) -> None:
    """Load data from CSV into the database in chunks."""
    df_iterator = pd.read_csv(
        url,
        dtype=DATA_TYPES,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=CONFIG["chunk_size"],
    )

    for chunk in tqdm(df_iterator):
        chunk.to_sql(name=table_name, con=engine, if_exists="append")


def main() -> None:
    """Main entry point for the data ingestion pipeline."""
    # Create database engine
    db_url = build_database_url()
    engine = create_engine(db_url)

    # Build data URL
    data_url = build_data_url(CONFIG["year"], CONFIG["month"])

    # Create table schema
    create_table(engine, CONFIG["table_name"])

    # Ingest data
    ingest_data(engine, data_url, CONFIG["table_name"])

    print("Data ingestion completed successfully!")


if __name__ == "__main__":
    main()




