# AGENTS.md — Credit Fraud

## Repository-first protocol
1. Read `README.md`, `notes/HANDOFF.md`, and the relevant `experiments/experimentNNN/README.md` before changes.
2. Inspect `main`, open PRs and the commit history; do not overwrite other agents' work or merge a PR without explicit authorization.
3. The repository root **is** the project root. Paths copied from the course repo must drop the prefix `final_project/`.
4. Preserve every existing notebook, figure, simulation summary and presentation; archive prior versions before replacing them. Label smoke results distinctly from full-run OOF metrics.
5. Use sequential experiment IDs; the next unallocated ID after this migration is `experiment012`. Every experiment must document what, why, reproduction, results, limitations, next steps.
6. Commit/push completed reproducible work. Do not force-push, commit credentials, raw Kaggle data, OOF/test row-level predictions, or fitted model binaries.

## Statistical contracts
- Binary target is `is_fraud`; `id` is not a predictor. Kaggle requires a probability, primary selection metric ROC AUC.
- Five stratified outer folds; fold-fit imputation, encoding, scaling, spline expansion and PCA to avoid leakage.
- XGBoost/CatBoost may use CUDA when genuinely available, otherwise CPU. Keep nested `GridSearchCV(n_jobs=1)` on one GPU, allowing estimator-level CPU parallelism where safe.
- Blending of probabilities is **not** classical bootstrap bagging. Logistic-offset XGBoost uses LR log-odds as `base_margin`; explicit residual XGBoost regresses `y - p_LR` separately. RF stacking consumes base-model OOF probability columns.
- The random-forest stacking meta-CV on cached OOF features is not fully nested; do not claim an unbiased model comparison or an independently tested Kaggle score.
- Paired stratified bootstrap resamples **identical row indices** for all models; its 600-replicate interval of the logit-offset minus fixed-XGBoost AUC difference includes zero. It does **not** resolve post-selection bias or possible customer/time dependence.
- Fixed-depth XGBoost (`xgb_depth5_lr05`) and `xgb_nested_grid` are distinct. Do not invent an AUC for the latter unless its OOF predictions are available.

## Repository artifacts and runner
- Core notebooks at root: `credit_card_fraud.ipynb`, `ensemble_comparison.ipynb`, `paired_bootstrap_comparison.ipynb`.
- Complete Spanish deck is v10; short Spanish deck is v11. Keep the `fraud-whitegrid` theme and small math consistent with text.
- `.github/workflows/verify-build.yml` is manually dispatched and runs on a self-hosted Windows x64 GitHub Actions runner. It validates/builds, **not trains**. Runner `PCAG103A-15` is a machine name, not automatically a GitHub Actions custom label.
- The local `outputs/` directory is intentionally Git-ignored; model artifacts on the runner's disk are not automatically accessible inside a fresh `GITHUB_WORKSPACE`.
- Publication of competition code from this public repository must satisfy Kaggle's associated competition-public-sharing requirements.
