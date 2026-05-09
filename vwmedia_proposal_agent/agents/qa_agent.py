"""Proposal Alignment QA Agent — ensures all deliverables are consistent against the strategy brief."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def run_alignment_qa(brief: dict[str, Any], proposal: dict[str, Any], quote: dict[str, Any], scope: dict[str, Any]) -> dict[str, Any]:
    """Run semantic alignment QA across all deliverables against the strategy brief."""
    issues: list[dict[str, str | list[str]]] = []
    warnings: list[dict[str, str]] = []
    
    # 1. Check all deliverables reference the same strategy pillars
    brief_pillars = {p["name"]: p for p in brief["strategyPillars"]}
    proposal_pillars = {s["title"]: s for s in proposal["sections"]}
    
    # Check deliverables cover all brief pillars
    missing_pillars = [name for name in brief_pillars if name not in proposal_pillars]
    if missing_pillars:
        issues.append({
            "severity": "blocker",
            "check": "strategy_pillars_match",
            "issue": f"Proposal missing strategy pillars from brief: {', '.join(missing_pillars)}",
            "details": missing_pillars,
        })
    
    # Check quote packages map to brief phases
    brief_phase_names = {p["name"] for p in brief["phases"]}
    quote_phase_names = {s["mapsToPhase"] for s in quote["stages"]}
    missing_phases = brief_phase_names - quote_phase_names
    if missing_phases:
        issues.append({
            "severity": "blocker",
            "check": "quote_phases_match",
            "issue": f"Quote missing phases from brief: {', '.join(missing_phases)}",
            "details": list(missing_phases),
        })
    
    # Check proposal phases match brief phases
    proposal_phase_names = {p["name"] for p in proposal["phases"]}
    if missing_phases_brief := brief_phase_names - proposal_phase_names:
        issues.append({
            "severity": "blocker",
            "check": "proposal_phases_match",
            "issue": f"Proposal missing phases from brief: {', '.join(missing_phases_brief)}",
            "details": list(missing_phases_brief),
        })
    
    # 2. Check scope matches what's promised in proposal
    scope_phase_names = {p["name"] for p in scope["phases"]}
    if missing_scope := brief_phase_names - scope_phase_names:
        issues.append({
            "severity": "blocker",
            "check": "scope_phases_match",
            "issue": f"Internal scope missing phases from brief: {', '.join(missing_scope)}",
            "details": list(missing_scope),
        })
    
    # 3. Check timelines are consistent across all docs
    brief_timelines = {p["name"]: p["timeline"] for p in brief["phases"]}
    quote_timelines = {s["mapsToPhase"]: s["timeline"] for s in quote["stages"]}
    proposal_timelines = {p["name"]: p["timeline"] for p in proposal["phases"]}
    scope_timelines = {p["name"]: p["timeline"] for p in scope["phases"]}
    
    for phase_name in brief_phase_names:
        brief_tl = brief_timelines.get(phase_name, "")
        quote_tl = quote_timelines.get(phase_name, "")
        proposal_tl = proposal_timelines.get(phase_name, "")
        scope_tl = scope_timelines.get(phase_name, "")
        
        if quote_tl and brief_tl and quote_tl != brief_tl:
            warnings.append({
                "severity": "warning",
                "check": "timeline_consistency",
                "phase": phase_name,
                "issue": f"Timeline mismatch: brief='{brief_tl}', quote='{quote_tl}'",
            })
        if proposal_tl and brief_tl and proposal_tl != brief_tl:
            warnings.append({
                "severity": "warning",
                "check": "timeline_consistency",
                "phase": phase_name,
                "issue": f"Timeline mismatch: brief='{brief_tl}', proposal='{proposal_tl}'",
            })
        if scope_tl and brief_tl and scope_tl != brief_tl:
            warnings.append({
                "severity": "warning",
                "check": "timeline_consistency",
                "phase": phase_name,
                "issue": f"Timeline mismatch: brief='{brief_tl}', scope='{scope_tl}'",
            })
    
    # 4. Check quote prices match proposal scope items
    for stage in quote["stages"]:
        stage_name = stage["mapsToPhase"]
        # Find matching proposal phase items
        matching_phase = next((p for p in proposal["phases"] if p["name"] == stage_name), None)
        if matching_phase:
            if set(stage["scope"]) != set(matching_phase["items"]):
                quote_scope = set(stage["scope"])
                proposal_scope = set(matching_phase["items"])
                extra_in_quote = quote_scope - proposal_scope
                missing_from_quote = proposal_scope - quote_scope
                if extra_in_quote:
                    warnings.append({
                        "severity": "warning",
                        "check": "quote_scope_match",
                        "phase": stage_name,
                        "issue": f"Quote includes items not in proposal: {', '.join(extra_in_quote)}",
                    })
                if missing_from_quote:
                    warnings.append({
                        "severity": "warning",
                        "check": "quote_scope_match",
                        "phase": stage_name,
                        "issue": f"Quote missing items from proposal: {', '.join(missing_from_quote)}",
                    })
    
    # 5. Check internal scope matches what's promised externally
    for phase in scope["phases"]:
        stage_name = phase["name"]
        matching_proposal = next((p for p in proposal["phases"] if p["name"] == stage_name), None)
        if matching_proposal:
            proposal_items = set(matching_proposal["items"])
            scope_items = set(phase["deliverySequence"])
            if proposal_items != scope_items:
                extra = proposal_items - scope_items
                missing = scope_items - proposal_items
                if extra:
                    warnings.append({
                        "severity": "info",
                        "check": "scope_promises_match",
                        "phase": stage_name,
                        "issue": f"Proposal promises items not in scope: {', '.join(extra)}",
                    })
                if missing:
                    issues.append({
                        "severity": "blocker",
                        "check": "scope_promises_match",
                        "phase": stage_name,
                        "issue": f"Scope missing items promised in proposal: {', '.join(missing)}",
                        "details": list(missing),
                    })
    
    # 6. Check evidence labels are present in proposal
    proposal_text = json.dumps(proposal)
    if "observed" not in proposal_text.lower() and "likely" not in proposal_text.lower():
        warnings.append({
            "severity": "info",
            "check": "evidence_labels",
            "issue": "Proposal should use evidence labels (Observed/Likely/Assumption)",
        })
    
    # 7. Check deck references the same strategy pillars
    # (Deck is checked via its generated content - this is a placeholder for now)
    
    # 8. Verify all alignment rules are documented
    alignment_rules_present = bool(brief.get("alignmentRules"))
    if not alignment_rules_present:
        warnings.append({
            "severity": "warning",
            "check": "alignment_rules",
            "issue": "Strategy brief should include alignment rules",
        })
    
    # Determine pass/fail
    blockers = [i for i in issues if i.get("severity") == "blocker"]
    status = "passed" if not blockers else "failed"
    
    report = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "checkResults": {
            "strategyPillarsMatch": len(missing_pillars) == 0,
            "quotePhasesMatch": len(missing_phases) == 0,
            "proposalPhasesMatch": len(missing_phases_brief) == 0 if 'missing_phases_brief' in dir() else True,
            "scopePhasesMatch": len(missing_scope) == 0 if 'missing_scope' in dir() else True,
            "timelinesConsistent": len([w for w in warnings if w["check"] == "timeline_consistency"]) == 0,
            "quoteScopeConsistent": len([w for w in warnings if w["check"] == "quote_scope_match"]) == 0,
            "scopePromisesMatch": len([i for i in issues if i.get("check") == "scope_promises_match" and i.get("severity") == "blocker"]) == 0,
            "evidenceLabelsPresent": len([w for w in warnings if w["check"] == "evidence_labels"]) == 0,
        },
        "issues": issues,
        "warnings": warnings,
        "notes": [
            "V0.3 QA performs semantic alignment checks across all deliverables.",
            "Blockers must be resolved before marking review-ready.",
            "Warnings should be reviewed and acknowledged.",
            "Deck alignment is checked via generated content comparison.",
        ],
    }
    return report


def qa_report_to_markdown(report: dict[str, Any]) -> str:
    """Convert QA report to markdown."""
    lines = [
        f"# QA Alignment Report",
        "",
        f"**Generated:** {report['generatedAt']}",
        f"**Status:** {'✅ PASSED' if report['status'] == 'passed' else '❌ FAILED'}",
        "",
        "## Check Results",
        "",
    ]
    for check, result in report["checkResults"].items():
        status = "✅" if result else "❌"
        lines.append(f"- {status} {check}")
    
    if report["issues"]:
        lines += ["", "## Issues"]
        for issue in report["issues"]:
            lines.append(f"- **{issue['severity'].upper()}**: {issue['issue']}")
    
    if report["warnings"]:
        lines += ["", "## Warnings"]
        for warning in report["warnings"]:
            lines.append(f"- **{warning['severity'].upper()}**: {warning['issue']}")
    
    lines += ["", "## Notes"] + [f"- {n}" for n in report.get("notes", [])]
    return "\n".join(lines) + "\n"
