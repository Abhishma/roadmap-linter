
from __future__ import annotations
from pathlib import Path
import json
import streamlit as st

from roadmap_linter.logic import lint_documents

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"

st.set_page_config(page_title="Roadmap Linter", layout="wide")
st.title("Roadmap Linter")
st.caption("AI-assisted contradiction and ambiguity detection across roadmap, PRD, and OKR artifacts.")

example_set = st.sidebar.selectbox("Example set", ["Main contradiction set", "Sparse abstention case"])

if example_set == "Main contradiction set":
    roadmap = (EXAMPLES / "roadmap_sample.md").read_text()
    prd = (EXAMPLES / "prd_sample.md").read_text()
    okr = (EXAMPLES / "okr_sample.md").read_text()
else:
    roadmap = ""
    prd = (EXAMPLES / "sparse_prd_sample.md").read_text()
    okr = ""

col1, col2 = st.columns(2)
with col1:
    st.subheader("Inputs")
    st.markdown("### Roadmap")
    st.code(roadmap or "[missing]")
    st.markdown("### PRD")
    st.code(prd or "[missing]")
    st.markdown("### OKR")
    st.code(okr or "[missing]")

with col2:
    st.subheader("Lint report")
    report = lint_documents(roadmap, prd, okr)
    st.json(report)
    if report["status"] == "abstained":
        st.warning("System abstained because the planning evidence is incomplete.")
    else:
        st.success(f"Found {len(report['contradictions'])} contradiction(s)")

st.markdown("---")
st.subheader("Portfolio interpretation")
if report["status"] == "abstained":
    st.write("This refusal is a feature. The system avoids fake certainty when the planning evidence is too sparse.")
else:
    st.write("This repo is designed to critique planning artifacts, not generate more PM theater.")
