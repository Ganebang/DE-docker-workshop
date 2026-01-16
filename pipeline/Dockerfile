FROM python:3.13.11-slim
RUN pip install --no-cache-dir pandas pyarrow
WORKDIR /code
COPY pipeline.py .
ENTRYPOINT ["python", "pipeline.py"]
