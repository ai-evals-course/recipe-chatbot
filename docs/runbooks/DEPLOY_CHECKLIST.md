# RCBT Deploy Checklist

No CI pipeline exists yet. Manual run only — there is no sanctioned deploy
path today. This checklist is written so it's ready the moment one exists;
until then, treat every "Deploy" step below as N/A and do not substitute a
manual deploy/rollback command for it.

Pre-deploy (all classes):
- [ ] CI green (build, static checks, test suite) — N/A until CI exists.
- [ ] Governance docs for this change updated in the same PR.
- [ ] Protected-zone invariants confirmed unchanged
      (`docs/architecture/DOMAIN_REGISTRY.md`), or constraint review recorded.

Mutative adds:
- [ ] Rollback target captured.

Destructive adds:
- [ ] Architecture sign-off recorded before the PR opened.
- [ ] Registry docs updated in this same PR.
- [ ] Rollback target captured live immediately before merge.
- [ ] Observed monitor planned for after deploy.

Deploy:
- [ ] Shipped via the sanctioned CI path — none exists yet. No direct
      deploy commands; update this line when `DEPLOY_PATH` is real.

Post-deploy:
- [ ] Smoke tests and health checks pass.
- [ ] Rollback tested or standing by.
- [ ] Registry row flipped to Complete once verified live.
