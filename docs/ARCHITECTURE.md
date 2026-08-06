# RCBT Architecture

Foundational architectural decisions live here, inline, rather than as
standalone `docs/ADR-NNN_slug.md` files, per
`docs/DOCUMENTATION_STANDARD.md`. Feature-level ADRs get their own files.

These four are the decisions that must be locked before Phase 1 code is
written (see the project knowledge doc this foundation was built from,
§10). All four are `Proposed` — none are decided yet. They will be filled
in during Phase 1 work, each promoted to `Accepted` (or split into a
standalone ADR) once a PLAN forces the decision.

---

## ADR-001: Ingredient tier taxonomy data model

Status: Proposed
Derived from: (no PLAN yet)

### Context
The recipe bot must enforce an ingredient tier system (deep storage,
rotation stock, grow/seasonal) — see the off-grid pantry domain knowledge.
The tier classification needs a home before the LLM-as-judge (Homework 3)
can query it.

### Decision
Not yet made. Options on the table: hardcode in the system prompt, a
structured JSON file the prompt references, a database table.

### Consequences
Undetermined — affects how the judge queries tier data and how later
storehouse-inventory work (Phase 3) integrates.

---

## ADR-002: Off-grid constraint encoding

Status: Proposed
Derived from: (no PLAN yet)

### Context
Fuel type, equipment availability, and time horizon need to reach the
chatbot somehow — per-query, session-level, or a hybrid with overridable
defaults. This shapes the query dimension matrix (Homework 2) and the
system prompt structure (Homework 1).

### Decision
Not yet made.

### Consequences
Undetermined.

---

## ADR-003: Recipe storage format

Status: Proposed
Derived from: (no PLAN yet)

### Context
How recipes are stored and retrieved — flat markdown, structured JSON with
a schema (see the minimum-fields schema in the project knowledge doc),
embedded in the prompt, or a vector store. Governs how Phase 2 meal
planning can query the corpus. Also governs whether extending
`homeworks/hw4/reference_files/processed_recipes.json` (see
`docs/architecture/BASELINE.md`) is the right move or a fresh corpus is
needed.

### Decision
Not yet made.

### Consequences
Undetermined.

---

## ADR-004: Trace and annotation storage

Status: Proposed
Derived from: (no PLAN yet)

### Context
The upstream course approach is JSON files to disk. Whether that holds, or
a lightweight SQLite / observability tool (e.g. Phoenix) replaces it,
needs deciding before the annotation tool is built out further.

### Decision
Not yet made.

### Consequences
Undetermined.
