#!/usr/bin/env python3
"""VWMedia Proposal Swarm — an OpenSwarm agency for converting website enquiries into proposals.

Usage:
    python vwmedia_proposal_swarm.py "Enquiry payload JSON string"
    or
    python vwmedia_proposal_swarm.py --file /path/to/enquiry.json

The swarm will:
  1. Run intake validation
  2. Fetch and assess the prospect website
  3. Research competitors and visibility
  4. Generate strategy brief (source of truth)
  5. Generate proposal, quote, scope, and deck
  6. Run QA alignment
  7. Save outputs to AI Shared Drive
"""
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from agency_swarm import Agency, Agent, Tool
from agency_swarm.tools import WebSearchTool, FileSearchTool
from config import get_default_model, is_openai_provider


class VWMediaProposalSwarmAgent(Agent):
    """Orchestrates the VWMedia proposal pipeline."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="VWMedia Proposal Swarm",
            description=(
                "VWMedia Proposal Swarm. This agency takes a website enquiry and produces "
                "a complete proposal package: strategy brief, proposal deck, client quote, "
                "internal scoping document, and aligned deliverables. It runs the full "
                "pipeline: intake → research → strategy brief → deliverables → QA → final output."
            ),
            instructions="""# VWMedia Proposal Swarm Orchestrator

You are the VWMedia Proposal Swarm orchestrator. Your job is to take a website enquiry 
and produce a complete proposal package.

## Pipeline You Must Follow

You MUST execute these steps in order:

1. **Intake** — validate the enquiry input (businessName, websiteUrl required)
2. **Research** — fetch and assess the prospect website, search competitors
3. **Strategy Brief** — generate the canonical strategy-brief.json (SOURCE OF TRUTH)
4. **Deliverables** — generate proposal, quote, scope, and deck from the brief
5. **QA Alignment** — cross-check all deliverables against the brief
6. **Final Output** — save to AI Shared Drive

## Critical Rules

- The strategy brief is the SINGLE SOURCE OF TRUTH. All deliverables consume it.
- Do NOT generate deliverables from raw research alone.
- Do NOT let the deck be the canonical record.
- QA must pass before marking anything review-ready.
- Timelines, pricing, and scope must be consistent across all documents.

## Output Location

Save all outputs to:
/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs/{jobId}/

## When Complete

Report:
- Job ID
- Status (passed/blocked)
- Paths to all deliverables
- Any QA issues that need human review
""",
            model=get_default_model(),
        )


class ResearchAgent(Agent):
    """Fetches and assesses the prospect website and competitors."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Research Agent",
            description=(
                "Fetches and assesses the prospect website, searches competitors, "
                "and produces a research package for the Strategy Brief."
            ),
            instructions="""# Research Agent

## Your Job
Fetch and assess the prospect website and competitors. Produce research data for the 
Strategy Brief.

## What You Must Do
1. **Fetch the homepage** — extract title, meta description, H1, visible services, 
   CTAs, proof signals
2. **Fetch robots.txt and sitemap** — note indexing status
3. **Search competitors** — find 3-5 competitors in the same category/location
4. **Assess the prospect** — evaluate website from a conversion, UX, and SEO perspective
5. **Return structured research data** including:
   - Category classification (what business are they actually in)
   - Keyword strategy (validated search terms)
   - Competitor gaps
   - Evidence references (URLs, page content)
   - Website health assessment

## Safety Boundaries
- Public-only assessment. No logins, analytics, or intrusive scanning.
- Use evidence labels: Observed, Likely, or Assumption.

## Output
Return all research as a JSON object that the Strategy Brief agent can consume directly.
""",
            tools=[WebSearchTool(search_context_size="medium")],
            model=get_default_model(),
        )


class StrategyBriefAgent(Agent):
    """Generates the strategy brief from research data."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Strategy Brief Agent",
            description=(
                "Generates the canonical strategy brief — the single source of truth for "
                "all VWMedia proposal deliverables."
            ),
            instructions="""# Strategy Brief Agent

You are the heart of the VWMedia proposal pipeline. You generate the strategy brief 
that ALL other agents consume.

## Your Input
- Enquiry data (businessName, websiteUrl, industry, location, goals, etc.)
- Research data (website assessment, competitor research, keyword strategy, evidence refs)

## What You Must Generate
A strategy brief containing:
- Category classification
- Keyword strategy
- Competitor gaps
- Strategic positioning (position + one-line strategy)
- Strategy pillars (each with quick wins, medium-term, long-term)
- Phases with TIMELINES (estimated work completion dates)
- Quote packages with price ranges
- Assumptions, exclusions, risks
- Alignment rules
- Implementation swarm handoff requirements

## Critical Rules
- TIMELINES MUST appear in every phase
- All strategy pillars must have: quick wins, medium-term, long-term
- Quote packages MUST map to phases
- Evidence must be labelled (Observed/Likely/Assumption)
- You are the SOURCE OF TRUTH. Everything downstream reads you.

## Output Format
Save as BOTH:
- /jobs/{jobId}/working/strategy-brief.json
- /jobs/{jobId}/working/strategy-brief.md
""",
            model=get_default_model(),
        )


class ProposalAgent(Agent):
    """Generates the proposal from the strategy brief."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Proposal Agent",
            description="Generates the persuasive written proposal from the strategy brief.",
            instructions="""# Proposal Agent

## Your Input
ONLY the strategy-brief.json — this is your source of truth.

## What You Must Generate
A persuasive written proposal that:
- Opens with an executive summary
- Maps each strategy pillar to detailed recommendations
- Includes phased timeline with AI vs human work split
- Uses evidence labels on all claims
- Lists assumptions, exclusions, and risks

## Critical Rules
- ALL content comes from the strategy brief. Do not invent new strategy pillars.
- Timeline must match the brief exactly.
- Pricing references must match the brief's quote packages.

## Output
Save as:
- /jobs/{jobId}/outputs/proposal.json
- /jobs/{jobId}/outputs/proposal.md
""",
            model=get_default_model(),
        )


class QuoteAgent(Agent):
    """Generates the client quote from the strategy brief."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Quote Agent",
            description="Generates the priced quote from the strategy brief.",
            instructions="""# Quote Agent

## Your Input
ONLY the strategy-brief.json — this is your source of truth.

## What You Must Generate
A staged quote that:
- Maps to the same phases as the proposal
- Uses the same timeline for each phase
- Shows price ranges per package
- Includes terms, assumptions, and exclusions
- Specifies AI-agent contribution vs human review for each stage

## Critical Rules
- Prices and timelines MUST match the brief exactly.
- Each stage scope items must match the proposal.
- No scope items in the quote that aren't in the proposal.

## Output
Save as:
- /jobs/{jobId}/outputs/quote.json
- /jobs/{jobId}/outputs/quote.md
""",
            model=get_default_model(),
        )


class ScopeAgent(Agent):
    """Generates the internal scoping document from the strategy brief."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Scope Agent",
            description="Generates the internal scoping document with timelines and AI vs human split.",
            instructions="""# Scope Agent

## Your Input
ONLY the strategy-brief.json — this is your source of truth.

## What You Must Generate
An internal scoping document that:
- Lists delivery sequence for each phase
- Estimated timeline for EACH phase (with work completion estimates)
- AI-agent deliverables vs human review items
- Client inputs required
- Client approvals required
- Discovery questions
- Next actions

## Critical Rules
- Timelines must match the brief exactly.
- Scope items must match the proposal.
- Every phase needs an estimated timeline.

## Output
Save as:
- /jobs/{jobId}/outputs/internal-scope.json
- /jobs/{jobId}/outputs/internal-scope.md
""",
            model=get_default_model(),
        )


class DeckAgent(Agent):
    """Generates the proposal deck from the strategy brief."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Deck Agent",
            description="Generates the proposal deck from the strategy brief.",
            instructions="""# Deck Agent

## Your Input
ONLY the strategy-brief.json — this is your source of truth.

## What You Must Generate
A proposal deck (PPTX) that:
- Condenses the strategy brief into a visual presentation
- Uses the same strategy pillars as the brief
- Includes timeline, pricing, and phased approach
- Matches VWMedia visual identity (dark navy, cyan, gold)

## Critical Rules
- Deck content must be derivable from the brief. No new claims.
- The deck is a VISUAL SUMMARY, not a standalone document.
- All data in the deck must match the proposal and quote.

## Output
Save as:
- /jobs/{jobId}/outputs/proposal-deck.pptx
- /jobs/{jobId}/outputs/proposal-deck.pdf
""",
            model=get_default_model(),
        )


class QAAlignmentAgent(Agent):
    """Runs QA alignment checks across all deliverables."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="QA Alignment Agent",
            description="Cross-checks all deliverables against the strategy brief for consistency.",
            instructions="""# QA Alignment Agent

## Your Job
Cross-check all deliverables against the strategy brief (SOURCE OF TRUTH).

## What You Must Check
1. **Strategy pillars match** — do all deliverables reference the same pillars?
2. **Phases match** — do quote, proposal, and scope use the same phases?
3. **Timelines match** — are timelines consistent everywhere?
4. **Scope items match** — does quote scope match proposal scope?
5. **Evidence labels present** — are claims properly labelled?
6. **No contradictions** — is anything promised in the deck that isn't in the quote/proposal?
7. **No missing items** — is anything in the quote that isn't in the proposal?
8. **No over-promising** — is anything in the proposal that isn't scoped?

## Output
- qa-alignment-report.json — structured results with blockers/warnings
- qa-alignment-report.md — human-readable summary

## Critical Rule
If any blocker is found, the job CANNOT be marked review-ready. 
The orchestrator must flag issues for Matt's review before proceeding.
""",
            model=get_default_model(),
        )


def create_vwmedia_agency():
    """Create the VWMedia Proposal Swarm agency with all agents wired up."""
    from agency_swarm import Agency
    
    # Create all agents
    orchestrator = VWMediaProposalSwarmAgent()
    research = ResearchAgent()
    strategy_brief = StrategyBriefAgent()
    proposal = ProposalAgent()
    quote = QuoteAgent()
    scope = ScopeAgent()
    deck = DeckAgent()
    qa = QAAlignmentAgent()
    
    all_agents = [orchestrator, research, strategy_brief, proposal, quote, scope, deck, qa]
    
    agency = Agency(
        *all_agents,
        communication_flows=[
            (orchestrator, research),
            (orchestrator, strategy_brief),
            (orchestrator, proposal),
            (orchestrator, quote),
            (orchestrator, scope),
            (orchestrator, deck),
            (orchestrator, qa),
        ],
        name="VWMedia Proposal Swarm",
    )
    
    return agency


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VWMedia Proposal Swarm")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", help="Enquiry payload JSON string")
    group.add_argument("--file", help="Path to enquiry JSON file")
    args = parser.parse_args()
    
    # Load enquiry
    if args.json:
        enquiry = json.loads(args.json)
    else:
        enquiry = json.loads(Path(args.file).read_text())
    
    print(f"VWMedia Proposal Swarm — processing {enquiry.get('businessName', 'unknown')}")
    print(f"Website: {enquiry.get('websiteUrl', 'unknown')}")
    print()
    
    agency = create_vwmedia_agency()
    agency.tui()
