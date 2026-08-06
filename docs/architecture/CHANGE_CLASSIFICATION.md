# RCBT Change Classification

Every change is Additive, Mutative, or Destructive. When unsure between
Mutative and Destructive, treat as Destructive.

**Additive** — adds behavior without altering what exists.
Example: adding a new recipe to the corpus (e.g. a new fermentation recipe)
without changing existing recipes, schema, or retrieval behavior.
Ceremony: standard deploy checklist.

**Mutative** — changes existing behavior or data in place.
Example: editing `backend/system_prompt.md` to tighten the off-grid
constraint language, changing how an existing chatbot response is shaped for
every future query.
Ceremony: deploy checklist plus a captured rollback target.

**Destructive** — removes or irreversibly transforms.
Example: changing the recipe corpus storage format (e.g. flat markdown to
structured JSON with a new schema), which invalidates or requires migrating
every existing recipe record.
Ceremony: architecture sign-off before the PR opens, registry docs updated
in the same PR, rollback target captured live immediately before merge,
observed monitor after deploy.
