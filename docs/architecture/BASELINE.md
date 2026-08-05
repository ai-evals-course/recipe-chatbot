# RCBT Baseline (architecture snapshot)

Snapshot at foundation time (RCBT-M001). Describes what exists today, not
what's planned — see `docs/ARCHITECTURE.md` for the foundational ADRs that
govern where this goes next.

## Provenance

Forked from `ai-evals-course/recipe-chatbot` (upstream `main`, untouched by
this fork except `data/sample_queries.csv`). This is simultaneously a
learning vehicle (the 5-homework evaluation course) and the base for a real
off-grid recipe chatbot — see `docs/DOCUMENTATION_STANDARD.md` and
`docs/ARCHITECTURE.md` for how the two relate.

## Components

- **`backend/main.py`** — FastAPI app, chat endpoint.
- **`backend/utils.py`** — loads `system_prompt.md`, builds the LiteLLM
  call (`get_agent_response`), currently defaults to OpenAI
  (`MODEL_NAME=gpt-4o-mini` fallback; `.env` not yet wired to Anthropic).
- **`backend/system_prompt.md`** — the system prompt itself. Protected, see
  `docs/architecture/DOMAIN_REGISTRY.md` P-01. Currently the generic
  upstream course prompt, not yet rewritten for the off-grid audience
  (Homework 1 work, not yet started).
- **`backend/retrieval.py`** — BM25 recipe retriever (`rank-bm25`), expects
  a corpus shaped like `homeworks/hw4/reference_files/processed_recipes.json`
  (200-recipe reference set from a prior homework; not yet confirmed wired
  into the live chat path).
- **`backend/query_rewrite_agent.py`** — LLM-powered query rewriting.
- **`backend/evaluation_utils.py`** — eval/metrics scaffolding, used with
  `judgy` for bias-corrected precision/recall.
- **`frontend/index.html`** — single-page chat UI, no build step.
- **`annotation/`** — FastHTML-based manual annotation tool
  (`annotation.py`), traces in `annotation/traces/` (gitignored).
- **`scripts/bulk_test.py`** — runs `data/sample_queries.csv` through the
  chat endpoint.
- **`homeworks/hw1`–`hw5`** — the course's progressive assignments, largely
  untouched; this fork works through them for the off-grid use case rather
  than skipping them.
- **`logs/`** — JSON trace output from the chat backend.

## Data

- `data/sample_queries.csv` — 50 rows (grown from the upstream 3), dietary
  and equipment edge cases. Protected, see DOMAIN_REGISTRY P-02.
- `homeworks/hw4/reference_files/processed_recipes.json` — 200-recipe
  reference corpus from Homework 4. Not yet confirmed as the live retrieval
  corpus vs. test fixture only; that confirmation is Phase 1 work.

## Known gaps at baseline (not yet fixed by this foundation build)

- No lint/test/build tooling configured.
- No CI pipeline.
- `MODEL_NAME`/`MODEL_NAME_JUDGE` env vars not yet pointed at Anthropic.
- `system_prompt.md` is still the generic upstream prompt, not the off-grid
  audience prompt (Homework 1, first unit of Phase 1 work).
- A prior, informal task attempt
  (`tasks/TASK-20260801-expand-dataset/`, untouched by this governance
  system) expanded `sample_queries.csv` but did not expand the recipe
  corpus or run any verification. Left as-is; the first BRIEF accounts for
  it.
