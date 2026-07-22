---
title: Philosophy — The DataEngineX Way
slug: philosophy
description: Core principles behind DataEngineX: library-first, config-driven, pluggable backends, local-first, security primitives.
template: page
---

## The DataEngineX Philosophy

> **One file. One library. Data + ML + AI unified.**

---

## 1. Library, Not Platform

```
┌─────────────────────────────────────────────────────────────────────┐
│  Traditional Platform          DataEngineX                          │
│  ─────────────────────          ─────────────                       │
│  You deploy our server         You import our library               │
│  You adapt to our API          You own the server layer             │
│  Our auth, our scaling         Your auth, your scaling              │
│  Upgrade = migration           Upgrade = pip install -U             │
│  Multi-tenant by default       Single-tenant by default             │
└─────────────────────────────────────────────────────────────────────┘
```

**Why:** Platforms force you into their operational model. Libraries let you choose yours.

- **Zero infrastructure** to run: `pip install dataenginex` works offline
- **You own the HTTP layer** — FastAPI, Flask, Lambda, notebook, CLI
- **No multi-tenancy** — each app = isolated process = simple
- **Version upgrades** are `pip install`, not migration projects

---

## 2. Config-Driven, Code-Optional

```yaml
# dex.yaml — your entire stack in one file
project:
  name: customer-intelligence

data:
  sources:
    events:
      type: kafka
      connection: {bootstrap: "kafka:9092"}
  pipelines:
    enrich_users:
      source: events
      transforms:
        - type: filter
          condition: "event_type = 'purchase'"
        - type: derive
          expression: "amount * 1.2"
          name: revenue_usd
      destination: silver.enriched_purchases

ml:
  tracking: mlflow
  tracking:
    uri: "http://mlflow:5000"
  experiments:
    churn_model:
      model_type: xgboost
      target: churned_30d
      features: [recency, frequency, monetary]

ai:
  llm:
    provider: ollama
    model: llama3.1
  retrieval:
    strategy: hybrid
  agents:
    analyst:
      runtime: builtin
      system_prompt: "You are a data analyst. Use the SQL tool."

observability:
  metrics: prometheus
  tracing: otel
```

**Use it from Python, the `dex` CLI, or the self-hosted web UI. No glue code.**

---

## 3. Pluggable Backends, One Pattern

Every subsystem uses the same `BackendRegistry[T]` pattern:

```python
# Same pattern for connectors, trackers, vector stores, LLMs, agents...
connector_registry = BackendRegistry[BaseConnector]("connector")

@connector_registry.decorator("csv")
class CsvConnector(BaseConnector): ...

@connector_registry.decorator("kafka")
class KafkaConnector(BaseConnector): ...

# In dex.yaml: type: "kafka" → registry.get("kafka") → KafkaConnector
```

**Result:** Learn one pattern, extend any subsystem. Third-party packages register via entry-points.

---

## 4. Local-First, Cloud-Optional

| Default (no extras) | Opt-in Extras |
|---------------------|---------------|
| DuckDB compute | PySpark `[data]` |
| Parquet + DuckDB lakehouse | Delta Lake `[delta]` |
| SQLite WAL metadata | PostgreSQL `[postgres]` |
| In-memory vector (DuckDB VSS) | Qdrant `[qdrant]` |
| JSON experiment tracking | MLflow `[tracking]` |
| Ollama / OpenAI / Anthropic | LiteLLM (100+ providers) |
| BM25 + dense retrieval | Elasticsearch (core dep) |

**Base install = ~50MB. Pay for what you use.**

---

## 5. Security as a Primitive, Not an Afterthought

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRUSTED (Your Code)                                                │
│  ├── dex-studio (FastAPI app)                                       │
│  ├── dataenginex (Library)                                          │
│  └── Project plugins/                                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  SECURITY BOUNDARY (PrivacyGuard + Sandbox)                         │
│  ├── PII detection (regex + NER)                                    │
│  ├── Masking strategies (mask/redact/hash/tokenize/block)           │
│  ├── Audit log (every outbound call)                                │
│  ├── Python sandbox (restricted builtins, no imports)               │
│  └── Resource limits (CPU, memory, time)                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  UNTRUSTED (External)                                               │
│  ├── LLM Providers (Ollama, OpenAI, Anthropic)                     │
│  ├── Vector DBs (Qdrant, Pinecone)                                  │
│  ├── Cloud Storage (S3, GCS, BigQuery)                              │
│  ├── Databases (PostgreSQL, MySQL)                                  │
│  └── Message Queues (Kafka, RabbitMQ)                               │
└─────────────────────────────────────────────────────────────────────┘
```

**PrivacyGuard wraps every LLM call** — not per-tool, at the boundary. Configure once in `dex.yaml`:

```yaml
secops:
  guard:
    enabled: true
    default_strategy: mask
    entities: [PERSON, EMAIL, PHONE, SSN, CREDIT_CARD, IP_ADDRESS]
    custom_patterns:
      - name: api_key
        regex: "sk-[a-zA-Z0-9]{32,}"
        strategy: redact
  audit:
    enabled: true
    db_path: ".dex/audit.duckdb"
```

---

## 6. Observability Built In, Not Bolted On

| Signal | Tech | Zero-Config |
|--------|------|-------------|
| **Logs** | structlog (JSON, KV, pretty) | ✅ |
| **Metrics** | Prometheus client (`/metrics`) | ✅ |
| **Traces** | OpenTelemetry SDK | ✅ |
| **Live logs** | SSE `/system/logs/stream` | ✅ |
| **Health** | `/health` → component status | ✅ |
| **Audit** | SQLite (DexStore) | ✅ |
| **AI costs** | Built-in token tracker | ✅ |

---

## 7. Persistence: One SQLite File

```
.dex/
├── store.duckdb          # All metadata (WAL mode)
│   ├── pipeline_runs     # execution history
│   ├── lineage_events    # data lineage graph
│   ├── model_artifacts   # ML model registry
│   ├── quality_runs      # data quality history
│   ├── audit_log         # security audit trail
│   ├── ai_memory         # long-term agent memory
│   ├── ai_episodes       # episodic trajectories
│   └── catalog_entries   # lakehouse datasets
├── lakehouse/            # Parquet/Delta files
│   ├── bronze/           # raw landings
│   ├── silver/           # cleaned, typed
│   └── gold/             # business-ready
└── audit.duckdb          # Separate audit DB
```

**Why SQLite WAL over DuckDB for metadata?**
- Multi-process safe: CLI + web server + workers coexist
- N readers + 1 writer with retries, no `SQLITE_BUSY` crashes
- Thread-local connections = no shared-state races
- Portable: single file, backup = `cp`

---

## 8. The Three Repos

| Repo | Purpose | Audience | Access |
|------|---------|----------|--------|
| **dataenginex** | PyPI library — engine, config, all backends | Developers, ML engineers | Public |
| **dex-studio** | Web UI — FastAPI + Jinja2 + HTMX | Data teams, analysts | Public |
| **infradex** | GitOps infra — K3s + ArgoCD + monitoring | Platform engineers | **Private** |

**Relationship:** `dex-studio` imports `dataenginex` directly. `infradex` deploys `dex-studio` via ArgoCD.

---

## 9. What We Don't Do

| Anti-Pattern | Our Approach |
|--------------|--------------|
| "Platform" with bundled HTTP server | Library — you own the server |
| Separate config per subsystem | One `dex.yaml` for everything |
| Custom DSL for pipelines | Python functions + SQL transforms |
| Proprietary experiment format | JSON (built-in) or MLflow |
| Forced SaaS subscription | Self-hosted, MIT licensed |
| Heavy JS frontend (React/Vue) | Server HTML + HTMX (no build step) |
| ORM for metadata | Dataclasses + raw SQLite |
| Framework-specific agents | Pluggable runtime, any LLM |

---

## 10. Built for Production, Designed for Simplicity

```
Production requirements              DataEngineX reality
────────────────────────────         ───────────────────
□ ACID metadata                     □ SQLite WAL
□ Multi-process safe                □ Thread-local conns + WAL
□ Pipeline lineage                  □ DexStore lineage_events
□ Data quality gates                □ Completeness + uniqueness + custom SQL
□ Model registry with stages        □ dev → staging → prod → archived
□ Drift detection (PSI, KS, MMD)    □ Scheduled via croniter
□ PII audit trail                   □ PrivacyGuard + AuditLog
□ Horizontal scaling                □ Swap DuckDB → PySpark
□ Canary deployments                □ infradex Traefik 90/10
□ Disaster recovery                 □ PVC snapshots + GitOps
```

---

## Get Started

```bash
# Library
pip install dataenginex

# Web UI
docker compose up
# → http://localhost:7860
```

**Read more:**
- [Architecture Overview](/ARCHITECTURE.md) — Platform-wide design
- [DataEngineX Architecture](/docs/dataenginex/latest/architecture/) — Library internals
- [DEX Studio Architecture](/docs/dex-studio/latest/architecture/) — Web UI design
- [InfraDEX Architecture](/docs/infradex/latest/architecture/) — GitOps infrastructure

---

*Philosophy version: 0.5.x | Updated: 2026-07-20*