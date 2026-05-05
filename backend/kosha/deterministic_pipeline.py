"""
Deterministic Kosha Pipeline
Clean OCR → Structured Kosha → Validated Signals → Synthesized Answer

This replaces the silent LLM fallback with explicit NO VERIFIED KNOWLEDGE responses.
Every answer is explainable. No hidden fallback.
"""
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

from kosha.kosha_loader import KoshaLoader
from kosha.kosha_retriever import KoshaRetriever
from kosha.kosha_enforcer import KoshaEnforcer
from kosha.signal_validator import SignalValidator, AnswerSynthesizer, NO_KNOWLEDGE_RESPONSE

logger = logging.getLogger(__name__)

_KOSHA_DIR = Path(__file__).parent.parent / "data" / "kosha"


def run_deterministic_pipeline(
    query: str,
    domain_hint: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full deterministic pipeline:
    1. Load Kosha entries
    2. Validate existing entries (enforce schema)
    3. Retrieve signals via keyword+tag matching
    4. Validate signals against query (domain+tag+content)
    5. Synthesize clean answer OR return NO VERIFIED KNOWLEDGE

    No LLM fallback. No silent failure. Every decision is logged.
    """
    # Phase 1: Load Kosha entries
    loader = KoshaLoader(data_sources=[str(_KOSHA_DIR)])
    raw_entries = loader.load_all()

    # Phase 3: Enforce Kosha schema — validate existing entries
    enforcement_result = KoshaEnforcer.validate_existing_entries(raw_entries)
    valid_entries = enforcement_result["valid_entries"]

    logger.info(
        f"Kosha enforcement: {enforcement_result['valid']}/{enforcement_result['total']} entries valid, "
        f"{enforcement_result['rejected']} rejected"
    )

    if not valid_entries:
        return {
            "answer": NO_KNOWLEDGE_RESPONSE,
            "verification_status": "NO_VERIFIED_KNOWLEDGE",
            "confidence": 0.0,
            "signals_found": 0,
            "signals_rejected": 0,
            "kosha_attempted": True,
            "fallback_to_llm": False,
            "reasoning": "No valid Kosha entries passed schema enforcement.",
            "enforcement_stats": enforcement_result,
        }

    # Phase 2 (retrieval): Get candidate signals from valid entries
    retriever = KoshaRetriever(valid_entries)
    raw_signals, detected_domain = retriever.retrieve(query=query, domain=domain_hint)

    # Phase 4: Deterministic signal validation
    validation_result = SignalValidator.validate_all(
        signals=raw_signals,
        query=query,
    )

    # Phase 6: Answer synthesis
    synthesis = AnswerSynthesizer.synthesize(
        query=query,
        validation_result=validation_result,
    )

    return {
        "answer": synthesis["answer"],
        "verification_status": synthesis["verification_status"],
        "confidence": synthesis["confidence"],
        "signals_found": validation_result["signals_found"],
        "signals_rejected": validation_result["signals_rejected"],
        "signals_accepted": [
            {
                "signal_id": s.get("signal_id"),
                "source": s.get("source"),
                "confidence": s.get("confidence"),
                "tag_match": s.get("_validation", {}).get("matched_tags", []),
                "content_overlap": s.get("_validation", {}).get("content_overlap", 0.0),
            }
            for s in validation_result["accepted_signals"]
        ],
        "signals_rejected_detail": validation_result["rejected_signals"],
        "kosha_attempted": True,
        "fallback_to_llm": False,
        "detected_domain": detected_domain,
        "reasoning": synthesis["reasoning"],
        "enforcement_stats": {
            "total_entries": enforcement_result["total"],
            "valid_entries": enforcement_result["valid"],
            "rejected_entries": enforcement_result["rejected"],
        },
    }


def run_proof_queries(queries: List[str]) -> List[Dict[str, Any]]:
    """
    Run a batch of queries and return structured proof logs.
    Used for generating the 20-query proof log deliverable.
    """
    results = []
    for i, query in enumerate(queries):
        logger.info(f"[{i+1}/{len(queries)}] Query: {query[:60]}...")
        result = run_deterministic_pipeline(query)
        results.append({
            "query_number": i + 1,
            "query": query,
            "answer": result["answer"],
            "verification_status": result["verification_status"],
            "confidence": result["confidence"],
            "signals_found": result["signals_found"],
            "signals_rejected": result["signals_rejected"],
            "reasoning": result["reasoning"],
        })
    return results
