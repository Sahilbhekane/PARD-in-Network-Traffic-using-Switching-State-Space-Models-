# Contributing

Thanks for your interest in PARD-SSM. This is an academic research project, and
contributions that improve rigour, reproducibility or clarity are especially welcome.

## Getting set up

```bash
git clone https://github.com/Sahilbhekane/PARD-in-Network-Traffic-using-Switching-State-Space-Models-.git
cd PARD-in-Network-Traffic-using-Switching-State-Space-Models-
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m pytest -q
```

## Ground rules for changes

1. **Keep the evaluation honest.** Order must never be shuffled; fit selectors and scalers on
   training data only; choose thresholds on validation data only; touch the test partition once.
2. **Report negative results.** If a change does not help, say so in the PR.
3. **Keep results reproducible.** Any new number should come from a script in `scripts/` or
   `experiments/`, with a fixed seed. If metrics change, re-run
   `python scripts/export_artifacts.py --dataset <name>` and `python scripts/make_figures.py`.
4. **Add tests** for new behaviour and run `python -m pytest -q` before opening a PR.
5. **Do not commit** raw datasets, processed arrays, secrets or large binaries.

## Pull requests

- Branch from `main`, keep PRs focused, and fill in the PR template.
- CI must pass (tests on Python 3.10-3.12 and figure regeneration).

## Reporting issues

Use the issue templates. For bugs, include your OS, Python version and the versions of
numpy, scikit-learn, pandas, scipy and joblib.

## Licence

By contributing you agree that your contributions are licensed under the Apache License 2.0.
