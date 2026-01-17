FROM python:3.13.11-slim
# Copy the uv binary from the Astral UV image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set the working directory inside the container
WORKDIR /code
# Create a virtual environment
ENV PATH="/code/.venv/bin:$PATH"

# Copy the Python version and dependency files
COPY .python-version pyproject.toml uv.lock ./

# Install UV and dependencies
RUN uv sync --locked

# Install required Python packages
# RUN pip install --no-cache-dir pandas pyarrow



# Copy the pipeline script into the container
COPY simple_data_ingestion.py .
# Set the entry point for the container
ENTRYPOINT ["python", "simple_data_ingestion.py"]
