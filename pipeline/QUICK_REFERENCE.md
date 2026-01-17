# Quick Reference - NYC Taxi Data Ingestion

## Most Common Commands

```bash
# Default (2021-01, 100k chunks)
uv run simple_data_ingestion.py

# Different month
uv run simple_data_ingestion.py --month 6

# Different year
uv run simple_data_ingestion.py --year 2020

# Year + Month
uv run simple_data_ingestion.py --year 2020 --month 3

# Smaller chunks (for low memory)
uv run simple_data_ingestion.py --chunk-size 50000

# Custom database
uv run simple_data_ingestion.py --db-host db.company.com --db-user admin

# Debug mode
uv run simple_data_ingestion.py --log-level DEBUG

# Custom table name
uv run simple_data_ingestion.py --table-name taxi_jan_2021
```

## Environment Variable Mode (Best Practice)

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=root
export DB_PASSWORD=root
export DB_NAME=ny_taxi

uv run simple_data_ingestion.py --year 2021 --month 1
```

## Docker Examples

```bash
# Build
docker build -t taxi-ingest .

# Run with default settings
docker run taxi-ingest

# Run with custom parameters
docker run taxi-ingest --year 2020 --month 6

# Run with environment variables
docker run \
  -e DB_HOST=postgres \
  -e DB_USER=admin \
  -e DB_PASSWORD=secret \
  taxi-ingest
```

## In Python Scripts

```python
import subprocess
import sys

years = [2020, 2021, 2022]
for year in years:
    cmd = [
        sys.executable,
        "simple_data_ingestion.py",
        "--year", str(year),
        "--log-level", "INFO"
    ]
    result = subprocess.run(cmd, cwd="/path/to/pipeline")
    if result.returncode != 0:
        print(f"Failed for year {year}")
```

## Cron Job Example

```bash
# Ingest data monthly on the 5th day
# Add to crontab: crontab -e

0 2 5 * * cd /workspaces/DE-docker-workshop/pipeline && \
  DB_HOST=db.prod.com DB_USER=admin DB_PASSWORD=$DB_PASS \
  uv run simple_data_ingestion.py --year $(date +\%Y) --month $(date +\%m)
```

## Kubernetes Example

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: taxi-data-ingest
spec:
  schedule: "0 2 5 * *"  # 2 AM on 5th of month
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: ingest
            image: taxi-ingest:latest
            args: ["--year", "2021", "--month", "1"]
            env:
            - name: DB_HOST
              value: postgres.prod.svc.cluster.local
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
          restartPolicy: OnFailure
```

## Return Codes

- `0` - Success
- `1` - Error (check logs)

## Getting Help

```bash
uv run simple_data_ingestion.py --help
```
