
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

from .logic import lint_documents
from .utils import load_jsonl

def main() -> None:
    parser = argparse.ArgumentParser(description="Run eval over seeded planning doc sets.")
    parser.add_argument("gold_path")
    args = parser.parse_args()

    golds = load_jsonl(Path(args.gold_path))
    total = len(golds)
    abstain_ok = 0
    issue_hits = 0
    issue_total = 0
    rows = []
    pred_dist = Counter()
    exp_dist = Counter()

    for g in golds:
        report = lint_documents(g["roadmap_text"], g["prd_text"], g["okr_text"])
        predicted_types = {c["issue_type"] for c in report["contradictions"]}
        expected_types = set(g["expected_issue_types"])
        if "ambiguity_flag" in expected_types and report["ambiguity_flags"]:
            predicted_types.add("ambiguity_flag")

        issue_hits += len(predicted_types & expected_types)
        issue_total += max(len(expected_types), 1)
        abstain_case_ok = (report["status"] == "abstained") == g["should_abstain"]
        abstain_ok += int(abstain_case_ok)

        for p in predicted_types:
            pred_dist[p] += 1
        for e in expected_types:
            exp_dist[e] += 1

        rows.append({
            "case_id": g["case_id"],
            "predicted_types": sorted(predicted_types),
            "expected_types": sorted(expected_types),
            "status": report["status"],
            "abstain_ok": abstain_case_ok
        })

    summary = {
        "total_cases": total,
        "issue_match_score": round(issue_hits / issue_total, 3) if issue_total else 0.0,
        "abstention_accuracy": round(abstain_ok / total, 3) if total else 0.0,
        "predicted_distribution": dict(pred_dist),
        "expected_distribution": dict(exp_dist),
        "rows": rows
    }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
