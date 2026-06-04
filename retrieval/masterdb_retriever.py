from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.service.uniguru_runtime_api import RuntimeRequest, execute_runtime
from backend.memory.constitutional_semantic_memory import stable_hash


def retrieve_from_masterdb(
    query: str,
    grade: Optional[int] = None,
    medium: Optional[str] = None,
    subject: Optional[str] = None,
) -> Dict[str, Any]:
    request = RuntimeRequest(
        query=query,
        grade=grade,
        medium=medium,
        subject=subject,
        emit_proof=False,
    )
    return execute_runtime(request)


def generate_retrieval_artifact(
    query: str,
    grade: Optional[int] = None,
    medium: Optional[str] = None,
    subject: Optional[str] = None,
) -> Dict[str, Any]:
    runtime_payload = retrieve_from_masterdb(query=query, grade=grade, medium=medium, subject=subject)
    record = runtime_payload["response_payload"].get("matched_record") or {}
    return {
        "trace_id": runtime_payload["trace_id"],
        "query": query,
        "retrieved_concepts": [record.get("concept")] if record else [],
        "curriculum_version": record.get("curriculum_version"),
        "knowledge_hash": stable_hash(record) if record else None,
        "source_lineage": record.get("source_lineage"),
        "confidence_state": {
            "confidence": runtime_payload["response_payload"].get("retrieval_confidence", 0.0),
            "classification": runtime_payload["uncertainty_state"]["classification"],
        },
        "matched_record": record,
    }
