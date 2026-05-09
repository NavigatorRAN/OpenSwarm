# VWMedia Proposal Swarm Pipeline

## Architecture

The VWMedia Proposal Swarm operates through a **sequential pipeline** with a **Strategy Brief** as the single source of truth.

### Pipeline Flow

```
Enquiry Input
    ↓
1. Intake Agent  (validate + normalize)
    ↓
2. Research Agents  (website, SEO, competitor, keyword)
    ↓
3. Strategy Brief Agent  ← SOURCE OF TRUTH
    ↓
4. Deliverable Agents (all consume the brief):
   - Proposal Generator
   - Quote Generator
   - Internal Scope Generator
   - Deck Generator (optional, from brief)
    ↓
5. QA Alignment Agent  (cross-checks all deliverables)
    ↓
6. Finalizer  (copies approved outputs to outputs/final)
```

### Key Design Principles

1. **Strategy brief is the source of truth** — all deliverables consume it, not each other
2. **No deck-as-master** — the PPTX is a visual summary only, not the canonical record
3. **QA gate before review-ready** — no output is marked review-ready until alignment passes
4. **Timelines in every document** — brief, proposal, quote, and scope all have consistent timelines
5. **AI vs human split documented** — every phase distinguishes what AI does vs what requires human review

## Agent Instructions

### Intake Agent
- Validates enquiry fields (businessName, websiteUrl required)
- Normalizes input into standard format
- Writes `input.json`

### Research Agents
- Public website assessment → `website-assessment.md`
- SEO assessment → `seo-assessment.md`  
- Competitor research → `competitor-profiles.md`
- Keyword strategy → `keyword-strategy.md`
- All merged into research dict for strategy brief

### Strategy Brief Agent
- Generates `strategy-brief.json` and `strategy-brief.md`
- Contains: category classification, keyword strategy, competitor gaps, positioning, strategy pillars, phases with timelines, quote packages, assumptions, exclusions, risks, alignment rules, implementation handoff
- **This is the canonical source that all downstream agents read**

### Proposal Generator Agent
- Consumes strategy-brief.json
- Generates persuasive written proposal
- All sections derive from strategy pillars
- Includes phases with timelines, evidence labels

### Quote Generator Agent  
- Consumes strategy-brief.json
- Generates priced quote with stages mapping to brief phases
- Includes terms, assumptions, exclusions
- Prices map to the same timeline structure as proposal

### Internal Scope Generator Agent
- Consumes strategy-brief.json  
- Generates delivery plan with AI vs human split
- Includes discovery questions, next actions, client inputs required

### Deck Generator (Visual Strategy Agent)
- Consumes strategy-brief.json
- Creates visual PPTX as condensed presentation
- Must not add claims not supported by the brief

### QA Alignment Agent
- Cross-checks: deck, proposal, quote, and scope against the brief
- Checks: strategy pillars match, phases match, timelines consistent, scope items match, evidence labels present
- Blocker prevents review-ready status
- Warnings flag items for human review

## Output Structure

```
jobs/{jobId}/
  input.json
  working/
    strategy-brief.json
    strategy-brief.md
    qa-alignment-report.json
    qa-alignment-report.md
  outputs/
    proposal.json
    proposal.md
    quote.json
    quote.md
    internal-scope.json
    internal-scope.md
    proposal-deck.json
  outputs/final/
    (approved outputs only, QA-gated)
```

## Implementation Notes

- Implementation swarm is a **separate post-acceptance project**
- Deck generation (PPTX) is optional — markdown outputs are the primary artifacts
- All pricing in AUD with GST exclusions clearly stated
- Australian labour rates used as costing baseline
- Evidence labels (Observed/Likely/Assumption) required for all claims
