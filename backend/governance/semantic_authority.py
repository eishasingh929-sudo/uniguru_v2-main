from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory.constitutional_semantic_memory import stable_hash, utc_now_iso
from ontology.drift_detector import detect_semantic_drift


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 4)


def _signal_ids(signals: List[Dict[str, Any]]) -> List[str]:
    return sorted(str(signal.get("signal_id") or "unknown") for signal in signals)


class SemanticDriftObservabilityEngine:
    """Deterministic drift telemetry. It observes pressure; it does not mutate truth."""

    @classmethod
    def observe(
        cls,
        *,
        previous_snapshot: Dict[str, Any],
        current_snapshot: Dict[str, Any],
        semantic_events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        drift = detect_semantic_drift(previous_snapshot, current_snapshot)
        lineage = cls._ontology_lineage(previous_snapshot, current_snapshot)
        confidence_pressure = cls._confidence_pressure(semantic_events)
        reinforcement_pressure = cls._reinforcement_pressure(semantic_events)
        continuity_pressure = cls._continuity_pressure(semantic_events)
        authority_gravity = AuthorityGravityDiagnostics.evaluate(
            confidence_pressure=confidence_pressure,
            reinforcement_pressure=reinforcement_pressure,
            continuity_pressure=continuity_pressure,
            contradiction_pressure=max(
                [float(event.get("contradiction_pressure") or 0.0) for event in semantic_events] or [0.0]
            ),
            ontology_violation_count=len(drift.get("violations") or []),
        )

        telemetry = {
            "schema": "UNIGURU_SEMANTIC_DRIFT_OBSERVABILITY_V1",
            "observed_at": utc_now_iso(),
            "observable_only": True,
            "canonical_authority_granted": False,
            "ontology_drift": drift,
            "ontology_mutation_lineage": lineage,
            "confidence_pressure": confidence_pressure,
            "reinforcement_pressure": reinforcement_pressure,
            "semantic_continuity_pressure": continuity_pressure,
            "authority_gravity": authority_gravity,
            "rules": [
                "drift_observation_never_mutates_ontology",
                "confidence_growth_is_pressure_not_legitimacy",
                "reinforcement_frequency_is_not_truth_authority",
                "continuity_does_not_grant_canonical_authority",
            ],
        }
        telemetry["telemetry_hash"] = stable_hash(telemetry)
        return telemetry

    @staticmethod
    def _ontology_lineage(previous_snapshot: Dict[str, Any], current_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        previous = {row["concept_id"]: row for row in previous_snapshot.get("concepts", [])}
        current = {row["concept_id"]: row for row in current_snapshot.get("concepts", [])}
        lineage: List[Dict[str, Any]] = []

        for concept_id in sorted(set(previous) | set(current)):
            before = previous.get(concept_id)
            after = current.get(concept_id)
            if before is None:
                mutation_type = "concept_added"
            elif after is None:
                mutation_type = "concept_removed"
            else:
                changed_fields = sorted(
                    key for key in {"canonical_name", "parent_id", "truth_level", "domain"} if before.get(key) != after.get(key)
                )
                if not changed_fields:
                    continue
                mutation_type = "concept_changed"

            lineage.append(
                {
                    "concept_id": concept_id,
                    "mutation_type": mutation_type,
                    "previous_hash": stable_hash(before) if before is not None else None,
                    "current_hash": stable_hash(after) if after is not None else None,
                    "changed_fields": [] if before is None or after is None else changed_fields,
                }
            )
        return lineage

    @staticmethod
    def _confidence_pressure(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        scores = [float(event.get("confidence") or 0.0) for event in events]
        if not scores:
            return {"score": 0.0, "inflation_detected": False, "max_delta": 0.0, "event_count": 0}
        deltas = [round(scores[index] - scores[index - 1], 4) for index in range(1, len(scores))]
        max_delta = max(deltas or [0.0])
        high_confidence_count = sum(1 for score in scores if score >= 0.85)
        pressure = _clamp((max_delta * 1.6) + (high_confidence_count / max(len(scores), 1) * 0.35))
        return {
            "score": pressure,
            "inflation_detected": pressure >= 0.55,
            "max_delta": round(max_delta, 4),
            "event_count": len(scores),
            "high_confidence_count": high_confidence_count,
        }

    @staticmethod
    def _reinforcement_pressure(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for event in events:
            claim_key = str(event.get("claim_key") or "unclassified_claim")
            counts[claim_key] = counts.get(claim_key, 0) + int(event.get("reinforcement_count") or 0)
        max_reinforcement = max(counts.values() or [0])
        pressure = _clamp(max_reinforcement / 5.0)
        return {
            "score": pressure,
            "authority_accumulation_detected": pressure >= 0.6,
            "max_reinforcement_count": max_reinforcement,
            "claim_reinforcement_counts": {key: counts[key] for key in sorted(counts)},
        }

    @staticmethod
    def _continuity_pressure(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        trace_ids = {str(event.get("trace_id") or "") for event in events if event.get("trace_id")}
        unresolved = sum(1 for event in events if bool(event.get("unresolved")))
        pressure = _clamp((len(events) / 8.0) + (unresolved / max(len(events), 1) * 0.4))
        return {
            "score": pressure,
            "bounded_continuity_required": pressure >= 0.5,
            "event_count": len(events),
            "trace_count": len(trace_ids),
            "unresolved_event_count": unresolved,
        }


class ContradictionEscalationGovernance:
    """Contradiction lifecycle. Contradictions become audit states, not merged truth."""

    @classmethod
    def evaluate(
        cls,
        *,
        contradictions: List[Dict[str, Any]],
        signals: List[Dict[str, Any]],
        prior_unresolved_count: int = 0,
        quorum_required: int = 2,
    ) -> Dict[str, Any]:
        contradiction_count = len(contradictions)
        evidence_count = len(_signal_ids(signals))
        quorum_met = evidence_count >= quorum_required

        if contradiction_count == 0:
            state = "NO_CONTRADICTION"
            action = "ALLOW_WITH_NO_CONTRADICTION"
        elif prior_unresolved_count > 0:
            state = "PERSISTENT_UNRESOLVED"
            action = "QUARANTINE_AND_ESCALATE_REVIEW"
        elif quorum_met:
            state = "ESCALATED"
            action = "QUARANTINE_AND_REQUIRE_REVIEW"
        else:
            state = "OBSERVED"
            action = "PERSIST_AS_UNRESOLVED_AUDIT"

        trace = {
            "schema": "UNIGURU_CONTRADICTION_REPLAY_AUDIT_V1",
            "lifecycle_state": state,
            "action": action,
            "quorum": {
                "required": quorum_required,
                "evidence_count": evidence_count,
                "met": quorum_met,
            },
            "prior_unresolved_count": int(prior_unresolved_count),
            "signal_ids": _signal_ids(signals),
            "contradictions": contradictions,
            "canonical_authority_granted": False if contradiction_count else None,
            "lineage_preserved": True,
            "silent_merge_allowed": False,
        }
        trace["audit_hash"] = stable_hash(trace)
        return trace


class TrustBoundSemanticWeightingFramework:
    """Separates truth-likelihood confidence from legitimacy and provenance trust."""

    CONFIDENCE_INFLATION_DELTA = 0.25

    @classmethod
    def score(
        cls,
        *,
        confidence: float,
        prior_confidence: float,
        provenance_weight: float,
        legitimacy_evidence: float,
        reinforcement_count: int,
        contradiction_pressure: float,
        uncertainty: float,
    ) -> Dict[str, Any]:
        confidence = _clamp(confidence)
        prior_confidence = _clamp(prior_confidence)
        provenance_weight = _clamp(provenance_weight)
        legitimacy_evidence = _clamp(legitimacy_evidence)
        contradiction_pressure = _clamp(contradiction_pressure)
        uncertainty = _clamp(uncertainty)
        reinforcement_pressure = _clamp(reinforcement_count / 5.0)

        confidence_delta = round(confidence - prior_confidence, 4)
        legitimacy_ceiling = _clamp(
            (0.48 * provenance_weight)
            + (0.32 * legitimacy_evidence)
            - (0.35 * contradiction_pressure)
            - (0.2 * uncertainty)
        )
        trust_score = _clamp(min(confidence, legitimacy_ceiling))
        inflation_detected = confidence_delta > cls.CONFIDENCE_INFLATION_DELTA and legitimacy_ceiling < confidence
        reinforcement_abuse_detected = reinforcement_pressure >= 0.6 and legitimacy_evidence < 0.5

        result = {
            "schema": "UNIGURU_TRUST_BOUND_SEMANTIC_WEIGHTING_V1",
            "confidence": confidence,
            "prior_confidence": prior_confidence,
            "confidence_delta": confidence_delta,
            "legitimacy_ceiling": legitimacy_ceiling,
            "trust_score": trust_score,
            "reinforcement_pressure": reinforcement_pressure,
            "confidence_inflation_detected": inflation_detected,
            "reinforcement_abuse_detected": reinforcement_abuse_detected,
            "canonical_authority_granted": False,
            "uncertainty_preserved": uncertainty > 0.0 or contradiction_pressure > 0.0,
            "boundary_decision": "REJECT_LEGITIMACY_ESCALATION"
            if inflation_detected or reinforcement_abuse_detected or contradiction_pressure > 0
            else "OBSERVE_WITH_BOUNDED_TRUST",
            "discipline": {
                "confidence_is_not_legitimacy": True,
                "reinforcement_is_not_truth_authority": True,
                "uncertainty_reduces_trust_ceiling": True,
                "contradiction_blocks_legitimacy_escalation": contradiction_pressure > 0,
            },
        }
        result["weighting_hash"] = stable_hash(result)
        return result


class AuthorityGravityDiagnostics:
    """Pressure metric for authority accumulation attempts."""

    @staticmethod
    def evaluate(
        *,
        confidence_pressure: Dict[str, Any],
        reinforcement_pressure: Dict[str, Any],
        continuity_pressure: Dict[str, Any],
        contradiction_pressure: float,
        ontology_violation_count: int,
    ) -> Dict[str, Any]:
        score = _clamp(
            (0.28 * float(confidence_pressure.get("score") or 0.0))
            + (0.28 * float(reinforcement_pressure.get("score") or 0.0))
            + (0.2 * float(continuity_pressure.get("score") or 0.0))
            + (0.14 * float(contradiction_pressure or 0.0))
            + (0.1 * min(int(ontology_violation_count), 3) / 3.0)
        )
        return {
            "score": score,
            "authority_gravity_detected": score >= 0.55,
            "diagnostic_inputs": {
                "confidence_pressure_score": float(confidence_pressure.get("score") or 0.0),
                "reinforcement_pressure_score": float(reinforcement_pressure.get("score") or 0.0),
                "continuity_pressure_score": float(continuity_pressure.get("score") or 0.0),
                "contradiction_pressure": _clamp(contradiction_pressure),
                "ontology_violation_count": int(ontology_violation_count),
            },
            "governance_response": "ESCALATE_OBSERVABILITY"
            if score >= 0.55
            else "OBSERVE_WITH_STANDARD_TELEMETRY",
        }


class UncertaintyLineageTracker:
    """Replay-safe uncertainty lineage reconstruction helper."""

    @staticmethod
    def reconstruct(events: List[Dict[str, Any]], *, lineage_id: Optional[str] = None) -> Dict[str, Any]:
        rows = []
        previous_hash: Optional[str] = None
        for index, event in enumerate(events):
            row = {
                "index": index,
                "trace_id": event.get("trace_id"),
                "claim_key": event.get("claim_key"),
                "uncertainty": _clamp(event.get("uncertainty") or 0.0),
                "ambiguity_class": event.get("ambiguity_class") or "unspecified",
                "contradiction_pressure": _clamp(event.get("contradiction_pressure") or 0.0),
                "previous_lineage_hash": previous_hash,
            }
            row["lineage_hash"] = stable_hash(row)
            previous_hash = row["lineage_hash"]
            rows.append(row)

        payload = {
            "schema": "UNIGURU_UNCERTAINTY_LINEAGE_V1",
            "lineage_id": lineage_id or stable_hash({"events": events}),
            "event_count": len(rows),
            "lineage": rows,
            "replay_safe": True,
            "last_lineage_hash": previous_hash,
        }
        payload["lineage_state_hash"] = stable_hash(payload)
        return payload
