# Integrated Skills v0.1

This project integrates two external AgentSkills as guidance sources for the VWMedia Proposal Swarm. They are installed globally for OpenClaw/Codex use and mirrored here as project integration notes so the OpenSwarm agents can apply their frameworks consistently.

## Installed Skills

### Web Design Guidelines

- Source: `vercel-labs/agent-skills`, skill `web-design-guidelines`
- Local install: `~/.agents/skills/web-design-guidelines/SKILL.md`
- skills.sh: `https://skills.sh/vercel-labs/agent-skills/web-design-guidelines`
- Purpose in this swarm: improve public website assessment, UX/design critique, accessibility observations, and proposal deck quality.

Operational notes:

- The skill fetches the latest Vercel Web Interface Guidelines from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before each detailed UI review.
- For v0.1, use it as a review framework, not as an automated claim generator.
- Apply findings only to public pages/files we can inspect safely.

### SEO Audit

- Source: `coreyhaines31/marketingskills`, skill `seo-audit`
- Local install: `~/.agents/skills/seo-audit/SKILL.md`
- skills.sh: `https://skills.sh/coreyhaines31/marketingskills/seo-audit`
- Purpose in this swarm: strengthen crawlability, indexation, technical SEO, on-page SEO, content quality, local-business SEO, and prioritized action plans.

Operational notes:

- The skill explicitly warns that `curl`/static fetch cannot reliably detect JavaScript-injected schema markup.
- Use browser-rendered checks or rich-results tooling before claiming schema is absent.
- In v0.1, phrase schema findings as `not detected by static/public fetch` unless browser-rendered evidence exists.


### Marketing Ideas

- Source: `coreyhaines31/marketingskills`, skill `marketing-ideas`
- Local install: `~/.agents/skills/marketing-ideas/SKILL.md`
- skills.sh: `https://skills.sh/coreyhaines31/marketingskills/marketing-ideas`
- Purpose in this swarm: expand practical marketing recommendations, prioritize quick wins vs medium/long-term strategies, and suggest campaign/content/growth ideas matched to the prospect's stage and resources.

### Competitor Alternatives

- Source: `coreyhaines31/marketingskills`, skill `competitor-alternatives`
- Local install: `~/.agents/skills/competitor-alternatives/SKILL.md`
- skills.sh: `https://skills.sh/coreyhaines31/marketingskills/competitor-alternatives`
- Purpose in this swarm: structure competitor comparison insights, identify comparison-page/content opportunities, and keep competitor claims honest and useful.

### Competitor Profiling

- Source: `coreyhaines31/marketingskills`, skill `competitor-profiling`
- Local install: `~/.agents/skills/competitor-profiling/SKILL.md`
- skills.sh: `https://skills.sh/coreyhaines31/marketingskills/competitor-profiling`
- Purpose in this swarm: create structured competitor profiles from public competitor URLs. In v0.1, use quick public scans only unless deeper tools such as Firecrawl/DataForSEO are explicitly configured and approved.

### Marketing Skills Collection

- Source attempted: `supercent-io/skills-template`, skill `marketing-skills-collection`
- skills.sh: `https://skills.sh/supercent-io/skills-template/marketing-skills-collection`
- Install status: not installed; `npx skills add` failed because the GitHub repository clone required authentication or was inaccessible from this runtime.
- Purpose if later available: broad marketing deliverable framework across CRO, copywriting, SEO, analytics, and growth. For now, treat it as a reference candidate only, not an installed dependency.

## Agent Mapping

| Swarm Agent | Skill Guidance |
| --- | --- |
| Public Website Assessment Agent | Web Design Guidelines |
| Visibility And SEO Agent | SEO Audit |
| Competitor Research Agent | Competitor Profiling, Competitor Alternatives |
| Marketing Strategy Agent | SEO Audit, Marketing Ideas, Marketing Skills Collection candidate |
| Quote And Scope Agent | Marketing Ideas, Marketing Skills Collection candidate |
| Proposal Deck Agent | Web Design Guidelines |
| Internal Scope QA Agent | Both skills, to verify claims and risk levels |

## Integration Rules

1. External skills are guidance, not authority. The swarm still obeys VWMedia boundaries and non-intrusive assessment rules.
2. Do not run intrusive scans or require private credentials just because a skill mentions a deeper audit tool.
3. Evidence-label all findings: `Observed`, `Likely`, or `Assumption`.
4. Where the skill requires tools not available in v0.1, record the item as a future/manual check.
5. Keep client-facing language practical and non-alarmist.
