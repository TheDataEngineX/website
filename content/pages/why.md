---
title: Why DataEngineX — Data + ML + AI Engineering
slug: why
description: DataEngineX is an open-source, self-hosted Python framework for data pipelines, ML lifecycle, and AI agents — unified under one dex.yaml. Native integrations with DuckDB, Spark, MLflow, LiteLLM, and more.
template: page
---

## The Modern Data Stack Is Broken

A typical production data + ML + AI setup looks like this:

| Concern | Tool you add |
|---------|-------------|
| Orchestration | Airflow or Prefect |
| Experiment tracking | MLflow or W&B |
| AI / LLM agents | LangChain or LlamaIndex |
| Data serving | FastAPI (custom) |
| Observability | Prometheus + Grafana + custom logging |
| Deployment | Helm + Terraform + custom CI |

You are not building a product. You are building glue.

Every new tool is another configuration format, another auth system, another failure mode, another oncall page.

DataEngineX does not rip out those tools. It ships production-ready implementations of every layer — and integrates cleanly with the tools you already run.

---

## One File, Entire Stack

DataEngineX is a Python framework for your Data + ML + AI engineering lifecycle. Define once, run anywhere:

```yaml
# dex.yaml
data:
  source: s3://my-bucket/raw/
  format: parquet
  quality:
    null_threshold: 0.05

ml:
  backend: mlflow          # or built-in — swap without code change
  training:
    model: xgboost
    target: revenue

ai:
  provider: openai
  retrieval: hybrid        # BM25 + dense — built in
  agents:
    - name: analyst
      tools: [sql, search]

observability:
  metrics: prometheus
  tracing: otel
```

Use it from Python, the `dex` CLI, or the self-hosted web UI. No glue code.

---

## Complete Platform — Built-In and Integrated

DataEngineX ships production-ready implementations of every layer:

- **Data pipelines** — DuckDB engine, S3/GCS connectors, quality gates, medallion lakehouse, optional Spark backend
- **ML lifecycle** — experiment tracking, model registry, training, serving, drift detection
- **AI agents** — LLM routing via LiteLLM, hybrid BM25+dense retrieval, LangGraph runtime
- **DEX Studio** — self-hosted web UI (FastAPI + Jinja2 + HTMX, port 7860)
- **Observability** — structlog structured logging, Prometheus metrics, OpenTelemetry tracing — built in, no extra packages

When you already run external tools, DataEngineX integrates natively — not against them:

| External Tool | DataEngineX integration |
|---------------|----------------|
| MLflow | Point `ml.backend: mlflow` — tracking_uri wired automatically |
| LiteLLM | LLM routing layer — 100+ providers, swap without code changes |
| Qdrant | Vector store for RAG — configured in `ai.retrieval` |
| Langfuse | LLM observability — enabled via config, not code |
| PySpark | Big-data backend — swap `data.backend: spark` in config |
| dbt | Run dbt transforms as pipeline steps |
| Kafka / Redpanda | Stream sources for real-time ingestion |
| Authentik | OIDC SSO for dex-studio |

---

## Swappable Backends

Opinionated defaults, zero lock-in. Every layer is swappable:

```bash
pip install "dataenginex[cloud]"         # S3 + GCS + BigQuery connectors
pip install "dataenginex[qdrant]"        # Qdrant vector store
pip install 'litellm>=1.83.3' --no-deps  # 100+ LLM providers (separate install)
```

The config stays the same. The backend changes.

---

## Self-Hosted

Your data never leaves your infrastructure. No SaaS subscription. No vendor lock-in. Run on a VPS, K3s cluster, or bare metal.

**Complete Data + ML + AI engineering, unified.**

[Get started →](https://docs.thedataenginex.org/getting-started/)
