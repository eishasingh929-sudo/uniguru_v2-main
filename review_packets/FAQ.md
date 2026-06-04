# UniGuru Sprint FAQ

## What is the canonical runtime entry point?
The canonical runtime entry point for this sprint is `backend/service/uniguru_runtime_api.py`. It drives MasterDB retrieval and governance through `backend/governance/constitutional_runtime.py`.

## Where is the curriculum stored?
The canonical curriculum path is `masterdb/balbharti/`. This directory contains the sample ingestion dataset, lineage schema, ingestion manifest, and proof artifacts.

## What files define the curriculum schema?
The canonical curriculum schema is `curriculum/curriculum_schema_v1.json`. The current sample coverage report is in `curriculum/coverage_report.json`.

## How do I generate retrieval metadata and trace artifacts?
Use `retrieval/masterdb_retriever.py` to generate retrieval artifacts programmatically. A sample artifact is stored in `retrieval/retrieval_artifact.json`.

## What is the new learning runtime flow?
The learning runtime flow is documented in `learning_runtime/learning_runtime_flow.json`, and implemented in `learning_runtime/runtime.py`.

## What curriculum coverage is missing?
The current sample seed covers only grades 1, 3, and 6 in Mathematics, EVS, and Science. Missing grades are 2, 4, 5, 7, 8, 9, and 10, and missing subjects include History, Geography, and Language.

## What should I use for dashboard visibility?
Use `masterdb/masterdb_dashboard.json` for subject, grade, chapter visibility and missing coverage analysis.

## Does this sprint change governance?
No. Governance remains anchored in `backend/governance/constitutional_runtime.py`. This sprint does not redesign authority systems or create parallel runtimes.

## How do I validate the Balbharti ingestion?
Run `python scripts/ingest_balbharti_masterdb.py`. It validates the dataset and writes `masterdb/balbharti/ingestion_manifest.json` and the proof file `review_packets/proof_logs/balbharti_masterdb_ingestion_proof.json`.
