
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .logic import lint_documents
from .utils import load_text

def main() -> None:
    parser = argparse.ArgumentParser(description="Lint roadmap, PRD, and OKR documents.")
    parser.add_argument("--roadmap", required=False, default="")
    parser.add_argument("--prd", required=False, default="")
    parser.add_argument("--okr", required=False, default="")
    args = parser.parse_args()

    roadmap = load_text(Path(args.roadmap)) if args.roadmap else ""
    prd = load_text(Path(args.prd)) if args.prd else ""
    okr = load_text(Path(args.okr)) if args.okr else ""

    report = lint_documents(roadmap, prd, okr)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
