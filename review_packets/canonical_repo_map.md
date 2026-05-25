# Canonical Repository Map

Generated/updated for the Isha unified runtime convergence sprint.

## One Runtime

- Canonical service runtime: `backend/service/uniguru_runtime_api.py`
- Canonical governance coordinator: `backend/governance/constitutional_runtime.py`
- Canonical app API remains: `backend/service/api.py`
- Runtime execution surface: CLI plus FastAPI `POST /runtime/execute`

## One Governance Path

`backend/service/uniguru_runtime_api.py -> ConstitutionalCognitionRuntime.execute(...) -> backend/governance/semantic_authority.py`

Semantic interpretation does not grant authority. Governance remains bounded by:

- semantic drift observation
- authority pressure scoring
- contradiction arbitration
- ontology legitimacy boundaries
- uncertainty lineage preservation

## One Replay Path

Replay is hash-bound through:

- `backend/memory/constitutional_semantic_memory.py::stable_hash`
- `constitutional_event_registry` inside `runtime_trace`
- runtime proof output: `review_packets/proof_logs/uniguru_runtime_execution_latest.json`
- ingestion proof output: `review_packets/proof_logs/balbharti_masterdb_ingestion_proof.json`

## One Observability Layer

Observability is emitted by `SemanticPressureObservabilityEngine` and surfaced through the runtime contract as:

- `trust_state`
- `uncertainty_state`
- `contradiction_state`
- `ontology_boundary_state`
- `constitutional_reasoning_summary`

Observability is read-only and never grants canonical authority.

## One Proof Pipeline

Proof commands:

```powershell
python scripts\ingest_balbharti_masterdb.py
python backend\service\uniguru_runtime_api.py "What is a balanced diet in Class 6 Science?" --grade 6 --medium "English Medium" --subject Science
python scripts\run_constitutional_runtime_convergence_proof.py
```

Proof files:

- `masterdb/balbharti/ingestion_manifest.json`
- `review_packets/proof_logs/balbharti_masterdb_ingestion_proof.json`
- `review_packets/proof_logs/uniguru_runtime_execution_latest.json`
- `review_packets/proof_logs/constitutional_runtime_trace.json`

## One Canonical Execution Surface

The sprint execution surface is:

`Query -> MasterDB lookup -> semantic interpretation -> constitutional runtime -> bounded response contract -> replay proof artifact`

There are no competing runtime coordinators in this sprint. Older proof scripts remain as regression proof generators, not active runtime entry points.

## Current Proof Hashes

- MasterDB dataset hash: `392b3c1d013633e41200d6716a8f4721917863f41861d2f39c2f417d6eeaecd8`
- MasterDB manifest hash: `0b9f1aab41bc132e54ea92c24ec7ef17000a9c2e5ebda6194c68c980073810df`
- Runtime execution hash: `57f0be64dda0a2a7f8d1acca5a024eeab7f8382eeffd60cf47770ebea670ae6e`
- Runtime contract hash: `0bb10f59c24d26d260171bb31531b64d0c8c73fee7ea7939411536ea0f4b601f`
