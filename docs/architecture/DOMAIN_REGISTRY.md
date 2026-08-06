# RCBT Domain Registry (protected zones)

Each protected zone names the file it protects, what it protects, and the
changes prohibited without constraint review. These are the designed
decisions future agents must not helpfully undo.

## P-01: System prompt content

- File: `backend/system_prompt.md`
- Protects: the off-grid audience contract — no electricity/refrigeration
  assumptions unless flagged, no supermarket-only ingredients, ingredient
  tier awareness, precise measurements, explicit time/temperature, output
  format (serving size, ingredients, numbered steps, notes).
- Prohibited without constraint review: any edit that loosens or removes
  these constraints, or that changes the output format the eval/judge
  pipeline (Homework 3+) is built against.
- Note: `backend/utils.py` only loads this file (`_PROMPT_PATH`) and calls
  the model; it is not itself the protected content, but changes to how it
  loads or post-processes the prompt are Mutative and should reference this
  zone in the PLAN.

## P-02: Sample query coverage

- File: `data/sample_queries.csv`
- Protects: the only real content diff this fork has made from upstream —
  50 rows covering dietary-restriction and equipment-limitation edge cases,
  consumed by `scripts/bulk_test.py`.
- Prohibited without constraint review: bulk rewrites or row deletions that
  reduce edge-case coverage. Additive rows (new queries) do not require
  review; removing or overwriting existing rows does.
