# Off-Grid Recipe Chatbot (RCBT) — Claude Code context

## Boundary (read first)

- This repo is a personal fork of `ai-evals-course/recipe-chatbot`, extended
  into an off-grid homestead recipe chatbot: meal planning, storehouse
  management, and cooking under real off-grid constraints (fuel, equipment,
  storage tier). It does not replace the upstream course files. Work ONLY
  inside this repository root.
- Do NOT read, reference, or act on files outside this repo, including
  parent directories and sibling projects. Ignore any CLAUDE.md inherited
  from a parent directory. If context seems missing, ask.

## Stack and commands

- Python (>=3.13), managed with `uv`. Backend: FastAPI (`backend/main.py`).
  LLM calls via LiteLLM; target provider is the Anthropic API
  (`claude-sonnet-4-6`) — `MODEL_NAME`/`MODEL_NAME_JUDGE` env vars currently
  default to OpenAI models from the upstream course, not yet switched.
- Tracing: JSON/JSONL to disk (`logs/`). Query sets: CSV (`data/`). Eval
  metrics: `judgy` (bias-corrected precision/recall with bootstrapped CIs).
- No lint/test/build tooling is configured yet (no ruff/pytest/mypy in
  `pyproject.toml`). Do not assume any exist.
- Setup: `uv sync`. Dev server:
  `uv run uvicorn backend.main:app --reload --reload-include '*.md'`.
- No CI pipeline exists yet. Manual run only.

## Working rules

- `main` is the source of truth. Never force-push. One logical change per
  commit. Push is deliberate.
- No code without an approved PLAN. No PLAN without an approved BRIEF. No
  ADR without a PLAN to derive it from.
- `docs/architecture/MILESTONE_REGISTRY.md` plus the milestone QA checklist
  is the only completion authority. Code landed is not QA closed. Never
  state a milestone is done from a handoff, a session doc, or memory.
- Owner-side living docs (`RCBT_CURRENT_STATE`, `RCBT_OPEN_DECISIONS`,
  `RCBT_CONSTRAINTS_AND_CONVENTIONS`) exist outside this repo, in Claude.ai
  project knowledge, and are never created or committed here. Docs are
  authoritative over memory. For permanent facts, repo beats chat.
- Every behavior-changing PR updates its governance docs in the same PR.
- This file only grows. Rules are appended, never deleted.
- `GO RCBT-M###` is the only merge authorization. Nothing else is a go. A
  placeholder in a GO message is refused. No agent merges on its own.
- Plan first for anything in `docs/architecture/DOMAIN_REGISTRY.md`. One
  protected-zone change in flight at a time. No speculative refactors.
- When unsure between Mutative and Destructive, treat as Destructive.
- Verification work touches no repo files; test apparatus lives in `/tmp`.
- CI is the only sanctioned deploy path (none exists yet). Never run deploy
  or rollback commands directly; a denial is an owner action, never worked
  around.
- Never accept, echo, or store credentials. Prompt at runtime.
- The stalled task scaffolding (`tasks/`, `.pi/`, `.project/`,
  `scripts/task-*.sh`) predates this governance system. Do not touch it
  without explicit instruction; it is not part of the BRIEF/PLAN/ADR flow.
