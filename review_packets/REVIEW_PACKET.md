# REVIEW_PACKET.md - TANTRA Convergence Sprint

Generated for: UniGuru live deterministic convergence  
Generated at: 2026-05-07  
Status: Implemented with Bucket-ready trace proofs

## Entry Points

- `backend/kosha/deterministic_pipeline.py`
  - Primary TANTRA intelligence contract boundary.
  - Emits `trace_id`, accepted/rejected signals, semantic path, epistemic confidence, consensus analysis, output contract, downstream execution status, and Bucket-ready proof.
- `backend/kosha/kosha_retriever.py`
  - Ontology-aware retrieval with source governance and local deterministic embedding trace.
- `backend/kosha/signal_validator.py`
  - Deterministic validation boundary with epistemic confidence derivation.
- `backend/governance/source_governance.py`
  - Canonical source hierarchy, authority weight, OCR integrity penalty, confidence ceilings, and source lineage.
- `backend/governance/epistemic_confidence.py`
  - Truth-likelihood scoring separate from match strength.
- `backend/governance/contradiction.py`
  - Deterministic contradiction, ambiguity, and consensus analysis.
- `backend/retrieval/embedding_provider.py`
  - Offline provider-independent `LocalHashEmbeddingProvider`.
- `backend/retrieval/ontology_retriever.py`
  - Emits ontology score plus embedding trace proof.
- `backend/loaders/ingestor.py`
  - Builds legacy keyword index and `semantic_memory_index.json`.
- `scripts/ingest_kb.py`
  - Regenerates `backend/knowledge/index/*` artifacts.

## Semantic Execution Flow

`Input -> Kosha load -> schema enforcement -> canonical entity extraction -> ontology retrieval -> source governance -> deterministic validation -> epistemic confidence -> contradiction/consensus -> contract emission -> downstream-ready execution status -> Bucket proof`

No free-form fallback is emitted from this path. If no signal passes validation, the system emits `NO_VERIFIED_KNOWLEDGE`, `REJECTED_NO_SYNTHESIS`, and `REJECTED_NO_DOWNSTREAM_ACTION`.

## Trace Contract

Every proof payload carries a single immutable trace:

- `trace_id`
- `matched_signals[*].trace.trace_id`
- `output_contract.trace_id`
- `downstream_execution.trace_id`
- `bucket_proof.trace_id`
- `bucket_proof.trace_continuity.retrieval`
- `bucket_proof.trace_continuity.validation`
- `bucket_proof.trace_continuity.synthesis`
- `bucket_proof.trace_continuity.contract_emission`
- `bucket_proof.trace_continuity.downstream_execution`
- `bucket_proof.trace_continuity.bucket_proof`

Trace mutation is therefore machine-detectable by comparing these fields.

## Governance-Safe Contract

The response is schema-bound JSON with:

- `output_contract.schema: TANTRA_UNIGURU_INTELLIGENCE_CONTRACT_V1`
- `contract_bound: true`
- `downstream_consumable: true`
- `free_form_output: false`
- `fallback_to_llm: false`
- `matched_signals`
- `rejected_signals`
- `semantic_path`
- `confidence_breakdown`
- `consensus_analysis`
- `bucket_proof`

## Confidence Derivation

Confidence is now epistemic, not just retrieval strength. Dimensions:

- source authority
- semantic agreement
- contradiction pressure
- contextual consistency
- ontology convergence
- OCR integrity
- multi-source reinforcement
- retrieval strength

Confidence ceilings prevent weak OCR or weak semantic convergence from producing high confidence. Example verified trace: `trace_f3c8162c107a5e10` has match confidence `0.7711`, but epistemic confidence is capped to `0.5972` because the source is an OCR derivative.

## Source Governance

Source hierarchy:

- canonical scripture
- commentary
- translation
- OCR derivative
- inferred synthesis
- unknown

Each signal includes:

- `source_governance.source_type`
- `authority_weight`
- `confidence_ceiling`
- `ocr_integrity_penalty`
- `lineage.original_source`
- `lineage.transformation_history`

Weak source suppression prevents very low-authority signals from dominating retrieval.

## Contradiction And Consensus

`consensus_analysis` includes:

- contradiction list
- ambiguity classification
- consensus score
- contradiction pressure
- source count
- disagreement-aware synthesis note

Contradictory or interpretive cases reduce epistemic confidence instead of being flattened into certainty.

## Semantic Memory

`backend/knowledge/index/semantic_memory_index.json` contains:

- entities
- relationships
- semantic edges
- hierarchical concept chains
- source lineage

This preserves compatibility with the old keyword index while adding graph-grounded memory artifacts for downstream convergence.

## Proof Logs

Proof directory:

- `review_packets/proof_logs/`

Generated files:

- `proof_log_summary.json`
- `retrieval_benchmark.json`
- 15 latest per-trace proof files listed in `proof_log_summary.json`

Proof run summary:

- Total queries: 15
- Verified knowledge responses: 3
- Deterministic rejections: 12
- Trace continuity: Bucket proof and downstream execution share the same trace id.

Representative traces:

- Verified + Bucket proof: `trace_f3c8162c107a5e10`
- Consensus case: `trace_2fbb372950f250a1`
- Cross-domain rejection: `trace_b3b508fcdf505233`
- Current-events rejection: `trace_2b915a620b915df7`

## Benchmark Report

Benchmark file:

- `review_packets/proof_logs/retrieval_benchmark.json`

Metrics from final run:

- Precision: `1.0`
- Rejection correctness: `1.0`
- Semantic accuracy: `1.0`

Compared behavior:

- OLD: keyword overlap only.
- Ontology retrieval: canonical entity extraction, synonym expansion, concept overlap, entity overlap, domain consistency, contextual proximity.
- Semantic graph retrieval: `semantic_memory_index.json` preserves entity, relationship, edge, hierarchy, and lineage artifacts.
- Hybrid retrieval: ontology score plus local hash embedding score plus source authority weighting.

## TANTRA End-To-End Proof

Required flow demonstrated by `trace_f3c8162c107a5e10`:

`Input -> UniGuru semantic retrieval -> deterministic validation -> epistemic confidence -> contract emission -> downstream consumption status -> Bucket proof -> immutable trace continuity`

Downstream field:

- `downstream_execution.consumer: TANTRA_EXECUTION_CHAIN`
- `downstream_execution.status: READY_FOR_CONSUMPTION`
- `bucket_proof.event: tantra_uniguru_intelligence_contract`

## Video Walkthrough Notes

Recommended 10-15 minute walkthrough:

1. Show `backend/kosha/deterministic_pipeline.py` and the TANTRA contract payload.
2. Show `backend/governance/source_governance.py`, `epistemic_confidence.py`, and `contradiction.py`.
3. Show `backend/retrieval/ontology_retriever.py` embedding trace emission.
4. Open `backend/knowledge/index/semantic_memory_index.json`.
5. Open `review_packets/proof_logs/trace_f3c8162c107a5e10.json`.
6. Open `proof_log_summary.json` and `retrieval_benchmark.json`.
7. Explain rejection cases and confidence ceilings.

## Handover Notes

Current limitations:

- Kosha data still contains OCR artifacts and thin entries; stricter confidence ceilings intentionally reduce certainty.
- Legacy unreachable helper code remains below `_execute_kosha_pipeline()` in `backend/service/api.py`; endpoint execution returns before that code.
- Source hierarchy is deterministic but should be reviewed by Soham before being treated as final ontology governance.
- Bucket proof is file-backed and Bucket-ready; live external Bucket transport remains an infrastructure task.

Integration dependencies:

- Vijay: confirm exact downstream TANTRA contract fields.
- Soham: review entity taxonomy, Sanskrit mappings, and source hierarchy.
- Alay: pin `python backend/run_proof_log.py`, `python backend/run_retrieval_benchmark.py`, and `python scripts/ingest_kb.py` in CI.
- Vinayak: run final deterministic trace verification against `review_packets/proof_logs/`.
