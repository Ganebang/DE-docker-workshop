#!/bin/bash
# Example usage scripts for NYC Taxi Data Ingestion

# ============================================================
# BASIC EXAMPLES
# ============================================================

# 1. Run with defaults (2021-01, 100k chunks)
echo "Example 1: Default execution"
uv run simple_data_ingestion.py

# 2. Get help
echo "Example 2: Show help"
uv run simple_data_ingestion.py --help

# ============================================================
# CUSTOMIZING DATA SOURCE
# ============================================================

# 3. Different month
echo "Example 3: Load June 2021"
uv run simple_data_ingestion.py --month 6

# 4. Different year
echo "Example 4: Load 2020 data"
uv run simple_data_ingestion.py --year 2020

# 5. Specific year and month
echo "Example 5: Load January 2019"
uv run simple_data_ingestion.py --year 2019 --month 1

# ============================================================
# PERFORMANCE TUNING
# ============================================================

# 6. Smaller chunks (for low memory systems)
echo "Example 6: Small chunk size for 4GB RAM"
uv run simple_data_ingestion.py --chunk-size 25000

# 7. Larger chunks (for high performance)
echo "Example 7: Large chunk size for fast servers"
uv run simple_data_ingestion.py --chunk-size 200000

# ============================================================
# DATABASE CUSTOMIZATION
# ============================================================

# 8. Custom table name
echo "Example 8: Custom table name"
uv run simple_data_ingestion.py --table-name taxi_jan_2021

# 9. Different database server
echo "Example 9: Remote database"
uv run simple_data_ingestion.py \
  --db-host db.example.com \
  --db-port 5432 \
  --db-user admin

# 10. Different database credentials
echo "Example 10: Specific credentials"
uv run simple_data_ingestion.py \
  --db-user production_user \
  --db-password my_password \
  --db-name production_db

# ============================================================
# ENVIRONMENT VARIABLE EXAMPLES
# ============================================================

# 11. All parameters via environment (recommended for secrets)
echo "Example 11: Environment variables only"
export DB_HOST=db.prod.com
export DB_PORT=5432
export DB_USER=admin
export DB_PASSWORD=secure_password
export DB_NAME=production
uv run simple_data_ingestion.py --year 2021 --month 1

# 12. Mix CLI args with environment variables
echo "Example 12: Mix of CLI and environment"
DB_PASSWORD=secret uv run simple_data_ingestion.py --year 2020

# 13. Load from .env file (create manually)
echo "Example 13: Using .env file"
# First create .env file:
# cat > .env << EOF
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=root
# DB_NAME=ny_taxi
# EOF
source .env
uv run simple_data_ingestion.py --year 2021

# ============================================================
# LOGGING EXAMPLES
# ============================================================

# 14. Debug mode (verbose logging)
echo "Example 14: Debug mode"
uv run simple_data_ingestion.py --log-level DEBUG

# 15. Error only mode
echo "Example 15: Error level only"
uv run simple_data_ingestion.py --log-level ERROR

# ============================================================
# BATCH PROCESSING EXAMPLES
# ============================================================

# 16. Load entire year
echo "Example 16: Load all months of 2021"
for month in {1..12}; do
  echo "Loading month $month..."
  uv run simple_data_ingestion.py --year 2021 --month $month
done

# 17. Load multiple years
echo "Example 17: Load 2019-2021"
for year in 2019 2020 2021; do
  uv run simple_data_ingestion.py --year $year --month 1
done

# 18. Load with custom naming
echo "Example 18: Load multiple months with unique tables"
for month in 1 2 3; do
  TABLE="taxi_2021_m$(printf "%02d" $month)"
  uv run simple_data_ingestion.py --year 2021 --month $month --table-name $TABLE
done

# ============================================================
# ERROR HANDLING EXAMPLES
# ============================================================

# 19. Check exit code
echo "Example 19: Error handling"
uv run simple_data_ingestion.py --year 2025
if [ $? -eq 0 ]; then
  echo "Success!"
else
  echo "Failed! Check logs above."
fi

# 20. Retry logic
echo "Example 20: Retry on failure"
MAX_RETRIES=3
for i in $(seq 1 $MAX_RETRIES); do
  echo "Attempt $i of $MAX_RETRIES..."
  uv run simple_data_ingestion.py --year 2021 --month 1 && break
  if [ $i -lt $MAX_RETRIES ]; then
    echo "Retrying in 5 seconds..."
    sleep 5
  fi
done

# ============================================================
# PARALLEL PROCESSING EXAMPLES
# ============================================================

# 21. Parallel processing with GNU Parallel
echo "Example 21: Parallel load all months of 2021"
seq 1 12 | parallel uv run simple_data_ingestion.py --year 2021 --month {}

# 22. Parallel with xargs
echo "Example 22: Parallel with xargs"
seq 1 12 | xargs -I {} -P 4 \
  uv run simple_data_ingestion.py --year 2021 --month {}

# ============================================================
# DOCKER EXAMPLES
# ============================================================

# 23. Build Docker image
echo "Example 23: Docker build"
docker build -t taxi-ingest:latest .

# 24. Run in Docker with defaults
echo "Example 24: Docker run defaults"
docker run --rm taxi-ingest:latest

# 25. Run in Docker with args
echo "Example 25: Docker run with args"
docker run --rm taxi-ingest:latest \
  --year 2021 --month 6

# 26. Run in Docker with environment
echo "Example 26: Docker with environment"
docker run --rm \
  -e DB_HOST=postgres \
  -e DB_USER=admin \
  -e DB_PASSWORD=secret \
  taxi-ingest:latest \
  --year 2021

# 27. Docker with network
echo "Example 27: Docker with postgres service"
docker run --rm \
  --network postgres-network \
  -e DB_HOST=postgres \
  taxi-ingest:latest

# ============================================================
# KUBERNETES EXAMPLES
# ============================================================

# 28. Create Kubernetes job
echo "Example 28: Kubernetes job"
cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: taxi-ingest-2021-01
spec:
  template:
    spec:
      containers:
      - name: ingest
        image: taxi-ingest:latest
        args: ["--year", "2021", "--month", "1"]
        env:
        - name: DB_HOST
          value: postgres.default.svc.cluster.local
      restartPolicy: Never
EOF

# ============================================================
# CRON JOB EXAMPLES
# ============================================================

# 29. Cron job script
echo "Example 29: Cron job"
# Add to crontab with: crontab -e
# 0 2 5 * * cd /path/to/pipeline && uv run simple_data_ingestion.py --year $(date +\%Y) --month $(date +\%m)

# 30. Cron with logging
echo "Example 30: Cron with logging"
# 0 2 5 * * cd /path/to/pipeline && uv run simple_data_ingestion.py >> /var/log/taxi_ingest.log 2>&1

# ============================================================
# PRODUCTION EXAMPLES
# ============================================================

# 31. Production with full error handling
echo "Example 31: Production script"
#!/bin/bash
set -e  # Exit on error

LOG_DIR="/var/log/taxi-ingest"
mkdir -p "$LOG_DIR"

YEAR=$(date +%Y)
MONTH=$(date +%m)
LOG_FILE="$LOG_DIR/$YEAR-$MONTH.log"

{
  echo "Starting ingestion at $(date)"
  
  uv run simple_data_ingestion.py \
    --year "$YEAR" \
    --month "$MONTH" \
    --log-level INFO
  
  echo "Completed at $(date)"
} | tee -a "$LOG_FILE"

exit $?

# 32. Systemd service example
echo "Example 32: Systemd service"
# Save as /etc/systemd/system/taxi-ingest.service
cat <<EOF
[Unit]
Description=NYC Taxi Data Ingestion
After=network.target postgresql.service

[Service]
Type=oneshot
User=data-pipeline
WorkingDirectory=/opt/taxi-ingest
Environment="DB_HOST=localhost"
Environment="DB_USER=pipeline"
ExecStart=/usr/bin/uv run simple_data_ingestion.py

[Install]
WantedBy=multi-user.target
EOF

# 33. Systemd timer example
echo "Example 33: Systemd timer"
# Save as /etc/systemd/system/taxi-ingest.timer
cat <<EOF
[Unit]
Description=Run taxi ingestion daily

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# ============================================================
# MONITORING EXAMPLES
# ============================================================

# 34. With timestamps and monitoring
echo "Example 34: Monitoring wrapper"
START_TIME=$(date +%s)
uv run simple_data_ingestion.py --year 2021 --month 1
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Execution time: ${DURATION} seconds"

# 35. Send to monitoring service
echo "Example 35: Monitoring integration"
uv run simple_data_ingestion.py --year 2021 --month 1
EXIT_CODE=$?

# Send metric
curl -X POST http://monitoring.local/metrics \
  -d "ingestion_status=$EXIT_CODE" \
  -d "timestamp=$(date -u +%s)"

exit $EXIT_CODE

# ============================================================
# CI/CD EXAMPLES
# ============================================================

# 36. GitHub Actions example
echo "Example 36: GitHub Actions workflow"
cat <<EOF
name: Taxi Data Ingestion

on:
  schedule:
    - cron: '0 2 5 * *'  # 2 AM on 5th of month

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: uv run simple_data_ingestion.py --year 2021 --month 1
        env:
          DB_HOST: \${{ secrets.DB_HOST }}
          DB_USER: \${{ secrets.DB_USER }}
          DB_PASSWORD: \${{ secrets.DB_PASSWORD }}
EOF

# ============================================================
# NOTES
# ============================================================

# • Always use environment variables for sensitive data
# • Test with --log-level DEBUG before production
# • Monitor disk space for large ingestions
# • Consider connection pooling for concurrent runs
# • Use appropriate chunk size for your infrastructure
# • Keep logs for audit trails
# • Implement retry logic for network issues
# • Use timestamped table names for data versioning
