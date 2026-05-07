---
title: Why DataEngineX — Complete Data + ML + AI Engineering
slug: why
description: DataEngineX is an open-source, self-hosted Python framework for the complete platform for Data + ML + AI engineering — production-ready pipelines, ML lifecycle, and AI agents unified under one dex.yaml. Native integrations with Airflow, MLflow, LangChain, and more.
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

DataEngineX is the complete platform for your Data + ML + AI engineering lifecycle. Define once, run anywhere:

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

server:
  auth: jwt
  rate_limit: 100/min

observability:
  metrics: prometheus
  tracing: otel
```

One `dex serve` command starts everything. No glue code.

---

## Complete Platform — Built-In and Integrated

DataEngineX ships production-ready implementations of every layer:

- **Data pipelines** — DuckDB engine, S3/GCS connectors, quality gates, medallion lakehouse
- **ML lifecycle** — experiment tracking, model registry, training, serving, drift detection
- **AI agents** — LLM routing via LiteLLM, hybrid BM25+dense retrieval, LangGraph runtime
- **API server** — FastAPI with JWT auth, rate limiting, RBAC, SCIM v2
- **Observability** — Prometheus metrics, OpenTelemetry tracing, Langfuse LLM tracing

When you already run external tools, DEX integrates natively — not against them. Airflow only schedules. MLflow only tracks. LangChain only chains. DEX gives you the complete end-to-end stack:

| External Tool | DEX integration |
|---------------|----------------|
| Airflow | Schedule DEX pipelines from Airflow DAGs |
| MLflow | Point `ml.backend: mlflow` — tracking_uri wired automatically |
| LangChain / LiteLLM | LLM routing layer — 100+ providers, swap without code changes |
| Qdrant | Vector store for RAG — configured in `ai.retrieval` |
| Langfuse | LLM observability — enabled via `[observability]` extra |
| PySpark | Big-data backend — swap `data.backend: spark` in config |

---

## Swappable Backends

Opinionated defaults, zero lock-in. Every layer is swappable:

```bash
pip install "dataenginex[cloud]"         # S3 + GCS + BigQuery connectors
pip install "dataenginex[auth]"          # RS256/JWKS + SCIM v2 + LDAP sync
pip install "dataenginex[observability]" # Langfuse LLM tracing
pip install 'litellm>=1.83.3' --no-deps  # 100+ LLM providers (separate install)
```

The config stays the same. The backend changes.

---

## Enterprise-Ready Auth

RBAC, SCIM v2 user provisioning, LDAP/AD sync, and OIDC federation (RS256/JWKS) ship as first-class extras — not bolt-ons. Enable them with env vars, not code changes.

---

## Self-Hosted

Your data never leaves your infrastructure. No SaaS subscription. No vendor lock-in. Run on a VPS, K3s cluster, or bare metal.

**Complete Data + ML + AI engineering, unified.**

[Get started →](https://docs.thedataenginex.org/getting-started/)
