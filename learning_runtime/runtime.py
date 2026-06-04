from __future__ import annotations

from typing import Any, Dict, List, Optional

from retrieval.masterdb_retriever import retrieve_from_masterdb


def build_learning_runtime(
    question: str,
    grade: Optional[int] = None,
    medium: Optional[str] = None,
    subject: Optional[str] = None,
) -> Dict[str, Any]:
    runtime_payload = retrieve_from_masterdb(question, grade, medium, subject)
    record = runtime_payload["response_payload"].get("matched_record") or {}
    matched = bool(record)
    follow_up_concepts: List[str] = []
    if matched:
        base = record.get("concept") or "Curriculum concept"
        follow_up_concepts = [
            f"Related idea: {record.get('chapter')} understanding",
            f"Practice: explain why {base} matters",
            f"Extension: connect {base} to daily life",
        ]
    else:
        follow_up_concepts = [
            "Curriculum seed needs expansion",
            "Collect grade-level standards for this subject",
            "Map question to Balbharti chapter taxonomy",
        ]

    learning_outcome = (
        record.get("learning_outcome")
        if record.get("learning_outcome")
        else f"Understand the concept of {record.get('concept')} through Balbharti curriculum guidance."
    )

    return {
        "student_question": question,
        "retrieval": {
            "matched": matched,
            "grade": grade,
            "medium": medium,
            "subject": subject,
            "retrieval_confidence": runtime_payload["response_payload"].get("retrieval_confidence", 0.0),
            "matched_record_id": record.get("record_id"),
        },
        "concept_match": {
            "concept": record.get("concept"),
            "chapter": record.get("chapter"),
            "subject": record.get("subject"),
            "learning_outcome": learning_outcome,
        },
        "curriculum_mapping": {
            "source_lineage": record.get("source_lineage"),
            "curriculum_version": record.get("curriculum_version"),
            "provenance_status": (record.get("source_lineage") or {}).get("provenance_status"),
        },
        "explanation": runtime_payload["response_payload"].get("answer"),
        "follow_up_concepts": follow_up_concepts,
        "learning_outcome": learning_outcome,
        "trace_artifact": {
            "trace_id": runtime_payload["trace_id"],
            "runtime_hash": runtime_payload["runtime_hash"],
            "schema_version": runtime_payload["schema_version"],
        },
    }
