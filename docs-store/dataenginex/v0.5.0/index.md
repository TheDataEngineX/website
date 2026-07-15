# DataEngineX Documentation v0.5.0

The Python library that powers DataEngineX Studio — an open-source, self-hosted, local-first Data + ML + AI workbench for individuals and small teams.

## Quick Start

```bash
pip install dataenginex
```

## Features

| Subsystem | Built-in | Optional backend |
|-----------|----------|------------------|
| Data engine | DuckDB | PySpark |
| Storage | Local parquet + DuckDB | S3, GCS, BigQuery |
| Lineage | DuckDB / JSON | PostgreSQL |
| Scheduler | croniter | — |
| ML training | scikit-learn | XGBoost, PyTorch |
| ML tracking | JSON-based | MLflow |
| LLM providers | Ollama, OpenAI, Anthropic | LiteLLM |
| Vector store | DuckDB VSS | Qdrant |
| Retrieval | BM25 + dense + hybrid + graph | Elasticsearch |
| Connectors | CSV, Parquet, DuckDB, REST, Kafka, SSE, HTTP | Spark, dbt, Delta, PostgreSQL |

## Links

- [GitHub](https://github.com/TheDataEngineX/dataenginex)
- [PyPI](https://pypi.org/project/dataenginex/)
- [Docs](https://docs.thedataenginex.org)
