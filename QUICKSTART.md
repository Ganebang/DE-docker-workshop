# Quick Start Guide - NYC Taxi Pipeline

## 🚀 Get Running in 5 Minutes

### Option 1: Docker Compose (Easiest) ⭐ Recommended

```bash
# Start database and pipeline
docker-compose up -d

# Run pipeline (ingest 2021-01 data)
docker-compose run pipeline uv run simple_data_ingestion.py --year 2021 --month 1

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Manual Docker Commands

```bash
# Terminal 1: Create network and start database
docker network create taxi-network

docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# Wait 5 seconds for database to be ready
sleep 5

# Terminal 2: Build and run pipeline
cd pipeline
docker build -t taxi-pipeline .

docker run -it \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline --year 2021 --month 1

# Terminal 3: Verify data (optional)
docker exec postgres-db psql -U root -d ny_taxi -c "SELECT COUNT(*) FROM yellow_taxi_data;"
```

### Option 3: Local Development

```bash
# Start database only
docker run -d \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# Install dependencies
cd pipeline
uv sync

# Run pipeline
uv run simple_data_ingestion.py --year 2021 --month 1
```

---

## 📋 Common Commands

```bash
# View all available arguments
docker-compose run pipeline uv run simple_data_ingestion.py --help

# Ingest different months
docker-compose run pipeline uv run simple_data_ingestion.py --year 2020 --month 6

# Debug mode (verbose logging)
docker-compose run pipeline uv run simple_data_ingestion.py --log-level DEBUG

# Check database contents
docker-compose exec database psql -U root -d ny_taxi -c "SELECT COUNT(*) FROM yellow_taxi_data;"

# View container logs
docker-compose logs database
docker-compose logs pipeline

# Clean up everything
docker-compose down -v
```

---

## 🔍 Verify Everything Works

```bash
# 1. Start services
docker-compose up -d

# 2. Check database is ready
docker-compose ps

# 3. Run pipeline
docker-compose run pipeline uv run simple_data_ingestion.py --year 2021 --month 1

# 4. Verify data
docker-compose exec database psql -U root -d ny_taxi \
  -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"

# Expected output should show: yellow_taxi_data table
```

---

## 🛠️ Troubleshooting

### Port 5432 already in use?
```bash
docker-compose down
# or change port in docker-compose.yml: "5433:5432"
```

### Database connection failed?
```bash
# Check if database container is healthy
docker-compose ps

# Check logs
docker-compose logs database

# Wait a bit longer for database to start
sleep 10
```

### Out of disk space?
```bash
# Clean up Docker volumes
docker volume prune -f

# Remove old data
rm -rf ny_taxi_postgres_data
```

---

## 📚 For More Information

See [README.md](README.md) for comprehensive documentation including:
- Complete installation guide
- Database management
- Pipeline CLI arguments
- Docker networking details
- Advanced examples
- Troubleshooting guide

---

**Quick Links:**
- 📖 [Main README](README.md) - Full documentation
- 🚀 [CLI Reference](pipeline/README_CLI.md) - All command-line arguments
- 💡 [Examples](pipeline/EXAMPLES.sh) - 36+ real-world usage examples
- 📓 [Notebook](pipeline/Notebook.ipynb) - Interactive analysis
