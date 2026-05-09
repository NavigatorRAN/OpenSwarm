"""Proposal Generator Agent — creates the persuasive written proposal from the strategy brief."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def generate_proposal_from_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Generate a proposal document from the strategy brief."""
    business = brief["enquiry"]["businessName"]
    website = brief["enquiry"].get("websiteUrl", "")
    
    # Executive summary from positioning
    exec_summary = (
        f"We've assessed {business}'s public presence and market position to identify "
        f"opportunities that make {brief['positioning']['strategicPosition'].lower()}.\n\n"
        f"**Our one-line strategy:** {brief['positioning']['oneLineStrategy']}\n\n"
        f"Based on our analysis of the website, public visibility, and competitive landscape, "
        f"we recommend a phased approach focused on the five strategy pillars outlined below."
    )

    # Build proposal sections from strategy pillars
    sections = []
    for i, pillar in enumerate(brief["strategyPillars"], 1):
        section = {
            "number": i,
            "title": pillar["name"],
            "strategy": pillar["recommendation"],
            "quick_wins": pillar.get("quick_wins", []),
            "medium_term": pillar.get("medium_term", []),
            "long_term": pillar.get("long_term", []),
            "evidence_needed": pillar["evidenceNeeded"],
        }
        sections.append(section)

    # Build proposal document
    proposal = {
        "version": "0.3",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "businessName": business,
        "websiteUrl": website,
        "executiveSummary": exec_summary,
        "sections": sections,
        "phases": [
            {
                "name": phase["name"],
                "timeline": phase["timeline"],
                "items": phase["items"],
                "ai_agent_work": phase["ai_agent_work"],
                "human_work": phase["human_work"],
            }
            for phase in brief["phases"]
        ],
        "assumptions": brief["assumptions"],
        "exclusions": brief["exclusions"],
        "risks": brief["risks"],
        "evidenceLabels": {
            "observed": "Directly visible on public website or in search results",
            "likely": "Inferred from public signals (not guaranteed)",
            "assumption": "Used for planning/costing; requires validation",
        },
    }
    return proposal


def proposal_to_markdown(proposal: dict[str, Any]) -> str:
    """Convert proposal dict to a formatted markdown document."""
    lines = [
        f"# Proposal - {proposal['businessName']}",
        "",
        f"**Prepared:** {proposal['generatedAt']}",
        f"**Website:** {proposal['websiteUrl']}",
        "",
        "## Executive Summary",
        "",
        proposal["executiveSummary"],
        "",
        "## Strategic Approach",
        "",
        f"**Our one-line strategy:** {proposal.get('strategyPillars', [{}])[0].get('strategy', '') if 'strategyPillars' in proposal else ''}",
        "",
        "## Detailed Recommendations",
    ]

    for section in proposal["sections"]:
        lines += ["", f"### {section['number']}. {section['title']}", "", section["strategy"], ""]
        if section["quick_wins"]:
            lines.append("**Quick wins:**")
            for w in section["quick_wins"]:
                lines.append(f"- {w}")
            lines.append("")
        if section["medium_term"]:
            lines.append("**Medium-term:**")
            for m in section["medium_term"]:
                lines.append(f"- {m}")
            lines.append("")
        if section["long_term"]:
            lines.append("**Long-term:**")
            for l in section["long_term"]:
                lines.append(f"- {l}")
            lines.append("")
        lines.append(f"**Evidence needed:** {section['evidence_needed']}")

    lines += ["", "## Implementation Timeline"]
    for phase in proposal["phases"]:
        lines += ["", f"### {phase['name']}", f"**Timeline:** {phase['timeline']}", "", "**Scope:**"]
        for item in phase["items"]:
            lines.append(f"- {item}")
        lines += ["", "**AI-agent contribution:**"]
        for item in phase["ai_agent_work"]:
            lines.append(f"- {item}")
        lines += ["", "**Human review required:**"]
        for item in phase["human_work"]:
            lines.append(f"- {item}")

    lines += ["", "## Assumptions"] + [f"- {a}" for a in proposal.get("assumptions", [])]
    lines += ["", "## Exclusions"] + [f"- {e}" for e in proposal.get("exclusions", [])]
    lines += ["", "## Risks"] + [f"- {r}" for r in proposal.get("risks", [])]
    lines += ["", "## Evidence Labels"]
    for label, meaning in proposal.get("evidenceLabels", {}).items():
        lines.append(f"- **{label.title()}**: {meaning}")

    return "\n".join(lines) + "\n"
