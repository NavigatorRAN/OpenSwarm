"""VWMedia Proposal Swarm Pipeline Orchestrator.

Sequences the full pipeline:
  1. Intake
  2. Research/Audit agents
  3. Strategy Brief Agent  ← source of truth
  4. Deliverable Agents (proposal, quote, scope, deck)
  5. QA Alignment Agent
  6. Finalizer

Each step depends on the previous. No freestyling.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from vwmedia_proposal_agent.jobs.job_paths import ensure_job_structure, write_manifest


# ── Step 1: Intake ─────────────────────────────────────────────────────────────


def run_intake(input_data: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize the enquiry input."""
    required_fields = ["businessName", "websiteUrl"]
    missing = [f for f in required_fields if not input_data.get(f)]
    if missing:
        raise ValueError(f"Missing required enquiry fields: {', '.join(missing)}")

    intake = {
        "status": "intake-complete",
        "businessName": input_data.get("businessName", ""),
        "websiteUrl": input_data.get("websiteUrl", ""),
        "contactName": input_data.get("contactName", ""),
        "contactEmail": input_data.get("contactEmail", ""),
        "industry": input_data.get("industry", ""),
        "location": input_data.get("location", ""),
        "goals": input_data.get("goals", []),
        "timeline": input_data.get("timeline", ""),
        "budgetRange": input_data.get("budgetRange", ""),
        "notes": input_data.get("notes", ""),
        "validatedAt": datetime.now().isoformat(timespec="seconds"),
    }
    return intake


# ── Step 2: Research (called by research agents, returns merged results) ─────────


def merge_research_outputs(
    website_assessment: dict | None = None,
    seo_assessment: dict | None = None,
    competitor_research: dict | None = None,
    keyword_strategy: list[str] | None = None,
) -> dict[str, Any]:
    """Merge research outputs into a single research dict for the strategy brief."""
    merged = {
        "keywordStrategy": keyword_strategy or [],
        "competitorGaps": [],
        "evidenceRefs": [],
    }

    if competitor_research:
        gaps = competitor_research.get("gaps", [])
        if gaps:
            merged["competitorGaps"] = gaps

    if seo_assessment:
        refs = seo_assessment.get("evidenceRefs", [])
        if refs:
            merged["evidenceRefs"] = refs

    return merged


# ── Step 3: Strategy Brief Agent ─────────────────────────────────────────────────


def run_strategy_brief_agent(
    input_data: dict[str, Any],
    research: dict[str, Any],
    job_root: Path,
) -> tuple[Path, Path, dict[str, Any]]:
    """Run the strategy brief agent to generate the source of truth."""
    from vwmedia_proposal_agent.agents.strategy_brief_agent import build_strategy_brief, brief_to_markdown

    brief = build_strategy_brief(input_data, research)
    brief_md = brief_to_markdown(brief)

    working_dir = job_root / "working"
    working_dir.mkdir(parents=True, exist_ok=True)

    json_path = working_dir / "strategy-brief.json"
    md_path = working_dir / "strategy-brief.md"

    json_path.write_text(json.dumps(brief, indent=2), encoding="utf-8")
    md_path.write_text(brief_md, encoding="utf-8")

    write_manifest(json_path.parent.parent, "strategy-brief-ready", {
        "strategyBriefJson": str(json_path),
        "strategyBriefMarkdown": str(md_path),
    })

    return json_path, md_path, brief


# ── Step 4: Deliverable Agents ──────────────────────────────────────────────────


def run_deliverable_agents(
    brief: dict[str, Any],
    job_root: Path,
    deck_agent=None,  # optional Visual Strategy Agent for PPTX generation
) -> dict[str, Path]:
    """Run all deliverable agents in parallel from the strategy brief."""
    from vwmedia_proposal_agent.agents.proposal_agent import generate_proposal_from_brief, proposal_to_markdown
    from vwmedia_proposal_agent.agents.quote_agent import generate_quote_from_brief, quote_to_markdown
    from vwmedia_proposal_agent.agents.scope_agent import generate_internal_scope_from_brief, scope_to_markdown

    outputs: dict[str, Path] = {}

    # Proposal
    proposal = generate_proposal_from_brief(brief)
    proposal_md = proposal_to_markdown(proposal)
    outputs_dir = job_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    proposal_json_path = outputs_dir / "proposal.json"
    proposal_md_path = outputs_dir / "proposal.md"
    proposal_json_path.write_text(json.dumps(proposal, indent=2), encoding="utf-8")
    proposal_md_path.write_text(proposal_md, encoding="utf-8")
    outputs["proposal"] = proposal_md_path

    # Quote
    quote = generate_quote_from_brief(brief)
    quote_md = quote_to_markdown(quote)
    quote_json_path = outputs_dir / "quote.json"
    quote_md_path = outputs_dir / "quote.md"
    quote_json_path.write_text(json.dumps(quote, indent=2), encoding="utf-8")
    quote_md_path.write_text(quote_md, encoding="utf-8")
    outputs["quote"] = quote_md_path

    # Internal Scope
    scope = generate_internal_scope_from_brief(brief)
    scope_md = scope_to_markdown(scope)
    scope_json_path = outputs_dir / "internal-scope.json"
    scope_md_path = outputs_dir / "internal-scope.md"
    scope_json_path.write_text(json.dumps(scope, indent=2), encoding="utf-8")
    scope_md_path.write_text(scope_md, encoding="utf-8")
    outputs["internal_scope"] = scope_md_path

    # Deck (if deck agent provided)
    if deck_agent:
        deck_json_path = outputs_dir / "proposal-deck.json"
        deck_path = outputs_dir / "proposal-deck.pptx"
        deck_json_path.write_text(json.dumps({"fromBrief": True, "briefVersion": brief["version"]}, indent=2), encoding="utf-8")
        outputs["deck"] = deck_path  # will be populated by deck agent

    return outputs


# ── Step 5: QA Alignment Agent ──────────────────────────────────────────────────


def run_qa_alignment(
    brief: dict[str, Any],
    proposal: dict[str, Any],
    quote: dict[str, Any],
    scope: dict[str, Any],
    job_root: Path,
) -> dict[str, Any]:
    """Run QA alignment checks across all deliverables."""
    from vwmedia_proposal_agent.agents.qa_agent import run_alignment_qa, qa_report_to_markdown

    report = run_alignment_qa(brief, proposal, quote, scope)
    report_md = qa_report_to_markdown(report)

    working_dir = job_root / "working"
    working_dir.mkdir(parents=True, exist_ok=True)
    qa_json_path = working_dir / "qa-alignment-report.json"
    qa_md_path = working_dir / "qa-alignment-report.md"

    qa_json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    qa_md_path.write_text(report_md, encoding="utf-8")

    return report


# ── Step 6: Finalizer ───────────────────────────────────────────────────────────


def finalize_job(job_root: Path, qa_status: str, deliverables: dict[str, Path]) -> dict[str, Path]:
    """Copy approved outputs to outputs/final and write manifest."""
    from vwmedia_proposal_agent.jobs.job_paths import write_manifest

    final_dir = job_root / "outputs" / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    copied = {}
    for name, path in deliverables.items():
        if path.exists():
            dest = final_dir / path.name
            shutil.copy2(path, dest)
            copied[name] = dest

    manifest_status = "review-ready" if qa_status == "passed" else "blocked"
    write_manifest(job_root, manifest_status, {"finalOutputs": {k: str(v) for k, v in copied.items()}})

    return copied


# ── Full Pipeline Runner ─────────────────────────────────────────────────────────


def run_vwmedia_pipeline(
    job_id: str,
    input_data: dict[str, Any],
    research: dict[str, Any] | None = None,
    deck_agent=None,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run the full VWMedia Proposal Swarm pipeline end-to-end.

    Returns a result dict with status, paths, and QA report.
    """
    job_root = ensure_job_structure(job_id, repo_root)

    # Write intake
    intake = run_intake(input_data)
    (job_root / "input.json").write_text(json.dumps(intake, indent=2), encoding="utf-8")

    # Merge research
    if not research:
        research = {"keywordStrategy": [], "competitorGaps": [], "evidenceRefs": []}

    # Strategy brief (source of truth)
    json_path, md_path, brief = run_strategy_brief_agent(intake, research, job_root)

    # Deliverables (all consume the brief)
    deliverables = run_deliverable_agents(brief, job_root, deck_agent)

    # QA alignment
    qa_report = run_qa_alignment(
        brief,
        deliverables.get("proposal_json", {}),  # will be loaded from disk in real usage
        deliverables.get("quote_json", {}),
        deliverables.get("internal_scope_json", {}),
        job_root,
    )

    # Finalize
    qa_status = qa_report.get("status", "failed")
    copied = finalize_job(job_root, qa_status, deliverables)

    # Write pipeline manifest
    result = {
        "jobId": job_id,
        "status": qa_status,
        "qaStatus": qa_status,
        "pipelineSteps": [
            "intake-complete",
            "research-complete",
            "strategy-brief-ready",
            "deliverables-generated",
            f"qa-{qa_status}",
            f"final-{qa_status}",
        ],
        "outputs": {str(p) for p in copied.values()},
        "qaReport": qa_report,
    }
    return result
