# DE Docker Workshop - NYC Taxi Data Pipeline

A production-ready data engineering project demonstrating containerized ETL pipeline with PostgreSQL integration. This workshop showcases Docker best practices, SQL data ingestion, and orchestration techniques using NYC taxi data.

**Key Features:**
- 🐳 Fully containerized PostgreSQL database and Python pipeline
- 🔗 Docker networking for service communication
- 📊 CLI-driven data ingestion with argparse
- 🌍 Environment variable configuration
- 📝 Jupyter notebook for exploratory analysis
- 📦 uv package manager for reproducible dependencies
- ✅ Production-ready with error handling and logging
- 🚀 Docker Compose for easy orchestration

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Running the Database](#running-the-database)
5. [Running the Pipeline](#running-the-pipeline)
6. [Linking Services](#linking-services)
7. [Usage Examples](#usage-examples)
8. [Documentation](#documentation)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
git clone https://github.com/Ganebang/DE-docker-workshop.git
cd DE-docker-workshop

# Start both database and pipeline
docker-compose up -d

# Run the pipeline
docker-compose exec pipeline uv run simple_data_ingestion.py --year 2021 --month 1

# View logs
docker-compose logs -f database
docker-compose logs -f pipeline

# Stop services
docker-compose down
```

### Option 2: Manual Docker Commands

```bash
# Terminal 1: Start PostgreSQL container
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --name postgres-db \
  --network taxi-network \
  postgres:18

# Terminal 2: Build and run pipeline container
docker build -t taxi-pipeline ./pipeline
docker run -it \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  --network taxi-network \
  --name pipeline \
  taxi-pipeline --year 2021 --month 1

# Terminal 3: Run psql to verify data
docker run -it --rm \
  --network taxi-network \
  postgres:18 psql -h postgres-db -U root -d ny_taxi \
  -c "SELECT COUNT(*) FROM yellow_taxi_data;"
```

### Option 3: Local Development

```bash
# Start PostgreSQL (requires local PostgreSQL installation)
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

## 📁 Project Structure

```
DE-docker-workshop/
├── README.md                          # This file
├── docker-compose.yml                 # Orchestration config (create if needed)
├── pyproject.toml                     # Root project config
├── .python-version                    # Python version specification
├── .gitignore                         # Git ignore rules
│
├── pipeline/                          # Main pipeline application
│   ├── Dockerfile                     # Container image definition
│   ├── pyproject.toml                 # Pipeline dependencies
│   ├── .python-version                # Python version
│   ├── uv.lock                        # Locked dependencies
│   ├── simple_data_ingestion.py       # Main ingestion script (311 lines)
│   ├── pipeline.py                    # Pipeline utilities
│   ├── Notebook.ipynb                 # Jupyter notebook for analysis
│   ├── README.md                      # Pipeline-specific docs
│   │
│   ├── NY Taxi Documentation Files:
│   ├── README_CLI.md                  # CLI argument reference
│   ├── USAGE_GUIDE.md                 # Comprehensive usage guide
│   ├── QUICK_REFERENCE.md             # Quick command lookup
│   ├── BEST_PRACTICES.md              # Implementation patterns
│   ├── EXAMPLES.sh                    # 36+ usage examples
│   ├── IMPLEMENTATION_SUMMARY.md      # Technical summary
│   ├── DELIVERY_SUMMARY.txt           # Feature summary
│   │
│   └── ny_taxi_postgres_data/         # PostgreSQL data volume
│       └── 18/
│           └── docker/                # Database files
│
├── test/                              # Test files
│   ├── file1.txt
│   ├── file2.txt
│   ├── file3.txt
│   └── script.py
│
└── ny_taxi_postgres_data/             # Shared PostgreSQL volume
    └── (database files)
```

---

## 📋 Prerequisites

### Required Software

- **Docker**: v20.10+
- **Docker Compose**: v1.29+ (optional, for simpler orchestration)
- **Git**: v2.30+

### Optional (for local development)

- **Python**: 3.13.11+
- **PostgreSQL Client**: `psql` command-line tool
- **uv**: Python package manager

### System Resources

- **Disk Space**: ~2GB (for database and data)
- **Memory**: 2GB minimum (4GB recommended)
- **CPU**: 2 cores minimum

### Port Requirements

- **5432**: PostgreSQL (mapped from container)
- **8888**: Jupyter (if running notebook)

---

## 🐘 Running the Database

### PostgreSQL Container Setup

#### Basic Setup (Single Terminal)

```bash
# Create Docker network (required for linking services)
docker network create taxi-network

# Start PostgreSQL container
docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

#### Persistent Setup with Volume Mounting

```bash
# Create a named volume (persists across container restarts)
docker volume create taxi-postgres-data

# Start with named volume
docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v taxi-postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18
```

#### Environment Variables for Database

| Variable | Default | Purpose |
|----------|---------|---------|
| `POSTGRES_USER` | postgres | Database user (for auth) |
| `POSTGRES_PASSWORD` | (required) | User password |
| `POSTGRES_DB` | postgres | Database name to create |
| `PGDATA` | /var/lib/postgresql/data | Data directory inside container |

### Database Management

#### Check Database Status

```bash
# View container logs
docker logs postgres-db

# Connect to container
docker exec -it postgres-db bash

# Inside container, connect to database
psql -U root -d ny_taxi

# List all tables
\dt

# Exit psql
\q
```

#### View Database Data

```bash
# From host machine
docker exec postgres-db psql -U root -d ny_taxi -c "SELECT COUNT(*) FROM yellow_taxi_data;"

# Show table structure
docker exec postgres-db psql -U root -d ny_taxi -c "\d yellow_taxi_data;"

# Show first 5 rows
docker exec postgres-db psql -U root -d ny_taxi -c "SELECT * FROM yellow_taxi_data LIMIT 5;"
```

#### Backup and Restore

```bash
# Backup database
docker exec postgres-db pg_dump -U root ny_taxi > backup.sql

# Restore database
docker exec -i postgres-db psql -U root ny_taxi < backup.sql

# Backup volumes
docker run --rm -v taxi-postgres-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz -C /data .
```

#### Stop and Restart

```bash
# Stop container (data persists)
docker stop postgres-db

# Restart container
docker restart postgres-db

# Remove container (data in volume persists)
docker rm postgres-db

# Remove everything including data
docker volume rm taxi-postgres-data
docker network rm taxi-network
```

---

## 🔧 Running the Pipeline

### Build Pipeline Container

```bash
# Navigate to pipeline directory
cd pipeline

# Build container image
docker build -t taxi-pipeline:latest .

# Build with specific Python version
docker build -t taxi-pipeline:py313 \
  --build-arg PYTHON_VERSION=3.13.11 .

# View image info
docker images | grep taxi-pipeline
```

### Run Pipeline Container

#### Basic Execution

```bash
# Run with default parameters (2021, January)
docker run -it \
  --name pipeline \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline
```

#### Custom Parameters

```bash
# Specify year and month
docker run -it \
  --name pipeline-2020 \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline \
  --year 2020 --month 6 --chunk-size 100000

# Enable debug logging
docker run -it \
  --name pipeline-debug \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline \
  --log-level DEBUG
```

#### Background Execution

```bash
# Run in background with volume mounting for logs
docker run -d \
  --name pipeline-batch \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  -v $(pwd)/logs:/logs \
  taxi-pipeline \
  --year 2021 --month 1

# Check status
docker ps -a | grep pipeline-batch

# View logs
docker logs -f pipeline-batch

# Stop container
docker stop pipeline-batch
```

### Pipeline Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DB_HOST` | localhost | PostgreSQL hostname |
| `DB_PORT` | 5432 | PostgreSQL port |
| `DB_USER` | root | Database username |
| `DB_PASSWORD` | root | Database password |
| `DB_NAME` | ny_taxi | Database name |

### Pipeline Command-Line Arguments

```bash
# Show all available arguments
docker run --rm taxi-pipeline --help

# Output:
# --year [2009-2025]          Year to ingest (default: 2021)
# --month [1-12]              Month to ingest (default: 1)
# --chunk-size N              Rows per chunk (default: 100000)
# --table-name NAME           Table name (default: yellow_taxi_data)
# --db-host HOST              Database host
# --db-port PORT              Database port
# --db-user USER              Database username
# --db-password PASSWORD      Database password
# --db-name NAME              Database name
# --log-level LEVEL           Logging level (DEBUG/INFO/WARNING/ERROR)
```

---

## 🔗 Linking Services

### Method 1: Docker Network (Recommended)

Docker networks enable automatic DNS resolution between containers.

#### Setup Steps

```bash
# 1. Create a custom bridge network
docker network create taxi-network

# 2. Run PostgreSQL with network
docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# 3. Run Pipeline with network (references postgres-db by name)
docker run -it \
  --name pipeline \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline --year 2021 --month 1

# 4. Verify communication
docker exec pipeline ping postgres-db
```

#### How It Works

- Container names become hostnames on the custom network
- `postgres-db` is resolvable to its IP address automatically
- No need for IP address management
- Automatic load balancing between containers

#### Network Management

```bash
# List all networks
docker network ls

# Inspect network
docker network inspect taxi-network

# View connected containers
docker network inspect taxi-network | grep -A 20 Containers

# Remove network (all containers must be disconnected)
docker network rm taxi-network
```

### Method 2: Docker Compose (Simplest)

Docker Compose automatically handles networking, volume management, and orchestration.

#### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database Service
  database:
    image: postgres:18
    container_name: postgres-db
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi
    volumes:
      - ./ny_taxi_postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - taxi-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U root"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Pipeline Service
  pipeline:
    build:
      context: ./pipeline
      dockerfile: Dockerfile
    container_name: pipeline
    depends_on:
      database:
        condition: service_healthy
    environment:
      DB_HOST: database
      DB_PORT: 5432
      DB_USER: root
      DB_PASSWORD: root
      DB_NAME: ny_taxi
    networks:
      - taxi-network
    volumes:
      - ./pipeline/logs:/logs
    restart: on-failure

networks:
  taxi-network:
    driver: bridge
```

#### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs (all services)
docker-compose logs -f

# View specific service logs
docker-compose logs -f database
docker-compose logs -f pipeline

# Run pipeline with specific parameters
docker-compose run pipeline \
  uv run simple_data_ingestion.py --year 2021 --month 1

# Execute command in running service
docker-compose exec database psql -U root -d ny_taxi -c "SELECT COUNT(*) FROM yellow_taxi_data;"

# Stop services (data persists)
docker-compose stop

# Stop and remove containers (data persists in volumes)
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

### Method 3: Host Network

For advanced use cases requiring host network access.

```bash
# Start PostgreSQL
docker run -d \
  --name postgres-db \
  --network host \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  postgres:18

# Start Pipeline
docker run -it \
  --name pipeline \
  --network host \
  -e DB_HOST="localhost" \
  taxi-pipeline
```

**Advantages:** Direct access to host ports  
**Disadvantages:** Reduced isolation, port conflicts, less portable

### Comparison of Linking Methods

| Method | Setup | Isolation | Portability | Recommended |
|--------|-------|-----------|-------------|-------------|
| Docker Network | Manual | Good | Good | ✅ For learning |
| Docker Compose | YAML file | Excellent | Excellent | ✅✅ For production |
| Host Network | Simple | Poor | Poor | ❌ Not recommended |

---

## 📝 Usage Examples

### Complete Data Pipeline Workflow

```bash
# 1. Create network
docker network create taxi-network

# 2. Start PostgreSQL
docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# 3. Wait for database to be ready
sleep 5

# 4. Build pipeline image
cd pipeline
docker build -t taxi-pipeline:latest .

# 5. Run pipeline for single month
docker run -it \
  --name pipeline \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline \
  --year 2021 --month 1

# 6. Verify data was ingested
docker exec postgres-db psql -U root -d ny_taxi \
  -c "SELECT COUNT(*) as total_rows FROM yellow_taxi_data;"

# 7. Ingest multiple months
for month in {1..6}; do
  docker run -it \
    --name pipeline-month-$month \
    --network taxi-network \
    -e DB_HOST="postgres-db" \
    -e DB_USER="root" \
    -e DB_PASSWORD="root" \
    -e DB_NAME="ny_taxi" \
    taxi-pipeline \
    --year 2021 --month $month
  docker rm pipeline-month-$month
done
```

### Batch Processing with Error Handling

```bash
#!/bin/bash
# script: batch_ingest.sh

set -e  # Exit on error
NETWORK="taxi-network"
IMAGE="taxi-pipeline:latest"

# Create network if not exists
docker network create $NETWORK 2>/dev/null || true

# Start database if not running
if ! docker ps | grep -q postgres-db; then
  echo "Starting PostgreSQL..."
  docker run -d \
    --name postgres-db \
    --network $NETWORK \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
    -p 5432:5432 \
    postgres:18
  sleep 5
fi

# Ingest multiple months
for year in 2019 2020 2021; do
  for month in {1..12}; do
    echo "Ingesting $year-$month..."
    docker run -it \
      --rm \
      --network $NETWORK \
      -e DB_HOST="postgres-db" \
      -e DB_USER="root" \
      -e DB_PASSWORD="root" \
      -e DB_NAME="ny_taxi" \
      $IMAGE \
      --year $year --month $month || echo "Failed for $year-$month"
  done
done

echo "Batch processing complete!"
```

### Debugging and Monitoring

```bash
# Monitor resource usage
docker stats postgres-db pipeline

# View detailed container info
docker inspect postgres-db | jq '.[0].NetworkSettings'

# Check network connectivity
docker exec pipeline ping postgres-db

# View all logs with timestamps
docker logs -f --timestamps postgres-db

# Execute interactive database shell
docker exec -it postgres-db psql -U root -d ny_taxi

# Export query results to CSV
docker exec postgres-db psql -U root -d ny_taxi \
  -c "COPY (SELECT * FROM yellow_taxi_data LIMIT 1000) TO STDOUT WITH CSV HEADER;" \
  > data_export.csv
```

---

## 📚 Documentation

### Pipeline Documentation

Comprehensive guides are available in the `pipeline/` directory:

- **[README_CLI.md](pipeline/README_CLI.md)** - Complete CLI argument reference
- **[USAGE_GUIDE.md](pipeline/USAGE_GUIDE.md)** - Comprehensive usage documentation
- **[QUICK_REFERENCE.md](pipeline/QUICK_REFERENCE.md)** - Quick command lookup
- **[BEST_PRACTICES.md](pipeline/BEST_PRACTICES.md)** - Implementation patterns and best practices
- **[EXAMPLES.sh](pipeline/EXAMPLES.sh)** - 36+ real-world usage examples
- **[IMPLEMENTATION_SUMMARY.md](pipeline/IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[Notebook.ipynb](pipeline/Notebook.ipynb)** - Interactive Jupyter notebook for data exploration

### Key Documentation Links

| Document | Purpose | Audience |
|----------|---------|----------|
| README_CLI.md | CLI argument reference | Data Engineers, DevOps |
| BEST_PRACTICES.md | Implementation patterns | Developers |
| EXAMPLES.sh | Real-world usage scenarios | DevOps, Automation |
| Notebook.ipynb | Data exploration and analysis | Data Scientists, Analysts |

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: "Connection refused" error when running pipeline

**Cause:** PostgreSQL container not running or not accessible

**Solutions:**

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres-db

# If not running, start it
docker start postgres-db

# If not created, run it
docker run -d \
  --name postgres-db \
  --network taxi-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# Verify connectivity
docker exec pipeline ping postgres-db
```

#### Issue: "Network postgres-db not found" error

**Cause:** Containers not on the same network

**Solutions:**

```bash
# Create network
docker network create taxi-network

# Connect existing container to network
docker network connect taxi-network postgres-db

# Restart pipeline container with correct network
docker run -it \
  --name pipeline \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  taxi-pipeline
```

#### Issue: "Permission denied" when accessing data volumes

**Cause:** Permission issues with mounted volumes

**Solutions:**

```bash
# Fix volume permissions
sudo chown -R 999:999 ./ny_taxi_postgres_data

# Or use Docker's built-in user mapping
docker run -d \
  --user postgres \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  postgres:18
```

#### Issue: Database disk quota exceeded

**Cause:** Large amount of data ingested

**Solutions:**

```bash
# Check disk usage
du -sh ./ny_taxi_postgres_data

# Clean up old data
docker volume prune
docker image prune -a

# Backup and remove old data
docker exec postgres-db pg_dump -U root ny_taxi > backup.sql
docker volume rm taxi-postgres-data
```

#### Issue: Port 5432 already in use

**Cause:** Another PostgreSQL instance running

**Solutions:**

```bash
# Find process using port 5432
lsof -i :5432

# Use different port mapping
docker run -d \
  --name postgres-db \
  -p 5433:5432 \
  postgres:18

# Connect with different port
docker run -it \
  -e DB_PORT=5433 \
  taxi-pipeline
```

#### Issue: Pipeline takes too long to run

**Cause:** Large chunk size or network issues

**Solutions:**

```bash
# Use smaller chunk size for faster memory usage
docker run -it \
  --network taxi-network \
  taxi-pipeline \
  --chunk-size 50000

# Enable debug logging to see progress
docker run -it \
  --network taxi-network \
  taxi-pipeline \
  --log-level DEBUG

# Check network performance
docker exec pipeline ping -c 10 postgres-db
```

### Getting Help

1. **Check logs:** `docker logs <container-name>`
2. **Inspect container:** `docker inspect <container-name>`
3. **Test connectivity:** `docker exec <container> ping <other-container>`
4. **View documentation:** See [Documentation](#documentation) section
5. **Check examples:** Run `cat pipeline/EXAMPLES.sh | grep <keyword>`

### Debug Mode

```bash
# Run with debug logging and interactive shell
docker run -it \
  --name pipeline-debug \
  --network taxi-network \
  -e DB_HOST="postgres-db" \
  -e DB_USER="root" \
  -e DB_PASSWORD="root" \
  -e DB_NAME="ny_taxi" \
  taxi-pipeline \
  --log-level DEBUG \
  --year 2021 \
  --month 1

# Inspect running container
docker exec -it pipeline-debug bash
```

---

## 🎯 Next Steps

### For Learning

1. Run the pipeline with default parameters
2. Explore the database using `psql`
3. Review the Jupyter notebook for data analysis
4. Check examples in `pipeline/EXAMPLES.sh`

### For Production

1. Create `docker-compose.yml` for orchestration
2. Set up CI/CD pipeline for automated ingestion
3. Implement backup and disaster recovery
4. Add monitoring and alerting
5. Create infrastructure as code (Terraform, Kubernetes)

### For Development

1. Study the `simple_data_ingestion.py` script
2. Review best practices in `pipeline/BEST_PRACTICES.md`
3. Modify parameters and run tests
4. Experiment with the Jupyter notebook
5. Create custom data transformations

---

## 📞 Support & Resources

- **Python Docs:** https://docs.python.org/3.13/
- **Docker Docs:** https://docs.docker.com/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/18/
- **NYC Taxi Data:** https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

---

## 📄 License

This project is provided as-is for educational and training purposes.

---

## ✅ Checklist Before Running

- [ ] Docker installed and running
- [ ] At least 2GB free disk space
- [ ] Port 5432 is available
- [ ] Git repository cloned
- [ ] Network connectivity available (for downloading data)

---

**Happy Data Engineering! 🚀**
