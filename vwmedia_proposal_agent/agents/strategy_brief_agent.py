"""Strategy Brief Agent — generates the single source of truth for all deliverables."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _slug(value: str) -> str:
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in value).split()) or "client"


def build_strategy_brief(input_data: dict[str, Any], research: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the strategy brief from enquiry input + research outputs."""
    business = input_data.get("businessName") or input_data.get("business_name") or "Unknown business"
    website = input_data.get("websiteUrl") or input_data.get("website") or ""
    contact = input_data.get("contactName", "")
    industry = input_data.get("industry") or "To be classified from enquiry and public website"
    location = input_data.get("location") or input_data.get("serviceArea") or "Not supplied"
    budget = input_data.get("budgetRange", "")
    timeline = input_data.get("timeline", "")
    goals = input_data.get("goals", [])
    notes = input_data.get("notes", "")

    # Merge research data into the brief
    cat_class = industry
    keyword_strategy = [f"{industry} {location}", f"{industry} services {location}"]
    competitor_gaps = []
    evidence_refs = []

    if research:
        if research.get("categoryClassification"):
            cat_class = research["categoryClassification"]["primary"]
        if research.get("keywordStrategy"):
            keyword_strategy = research["keywordStrategy"]
        if research.get("competitorGaps"):
            competitor_gaps = research["competitorGaps"]
        if research.get("evidenceRefs"):
            evidence_refs = research["evidenceRefs"]

    strategy_pillars = [
        {
            "name": "Own local service intent",
            "recommendation": "Create focused service/location pages mapped to validated buyer searches.",
            "quick_wins": [
                "Add location-specific landing pages for each primary service area",
                "Optimize existing pages for local search intent",
            ],
            "medium_term": [
                "Build dedicated service page for each primary offering",
                "Create project portfolio case studies with photos and proof",
            ],
            "long_term": [
                "Develop a content hub around local infrastructure topics",
                "Establish thought leadership through industry engagement",
            ],
            "evidence_needed": "Keyword strategy and competitor/service SERP review",
        },
        {
            "name": "Make expertise visible",
            "recommendation": "Turn project experience, capability, and service proof into portfolio/case-study assets.",
            "quick_wins": [
                "Add proof blocks and service-area clarity to homepage",
                "Showcase testing capability as differentiators",
            ],
            "medium_term": [
                "Build portfolio mini case studies from supplied project notes",
                "Develop before/after visual proof assets",
            ],
            "long_term": [
                "Create a searchable project database with filterable case studies",
                "Develop video testimonials and site walk-throughs",
            ],
            "evidence_needed": "Approved project examples, photos, testimonials, capability proof",
        },
        {
            "name": "Reduce enquiry friction",
            "recommendation": "Replace generic enquiry capture with guided quote-request questions.",
            "quick_wins": [
                "Redesign quote-request form with job-type selectors",
                "Add service-area dropdown and urgency indicators",
            ],
            "medium_term": [
                "Implement conditional form logic based on job type",
                "Add instant pricing estimates for common service types",
            ],
            "long_term": [
                "Deploy AI-assisted lead qualification with CRM integration",
                "Build client portal for project tracking",
            ],
            "evidence_needed": "Common job types and information needed to quote accurately",
        },
        {
            "name": "Educate before the call",
            "recommendation": "Publish FAQs and practical explainers based on buyer questions.",
            "quick_wins": [
                "Create FAQ section based on sales team common questions",
                "Add 'What to expect' guides for each service type",
            ],
            "medium_term": [
                "Build educational content cluster around buyer topics",
                "Create comparison pages (service types, processes, etc.)",
            ],
            "long_term": [
                "Develop a knowledge base with tutorials and checklists",
                "Create industry-specific buying guides for B2B segments",
            ],
            "evidence_needed": "Common sales questions and service misconceptions",
        },
        {
            "name": "Use AI behind the scenes",
            "recommendation": "Use internal AI triage to summarize, classify, and prepare follow-up notes for human approval.",
            "quick_wins": [
                "Implement AI-assisted enquiry summarization for sales team",
                "Auto-generate draft follow-up questions based on enquiry type",
            ],
            "medium_term": [
                "Deploy AI draft quote/proposal generation for common job types",
                "Create internal AI content repurposing workflow",
            ],
            "long_term": [
                "Build AI-powered project scoping assistant",
                "Develop automated reporting narratives from project data",
            ],
            "evidence_needed": "Sample enquiry types and preferred response workflow",
        },
    ]

    phases = [
        {
            "name": "Phase 1 - Quick Wins",
            "timeline": "1-2 weeks after approval and access to editable website content",
            "items": [
                "Homepage value proposition and CTA refresh",
                "Metadata and heading tune-up around validated service terms",
                "Proof blocks and service-area clarity additions",
                "Quote-request form question redesign",
                "First FAQ/topic content set",
            ],
            "ai_agent_work": [
                "Draft copy variants for homepage and service pages",
                "Draft metadata/headings for key pages",
                "Draft FAQ topics and content",
                "Draft quote form field structure",
            ],
            "human_work": [
                "Approve positioning statements and claims",
                "Validate technical language for accuracy",
                "Publish website changes",
                "Review final client-facing copy",
            ],
        },
        {
            "name": "Phase 2 - Website And Visibility Upgrade",
            "timeline": "3-6 weeks depending on page count, client review speed, and available proof assets",
            "items": [
                "Dedicated service/location landing pages for primary offerings",
                "Portfolio mini case studies from project data",
                "Internal linking improvements for SEO and navigation",
                "Educational content cluster around buyer topics",
                "First internal enquiry triage workflow setup",
            ],
            "ai_agent_work": [
                "Draft service page outlines and first-pass copy",
                "Draft case study structures from supplied project notes",
                "Draft internal linking map",
                "Draft triage prompts and templates",
            ],
            "human_work": [
                "Confirm service scope and pricing",
                "Select/approve images and project examples",
                "Perform CMS publishing and quality assurance",
                "Approve triage workflow before going live",
            ],
        },
        {
            "name": "Phase 3 - AI-Enabled Growth System",
            "timeline": "6-12+ weeks as a staged implementation after the core website assets are approved",
            "items": [
                "AI-assisted lead qualification and triage",
                "Quote/proposal draft workflow automation",
                "Content operations and repurposing workflow",
                "CRM-ready handoff structure",
                "Reporting narrative drafts once analytics access exists",
            ],
            "ai_agent_work": [
                "Summarize and classify incoming enquiries",
                "Generate draft follow-up questions per job type",
                "Draft quote/scoping notes for common service types",
                "Draft content/reporting narratives",
            ],
            "human_work": [
                "Approve all client-facing communications",
                "Validate pricing and technical scope",
                "Connect systems with client approval",
                "Review reporting and strategic recommendations",
            ],
        },
    ]

    quote_packages = [
        {
            "name": "Quick Wins Package",
            "priceRangeAud": "$1,500-$3,500 + GST",
            "timeline": phases[0]["timeline"],
            "mapsToPhase": phases[0]["name"],
            "includes": phases[0]["items"][:3],
        },
        {
            "name": "Website And Visibility Upgrade",
            "priceRangeAud": "$5,000-$12,000 + GST",
            "timeline": phases[1]["timeline"],
            "mapsToPhase": phases[1]["name"],
            "includes": phases[1]["items"][:4],
        },
        {
            "name": "AI-Enabled Growth System",
            "priceRangeAud": "$10,000-$28,000 + GST",
            "timeline": phases[2]["timeline"],
            "mapsToPhase": phases[2]["name"],
            "includes": phases[2]["items"][:3],
        },
    ]

    brief = {
        "version": "0.3",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "enquiry": {
            "businessName": business,
            "websiteUrl": website,
            "contactName": contact,
            "industry": industry,
            "location": location,
            "budgetRange": budget,
            "timeline": timeline,
            "goals": goals,
            "notes": notes,
        },
        "categoryClassification": {
            "primary": cat_class,
            "location": location,
            "excludedCategories": [
                "PR/media communications unless explicitly evidenced",
                "Generic digital agency unless explicitly evidenced",
            ],
            "confidence": "requires public-site validation",
        },
        "keywordStrategy": keyword_strategy,
        "competitorGaps": competitor_gaps,
        "evidenceRefs": evidence_refs,
        "positioning": {
            "strategicPosition": "Trusted local technical specialist with practical implementation expertise",
            "oneLineStrategy": "Make technical expertise easier to find, trust, and buy.",
        },
        "strategyPillars": strategy_pillars,
        "phases": phases,
        "quotePackages": quote_packages,
        "assumptions": [
            "Pricing based on Australian labour rates; actual costs may vary by project complexity",
            "Client will provide necessary content, images, and project data",
            "Timelines assume timely client reviews and approvals",
            "Access to editable website content required for implementation",
        ],
        "exclusions": [
            "Ongoing website hosting or maintenance unless specified",
            "Third-party service fees (domain renewal, hosting, premium plugins)",
            "Content creation from scratch without client-supplied source material",
            "SEO guarantee of specific rankings (algorithm-dependent)",
        ],
        "risks": [
            "Client unavailability during implementation phase may extend timelines",
            "Missing or outdated client data may require additional discovery time",
            "Dependence on third-party platform APIs may introduce scope changes",
        ],
        "alignmentRules": [
            "All deliverables must reference the same strategy pillars from this brief",
            "Quote packages must map to the same phases described in the proposal",
            "Internal scope must distinguish AI-agent-doable work from human-in-the-loop work for every phase",
            "Timelines must appear consistently in strategy brief, quote, and internal scope",
            "All claims must be evidence-labelled: Observed, Likely, or Assumption",
            "Final outputs cannot be marked review-ready until QA alignment passes or is waived",
        ],
        "implementationSwarmHandoff": {
            "note": "Implementation swarm is a separate post-acceptance project.",
            "handoffOutputsNeeded": [
                "approved scope from proposal",
                "accepted quote/package",
                "client access requirements",
                "timeline and milestone plan",
                "human approval points",
            ],
        },
    }
    return brief


def brief_to_markdown(brief: dict[str, Any]) -> str:
    """Convert strategy brief dict to a human-readable markdown document."""
    lines = [
        f"# Strategy Brief - {brief['enquiry']['businessName']}",
        "",
        f"**Generated:** {brief['generatedAt']}",
        f"**Website:** {brief['enquiry'].get('websiteUrl', '')}",
        f"**Contact:** {brief['enquiry'].get('contactName', '')}",
        f"**Industry:** {brief['enquiry'].get('industry', '')}",
        f"**Location:** {brief['enquiry'].get('location', '')}",
        "",
        "## Strategic Position",
        "",
        brief["positioning"]["strategicPosition"],
        "",
        f"**One-line strategy:** {brief['positioning']['oneLineStrategy']}",
        "",
        "## Category Classification",
        "",
        f"- **Primary:** {brief['categoryClassification']['primary']}",
        f"- **Location:** {brief['categoryClassification']['location']}",
        f"- **Confidence:** {brief['categoryClassification']['confidence']}",
        "- **Excluded:** " + ", ".join(brief['categoryClassification']['excludedCategories']),
        "",
        "## Keyword Strategy",
        "",
        "- " + "\n- ".join(brief.get("keywordStrategy", ["TBD"])) or "TBD",
        "",
        "## Competitor Gaps",
        "",
    ]
    for gap in brief.get("competitorGaps", []):
        lines.append(f"- **{gap.get('gap', 'TBD')}**: {gap.get('description', '')}")
    if not brief.get("competitorGaps"):
        lines.append("- TBD (to be populated from competitor research)")

    lines += ["", "## Strategy Pillars"]
    for pillar in brief["strategyPillars"]:
        lines += ["", f"### {pillar['name']}", "", pillar["recommendation"], "", "**Quick wins:**"]
        for w in pillar.get("quick_wins", []):
            lines.append(f"- {w}")
        lines += ["", "**Medium-term:**"]
        for m in pillar.get("medium_term", []):
            lines.append(f"- {m}")
        lines += ["", "**Long-term:**"]
        for l in pillar.get("long_term", []):
            lines.append(f"- {l}")
        lines += ["", f"**Evidence needed:** {pillar['evidenceNeeded']}"]

    lines += ["", "## Phases, Timelines, and Delivery Split"]
    for phase in brief["phases"]:
        lines += ["", f"### {phase['name']}", f"**Timeline:** {phase['timeline']}", "", "**Work items:**"]
        for item in phase["items"]:
            lines.append(f"- {item}")
        lines += ["", "**AI-agent-doable:**"]
        for item in phase["ai_agent_work"]:
            lines.append(f"- {item}")
        lines += ["", "**Human-in-the-loop:**"]
        for item in phase["human_work"]:
            lines.append(f"- {item}")

    lines += ["", "## Quote Packages"]
    for pkg in brief["quotePackages"]:
        lines += ["", f"### {pkg['name']}", f"- **Price:** {pkg['priceRangeAud']}", f"- **Timeline:** {pkg['timeline']}", f"- **Maps to:** {pkg['mapsToPhase']}"]

    lines += ["", "## Assumptions"] + [f"- {a}" for a in brief.get("assumptions", [])]
    lines += ["", "## Exclusions"] + [f"- {e}" for e in brief.get("exclusions", [])]
    lines += ["", "## Risks"] + [f"- {r}" for r in brief.get("risks", [])]
    lines += ["", "## Alignment Rules"] + [f"- {rule}" for rule in brief["alignmentRules"]]
    lines += ["", "## Implementation Swarm Handoff", "", brief["implementationSwarmHandoff"]["note"], "", "**Required handoff outputs:**"]
    lines += [f"- {item}" for item in brief["implementationSwarmHandoff"]["handoffOutputsNeeded"]]

    return "\n".join(lines) + "\n"
