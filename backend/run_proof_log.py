"""
Proof Log Generator — Isha Task Deliverable
Runs 20+ queries through the deterministic Kosha pipeline.
Produces: signals found, signals rejected, confidence reasoning.
Includes 5+ queries that return NO VERIFIED KNOWLEDGE.
"""
import sys
import os
import json
import logging
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.WARNING)

from kosha.deterministic_pipeline import run_deterministic_pipeline

PROOF_QUERIES = [
    # Queries expected to FIND knowledge
    "What is the Bhagavad Gita?",
    "Tell me about the Upanishads",
    "What does the Mahabharata say about dharma?",
    "Explain the concept of karma in Hindu philosophy",
    "What are the Vedas?",
    "Tell me about Vishnu in the Puranas",
    "What is the significance of the Narada Purana?",
    "Explain the teachings of the Bhagavad Gita on decision making",
    "What is Brahman according to the Upanishads?",
    "Tell me about tantra and the Bhairava tradition",
    "What does the Ramayana teach?",
    "Explain the concept of yoga in the Upanishads",
    "What is the Tripura Rahasya?",
    "Tell me about Indra in the Puranas",
    "What are the teachings on self-realization?",
    # Queries expected to return NO VERIFIED KNOWLEDGE
    "What is the current stock price of Apple?",
    "Who won the cricket match yesterday?",
    "What is the latest news from Ukraine?",
    "Explain quantum entanglement in physics",
    "What is the GDP of India in 2024?",
    "How do I fix a Python import error?",
    "What is the recipe for biryani?",
]


def run_proof_log():
    results = []
    no_knowledge_count = 0
    knowledge_found_count = 0

    print("=" * 70)
    print("UNIGURU DETERMINISTIC KOSHA PIPELINE — PROOF LOG")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    for i, query in enumerate(PROOF_QUERIES):
        result = run_deterministic_pipeline(query)

        status = result["verification_status"]
        confidence = result["confidence"]
        signals_found = result["signals_found"]
        signals_rejected = result["signals_rejected"]
        answer = result["answer"]
        reasoning = result["reasoning"]

        if status == "NO_VERIFIED_KNOWLEDGE":
            no_knowledge_count += 1
        else:
            knowledge_found_count += 1

        entry = {
            "query_number": i + 1,
            "query": query,
            "verification_status": status,
            "confidence": confidence,
            "signals_found": signals_found,
            "signals_rejected": signals_rejected,
            "answer_preview": answer[:120] + "..." if len(answer) > 120 else answer,
            "reasoning": reasoning,
        }
        results.append(entry)

        # Print to console
        print(f"\n[{i+1:02d}] {query}")
        print(f"     Status    : {status}")
        print(f"     Confidence: {confidence:.4f}")
        print(f"     Signals   : {signals_found} found, {signals_rejected} rejected")
        print(f"     Answer    : {entry['answer_preview']}")
        print(f"     Reasoning : {reasoning}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print(f"  Total queries       : {len(PROOF_QUERIES)}")
    print(f"  Knowledge found     : {knowledge_found_count}")
    print(f"  NO VERIFIED KNOWLEDGE: {no_knowledge_count}")
    print("=" * 70)

    # Save proof log
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "review_packets", "proof_log.json"
    )
    output_path = os.path.normpath(output_path)

    proof_log = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": "deterministic_kosha_v2",
        "total_queries": len(PROOF_QUERIES),
        "knowledge_found": knowledge_found_count,
        "no_verified_knowledge": no_knowledge_count,
        "results": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(proof_log, f, indent=2, ensure_ascii=False)

    print(f"\nProof log saved to: {output_path}")
    return proof_log


if __name__ == "__main__":
    run_proof_log()
