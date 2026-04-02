---
title: Why DataEngineX
slug: why
description: Why one config file beats stitching N tools together
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

---

## One File, Entire Stack

DataEngineX is the opposite approach. Define once, run anywhere:

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

## Swappable Backends

Opinionated defaults, zero lock-in. Every layer is swappable:

```bash
pip install "dataenginex[dagster]"    # swap orchestration
pip install "dataenginex[mlflow]"     # swap experiment tracking
pip install "dataenginex[agents]"     # LangGraph agent runtime
pip install "dataenginex[spark]"      # PySpark transforms
```

The config stays the same. The backend changes.

---

## Self-Hosted

Your data never leaves your infrastructure. No SaaS subscription. No vendor lock-in. Run on a VPS, K3s cluster, or bare metal.

[Get started →](https://docs.thedataenginex.org/getting-started/)
