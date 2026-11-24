# AGENTS.md — Kaggle final project (scoped)

Read repository-root `README.md`, `AGENTS.md`, `docs/handoff.md`, then this file and `final_project/notes/HANDOFF.md` before editing. Preserve lecture PDFs, course notebooks, and all prior experiments unchanged.

- Single course-deliverable notebook: `final_project/credit_card_fraud.ipynb`.
- Number future experiments consecutively: `experiment001`, `experiment002`, etc. Document purpose, parameter ranges, exact run commands, fold scores, limitations, and next steps.
- Competition deadline: 2026-11-30 23:59 UTC. Metric: ROC AUC. Target: `is_fraud`. Drop `id` from model features.
- Critical: repository is **public** and competition rules require public competition code to be shared **also** on the competition's Kaggle forum/notebook. Do not push this notebook or derivative competition code publicly until that condition is satisfied. No dataset redistribution. `.gitignore` must exclude input CSVs, model files, outputs, and secrets.
- Avoid data leakage: preprocessing and PCA inside each CV fold. Use common StratifiedKFold(5, shuffle=True, random_state=42) and an honest holdout/nested CV for unbiased selection assessment if added.
- Retain all candidate metrics and OOF predictions; do not equate 5-fold ensembling to independent bootstrap bagging.
- `n_jobs=-1` within one estimator at a time. Do not nest full parallel CV/search around estimators using all cores.
- Do not merge PRs without explicit user approval; check branches/PRs and preserve concurrent work.

- `experiment002` adds exploratory Seaborn plots and spline logistic regression while preserving `experiment001` files.
- Include plot titles, axes, units, legends where appropriate, source/sample caveats, and saved PNGs. Keep class-conditional density plots distinct from actual fraud-rate plots.
- Save all aggregated EDA rates, model fold metrics, and model results. EDA anomalies are not automatic exclusions. SplineTransformer belongs inside each CV fold.
- Limit BLAS internal threads to avoid slowdown from oversubscription; do not nest outer and inner `n_jobs=-1`.

- `experiment003` adds assumption diagnostics and a `logistic_offset_xgb` model; never pass predicted *probabilities* as XGBoost `base_margin`. Use raw LR `decision_function` logits at **fit and inference**, fitted inside each CV fold. Compare OOF metrics, not training residuals, and retain both stage components for diagnostics.
- The completed smoke test uses 6,000 rows, not the full dataset; do not claim a full-run gain or a Kaggle score. For full run expect 15 configurations × 5 outer folds (75 fits), with two stages in offset candidates.

## experiment004 extension

The current notebook is 96 cells. New figures 20–25 run as EDA, 26–41 run after five-fold model fitting. All post-model comparisons use OOF scores; avoid computing metrics from training-fit predictions or treating class-balanced display samples as prevalence. Fold-1 importance and partial dependence are descriptive and require saved models (`SAVE_FOLD_MODELS=True`), with an optional `RUN_PDP` switch. Do not erase previous experiments. Record full model results as sequential experiment005. Competition-code publication restriction remains in force.


## experiment005 — environment, native CatBoost, and nested hyperparameter searches
- Prefer `environment.yml` on PowerShell, register `lds1071-fraud` ipykernel, and keep `requirements.txt` synchronized with pip dependencies.
- `CATBOOST_DEVICE='auto'` and `XGBOOST_DEVICE='auto'` each probe a real CUDA fit; both use CPU when CUDA is unavailable. XGBoost uses `tree_method='hist'`, `device='cuda:0'` after a verified probe, else `device='cpu'`. XGBoost **may silently switch to CPU**, so record the actual trained booster device, not the requested device. The logistic-offset XGBoost second stage shares this resolved device. GPU-related training failures can retry on CPU.
- CatBoost consumes categorical features natively. `CatBoostNativePreprocessor` is fitted on each fold's training part, never on held-out data.
- GridSearchCV with inner stratified folds occurs only on a stratified subset of the corresponding outer fold's training data; selected parameters are refitted on the full outer training fold before OOF evaluation. Do not select inner params using outer validation metrics.
- Keep `GRID_SEARCH_N_JOBS=1` by default to avoid parallel GPU jobs and nested CPU oversubscription.
- Record grid results/best parameters and final OOF metrics. Explicitly state that overall model/blend selection is optimistic without a held-out dataset.
- Preserve experiment001–004; source notebook must not be pushed to public GitHub without the required competition-associated Kaggle sharing.

## experiment005 CUDA preference amendment (same sequential experiment)

The user's preferred behavior is **GPU for XGBoost grid search when available**, matching CatBoost. `XGBOOST_DEVICE='auto'` probes a real CUDA-trained booster, inspecting `save_config()` to reject silent CPU fallback. All fixed XGBoost and logit-offset boosting models use the resolved backend too. When GPU is active, search jobs run sequentially (`GRID_SEARCH_N_JOBS=1`) to avoid VRAM oversubscription. Preserve `model_device` in inner search and outer OOF metric files. CPU-only smoke validation passes, but GPU hardware validation is still pending; do not claim GPU speedup without timing evidence. Continue to respect Kaggle's public sharing restriction.
