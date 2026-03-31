# Roadmap Linter

AI-assisted contradiction and ambiguity detection for roadmaps, PRDs, and OKRs.

## Why this exists

Product documents decay.

Roadmaps drift from strategy.
PRDs contradict launch goals.
Dependencies remain implicit.
Teams align on slides, then execute against something else.

This problem is observed directly in real cross-functional PM environments where planning artifact inconsistency becomes execution misalignment weeks later — after teams have already built toward conflicting goals.

**Roadmap Linter** makes hidden inconsistency visible early by flagging:
- contradiction across docs
- vague requirement language
- missing assumptions
- unresolved dependencies
- questions that must be answered before execution

This tool does not make prioritization decisions for you.
It makes drift and ambiguity harder to ignore.

## What it does

Input:
- roadmap
- PRD
- OKRs
- dependency notes

Output:
- contradiction list
- ambiguity flags
- severity ranking
- missing assumption checklist
- questions to resolve now
- abstention if inputs are incomplete

## What it does not do

- It does not choose roadmap priorities
- It does not rewrite strategy for you
- It does not act as a planning copilot

## Run

```bash
pip install -r requirements.txt
export PYTHONPATH=src
python -m roadmap_linter.cli --roadmap examples/roadmap_sample.md --prd examples/prd_sample.md --okr examples/okr_sample.md
python -m roadmap_linter.eval_runner eval/goldens/doc_sets.jsonl
streamlit run streamlit_app.py
```

## Design choices

- **Constrained contradiction taxonomy** — contradiction types are bounded and auditable, not open-ended inference. v1 uses heuristic pattern matching against a defined taxonomy. This is intentional: a constrained, evaluable heuristic is more trustworthy in a review workflow than a model generating plausible-sounding issues without traceable evidence.
- **Abstention preferred over fake certainty** — if fewer than two planning artifacts are provided, or if the PRD is too sparse, the system abstains rather than flagging spurious contradictions.
- The goal is critique, not content generation — this is the PM design choice that distinguishes it from artifact-generation tools.

## Repo structure

- `src/roadmap_linter/` — core implementation
- `examples/` — sample planning artifacts
- `schemas/` — claim and contradiction JSON schemas
- `eval/` — rubric and evaluation harness
- `demo/` — sample reports

## Portfolio point

This repo critiques planning artifacts instead of generating more of them. The PM value is in the taxonomy design, severity model, and abstention conditions — not the classifier sophistication.

## Known limitations

- contradiction detection is deliberately narrow in v1 — heuristic pattern matching, not semantic inference
- it does not understand every planning nuance or organizational tradeoff
- it is strongest when seeded with realistic contradictory examples
- next upgrade: expand contradiction taxonomy, add semantic similarity layer, grow gold case set

## Where automation stops

- it does not prioritize roadmap items
- it does not rewrite strategy
- it does not resolve contradictions automatically
- humans decide how to act on flagged issues

## Trust boundary

This project is decision support, not automation. It produces structured outputs for human review and abstains when planning evidence is too sparse.
