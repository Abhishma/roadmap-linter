
from roadmap_linter.logic import lint_documents

def test_abstain_on_sparse_inputs():
    report = lint_documents("", "Goal: improve checkout", "")
    assert report["status"] == "abstained"

def test_detects_core_conflict():
    roadmap = "Minimize checkout changes this quarter due to payment migration risk"
    prd = "Scope: redesign shipping and payment workflows\nDependencies: payment gateway migration in progress\nRollout: 100% rollout targeted in 2 weeks\nOwner: Product"
    okr = "Keep launch risk low during migration"
    report = lint_documents(roadmap, prd, okr)
    issue_types = {c["issue_type"] for c in report["contradictions"]}
    assert "strategy_scope_conflict" in issue_types or "risk_goal_conflict" in issue_types
