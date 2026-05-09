"""Quote Generator Agent — creates the priced quote from the strategy brief."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def generate_quote_from_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Generate a client quote from the strategy brief."""
    business = brief["enquiry"]["businessName"]
    
    quote = {
        "version": "0.3",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "businessName": business,
        "websiteUrl": brief["enquiry"].get("websiteUrl", ""),
        "currency": "AUD",
        "gstInclusive": False,
        "stages": [],
        "assumptions": [],
        "exclusions": [],
        "terms": [
            "Prices valid for 30 days from quote date",
            "Timelines begin after written approval and payment of deposit",
            "Client deposits: 50% upfront, 25% at midpoint, 25% on completion",
            "Additional scope items quoted separately",
            "Prices exclude third-party costs (hosting, domain, premium plugins, stock assets)",
            "Changes to scope after approval may affect timeline and pricing",
        ],
    }

    for i, phase in enumerate(brief["phases"]):
        pkg = brief["quotePackages"][i] if i < len(brief["quotePackages"]) else None
        stage = {
            "name": f"Stage {i+1}: {phase['name']}",
            "timeline": phase["timeline"],
            "scope": phase["items"],
            "ai_agent_work": phase["ai_agent_work"],
            "human_work": phase["human_work"],
            "priceRange": pkg["priceRangeAud"] if pkg else "TBD",
            "mapsToPhase": phase["name"],
        }
        quote["stages"].append(stage)

    quote["assumptions"] = brief.get("assumptions", [
        "Pricing based on Australian labour rates",
        "Client provides necessary content and data",
    ])
    quote["exclusions"] = brief.get("exclusions", [
        "Ongoing hosting/maintenance unless specified",
        "Third-party fees",
        "Content from scratch without source material",
    ])

    return quote


def quote_to_markdown(quote: dict[str, Any]) -> str:
    """Convert quote dict to a formatted markdown document."""
    lines = [
        f"# Quote - {quote['businessName']}",
        "",
        f"**Prepared:** {quote['generatedAt']}",
        f"**Currency:** {quote['currency']} (GST {'inclusive' if quote['gstInclusive'] else 'exclusive'})",
        "",
        "## Staged Pricing",
    ]

    for stage in quote["stages"]:
        lines += ["", f"### {stage['name']}", f"**Timeline:** {stage['timeline']}", f"**Price:** {stage['priceRange']}", "", "**Scope:**"]
        for item in stage["scope"]:
            lines.append(f"- {item}")
        lines += ["", "**AI-agent contribution:**"]
        for item in stage["ai_agent_work"]:
            lines.append(f"- {item}")
        lines += ["", "**Human review:**"]
        for item in stage["human_work"]:
            lines.append(f"- {item}")

    lines += ["", "## Assumptions"] + [f"- {a}" for a in quote.get("assumptions", [])]
    lines += ["", "## Exclusions"] + [f"- {e}" for e in quote.get("exclusions", [])]
    lines += ["", "## Terms"] + [f"- {t}" for t in quote.get("terms", [])]

    return "\n".join(lines) + "\n"
