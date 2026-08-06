# Contributing (RCBT)

Single-maintainer project. This file carries the merge policy referenced by
[`CLAUDE.md`](CLAUDE.md) and [`docs/DOCUMENTATION_STANDARD.md`](docs/DOCUMENTATION_STANDARD.md).

## Merge policy

- **Human merges only.** No agent merges a branch on its own, regardless of
  how affirmative its own assessment is.
- **The GO token is the only merge authorization.** Format: `GO RCBT-M###`.
  Nothing else — not "looks good," not an implicit approval — authorizes a
  merge. A placeholder or template value in a GO message is refused.
- **Docs-only branches** (briefs, plans, solution docs, governance files —
  no code changed): self-merge after review. No multi-agent code review
  required; it would produce no actionable findings on a docs-only diff.
- **Code branches** (any branch with a code change): human reviews before
  merge. Review is `Required`, not `Skip`, per the PRD's Review field.

## Before opening a branch

1. No code without an approved PLAN. No PLAN without an approved BRIEF.
2. Read `docs/architecture/DOMAIN_REGISTRY.md` first if the change touches a
   protected zone. Plan first for anything in a protected zone; one
   protected-zone change in flight at a time.
3. Tag the work with its three dials (fidelity, change class, review) in the
   BRIEF and PLAN — see `docs/DOCUMENTATION_STANDARD.md`.

## Branch naming

`{type}/RCBT-M###-{slug}` — e.g. `feature/RCBT-M002-storage-tier-judge`.
Incidents: `{YYYY-MM-DD}-{slug}.md`.

## What closes a unit of work

Landing code is not completion. `docs/architecture/MILESTONE_REGISTRY.md`
plus a green QA checklist is the only completion authority — a row flips to
Complete only when the change is live and verified.
