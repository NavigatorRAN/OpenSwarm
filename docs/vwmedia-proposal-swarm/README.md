# VWMedia Proposal Swarm

## Goal

Build an OpenSwarm workflow for VWMedia that turns a public website enquiry into three human-reviewable deliverables:

1. Proposal slide deck
2. Client quote
3. Internal scoping document

The workflow is intentionally non-intrusive. It must not require website login details, Google Analytics, Search Console, CRM access, or private customer systems.

## Desired End State

A user submits an enquiry through the VWMedia website. The enquiry is passed to OpenSwarm, which performs a public-facing assessment of the prospect's website and market position, researches competitors, identifies visibility and marketing opportunities, then generates proposal materials with staged recommendations and Australian labour-cost assumptions.

## Inputs

Minimum enquiry fields:

- Business name
- Website URL
- Contact name
- Contact email
- Contact phone, optional
- Industry/category
- Location/service area
- Goals/challenges
- Desired timeline
- Budget range, optional
- Notes/free-text enquiry

Optional enrichment fields:

- Target services/products
- Main competitors supplied by prospect
- Existing social profiles
- Existing CRM/booking/quote workflow notes
- Preferred proposal package level

## Non-Intrusive Assessments

The swarm may use only publicly accessible information and safe checks:

- Website crawl of public pages
- Metadata and title/description review
- Page structure and heading review
- Copy clarity and offer positioning
- Call-to-action and conversion path review
- Mobile/responsive qualitative review
- Basic performance observations from public page load behaviour
- Indexability-visible checks where available from public HTML/robots/sitemap
- Local/category competitor review
- Google/Brave-style visibility research from public search results
- Public review/profile presence where accessible
- Social/profile consistency checks
- Content gap analysis
- Basic technical SEO observations visible without authentication

The swarm must not:

- Attempt login or bypass access controls
- Request or require analytics credentials
- Scrape private/customer data
- Run aggressive scans, vulnerability scans, load tests, or intrusive probes
- Make claims about analytics, conversions, traffic, or revenue that are not supported by provided/public data

## Core Agents

### 1. Intake Orchestrator

Responsibilities:

- Normalize enquiry data into a structured job brief
- Identify missing information
- Select the right agent sequence
- Maintain the job folder and final deliverable checklist
- Ensure the original enquiry is preserved unchanged

Outputs:

- `01-intake-brief.md`
- `job.json`

### 2. Public Website Assessment Agent

Responsibilities:

- Review the public website for UX, copy, trust, conversion, offer clarity, navigation, mobile signals, and non-intrusive technical SEO observations
- Capture quick wins and evidence
- Avoid unsupported analytics claims

Outputs:

- `02-website-assessment.md`
- `website-findings.json`

### 3. Visibility And SEO Agent

Responsibilities:

- Assess public search visibility and discoverability
- Review titles, descriptions, headings, sitemap/robots where public
- Identify content gaps, local SEO opportunities, schema opportunities, internal linking improvements, and service-page opportunities
- Suggest practical SEO improvements that can be delivered without private account access

Outputs:

- `03-visibility-seo-assessment.md`

### 4. Competitor Research Agent

Responsibilities:

- Identify likely competitors from public search and supplied enquiry context
- Compare positioning, offers, proof, content, calls to action, and service coverage
- Highlight competitor patterns VWMedia can use in the proposal

Outputs:

- `04-competitor-research.md`

### 5. Marketing Strategy Agent

Responsibilities:

- Translate findings into positioning, funnel, content, and conversion strategy
- Use marketing skills/frameworks where available, such as `coreyhaines31/marketingskills`
- Separate quick wins, medium-term projects, and long-term solutions

Outputs:

- `05-marketing-opportunity-map.md`

### 6. AI Integration Strategist

Responsibilities:

- Identify AI-enabled improvements that do not require risky access by default
- Distinguish agent-doable work from human-in-the-loop work
- Suggest automation opportunities: enquiry triage, quote assistant, content workflows, FAQ/chat, lead follow-up, document generation, CRM preparation, reporting drafts

Outputs:

- `06-ai-integration-map.md`

### 7. Quote And Scope Agent

Responsibilities:

- Convert recommendations into priced packages and staged options
- Include quick wins, medium-term projects, and long-term solutions
- Use Australian labour-cost assumptions, with AI assistance reducing delivery effort but not valuing human work below minimum wage requirements
- Include assumptions, exclusions, dependencies, and optional extras

Outputs:

- `07-quote.md`
- `quote.json`

### 8. Proposal Deck Agent

Responsibilities:

- Create a polished proposal slide deck for the prospect
- Use VWMedia tone and visual style
- Focus on clear business outcomes, evidence, recommended roadmap, and pricing options

Outputs:

- `08-proposal-deck.pptx`
- `08-proposal-deck-outline.md`

### 9. Internal Scope QA Agent

Responsibilities:

- Produce the internal scoping document
- Flag what can be done by AI agents, what requires human review, what requires client access, and what should not be automated
- Check unsupported claims, pricing assumptions, legal/commercial risk, and missing discovery questions

Outputs:

- `09-internal-scope.md`
- `risk-checklist.md`

## Final Deliverables

### Proposal Slide Deck Visual Style

The deck should borrow the VWMedia website visual identity from `https://vwmedia.home.arpa`: colour palette, typography feel, gradients/card treatments, spacing, and overall premium digital-consultancy tone. The proposal generator should create `08-proposal-deck-style-notes.md` before PPTX generation so the visual direction is explicit and reviewable.

### Proposal Slide Deck

Client-facing deck covering:

- Executive summary
- Current public website/visibility observations
- Competitive context
- Key opportunities
- Quick wins
- Medium-term projects
- Long-term solutions
- Recommended roadmap
- Investment options
- Next steps

### Quote

Client-facing quote covering:

- Scope by phase
- Deliverables
- Pricing
- Assumptions
- Exclusions
- Timeline
- Payment terms placeholder
- Validity period placeholder

### Internal Scoping Document

Internal VWMedia document covering:

- Work breakdown
- AI-agent-doable tasks
- Human-in-the-loop tasks
- Tasks requiring client access or approval
- Unknowns and discovery questions
- Delivery risks
- Suggested production sequence
- Margin/labour assumption notes

## Pricing Principles

- Pricing must not imply human labour below Australian minimum wage requirements.
- AI assistance may reduce hours, but planning, supervision, QA, client communication, and accountability remain priced as real work.
- Quote ranges should include assumptions and confidence levels.
- Any claim about savings or outcomes must be framed as an estimate unless supported by data.

Suggested internal labour assumptions to parameterize later:

- Admin/research baseline hourly rate
- Specialist marketing hourly rate
- Web/technical implementation hourly rate
- Strategy/consulting hourly rate
- AI-agent execution supervision multiplier
- Human QA/review minimum allocation per deliverable

## Job Folder Shape

```text
jobs/{jobId}/
  input.json
  public-research/
  working/
  outputs/
    01-intake-brief.md
    02-website-assessment.md
    03-visibility-seo-assessment.md
    04-competitor-research.md
    05-marketing-opportunity-map.md
    06-ai-integration-map.md
    07-quote.md
    08-proposal-deck.pptx
    08-proposal-deck-outline.md
    09-internal-scope.md
    risk-checklist.md
```

## Build Phases

### Phase 1 - Manual Prototype

- Use a sample enquiry JSON
- Run the swarm manually from the Mac
- Produce markdown outputs first
- Generate deck after content quality is proven

### Phase 2 - Semi-Automated Intake

- Website form stores enquiry JSON
- Human or Pauline triggers OpenSwarm job
- Outputs saved to a job folder for review

### Phase 3 - Automated Intake Worker

- New enquiries enqueue jobs automatically
- OpenSwarm worker processes job
- Human receives notification when outputs are ready

### Phase 4 - Client Workflow Integration

- Add CRM/email handoff
- Add approval workflow
- Add reusable proposal/quote templates
- Add optional skills from skills.sh after vetting

## Open Questions

- What exact VWMedia price bands should the Quote Agent use?
- What proposal visual style should the deck use?
- Should first live deployment send outputs only to Matt/Veronika for approval, or create draft emails automatically?
- Which skills from skills.sh should be vendored or referenced first?
- What is the minimum acceptable evidence for competitor/visibility claims?


## Canonical Shared Output Location

All VWMedia Proposal Swarm jobs should write durable outputs to the AI Shared Drive, not only to the local Mac repo `mnt/` folder.

Canonical root:

```text
/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs/{jobId}/
```

The OpenSwarm repo-local `mnt/` directory may be used only as a temporary working area for agent tools that require it. Any final artifacts must be copied/synced back to the canonical shared job folder.

Final deliverables should live under:

```text
/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs/{jobId}/outputs/final/
```

For this workflow, final client/review artifacts are:

- `proposal-deck.pptx` where generated
- `proposal-deck.pdf`
- `proposal.pdf`
- `quote.pdf`
- `internal-scoping-document.pdf`
```


## Job Output Contract

All VWMedia Proposal Swarm agents must follow `docs/vwmedia-proposal-swarm/job-output-contract.md`. Durable outputs belong under:

```text
/Volumes/AISharedDrive/family-agents/shared/projects/vwmedia-proposal-swarm/jobs/{jobId}/
```

Repo-local `mnt/{jobId}` may be used only as a symlink/compatibility alias to the shared job folder. Final review artifacts must be written to `outputs/final/` in the canonical shared job folder.
