# experiment002 — Seaborn visualization, nonlinear structure, and anomalies

## What and why

Extended experiment001 without modifying its source CSV metric summaries. Added explanatory Seaborn figures, a nonlinear spline-logistic baseline, and two non-destructive outlier diagnostics. Questions: (1) Does marginal fraud prevalence vary nonlinearly? (2) Are risk variables interacting? (3) Do multivariate anomalies overlap with fraud? (4) Does additive spline logistic outperform linear logistic under five-fold CV?

## Reproduce

1. Install `final_project/requirements.txt` and place original Kaggle `playground-series-s6e11.zip` alongside the notebook (or unzip to `data/`).
2. Run `final_project/credit_card_fraud.ipynb`. EDA uses full 699,960 labeled rows for rates and fixed-seed representative samples of 30,000 for plotting / IsolationForest; figures are saved to `outputs/figures/`.
3. For a small code-path smoke test, temporarily set `FAST_DEV_RUN=True`, `DEV_SAMPLE_SIZE=3000`, `MAX_CANDIDATES_PER_FAMILY=1`, `N_JOBS=2`, and `SAVE_FOLD_MODELS=False`. The actual developer check additionally limited test rows to 3000 and RF/XGBoost trees to 10/12 **only in the validation copy**. Restore full-run defaults for real submissions.
4. Full run: `FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`. Training 13 candidate configurations with five stratified folds = **65 fitted pipelines**. Save and evaluate all candidates/OOF predictions. Do not extrapolate the smoke-test scores.

## Findings: descriptive full-training-set EDA

- Fraud prevalence 1.67%. Transaction amount has a nonmonotone binned association; velocity and merchant risk have strong curved associations; very short time since last transaction has elevated fraud rates.
- The high-high quintile of `merchant_risk_score` and `velocity_score` has **9.10%** observed fraud versus **0.03%** in the low-low quintile (binned counts roughly 29k per cell). These are marginal comparisons, not causal effects or a conditional interaction test.
- Conservative 3×IQR fences flag 61,219 transaction amounts (8.75% of labeled rows) and 479 high merchant-risk scores (~0.068%). Some extremes are genuine observations; they are kept for modeling.
- A 30,000-row unsupervised Isolation Forest diagnostic with `contamination=0.02` flagged 600 transactions; **85/600 = 14.17%** were fraudulent, versus **410/29,400 = 1.39%** among unflagged observations. The scores are on the same sample used to fit the anomaly detector and are not an out-of-sample fraud classifier result.

## Validation

A reduced test executed the five model families (linear logistic, spline logistic, PCA logistic, random forest, XGBoost) across 5 folds, plus all post-CV figures and Kaggle file-format assertions, successfully. Exploratory plots generated successfully using full train labels for rates. Full-data model hyperparameter runs are pending.

## Limits and next steps

`experiment001` results remain authoritative as the **first** 15k smoke test; the newly added spline candidate has not been benchmarked in a comparable full 15k run. EDA-informed selection can bias reported OOF scores even if transforms are fitted per fold; use untouched holdout/nested CV for a final generalization claim. Pairwise heatmaps do not establish conditional interactions. Do not remove or relabel unusual transactions without justification. Publish notebook on Kaggle first if making competition code public in GitHub.
