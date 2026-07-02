from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from service.ecosystem_runtime import execute_ecosystem_runtime


def test_execute_ecosystem_runtime_emits_evidence():
    temp_dir = tempfile.mkdtemp(prefix="ecosystem_test_", dir=".")
    proof_dir = Path(temp_dir) / "proofs"
    result = execute_ecosystem_runtime(
        query="What is the Bhagavad Gita?",
        proof_dir=proof_dir,
        emit_proof=True,
    )

    assert result["trace_id"].startswith("ecosystem_")
    assert result["vijay_validation"]["replay_safe"] is True
    assert result["tantra_contract"]["verification_status"] in {"VERIFIED", "NO_VERIFIED_KNOWLEDGE", "PARTIAL"}
    assert result["bucket_telemetry"]["emitted"] is True
    assert result["insightflow_observability"]["trace_complete"] is True
    assert result["gc_validation"]["authority_enforced"] is True
    assert result["mdu_validation"]["schema_compatible"] is True
    assert (proof_dir / "ecosystem_execution_latest.json").exists()
