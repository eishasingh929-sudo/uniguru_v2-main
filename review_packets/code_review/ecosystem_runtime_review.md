# Core File Review

## backend/service/ecosystem_runtime.py
- Adds a deterministic ecosystem orchestration path that composes Vijay validation, TANTRA contract generation, Bucket telemetry, InsightFlow observability, GC validation, and MDU evidence generation.
- Emits proof artifacts to review_packets/integration_proof.

## backend/service/uniguru_runtime_api.py
- Exposes the new /runtime/ecosystem/execute endpoint without altering the existing runtime contract path.

## backend/kosha/kosha_retriever.py
- Includes a resilient fallback when the optional ontology-aware retriever dependency is absent so the deterministic pipeline remains testable.
