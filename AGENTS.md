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


## experiment012 — Exploratory manifold and clustering ablations

A private experiment patch contains `experiments/experiment012/` with the dashboard (PCA, t-SNE, Isomap, FastICA), K-means silhouette/inertia and DBSCAN cluster-sensitivity diagnostics, and a *fold-fit* XGBoost ablation. Two pilots (30k/3fold/180trees; 100k/5fold/350trees) have been **executed**, with bootstrap B=600 on the larger OOF data. Treat results as exploratory: the +0.000284 DBSCAN AUC gain has CI [−0.000632,+0.001067] and slightly worse AP. No changes were made to the final training notebook. Geometric transformations, K selection, DBSCAN radius selection and cluster fitting must remain strictly inside each supervised outer training fold. Do not treat t-SNE/Isomap coordinates as inductively available predictors or use oversampled visualization prevalence for risk estimation. Source/data publication rule remains in force; consult `experiments/experiment012/README.md`. Next experiment index: `experiment013`.


## experiment013 — Full-data clustering test and decision

Completed all 699,960 rows, five stratified folds and four fixed-configuration XGBoost feature sets (20 fits). Derived K-means/DBSCAN features are produced from training-fold-only unsupervised reference samples (15k geometry, 2.3k DBSCAN), never from validation fold labels. Full OOF AUC baseline .94570236; DBSCAN .94570502; K-means .94543602; combined .94545948. Paired bootstrap B=1000 yields DBSCAN Δ+.00000266 CI [−.000139,+.000158], thus **no evidence of improvement**. Keep the existing final classifier unchanged. See `experiments/experiment013/README.md`. Store row-level OOF data only in private local/external archival storage; public Git contains aggregates and documentation. Next experiment number: **experiment014**.
