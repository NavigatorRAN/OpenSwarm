# VWMedia Proposal Swarm Skill Integration Backlog

This backlog tracks future skills/tools to evaluate after v0.1 instructions are validated.

## Candidate Skill Areas

- Marketing frameworks and positioning, including `coreyhaines31/marketingskills`
- SEO audit and content gap analysis
- Local SEO and Google Business Profile guidance
- Competitive landing-page teardown
- Proposal writing and sales packaging
- Pricing/quoting calculators for Australian service businesses
- Website crawl/sitemap summarization
- Accessibility basics
- Copywriting and conversion-rate optimization
- AI automation opportunity mapping

## Evaluation Criteria

A skill is useful only if it:

- Improves output quality or repeatability
- Can run non-intrusively from public data or supplied enquiry data
- Keeps claims evidence-based
- Does not require private credentials for first-pass assessment
- Can be documented and tested with a sample enquiry
- Does not make the workflow brittle or opaque

## First Skills To Investigate

1. `coreyhaines31/marketingskills` for positioning, offer design, landing-page critique, and marketing strategy structure.
2. SEO/content audit skills that operate on public URLs only.
3. Proposal/quote generation skills that support staged packages and assumptions.
4. Website crawl/summarization tools that are polite, low-rate, and non-invasive.

## 2026-05-09 Additions

Installed:

- `marketing-ideas` from `coreyhaines31/marketingskills`
- `competitor-alternatives` from `coreyhaines31/marketingskills`
- `competitor-profiling` from `coreyhaines31/marketingskills`

Attempted but blocked:

- `marketing-skills-collection` from `supercent-io/skills-template`; install failed because cloning `https://github.com/supercent-io/skills-template.git` required authentication or was inaccessible from this runtime.

Integration notes:

- Use `competitor-profiling` for structured public competitor dossiers.
- Use `competitor-alternatives` for comparison/alternative positioning and competitor-content opportunities.
- Use `marketing-ideas` for staged quick-win / medium-term / long-term growth ideas.
- Treat `marketing-skills-collection` as a reference candidate until install/access is resolved.
