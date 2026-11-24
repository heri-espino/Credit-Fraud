# experiment004 — Expanded Seaborn exploratory and model diagnostics

## Why

The project owner requested more interpretive visualizations **before** the full 699,960-row run, covering original predictors, nonlinear interactions, class-specific distributions, model quality, tuning, errors, uncertainty, and interpretability. The notebook remains the **single required course submission artifact**; this directory archives reproduction notes, aggregate numerical validation, and representative figures.

## What was changed

Extended `credit_card_fraud.ipynb` from 56 to 96 cells, keeping the 15 model-candidate configurations and five identical stratified CV splits unchanged. Added Seaborn/Matplotlib figures with consistent labels, titles, explanatory legends, and saved PNGs. Existing model selection, predictions and Kaggle submission logic are unchanged.

**Additional exploratory plots (before fitting):**

- `20`: single-predictor discrimination measured by direction-agnostic univariate AUC (30k fixed-seed sample; *not* multivariate feature importance)
- `21`: class-conditional ECDF comparison (equal-class sampling; not fraud prevalence)
- `22`: categorical × Boolean fraud-rate heatmaps with sample counts (all training rows)
- `23`: weekday × hour fraud prevalence and cell support (all training rows)
- `24`: pairwise feature geometry by class (class-balanced plot-only sampling)
- `25`: train-versus-test marginal ECDFs (unlabeled test, matched 12k fixed-seed samples)

**Additional diagnostics after five-fold evaluation:**

- `26`: four-score comparison (ROC AUC, average precision, log loss, Brier)
- `27`: OOF AUC versus CPU wall-clock cost
- `28`: held-out score distributions within true class
- `29`: cumulative fraud capture and lift by review budget
- `30`: precision and recall at top 0.1–10% review fractions
- `31`: confusion matrices for 0.5 probability cutoff and top-1%-rank decision rule
- `32–33`: OOF reliability across candidates plus Wilson 95% intervals for a fixed candidate
- `34` (two figures): descriptive subgroup ranking by `channel` / `merchant_category`; require >=20 fraud and >=20 legitimate cases
- `35`: pairwise Jaccard overlap for top-1% high-risk sets
- `36`: fixed first-fold logistic signed coefficients / tree model-internal importance, not permutation importance
- `37`: computationally bounded model partial-dependence curves, logistic versus spline logistic versus XGBoost (not causal)
- `38`: best single versus OOF-selected ensemble score changes by true class
- `39`: unlabeled test-vs-train OOF score distribution sanity check
- `40`: OOF hyperparameter configuration comparisons across model families
- `41`: shared held-out-fold AUC heatmap

All new plots have descriptive Markdown explanations and save into `outputs/figures/`. A CSV figure catalog is written after the final diagnostics. Models are not refit for plotting; PD and importance use saved fold-1 models when `SAVE_FOLD_MODELS=True`. Set `RUN_PDP=False` to skip PD if time or RAM is constrained. Existing sections 1–11, logistic assumptions and logit-offset boosting are preserved.

## Reproducible validation performed on 2026-11-22

1. **Syntax and structure:** notebook validated with `nbformat.validate` and all Python code cells compiled.
2. **Expanded EDA:** all six added EDA code sections executed on the original Kaggle train/test files. Group fraud rates use *all* 699,960 training rows; display plots are sampled explicitly in the notebook. Figure previews and aggregate tables saved here.
3. **Model/plot smoke test:** executed five-fold CV on **4,000** stratified labeled rows for fixed `logit_C1`, `logit_spline_C1`, `offset_xgb_depth2_lr05`, `rf_depth12_leaf10`, and `xgb_depth3_lr08`; tree counts limited using existing `FAST_DEV_RUN=True`. Used a 400-row test feature slice to speed prediction, with saved fold models enabled. All existing diagnostic plot sections and **all new post-model plots**, including partial dependence and feature importance, executed after correcting a near-zero floating-point Wilson interval plotting edge case.
4. In the 4k smoke test, logistic OOF ROC AUC was approximately **0.930162**, and offset boosting **0.929897**. These are **not** the full-data performance, cannot be compared to separate earlier 6k/15k smoke tests, and should not be reported as Kaggle results.
5. Full 699,960-row × 15-candidate × 5-fold sweep remains **unrun**. Final choice and upload of `outputs/submission.csv` are pending. The 400-row test slice used for graphical smoke checks was not submitted or packaged.

## Reproduce

1. Obtain the project ZIP plus your original Kaggle `playground-series-s6e11.zip` (the competition archive is intentionally not redistributed).
2. From `final_project/`, install `requirements.txt`, open `credit_card_fraud.ipynb`, and set `FAST_DEV_RUN=True`, `MAX_CANDIDATES_PER_FAMILY=1` for a quick smoke test. Execute all cells; selected smoke candidates may differ from this five-family validation.
3. For final execution, restore `FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`, `N_SPLITS=5`. Set `SAVE_FOLD_MODELS=True` to enable importance/partial-dependence figures. `RUN_PDP` is an independently controlled visualization switch.
4. Compare `outputs/candidate_metrics.csv`, `outputs/fold_metrics.csv`, `outputs/ensemble_metrics.csv`, `outputs/figure_catalog.csv`, and numbered figures. The 15×5 model sweep is computationally substantial; reserve resources and disk.
5. Keep `outputs/`, raw competition data, `.joblib` models and row-level predictions private. Before publishing code to this *public* GitHub repo, comply with the Kaggle public-code-sharing rule by also publishing the code to the competition's Kaggle Notebook or Discussion.

## Findings/interpretation

The new full-train categorical/flag heatmaps show large **marginal** differences; for example `auth_method=No Authentication` and `is_foreign_transaction=True` had 36.58% observed fraud among 1,427 training observations. This is descriptive, not causal nor necessarily representative of a deployed payment system. Model plots from the 4k-row smoke test are numerical/visual **execution validation only**, not evidence of model superiority on all data.

## Next step

Execute the complete training and evaluation in the notebook, and preserve final aggregate fold metrics, figure catalog, key plot exports and a new sequential `experiment005` write-up. Prefer separate untouched holdout/nested CV if making an unbiased final-performance claim. Do not publicly release code before meeting the competition's publication rules.
