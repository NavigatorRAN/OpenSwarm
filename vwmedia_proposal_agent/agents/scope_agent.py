"""Internal Scope Generator Agent — creates the delivery plan with AI vs human split."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def generate_internal_scope_from_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Generate internal scoping document from the strategy brief."""
    business = brief["enquiry"]["businessName"]
    
    scope = {
        "version": "0.3",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "businessName": business,
        "websiteUrl": brief["enquiry"].get("websiteUrl", ""),
        "phases": [],
        "discoveryQuestions": [],
        "nextActions": [],
    }

    for i, phase in enumerate(brief["phases"]):
        pkg = brief["quotePackages"][i] if i < len(brief["quotePackages"]) else None
        scope_phase = {
            "name": phase["name"],
            "timeline": phase["timeline"],
            "estimatedBudget": pkg["priceRangeAud"] if pkg else "TBD",
            "deliverySequence": phase["items"],
            "aiAgentDeliverables": phase["ai_agent_work"],
            "humanReviewItems": phase["human_work"],
            "clientInputsRequired": [
                "Written approval of each phase before starting",
                "Access to editable website content/CMS",
                "Project examples, photos, and testimonials",
                "Service area and pricing information",
                "Brand assets (logo, colors, typography)",
                "Analytics access (when available)",
            ],
            "clientApprovalsRequired": [
                "Positioning statements",
                "Pricing and scope finalization",
                "Published content (all pages)",
                "Workflow configurations before going live",
            ],
            "risks": phase.get("risks", []) if "risks" in phase else brief.get("risks", []),
        }
        scope["phases"].append(scope_phase)

    scope["discoveryQuestions"] = [
        "What are the top 3 services that drive most revenue?",
        "What service areas should be prioritized?",
        "What equipment/testing capability differentiates the business?",
        "What are the most common enquiry types and their average values?",
        "What are the typical sales cycle length and close rate?",
        "Are there industry certifications or licenses that should be highlighted?",
        "What project examples/case studies are available for the portfolio?",
        "What is the current website CMS and hosting provider?",
        "Do you have analytics access (Google Analytics, Search Console)?",
        "What is the preferred lead response time?",
    ]

    scope["nextActions"] = [
        "Review and approve strategy brief",
        "Provide additional business data and proof assets",
        "Schedule discovery call to fill information gaps",
        "Confirm which packages to prioritize",
        "Arrange CMS/access setup for Phase 1",
    ]

    return scope


def scope_to_markdown(scope: dict[str, Any]) -> str:
    """Convert internal scope dict to a formatted markdown document."""
    lines = [
        f"# Internal Scope Document - {scope['businessName']}",
        "",
        f"**Prepared:** {scope['generatedAt']}",
        f"**Website:** {scope['websiteUrl']}",
        "",
        "## Delivery Plan",
    ]

    for phase in scope["phases"]:
        lines += ["", f"### {phase['name']}", f"**Timeline:** {phase['timeline']}", f"**Estimated Budget:** {phase['estimatedBudget']}", "", "**Delivery Sequence:**"]
        for item in phase["deliverySequence"]:
            lines.append(f"- {item}")
        lines += ["", "**AI-agent deliverables:**"]
        for item in phase["aiAgentDeliverables"]:
            lines.append(f"- {item}")
        lines += ["", "**Human review items:**"]
        for item in phase["humanReviewItems"]:
            lines.append(f"- {item}")
        lines += ["", "**Client inputs required:**"]
        for item in phase["clientInputsRequired"]:
            lines.append(f"- {item}")
        lines += ["", "**Client approvals required:**"]
        for item in phase["clientApprovalsRequired"]:
            lines.append(f"- {item}")

    lines += ["", "## Discovery Questions"] + [f"- {q}" for q in scope.get("discoveryQuestions", [])]
    lines += ["", "## Next Actions"] + [f"- {a}" for a in scope.get("nextActions", [])]

    return "\n".join(lines) + "\n"
