# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-11-15

### Added
- Order-preserving data pipeline with a chronological 60/20/20 split and a 20-row embargo
  (`src/data_processing/loaders_v2.py`).
- Hybrid pipeline: SelectKBest + scaler fitted on training data only, two-regime Kalman-filter
  bank, Random Forest, validation-selected decision threshold (`src/pipeline/hybrid.py`).
- `scripts/export_artifacts.py`: trains, evaluates, exports and re-verifies one dataset's pipeline.
- Exported artifacts for CICIDS2017 and UNSW-NB15 (`artifacts/`).
- FastAPI inference service (`backend/`) with health, demo and predict endpoints.
- Ablation, baseline and statistical-significance scripts (`experiments/`).
- `scripts/make_figures.py`: regenerates result charts from `artifacts/*/metrics.json`.
- API and data-processing tests (28 tests in total); GitHub Actions CI on Python 3.10-3.12.
- Final project report (`docs/Final_Report.pdf`) and Explorer screenshots.
- README, `CITATION.cff`, contributing guide and issue / PR templates.

### Changed
- README rewritten to match the final report: reproduced held-out results are presented
  first, the earlier shuffled-split results are kept for transparency and clearly marked
  as not comparable and not reproduced.
- Documented that the reproduced pipeline uses two hand-set regimes, not learned parameters.

### Removed
- Claims of early-detection performance: the earlier lead-time metric came from shuffled
  data and does not reflect temporal detection.

## [0.1.0] - 2026

### Added
- Original research implementation: Kalman filter, EKF, UKF and switching Kalman filter
  (GPB2, Viterbi, EM), dataset loaders, feature engineering, metrics and visualisation.
