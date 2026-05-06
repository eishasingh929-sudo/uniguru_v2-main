# REVIEW_PACKET.md - Isha Signal Architecture Sprint

Generated for: UniGuru deterministic signal intelligence conversion  
Generated at: 2026-05-06  
Status: Implemented with deterministic proof logs

## Entry Points

- `backend/kosha/deterministic_pipeline.py`
  - Primary signal-first execution contract.
  - Emits `trace_id`, `query`, `verification_status`, `matched_signals`, `rejected_signals`, `reasoning_path`, `confidence_breakdown`, `knowledge_ids_used`, `domain_resolution`, and `synthesis_mode`.
- `backend/service/api.py`
  - `/new_rag` and `/new_query` now call `run_deterministic_pipeline()` before any legacy FAISS or LLM path.
  - The old helper body is unreachable from the endpoint boundary; no direct LLM answer bypass is executed.
- `backend/kosha/kosha_retriever.py`
  - Ontology-aware Kosha retrieval with canonical entity expansion.
- `backend/kosha/signal_validator.py`
  - Deterministic acceptance/rejection boundary with explicit categories.
- `backend/ontology/entity_resolver.py`
  - Canonical entity extraction, synonym handling, domain resolution, semantic scoring.
- `backend/retrieval/embedding_provider.py`
  - Provider-neutral `EmbeddingProvider` abstraction with offline `LocalHashEmbeddingProvider`.
- `backend/retrieval/ontology_retriever.py`
  - Combined concept, entity, domain, contextual, and local embedding score.

## Execution Flow

`Query -> Kosha load -> schema enforcement -> canonical entity extraction -> ontology-aware retrieval -> deterministic signal validation -> structured signal emission -> deterministic synthesis or rejection -> proof log`

Synthesis only occurs after accepted signals exist. If no signal passes validation, the system emits `NO_VERIFIED_KNOWLEDGE` and `synthesis_mode: REJECTED_NO_SYNTHESIS`.

## Structured Signal Contract

Each response is schema-bound JSON with:

- `trace_id`
- `query`
- `verification_status`
- `matched_signals`
- `rejected_signals`
- `reasoning_path`
- `confidence_breakdown`
- `knowledge_ids_used`
- `domain_resolution`
- `synthesis_mode`

Accepted signals include acceptance reasoning:

- why accepted
- what matched
- content/concept/entity overlap percentages
- confidence derivation formula and derived confidence

## Rejection Categories

Implemented categories include:

- `weak_semantic_alignment`
- `entity_conflict`
- `domain_mismatch`
- `low_contextual_overlap`
- `empty_or_short_content`
- `confidence_below_threshold`
- `no_query_relevance:tags_and_content_both_miss`

Non-answer content such as "not explicitly mentioned" is rejected as `low_contextual_overlap`.

## Ontology Alignment

Ontology seed:

- `backend/ontology/seed_entities.json`
- 100+ canonical entities
- Includes Sanskrit concepts, Purana names, Gita concepts, governance, ecology, dharma systems, and TANTRA preparation terms.

Examples:

- `Gita` maps to `Bhagavad Gita`
- `Vishnu`, `Narayana`, `Hari`, and `Visnu` align
- `Dharma` maps to righteous duty / duty / righteousness
- `Narada-Purana` maps to `Narada Purana`

## Proof Logs

Proof directory:

- `review_packets/proof_logs/`

Generated files:

- `proof_log_summary.json`
- `retrieval_benchmark.json`
- 15 per-trace proof files named `trace_*.json`

Proof run summary:

- Total queries: 15
- Verified knowledge responses: 3
- Deterministic rejections: 12
- Trace continuity: same `trace_id` appears in response payload and per-trace proof file.

Representative traces:

- Successful retrieval: `trace_41f8c9c7d7245fa8`
  - Query: `Tell me about Vishnu in the Narada Purana`
  - Status: `VERIFIED`
  - Synthesis mode: `DETERMINISTIC_FROM_ACCEPTED_SIGNALS`
- Ontology retrieval proof: `trace_d1bf5938862651e4`
  - Query: `Explain the Upanishadic concept of Brahman`
  - Status: `VERIFIED`
- Semantic mismatch proof: `trace_9fadbdd87eec51b3`
  - Query: `Return Upanishads for Bhagavad Gita teachings`
  - Status: `NO_VERIFIED_KNOWLEDGE`
- Required rejection proof: `trace_096358ebc3a25c54`
  - Query: `Give an Ahimsa answer from the Narada Purana`
  - Status: `NO_VERIFIED_KNOWLEDGE`
- External/current-events rejection: `trace_d25c508f97735dbd`
  - Query: `What is the current stock price of Apple?`
  - Status: `NO_VERIFIED_KNOWLEDGE`

## Benchmark Report

Benchmark file:

- `review_packets/proof_logs/retrieval_benchmark.json`

Metrics from final run:

- Precision: `1.0`
- Rejection correctness: `1.0`
- Semantic accuracy: `1.0`

Compared behavior:

- OLD: keyword overlap only.
- NEW: canonical entity extraction, synonym expansion, concept overlap, entity overlap, domain consistency, contextual proximity, and local embedding similarity.

Example benchmark row:

- Query: `Return Upanishads for Bhagavad Gita teachings`
- Expected domain: `gitas`
- Top normalized domain: `gitas`
- Old keyword score: `0.5`
- New ontology score: `0.5694`
- Rejection correctness: `true`

## 10-Query Deterministic Demo

The proof run includes more than 10 deterministic executions. Demo coverage:

- Trace continuity: all 15 outputs write per-trace logs.
- Signal validation: accepted and rejected signals include validation details.
- Ontology matching: Bhagavad Gita, Narada Purana, Vishnu, Padma Purana, Upanishads, and Brahman.
- Rejection correctness:
  - Upanishads for Bhagavad Gita rejected.
  - Ahimsa from Narada Purana rejected.
  - Quantum entanglement from Bhagavad Gita rejected.
  - Current stock price rejected.

## Video Walkthrough Notes

Recommended 5-10 minute walkthrough structure:

1. Show `backend/service/api.py` endpoint boundary and explain that `/new_rag` and `/new_query` now enter the deterministic pipeline.
2. Show `backend/kosha/deterministic_pipeline.py` and walk through the signal contract.
3. Show `backend/ontology/seed_entities.json` and `backend/ontology/entity_resolver.py`.
4. Show `review_packets/proof_logs/proof_log_summary.json`.
5. Open one successful trace and one rejection trace.
6. Open `retrieval_benchmark.json` and explain old vs new metrics.

## Handover Notes

Current limitations:

- The source Kosha data contains legacy OCR artifacts and some very thin entries. The stricter validator correctly rejects many queries rather than stretching weak data into answers.
- Legacy endpoint helper code remains below the early deterministic return in `backend/service/api.py`; it is not executed by `/new_rag` or `/new_query`, but should be removed in a cleanup sprint.
- Domain labels in stored Kosha entries are inconsistent; ontology normalization compensates at runtime.

Next risks:

- If new Kosha entries are auto-persisted by old tooling, they must be schema-clean and ontology-tagged before activation.
- Entity seed governance needs Vijay/Soham review before expanding into a formal TANTRA ontology contract.
- Alay should pin proof execution in CI so proof logs are reproducible across Windows/Linux paths.

Integration dependencies:

- Vijay: confirm trace contract fields for TANTRA execution chain consumption.
- Soham: review canonical entity taxonomy, aliases, and semantic domain standards.
- Alay: wire `python backend/run_proof_log.py` and `python backend/run_retrieval_benchmark.py` into deployment validation.
