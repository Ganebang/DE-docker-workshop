"""
Comprehensive test suite for NYC Taxi Data Ingestion Pipeline

Tests cover:
- Argument parsing and validation
- Database URL construction
- Data URL generation
- Configuration management
- Error handling
"""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

# Add pipeline directory to path
pipeline_dir = Path(__file__).parent.parent / "pipeline"
sys.path.insert(0, str(pipeline_dir))

from simple_data_ingestion import (
    build_database_url,
    build_data_url,
    parse_arguments,
    validate_arguments,
    DEFAULT_CONFIG,
    DATA_TYPES,
    PARSE_DATES,
)


class TestDatabaseURLConstruction:
    """Test database URL building"""

    def test_build_database_url_basic(self):
        """Test building database URL with basic config"""
        db_config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": "5432",
            "db": "ny_taxi"
        }
        url = build_database_url(db_config)
        assert url == "postgresql://root:root@localhost:5432/ny_taxi"

    def test_build_database_url_remote(self):
        """Test building database URL with remote host"""
        db_config = {
            "user": "admin",
            "password": "secure_pass",
            "host": "db.prod.example.com",
            "port": "5432",
            "db": "production_db"
        }
        url = build_database_url(db_config)
        assert url == "postgresql://admin:secure_pass@db.prod.example.com:5432/production_db"

    def test_build_database_url_special_characters(self):
        """Test building database URL with special characters in password"""
        db_config = {
            "user": "user",
            "password": "p@ssw0rd!",
            "host": "localhost",
            "port": "5432",
            "db": "testdb"
        }
        url = build_database_url(db_config)
        assert "p@ssw0rd!" in url
        assert "postgresql://" in url

    def test_build_database_url_custom_port(self):
        """Test building database URL with custom port"""
        db_config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": "5433",
            "db": "ny_taxi"
        }
        url = build_database_url(db_config)
        assert "5433" in url
        assert "postgresql://" in url


class TestDataURLGeneration:
    """Test data URL generation for various scenarios"""

    def test_build_data_url_2021_january(self):
        """Test building data URL for 2021-01"""
        url = build_data_url(2021, 1)
        assert "yellow_tripdata_2021-01.csv.gz" in url
        assert "https://github.com/DataTalksClub/nyc-tlc-data" in url

    def test_build_data_url_2020_december(self):
        """Test building data URL for 2020-12"""
        url = build_data_url(2020, 12)
        assert "yellow_tripdata_2020-12.csv.gz" in url

    def test_build_data_url_format(self):
        """Test data URL format with various dates"""
        test_cases = [
            (2021, 1, "yellow_tripdata_2021-01.csv.gz"),
            (2020, 6, "yellow_tripdata_2020-06.csv.gz"),
            (2019, 12, "yellow_tripdata_2019-12.csv.gz"),
        ]
        for year, month, expected_filename in test_cases:
            url = build_data_url(year, month)
            assert expected_filename in url

    def test_github_release_url_format(self):
        """Test that GitHub release URLs are correctly formatted"""
        url = build_data_url(2021, 1)
        assert url.startswith("https://")
        assert "github.com" in url
        assert "releases/download" in url
        assert "yellow_tripdata_2021-01.csv.gz" in url

    def test_all_months_url_generation(self):
        """Test URL generation for all months"""
        year = 2021
        for month in range(1, 13):
            url = build_data_url(year, month)
            filename = f"yellow_tripdata_{year}-{month:02d}.csv.gz"
            assert filename in url

    def test_historical_year_url_generation(self):
        """Test URL generation for historical years"""
        test_years = [2009, 2015, 2020, 2025]
        for year in test_years:
            url = build_data_url(year, 6)
            assert f"yellow_tripdata_{year}-06.csv.gz" in url


class TestArgumentValidation:
    """Test argument validation"""

    def test_validate_year_valid_range(self):
        """Test year validation with valid range"""
        args = Mock(year=2015, month=6, chunk_size=100000, log_level="INFO")
        validate_arguments(args)

    def test_validate_year_too_early(self):
        """Test year validation with year before 2009"""
        args = Mock(year=2008, month=6, chunk_size=100000, log_level="INFO")
        with pytest.raises(SystemExit):
            validate_arguments(args)

    def test_validate_year_too_late(self):
        """Test year validation with year after 2025"""
        args = Mock(year=2026, month=6, chunk_size=100000, log_level="INFO")
        with pytest.raises(SystemExit):
            validate_arguments(args)

    def test_validate_chunk_size_valid(self):
        """Test chunk size validation with valid values"""
        for size in [1000, 50000, 100000, 500000]:
            args = Mock(year=2020, month=6, chunk_size=size, log_level="INFO")
            validate_arguments(args)

    def test_validate_chunk_size_invalid_zero(self):
        """Test chunk size validation with zero"""
        args = Mock(year=2020, month=6, chunk_size=0, log_level="INFO")
        with pytest.raises(SystemExit):
            validate_arguments(args)

    def test_validate_chunk_size_invalid_negative(self):
        """Test chunk size validation with negative value"""
        args = Mock(year=2020, month=6, chunk_size=-1000, log_level="INFO")
        with pytest.raises(SystemExit):
            validate_arguments(args)

    def test_boundary_year_2009(self):
        """Test year boundary at 2009"""
        args = Mock(year=2009, month=1, chunk_size=100000, log_level="INFO")
        validate_arguments(args)

    def test_boundary_year_2025(self):
        """Test year boundary at 2025"""
        args = Mock(year=2025, month=1, chunk_size=100000, log_level="INFO")
        validate_arguments(args)


class TestArgumentParsing:
    """Test command-line argument parsing"""

    @patch('sys.argv', ['script'])
    def test_parse_arguments_defaults(self):
        """Test argument parsing with default values"""
        args = parse_arguments()
        assert args.year == 2021
        assert args.month == 1
        assert args.chunk_size == 100000
        assert args.table_name == "yellow_taxi_data"
        assert args.log_level == "INFO"

    @patch('sys.argv', ['script', '--year', '2020', '--month', '6', '--chunk-size', '50000', '--table-name', 'custom_table'])
    def test_parse_arguments_custom_values(self):
        """Test argument parsing with custom values"""
        args = parse_arguments()
        assert args.year == 2020
        assert args.month == 6
        assert args.chunk_size == 50000
        assert args.table_name == "custom_table"

    @patch('sys.argv', ['script', '--log-level', 'DEBUG'])
    def test_parse_arguments_log_level_debug(self):
        """Test parsing DEBUG log level"""
        args = parse_arguments()
        assert args.log_level == "DEBUG"

    @patch('sys.argv', ['script', '--log-level', 'ERROR'])
    def test_parse_arguments_log_level_error(self):
        """Test parsing ERROR log level"""
        args = parse_arguments()
        assert args.log_level == "ERROR"

    @patch('sys.argv', ['script', '--log-level', 'WARNING'])
    def test_parse_arguments_log_level_warning(self):
        """Test parsing WARNING log level"""
        args = parse_arguments()
        assert args.log_level == "WARNING"

    @patch('sys.argv', ['script', '--help'])
    def test_parse_arguments_help(self):
        """Test help argument"""
        with pytest.raises(SystemExit) as exc_info:
            parse_arguments()
        assert exc_info.value.code == 0

    @patch('sys.argv', ['script', '--invalid-arg', 'value'])
    def test_parse_arguments_invalid_argument(self):
        """Test parsing with invalid argument"""
        with pytest.raises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['script', '--year', 'invalid'])
    def test_invalid_year_type(self):
        """Test handling of invalid year type"""
        with pytest.raises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['script', '--chunk-size', 'invalid'])
    def test_invalid_chunk_size_type(self):
        """Test handling of invalid chunk size type"""
        with pytest.raises(SystemExit):
            parse_arguments()


class TestConfigurationDefaults:
    """Test default configuration values"""

    def test_default_config_structure(self):
        """Test default configuration structure"""
        assert "year" in DEFAULT_CONFIG
        assert "month" in DEFAULT_CONFIG
        assert "chunk_size" in DEFAULT_CONFIG
        assert "table_name" in DEFAULT_CONFIG
        assert "database" in DEFAULT_CONFIG

    def test_database_config_keys(self):
        """Test database configuration has required keys"""
        db_config = DEFAULT_CONFIG["database"]
        required_keys = ["host", "user", "password", "db", "port"]
        for key in required_keys:
            assert key in db_config

    def test_default_values_are_reasonable(self):
        """Test that default values are reasonable"""
        assert 2009 <= DEFAULT_CONFIG["year"] <= 2025
        assert 1 <= DEFAULT_CONFIG["month"] <= 12
        assert DEFAULT_CONFIG["chunk_size"] > 0
        assert len(DEFAULT_CONFIG["table_name"]) > 0


class TestDataConfiguration:
    """Test data type and parsing configurations"""

    def test_data_types_configuration(self):
        """Test that data types are properly configured"""
        required_columns = [
            "VendorID", "passenger_count", "trip_distance",
            "RatecodeID", "store_and_fwd_flag", "PULocationID",
            "DOLocationID", "payment_type", "fare_amount"
        ]
        for col in required_columns:
            assert col in DATA_TYPES

    def test_parse_dates_configuration(self):
        """Test that parse_dates configuration is correct"""
        assert "tpep_pickup_datetime" in PARSE_DATES
        assert "tpep_dropoff_datetime" in PARSE_DATES
        assert len(PARSE_DATES) == 2

    def test_data_types_have_valid_types(self):
        """Test that all data types are valid pandas types"""
        valid_dtypes = ["Int64", "float64", "string"]
        for dtype in DATA_TYPES.values():
            assert dtype in valid_dtypes


class TestIntegration:
    """Integration tests combining multiple components"""

    @patch('sys.argv', ['script', '--year', '2021', '--month', '3', '--chunk-size', '50000'])
    def test_valid_configuration_flow(self):
        """Test a complete valid configuration flow"""
        args = parse_arguments()
        validate_arguments(args)
        
        db_config = {
            "user": args.db_user,
            "password": args.db_password,
            "host": args.db_host,
            "port": args.db_port,
            "db": args.db_name
        }
        
        db_url = build_database_url(db_config)
        data_url = build_data_url(args.year, args.month)
        
        assert "postgresql://" in db_url
        assert "yellow_tripdata_2021-03.csv.gz" in data_url

    @patch('sys.argv', ['script', '--year', '2030'])
    def test_error_in_validation(self):
        """Test that validation errors are caught"""
        args = parse_arguments()
        with pytest.raises(SystemExit):
            validate_arguments(args)

    def test_multiple_months_data_urls(self):
        """Test data URL generation for multiple months"""
        months_to_process = [1, 6, 12]
        year = 2021
        
        for month in months_to_process:
            url = build_data_url(year, month)
            assert f"yellow_tripdata_{year}-{month:02d}.csv.gz" in url

    def test_full_year_processing(self):
        """Test that we can process all 12 months of a year"""
        year = 2021
        for month in range(1, 13):
            url = build_data_url(year, month)
            assert "yellow_tripdata" in url
            assert ".csv.gz" in url


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_chunk_size_boundary_one(self):
        """Test with chunk size of 1 (smallest possible)"""
        args = Mock(year=2020, month=6, chunk_size=1, log_level="INFO")
        validate_arguments(args)

    def test_chunk_size_large(self):
        """Test with very large chunk size"""
        args = Mock(year=2020, month=6, chunk_size=10000000, log_level="INFO")
        validate_arguments(args)

    @patch('sys.argv', ['script', '--month', '1'])
    def test_january_parsing(self):
        """Test parsing January (month 1)"""
        args = parse_arguments()
        assert args.month == 1

    @patch('sys.argv', ['script', '--month', '12'])
    def test_december_parsing(self):
        """Test parsing December (month 12)"""
        args = parse_arguments()
        assert args.month == 12


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
