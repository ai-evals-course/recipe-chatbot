# RCBT Documentation Standard

Condensed in-repo copy of the project's governance system. Source of truth
for the full rationale: the handoff package this was built from (owner-side,
not in this repo). This file is what agents and contributors read here.

## The lifecycle

```
BRIEF (PRD)  ->  PLAN (SDD)  ->  ADR  ->  SOLUTION
```

No code without an approved PLAN. No PLAN without an approved BRIEF. No ADR
without a PLAN to derive it from.

| Doc | File | Answers | Written by | Approved by |
|---|---|---|---|---|
| BRIEF | `docs/briefs/BRIEF_NNN_slug.md` | What are we building, why, for whom, what does success look like? No solutions here. | Human (agent-assisted) | Human, before planning |
| PLAN | `docs/plans/PLAN_NNN_slug.md` | How is it built? Components, sequence, acceptance criteria. | Agent, from the approved BRIEF | Human, before code |
| ADR | `docs/ADR-NNN_slug.md` (or inline in `docs/ARCHITECTURE.md` if foundational) | What specific decision was locked, what was rejected, why? | Agent drafts, human reviews | Human |
| SOLUTION | `docs/solutions/YYYY-MM-DD-slug.md` | What was built, what was learned, what's next? | Agent, after review | Human (implicit, accompanies the PR) |

The ADR closes the spec ledger (BRIEF, PLAN, ADR — intent and design). The
solution doc opens the completion ledger's memory loop.

## The two ledgers

- **Spec ledger** (front half): BRIEF, PLAN, ADR. Owns intent and design.
  Human-approved at the brief gate and the plan gate.
- **Completion ledger** (back half): `docs/architecture/MILESTONE_REGISTRY.md`,
  the milestone QA checklist (`docs/release/RCBT-M###-QA-CHECKLIST.md`), the
  solution doc. Owns shipped-and-verified. Complete means live and
  QA-verified, not code landed.

## The three dials

Every unit of work carries all three:

**Fidelity** — how much planning before execution:
- F1: clear requirement, obvious implementation, narrow scope. Docs-only or single-file.
- F2: clear scope, non-obvious implementation, multi-file. Full PLAN required.
- F3: fuzzy requirement, unclear done condition. Prototype first, then formalize.
- Schema, database, or evaluation-pipeline changes are minimum F2 always.

**Change class** — how much deploy/verify ceremony (see
`docs/architecture/CHANGE_CLASSIFICATION.md`):
- Additive: adds without altering existing behavior. Standard checklist.
- Mutative: changes existing behavior/data in place. Checklist plus rollback target.
- Destructive: removes or irreversibly transforms. Architecture sign-off before PR opens.
- When unsure between Mutative and Destructive, treat as Destructive.

**Review** — whether code review runs:
- Skip: docs-only branch, no code changed.
- Required: any branch containing a code change.

## Naming and numbering

- Short code: `RCBT`. Milestones: `RCBT-M001`, `RCBT-M002`, ... sequential, never reused.
- Briefs/plans: zero-padded 3 digits, sequential from the highest existing
  number, never reused. Read the directory before assigning the next number.
- ADRs: `ADR-NNN_slug.md`. Foundational ADRs may live inline in `docs/ARCHITECTURE.md`.
- Solutions: `YYYY-MM-DD-slug.md`.
- Branches: `{type}/RCBT-M###-{slug}`. Incidents: `{YYYY-MM-DD}-{slug}.md`.
- GO token: `GO RCBT-M###` — the only merge authorization.
- The numbering spine: when work is one-to-one, `BRIEF_007`, `PLAN_007`, and
  `RCBT-M007` are the same unit at three moments. Keep them aligned when the
  shape allows; a milestone closing several briefs runs its own sequence.

## The non-negotiable rules

1. No code without an approved PLAN. No PLAN without an approved BRIEF. No ADR without a PLAN to derive it from.
2. `MILESTONE_REGISTRY` plus the milestone QA checklist is the only completion authority.
3. Docs are authoritative over memory. Repo beats chat for permanent facts.
4. Every behavior-changing PR updates its governance docs in the same PR.
5. Governance docs are written before code, not after.
6. `CLAUDE.md` only grows. Rules are appended, never deleted.
7. `GO RCBT-M###` is the only merge authorization.
8. Living docs (`RCBT_CURRENT_STATE`, `RCBT_OPEN_DECISIONS`, `RCBT_CONSTRAINTS_AND_CONVENTIONS`) live in Claude.ai project knowledge only. Never committed here.
9. CI is the only sanctioned deploy path.
10. Verification work touches no repo files. Test apparatus lives in `/tmp`.
11. Credentials are never accepted, echoed, or stored. Prompt at runtime.

## Templates

### BRIEF (`docs/briefs/BRIEF_NNN_slug.md`)

```markdown
# BRIEF_NNN: [Feature or Problem Name]

Date: YYYY-MM-DD
Fidelity: F1 | F2 | F3
Change class: Additive | Mutative | Destructive
Review: Skip | Required
Milestone: RCBT-M### (if assigned)
Status: Draft | Approved | Superseded

## Problem
[1-3 sentences. What's broken or missing, who's affected. No solution here.]

## Context
[What exists today, what triggered this, what constraints apply.]

## Goals
- [ ] [measurable outcome]

## Non-Goals
- [explicit scope boundary]

## Open Questions
1. [question to answer before or during planning]

## References
- Related: BRIEF_NNN_slug.md, ADR-NNN_slug.md
```

### PLAN (`docs/plans/PLAN_NNN_slug.md`)

```markdown
# PLAN_NNN: [Feature Name]

Date: YYYY-MM-DD
Derived from: BRIEF_NNN_slug.md
Fidelity: F1 | F2 | F3
Change class: Additive | Mutative | Destructive
Review: Skip | Required
Protected zones touched: [P-## ids, or none]
Status: Draft | Approved

## Approach
[2-4 sentences. Chosen strategy and why, over alternatives.]

## Components
### [Component Name]
- Location: [path]
- Role: [what it does]
- Change: New | Modified | Deleted

## Implementation Sequence
1. [step, explicit dependencies]

## Acceptance Criteria
- [ ] [specific, testable condition]

## Risks and Mitigations
| Risk | Likelihood | Mitigation |
|---|---|---|

## Out of Scope
[What this plan does not cover.]

## Context Load Order
1. CLAUDE.md
2. docs/ARCHITECTURE.md
3. docs/plans/PLAN_NNN_slug.md
4. [files relevant to this task]
```

### ADR (`docs/ADR-NNN_slug.md`)

```markdown
# ADR-NNN: [Decision Title]

Date: YYYY-MM-DD
Status: Proposed | Accepted | Superseded by ADR-NNN
Derived from: PLAN_NNN_slug.md

## Context
[Why the decision was needed, and the constraints.]

## Decision
[Stated plainly, 1-2 sentences.]

## Alternatives Considered
### [Name]
- What it is: [description]
- Why rejected: [reason]

## Consequences
Positive:
- [consequence]
Negative:
- [consequence]

## References
- BRIEF_NNN_slug.md, PLAN_NNN_slug.md
```

An ADR is never edited after acceptance. A reversal is a new ADR that supersedes it.

### SOLUTION (`docs/solutions/YYYY-MM-DD-slug.md`)

```markdown
# [Feature or Problem Name] Solution

Date: YYYY-MM-DD
Branch: [branch]
PR: #[number]
Milestone: RCBT-M###
Derived from: PLAN_NNN_slug.md

## What Was Built
[2-4 sentences on what now exists that did not before.]

## Implementation Notes
[Gotchas, non-obvious execution decisions, things tried and dropped.]

## Files Changed
| File | Change |
|---|---|

## Learned Rules
1. [rule to append to CLAUDE.md, actionable and specific]

## What to Do Next
- [follow-on, with a BRIEF reference if one exists]
```

### QA CHECKLIST (`docs/release/RCBT-M###-QA-CHECKLIST.md`)

```markdown
# RCBT-M### QA Checklist

Milestone: RCBT-M###
Brief(s) closed: BRIEF_NNN
Change class: Additive | Mutative | Destructive

## CI gates
- [ ] Build, static checks, test suite green.

## Live precondition gates
- [ ] [preconditions confirmed on the real surface before deploy].

## Post-merge verification
- [ ] [each acceptance criterion demonstrated live, observation not conclusion].

## Rollback
- Shipped version id: [captured live]
- Preceding version id: [captured live]
- Rollback tested or standing by: [ ]
```

Both version ids are captured live, never carried over as expected values.
