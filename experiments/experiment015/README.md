# experiment015 — Cluster-augmented logistic-offset XGBoost (full-data OOF)

**Executed November 24, 2026.** Full 699,960 labeled rows, five stratified shuffled folds (seed 42). Original finalist notebooks are unchanged.

## Research question

Earlier experiment014 measured whether cluster-derived features improved *standalone* logistic regression; experiment013 compared gains under standalone XGBoost. **Neither experiment tested the two-stage logistic-offset XGBoost.** This experiment does: it initializes XGBoost with the fitted logistic regression's log-odds as `base_margin` and learns binary-logistic-loss corrections.

Mathematical model: `p(x) = sigmoid(f_LR(x) + g_XGB(x))`, with `f_LR(x) = beta_0 + beta^T phi(x)`. The logistic score is supplied as `base_margin` to XGBoost during **both fit and inference**. This is neither standard stacked generalization nor squared-error regression on fixed probability residuals.

## Experimental design

- Common outer 5-fold StratifiedKFold with random_state 42; `id` is removed.
- Four unique fitted logistic baselines per fold: original features, K-means distances/memberships, DBSCAN core/density distances, and both feature groups.
- Five XGBoost corrections per fold: original, K-means in both stages, DBSCAN in both stages, both groups in both stages, and `combined_lr_only` (both groups in logistic; only original features in the booster). The last variant reuses the combined logistic baseline.
- Fixed logistic regression: L2, C=1, lbfgs, max_iter=600; fold-only median imputation, StandardScaler and reference-level one-hot encoding.
- Fixed correction: XGBoost 240 trees, depth 3, learning rate 0.05, min_child_weight 5, subsample 0.85, colsample_bytree 0.85, hist, logistic loss and base_margin; not re-tuned post hoc.
- The same geometry class and fold-only settings as experiments013/014: PCA 6D after robust preprocessing; K-means candidates 3,5,8,12 (15k training-only reference), DBSCAN epsilon selection on 2,300 training-only reference observations. All supervised stages use every outer-training row.
- 20 logistic fits, 25 XGBoost corrections. All 699,960 OOF scores per model finite and in [0,1]. Ran in 238.4 seconds on an available Linux CPU, **not** the Windows self-hosted runner.

## Pooled OOF results

| Hybrid architecture | ROC AUC | Average precision | Log loss | Brier | Delta AUC |
|---|---:|---:|---:|---:|---:|
| Combined clustering in logistic only | **0.946160624** | **0.507244901** | **0.045807001** | **0.011053274** | **+0.000058273** |
| Original logistic-offset XGBoost | 0.946102351 | 0.507152395 | 0.045818659 | 0.011053446 | 0 |
| DBSCAN in both stages | 0.946065957 | 0.506380552 | 0.045853673 | 0.011063945 | -0.000036394 |
| Both clustering groups in both | 0.945986981 | 0.506576108 | 0.045855633 | 0.011061022 | -0.000115370 |
| K-means in both | 0.945969872 | 0.506620698 | 0.045855695 | 0.011060125 | -0.000132479 |

The baseline logistic-only stage had ROC AUC 0.941356842; when both cluster feature groups were added to that first stage, ROC AUC rose to 0.941549671. Its improvement did **not** carry through consistently after XGBoost corrected its logits.

## Paired class-stratified bootstrap

1,000 resamples, same resampled record indices for every candidate, seed 20261124. All nominal 95% percentile intervals for differences against original logistic-offset **contain zero**.

| Augmentation | Delta OOF AUC | Percentile 95% CI |
|---|---:|---:|
| Combined in logistic only | +0.000058273 | [-0.000127384,+0.000237351] |
| DBSCAN in both | -0.000036394 | [-0.000183208,+0.000110444] |
| Both groups in both | -0.000115370 | [-0.000320443,+0.000077265] |
| K-means in both | -0.000132479 | [-0.000318528,+0.000055891] |

**Decision:** retain the original finalist and treat experiment015 as a completed marginal/negative feature-engineering result. The gain of +0.000058 is not statistically established. The original historical best-model OOF AUC (~0.946205) was obtained in an earlier execution environment. The present experiment re-fitted a matched CPU baseline (0.946102); only its **within-run paired differences** are used for inference. We do not present the new top score as beating the previous original run.

## Reproducibility

The privately delivered ZIP `Credit-Fraud_experiment015_hybrid_clustering_full_results.zip` contains runnable scripts, a 12-cell executed review notebook, PNG figures, 25 fold metric records, 40 geometry diagnostic rows, saved aggregated metrics, provenance/manifest, test output and training logs. The separate `Credit-Fraud_experiment015_PRIVATE_OOF.zip` contains the 699,960 labels and nine OOF arrays; it must **never** be published in this public repository.

From PowerShell in the repository root, after overlaying the private patch:

```powershell
conda activate lds1071-fraud
python .\experiments\experiment015\test_hybrid.py
python .\experiments\experiment015\logistic_offset_clustering.py --data .\playground-series-s6e11.zip --sample-rows 0 --folds 5 --n-estimators 240 --jobs 4 --geometry-fit-rows 15000 --dbscan-rows 2300 --output .\outputs\experiment015\full_699960
python .\experiments\experiment015\bootstrap_comparison.py --input .\outputs\experiment015\full_699960\private_oof_predictions.npz --output .\outputs\experiment015\full_699960 --replicates 1000 --seed 20261124
jupyter lab .\experiments\experiment015\logistic_offset_clustering_review.ipynb
```

Tests passed: synthetic weighted tie-aware ROC AUC equality with scikit-learn, XGBoost base_margin dependence at inference, complete 2-fold five-variant synthetic run and small real-data smoke run. Executed review notebook passed all code cells. Full-data XGBoost ran on CPU. Hashes and exact software versions are recorded in the private ZIP.

**Scope and uncertainty:** This conditional OOF bootstrap does not account for repeated customers, fold-training uncertainty, dependence, model comparison multiplicity or earlier feature-selection exploration. All new code and record-level output stay in private project archives pending compliance with Kaggle's competition-associated public code-sharing requirement. This GitHub commit contains only documentation/aggregates. Next experiment ID: experiment016.