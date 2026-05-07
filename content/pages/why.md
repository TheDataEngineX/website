---
title: Why DataEngineX — Open Source Alternative to Airflow, MLflow, and LangChain
slug: why
description: DataEngineX is an open-source, self-hosted Python framework that replaces Airflow, MLflow, LangChain, and FastAPI glue. One dex.yaml config file manages your entire data pipeline, ML lifecycle, and AI agents stack.
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

[Get started →](https://docs.thedataenginex.org/getting-started/)
