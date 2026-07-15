# Getting Started

Install DataEngineX and run your first pipeline.

## Installation

```bash
pip install dataenginex
```

## Create a config file

Create `dex.yaml`:

```yaml
project:
  name: my-first-pipeline

data:
  sources:
    raw_users:
      type: csv
      path: data/users.csv
  pipelines:
    clean_users:
      source: raw_users
      destination: silver.users
```

## Validate and run

```bash
dex validate dex.yaml
```

```python
from dataenginex.engine import DexEngine

engine = DexEngine("dex.yaml")
result = engine.run_pipeline("clean_users")
print(result.rows_written)
```

## Optional extras

```bash
pip install "dataenginex[cloud]"     # S3, GCS, BigQuery
pip install "dataenginex[postgres]"  # PostgreSQL lineage
pip install "dataenginex[qdrant]"    # Qdrant vector store
pip install "dataenginex[ml]"        # scikit-learn + XGBoost
pip install "dataenginex[kafka]"     # Kafka connector
pip install "dataenginex[rabbitmq]"  # RabbitMQ backend
```
