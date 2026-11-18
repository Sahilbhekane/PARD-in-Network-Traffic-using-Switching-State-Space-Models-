## Summary
<!-- What does this change and why? -->

## Checklist
- [ ] `python -m pytest -q` passes locally
- [ ] Any new result is reproducible from a script in `scripts/` or `experiments/`
- [ ] If metrics changed, `artifacts/*/metrics.json` and `docs/figures/` were regenerated (`python scripts/make_figures.py`)
- [ ] Docs / README updated where behaviour changed
- [ ] No raw datasets, secrets or large binaries are committed
