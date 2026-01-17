"""
NYC Taxi Data Ingestion Pipeline

This module ingests NYC taxi data from GitHub and loads it into a PostgreSQL database.

Example usage:
    python simple_data_ingestion.py --year 2021 --month 1 --chunk-size 100000
    python simple_data_ingestion.py --help
"""

import argparse
import logging
import os
import sys
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default Configuration
DEFAULT_CONFIG = {
    "year": 2021,
    "month": 1,
    "chunk_size": 100000,
    "table_name": "yellow_taxi_data",
    "database": {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "db": os.getenv("DB_NAME", "ny_taxi"),
        "port": os.getenv("DB_PORT", "5432"),
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


def build_database_url(db_config: dict) -> str:
    """Build PostgreSQL database URL from configuration."""
    return (
        f"postgresql://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['db']}"
    )


def build_data_url(year: int, month: int) -> str:
    """Build the data URL for NYC taxi data."""
    url_prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    return f"{url_prefix}yellow_tripdata_{year}-{month:02d}.csv.gz"


def create_table(engine, year: int, month: int, table_name: str) -> None:
    """Create an empty table in the database with the correct schema."""
    try:
        logger.info(f"Creating table '{table_name}'...")
        df_sample = pd.read_csv(
            build_data_url(year, month),
            dtype=DATA_TYPES,
            parse_dates=PARSE_DATES,
            nrows=0,
        )
        schema = pd.io.sql.get_schema(df_sample, name=table_name, con=engine)
        logger.info("Generated schema:")
        print(schema)
        df_sample.to_sql(name=table_name, con=engine, if_exists="replace")
        logger.info(f"Table '{table_name}' created successfully!")
    except Exception as e:
        logger.error(f"Error creating table: {str(e)}")
        raise


def ingest_data(engine, url: str, table_name: str, chunk_size: int) -> None:
    """Load data from CSV into the database in chunks."""
    try:
        logger.info(f"Starting data ingestion into '{table_name}'...")
        
        # Pre-scan to get total rows for progress bar
        logger.info("Scanning file for total chunk count...")
        df_preview = pd.read_csv(url, usecols=['VendorID'])
        total_rows = len(df_preview)
        total_chunks = (total_rows + chunk_size - 1) // chunk_size
        del df_preview
        logger.info(f"Total rows: {total_rows:,}, Expected chunks: {total_chunks}")
        
        # Create iterator
        df_iterator = pd.read_csv(
            url,
            dtype=DATA_TYPES,
            parse_dates=PARSE_DATES,
            iterator=True,
            chunksize=chunk_size,
        )
        
        # Custom tqdm format
        bar_format = "Inserting chunk {n_fmt}/{total_fmt} |{bar}| {percentage:.1f}% [{elapsed}<{remaining}, {rate_fmt}]"
        
        rows_inserted = 0
        for chunk_idx, chunk in enumerate(tqdm(
            df_iterator,
            desc="📊",
            unit="chunk",
            total=total_chunks,
            bar_format=bar_format,
            ncols=90
        ), 1):
            chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)
            rows_inserted += len(chunk)
            logger.debug(f"Chunk {chunk_idx}/{total_chunks}: Inserted {len(chunk)} rows")
        
        logger.info(f"Ingestion complete: {rows_inserted:,} rows inserted")
        print(f"\n✓ Data ingestion completed successfully!")
        print(f"Total rows inserted: {rows_inserted:,}")
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {str(e)}")
        raise


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Ingest NYC Taxi data from GitHub into PostgreSQL database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default parameters (2021-01)
  python simple_data_ingestion.py

  # Custom year and month
  python simple_data_ingestion.py --year 2020 --month 6

  # Custom chunk size and table name
  python simple_data_ingestion.py --chunk-size 50000 --table-name taxi_2021

  # With custom database connection
  python simple_data_ingestion.py --db-host db.example.com --db-user admin

  # Using environment variables
  DB_HOST=mydb.com DB_USER=admin python simple_data_ingestion.py
        """
    )
    
    # Data source arguments
    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_CONFIG["year"],
        help=f"Year of taxi data (default: {DEFAULT_CONFIG['year']})"
    )
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        default=DEFAULT_CONFIG["month"],
        help=f"Month of taxi data 1-12 (default: {DEFAULT_CONFIG['month']})"
    )
    
    # Performance arguments
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CONFIG["chunk_size"],
        help=f"Number of rows per chunk (default: {DEFAULT_CONFIG['chunk_size']:,})"
    )
    
    # Database arguments
    parser.add_argument(
        "--table-name",
        type=str,
        default=DEFAULT_CONFIG["table_name"],
        help=f"Database table name (default: {DEFAULT_CONFIG['table_name']})"
    )
    parser.add_argument(
        "--db-host",
        type=str,
        default=DEFAULT_CONFIG["database"]["host"],
        help=f"Database host (default: {DEFAULT_CONFIG['database']['host']}, env: DB_HOST)"
    )
    parser.add_argument(
        "--db-port",
        type=str,
        default=DEFAULT_CONFIG["database"]["port"],
        help=f"Database port (default: {DEFAULT_CONFIG['database']['port']}, env: DB_PORT)"
    )
    parser.add_argument(
        "--db-user",
        type=str,
        default=DEFAULT_CONFIG["database"]["user"],
        help=f"Database user (default: {DEFAULT_CONFIG['database']['user']}, env: DB_USER)"
    )
    parser.add_argument(
        "--db-password",
        type=str,
        default=DEFAULT_CONFIG["database"]["password"],
        help="Database password (env: DB_PASSWORD)"
    )
    parser.add_argument(
        "--db-name",
        type=str,
        default=DEFAULT_CONFIG["database"]["db"],
        help=f"Database name (default: {DEFAULT_CONFIG['database']['db']}, env: DB_NAME)"
    )
    
    # Logging arguments
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate parsed arguments."""
    if args.year < 2009 or args.year > 2025:
        logger.error("Year must be between 2009 and 2025")
        sys.exit(1)
    
    if args.chunk_size <= 0:
        logger.error("Chunk size must be positive")
        sys.exit(1)
    
    logger.info(f"Arguments validated successfully")


def main() -> None:
    """Main entry point for the data ingestion pipeline."""
    # Parse arguments
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(args.log_level)
    
    # Validate arguments
    validate_arguments(args)
    
    logger.info("Starting NYC Taxi Data Ingestion Pipeline")
    logger.info(f"Parameters: Year={args.year}, Month={args.month}, Chunk Size={args.chunk_size:,}")
    
    try:
        # Build database config from arguments
        db_config = {
            "host": args.db_host,
            "port": args.db_port,
            "user": args.db_user,
            "password": args.db_password,
            "db": args.db_name,
        }
        
        # Create database engine
        logger.info(f"Connecting to database: {db_config['host']}:{db_config['port']}")
        db_url = build_database_url(db_config)
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✓ Database connection established")
        
        # Build data URL
        data_url = build_data_url(args.year, args.month)
        logger.info(f"Data URL: {data_url}")
        
        # Create table schema
        create_table(engine, args.year, args.month, args.table_name)
        
        # Ingest data
        ingest_data(engine, data_url, args.table_name, args.chunk_size)
        
        logger.info("✓ Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()




