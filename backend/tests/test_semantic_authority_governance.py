from __future__ import annotations

from governance.semantic_authority import (
    ContradictionEscalationGovernance,
    SemanticDriftObservabilityEngine,
    TrustBoundSemanticWeightingFramework,
    UncertaintyLineageTracker,
)


def _snapshots():
    previous = {
        "snapshot_version": 1,
        "concepts": [
            {
                "concept_id": "root",
                "canonical_name": "Governed Claim",
                "parent_id": None,
                "truth_level": 3,
                "domain": "core",
                "immutable": False,
            }
        ],
    }
    current = {
        "snapshot_version": 1,
        "concepts": [
            {
                "concept_id": "root",
                "canonical_name": "Self-Legitimized Claim",
                "parent_id": None,
                "truth_level": 3,
                "domain": "core",
                "immutable": False,
            }
        ],
    }
    return previous, current


def _events():
    return [
        {
            "trace_id": "semantic_pressure_1",
            "claim_key": "governed_claim",
            "confidence": 0.41,
            "reinforcement_count": 1,
            "contradiction_pressure": 0.0,
            "uncertainty": 0.48,
            "ambiguity_class": "interpretive",
            "unresolved": True,
        },
        {
            "trace_id": "semantic_pressure_2",
            "claim_key": "governed_claim",
            "confidence": 0.92,
            "reinforcement_count": 5,
            "contradiction_pressure": 0.75,
            "uncertainty": 0.52,
            "ambiguity_class": "conflicting_claims",
            "unresolved": True,
        },
    ]


def test_semantic_drift_observability_exposes_pressure_without_authority():
    previous, current = _snapshots()
    telemetry = SemanticDriftObservabilityEngine.observe(
        previous_snapshot=previous,
        current_snapshot=current,
        semantic_events=_events(),
    )

    assert telemetry["observable_only"] is True
    assert telemetry["canonical_authority_granted"] is False
    assert telemetry["ontology_drift"]["accepted"] is False
    assert telemetry["ontology_drift"]["violations"][0]["type"] == "canonical_name_change_requires_version_bump"
    assert telemetry["confidence_pressure"]["inflation_detected"] is True
    assert telemetry["reinforcement_pressure"]["authority_accumulation_detected"] is True
    assert telemetry["semantic_continuity_pressure"]["bounded_continuity_required"] is True
    assert telemetry["authority_gravity"]["authority_gravity_detected"] is True
    assert telemetry["telemetry_hash"]


def test_contradiction_escalation_preserves_lineage_and_blocks_silent_merge():
    result = ContradictionEscalationGovernance.evaluate(
        contradictions=[
            {
                "claim_key": "governed_claim",
                "signal_ids": ["signal_a", "signal_b"],
                "polarities": ["affirmative", "negative"],
            }
        ],
        signals=[{"signal_id": "signal_a"}, {"signal_id": "signal_b"}],
        prior_unresolved_count=0,
        quorum_required=2,
    )

    assert result["lifecycle_state"] == "ESCALATED"
    assert result["action"] == "QUARANTINE_AND_REQUIRE_REVIEW"
    assert result["canonical_authority_granted"] is False
    assert result["lineage_preserved"] is True
    assert result["silent_merge_allowed"] is False
    assert result["audit_hash"]


def test_persistent_unresolved_contradiction_escalates_harder():
    result = ContradictionEscalationGovernance.evaluate(
        contradictions=[{"claim_key": "governed_claim"}],
        signals=[{"signal_id": "signal_a"}],
        prior_unresolved_count=2,
    )

    assert result["lifecycle_state"] == "PERSISTENT_UNRESOLVED"
    assert result["action"] == "QUARANTINE_AND_ESCALATE_REVIEW"


def test_weighting_rejects_confidence_inflation_as_legitimacy():
    result = TrustBoundSemanticWeightingFramework.score(
        confidence=0.94,
        prior_confidence=0.42,
        provenance_weight=0.36,
        legitimacy_evidence=0.22,
        reinforcement_count=6,
        contradiction_pressure=0.2,
        uncertainty=0.44,
    )

    assert result["confidence_inflation_detected"] is True
    assert result["reinforcement_abuse_detected"] is True
    assert result["boundary_decision"] == "REJECT_LEGITIMACY_ESCALATION"
    assert result["trust_score"] < result["confidence"]
    assert result["discipline"]["confidence_is_not_legitimacy"] is True
    assert result["discipline"]["reinforcement_is_not_truth_authority"] is True


def test_uncertainty_lineage_reconstruction_is_replay_safe():
    first = UncertaintyLineageTracker.reconstruct(_events(), lineage_id="lineage_fixture")
    replay = UncertaintyLineageTracker.reconstruct(_events(), lineage_id="lineage_fixture")

    assert first["replay_safe"] is True
    assert first["lineage_state_hash"] == replay["lineage_state_hash"]
    assert first["lineage"][1]["previous_lineage_hash"] == first["lineage"][0]["lineage_hash"]
    assert first["lineage"][1]["contradiction_pressure"] == 0.75
