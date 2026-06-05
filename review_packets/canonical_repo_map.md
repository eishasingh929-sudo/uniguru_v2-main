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
- curriculum integrity output: `review_packets/proof_logs/curriculum_integrity_report.json`
- retrieval quality output: `review_packets/proof_logs/retrieval_quality_report.json`
- learning demo output: `review_packets/proof_logs/learning_intelligence_demo.json`

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
python scripts\expand_balbharti_masterdb.py
python scripts\ingest_balbharti_masterdb.py
python scripts\generate_retrieval_reports.py
python backend\service\uniguru_runtime_api.py "Grade 10 Science: explain force and motion with an example." --grade 10 --medium "English Medium" --subject Science
python scripts\run_constitutional_runtime_convergence_proof.py
```

Proof files:

- `masterdb/balbharti/ingestion_manifest.json`
- `review_packets/proof_logs/balbharti_masterdb_ingestion_proof.json`
- `review_packets/proof_logs/curriculum_integrity_report.json`
- `review_packets/proof_logs/retrieval_quality_report.json`
- `review_packets/proof_logs/learning_intelligence_demo.json`
- `review_packets/proof_logs/uniguru_runtime_execution_latest.json`
- `review_packets/proof_logs/constitutional_runtime_trace.json`

## One Canonical Execution Surface

The sprint execution surface is:

`Query -> MasterDB lookup -> semantic interpretation -> constitutional runtime -> bounded response contract -> replay proof artifact`

There are no competing runtime coordinators in this sprint. Older proof scripts remain as regression proof generators, not active runtime entry points.

## Current Proof Hashes

- MasterDB dataset hash: `ec4cd3c0c1f87770c4a2e496b88e1156e137e99aef4390fade31222cf8957489`
- MasterDB manifest hash: `05cc4145b24b27f8a270dbcf4224d6cd5ea92d4e34f7aa095cd6628c0a4c81c3`
- Coverage hash: `d5ef7b1238d8dcf1395a6597d0a3b43a4e0571febc0b0cadc30a7f66520812be`
- Integrity validation hash: `1972534f243c6254b960e0d605757b765a2991555ff76b6eb5814194ab98731d`
- Runtime execution hash: `00587305bb8390b3fb63a67d03c5755d735964a62616b0215287eea7ab694b93`
- Runtime contract hash: `49339074c0ff3d56b05f9155b471273cdc3aa07c03c65b1c2633a17f0168246e`
