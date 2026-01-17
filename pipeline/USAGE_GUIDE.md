# NYC Taxi Data Ingestion - Usage Guide

## Overview

The script now supports command-line arguments for flexible configuration without code changes.

## Basic Usage

### Default Parameters (2021-01)
```bash
python simple_data_ingestion.py
```

### Custom Year and Month
```bash
python simple_data_ingestion.py --year 2020 --month 6
```

### Custom Chunk Size
```bash
python simple_data_ingestion.py --chunk-size 50000
```

### Custom Table Name
```bash
python simple_data_ingestion.py --table-name my_taxi_data
```

## Database Configuration

### Command-Line Arguments
```bash
python simple_data_ingestion.py \
  --db-host localhost \
  --db-port 5432 \
  --db-user root \
  --db-password root \
  --db-name ny_taxi
```

### Environment Variables (Recommended for sensitive data)
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=root
export DB_PASSWORD=root
export DB_NAME=ny_taxi

python simple_data_ingestion.py
```

### Mix of Arguments and Environment Variables
```bash
DB_PASSWORD=secret python simple_data_ingestion.py --year 2021 --month 1
```

## Advanced Examples

### Load multiple months (script loop)
```bash
for month in {1..12}; do
  python simple_data_ingestion.py --year 2021 --month $month --table-name "yellow_taxi_2021_m$month"
done
```

### Large dataset with smaller chunks
```bash
python simple_data_ingestion.py --chunk-size 50000 --year 2019
```

### Debug mode
```bash
python simple_data_ingestion.py --log-level DEBUG
```

## Command-Line Arguments Reference

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--year` | int | 2021 | Year of taxi data (2009-2025) |
| `--month` | int | 1 | Month of taxi data (1-12) |
| `--chunk-size` | int | 100000 | Rows per chunk |
| `--table-name` | str | yellow_taxi_data | Database table name |
| `--db-host` | str | localhost | Database host (env: DB_HOST) |
| `--db-port` | str | 5432 | Database port (env: DB_PORT) |
| `--db-user` | str | root | Database user (env: DB_USER) |
| `--db-password` | str | root | Database password (env: DB_PASSWORD) |
| `--db-name` | str | ny_taxi | Database name (env: DB_NAME) |
| `--log-level` | str | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | Database host |
| `DB_PORT` | 5432 | Database port |
| `DB_USER` | root | Database user |
| `DB_PASSWORD` | root | Database password |
| `DB_NAME` | ny_taxi | Database name |

## Docker Usage

### Build Image
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY simple_data_ingestion.py .

ENTRYPOINT ["python", "simple_data_ingestion.py"]
```

### Run in Docker
```bash
docker build -t taxi-ingestion .

docker run --rm \
  -e DB_HOST=postgres \
  -e DB_USER=postgres \
  -e DB_PASSWORD=password \
  taxi-ingestion --year 2021 --month 1
```

## Best Practices Implemented

✅ **Argument Parsing**: Uses `argparse` for robust CLI handling
✅ **Type Validation**: Arguments are validated for correctness
✅ **Environment Variables**: Sensitive data via environment variables
✅ **Default Values**: Sensible defaults for all parameters
✅ **Help Text**: Detailed help with examples (`--help`)
✅ **Error Handling**: Graceful error handling with logging
✅ **Logging**: Structured logging with configurable levels
✅ **Documentation**: Help text in arguments and this guide
✅ **Flexible**: Mix CLI args with environment variables
✅ **Docker Ready**: Easy containerization

## Help

```bash
python simple_data_ingestion.py --help
```

## Error Handling

The script validates:
- Year is between 2009-2025
- Month is between 1-12
- Chunk size is positive
- Database connection is valid

All errors are logged with helpful messages.

## Performance Tips

- **Chunk Size**: Use 50k-100k for balance between memory and speed
- **Network**: Closer database = faster ingestion
- **Parallel**: Run multiple instances for different months
- **Logging**: Use INFO level in production, DEBUG for troubleshooting
