
from __future__ import annotations
from typing import Any

AMBIGUOUS_PHRASES = [
    "fast", "intuitive", "seamless", "optimized", "minimal impact",
    "improve significantly", "lightweight", "easy to use"
]

def _norm(text: str) -> str:
    return (text or "").lower()

def detect_ambiguity(text: str, source: str) -> list[str]:
    flags = []
    lower = _norm(text)
    for phrase in AMBIGUOUS_PHRASES:
        if phrase in lower:
            flags.append(f"{source} uses vague language: '{phrase}'")
    return flags

def missing_assumptions(roadmap: str, prd: str, okr: str) -> list[str]:
    missing = []
    all_text = _norm("\n".join([roadmap, prd, okr]))
    if "owner:" not in _norm(prd):
        missing.append("PRD does not specify a clear owner")
    if "dependencies:" not in _norm(prd):
        missing.append("PRD does not specify dependencies")
    if "rollout" in all_text and "guardrail" not in all_text:
        missing.append("Rollout plan lacks explicit guardrails or stop conditions")
    return missing

def should_abstain(roadmap: str, prd: str, okr: str) -> tuple[bool, list[str]]:
    present = sum(bool(x.strip()) for x in [roadmap, prd, okr])
    reasons = []
    if present < 2:
        reasons.append("Fewer than two planning artifacts provided")
    if len(prd.strip()) < 40:
        reasons.append("PRD is too sparse to compare meaningfully")
    return bool(reasons), reasons

def detect_contradictions(roadmap: str, prd: str, okr: str) -> list[dict[str, Any]]:
    roadmap_l = _norm(roadmap)
    prd_l = _norm(prd)
    okr_l = _norm(okr)
    contradictions = []

    if ("minimize checkout changes" in roadmap_l and
        ("redesign shipping" in prd_l or "redesign payment" in prd_l or "one-page checkout" in prd_l)):
        contradictions.append({
            "contradiction_id": "C-001",
            "severity": "high",
            "source_a": "roadmap",
            "source_b": "prd",
            "issue_type": "strategy_scope_conflict",
            "explanation": "Roadmap minimizes checkout changes while PRD scopes a broad checkout redesign.",
            "questions_to_resolve": [
                "Which checkout changes are explicitly allowed this quarter?",
                "What scope should be deferred until migration risk is lower?"
            ]
        })

    if ("migration" in prd_l and "100% rollout" in prd_l and "keep launch risk low" in okr_l):
        contradictions.append({
            "contradiction_id": "C-002",
            "severity": "high",
            "source_a": "prd",
            "source_b": "okr",
            "issue_type": "risk_goal_conflict",
            "explanation": "PRD targets full rollout during migration while OKRs emphasize low launch risk.",
            "questions_to_resolve": [
                "Should rollout be phased instead of 100%?",
                "What risk threshold must be met before broad rollout?"
            ]
        })

    if ("freeze search changes" in roadmap_l and "add 8 new filters" in prd_l):
        contradictions.append({
            "contradiction_id": "C-003",
            "severity": "high",
            "source_a": "roadmap",
            "source_b": "prd",
            "issue_type": "dependency_timing_conflict",
            "explanation": "Roadmap freezes search changes while PRD introduces substantial search scope.",
            "questions_to_resolve": [
                "Is the freeze still active?",
                "What dependency must be resolved before filters ship?"
            ]
        })

    if ("incident unresolved" in prd_l and "reduce search incidents" in okr_l and "launch new search filters" in roadmap_l):
        contradictions.append({
            "contradiction_id": "C-004",
            "severity": "medium",
            "source_a": "prd",
            "source_b": "okr",
            "issue_type": "risk_goal_conflict",
            "explanation": "Launch scope depends on an unresolved backend incident while OKRs emphasize incident reduction.",
            "questions_to_resolve": [
                "Should launch wait for incident resolution?",
                "What fallback plan exists if backend instability persists?"
            ]
        })

    return contradictions

def lint_documents(roadmap: str, prd: str, okr: str) -> dict[str, Any]:
    abstain, reasons = should_abstain(roadmap, prd, okr)
    if abstain:
        return {
            "status": "abstained",
            "sources_reviewed": [s for s, t in [("roadmap", roadmap), ("prd", prd), ("okr", okr)] if t.strip()],
            "contradictions": [],
            "ambiguity_flags": [],
            "missing_assumptions": reasons,
            "questions_to_resolve": [
                "Provide at least two complete planning artifacts",
                "Add clearer goals, dependencies, and rollout assumptions"
            ]
        }

    contradictions = detect_contradictions(roadmap, prd, okr)
    ambiguity = detect_ambiguity(roadmap, "roadmap") + detect_ambiguity(prd, "prd") + detect_ambiguity(okr, "okr")
    missing = missing_assumptions(roadmap, prd, okr)

    questions = []
    for c in contradictions:
        questions.extend(c["questions_to_resolve"])
    if ambiguity:
        questions.append("Which vague success criteria should be rewritten into measurable terms?")
    if missing:
        questions.append("Which missing assumptions must be documented before execution starts?")

    return {
        "status": "lint_ready",
        "sources_reviewed": ["roadmap", "prd", "okr"],
        "contradictions": contradictions,
        "ambiguity_flags": ambiguity,
        "missing_assumptions": missing,
        "questions_to_resolve": questions[:8],
    }
