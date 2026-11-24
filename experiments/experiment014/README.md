# experiment014 — Logistic regression with cluster-derived features

**Executed:** 2026-11-24. **Complete dataset:** 699,960 labeled transactions (11,689 fraudulent). **Protocol:** 5 shuffled stratified folds (seed 42); four input feature sets; **20 logistic-regression fits**. The finalist competition notebooks were not changed.

## Question

In experiment013, K-means and DBSCAN features did not improve XGBoost. Could the same nonlinear geometric features be more useful to a model with a linear logit, specifically penalized logistic regression?

Every fold fits the original numeric imputation/scaling, reference-level one-hot categoricals, six-dimensional PCA geometry, K-means, DBSCAN and derived-feature scaling using *training observations only*. The supervised model uses every row in the outer training partition; only unsupervised geometry is sampled (15,000 rows for PCA/K-means and 2,300 for DBSCAN). K-means selects k ∈ {3,5,8,12} by training silhouette; DBSCAN radius is selected from training kNN distance candidates. The class labels are never used in clustering.

**Estimator:** `LogisticRegression(C=1, penalty="l2", solver="lbfgs", max_iter=400, tol=1e-4, class_weight=None)`. Every fold converged without warnings. The original design contains 49 encoded features, DBSCAN 55, K-means 69–77, combined 75–83. Training and feature engineering completed in **142.8 s** in an available Linux CPU environment, **not** the Windows runner.

## Full pooled out-of-fold results

| Features | ROC AUC | Average precision | Log loss | Brier | Δ AUC |
|---|---:|---:|---:|---:|---:|
| Original | 0.941356842 | 0.486234633 | 0.047246398 | 0.011335365 | 0 |
| + K-means | 0.941511039 | 0.487335838 | 0.047184613 | 0.011320189 | +0.000154197 |
| + DBSCAN | 0.941451258 | 0.486430596 | 0.047227021 | 0.011332916 | +0.000094416 |
| **+ Both** | **0.941559127** | **0.487348829** | **0.047175832** | **0.011320619** | **+0.000202285** |

The expanded logistic model has marginally better AUC, AP, log loss and Brier than the logistic baseline. But its gain is exceptionally small.

## Paired bootstrap, conditional on full OOF scores

**1,000 paired class-stratified resamples** of all 699,960 rows using identical sampled indices for all four models, seed 20261124. Nominal 95% percentile intervals for **ΔAUC against original logistic regression**:

| Augmentation | Δ AUC | 95% percentile interval | Bootstrap fraction Δ > 0 |
|---|---:|---:|---:|
| Combined | +0.000202285 | **[−0.000009261,+0.000422475]** | 0.965 |
| K-means | +0.000154197 | [−0.000027990,+0.000359717] | 0.951 |
| DBSCAN | +0.000094416 | [−0.000067751,+0.000253895] | 0.870 |

**All intervals include zero.** There is no demonstrated nominal-95% positive gain over original logistic regression.

## Comparisons with the earlier full-data XGBoost experiment013

XGBoost baseline ROC AUC was **0.945702363**, and XGBoost with combined clusters **0.945459477** (Δ **−0.000242885**); both outperform even the best logistic regression score (0.941559127). Because the logistic and XGBoost pipelines use different supervised preprocessing/encoding suitable to each estimator, this is a descriptive between-pipeline comparison, not an isolated causal estimator-class contrast.

A **secondary, same-row paired bootstrap** tested the *difference between the clustering-induced AUC changes*:

| Augmentation | (LR gain) − (XGB gain) | Nominal 95% percentile interval |
|---|---:|---:|
| Combined | **+0.000445170** | **[+0.000155034,+0.000767890]** |
| K-means | **+0.000420539** | **[+0.000143914,+0.000732889]** |
| DBSCAN | +0.000091759 | [−0.000135377,+0.000303578] |

This is compatible with K-means-derived features being **relatively more useful for the logistic pipeline** than for XGBoost, even though the within-logistic gain is not established. These are exploratory, post-selection OOF intervals, not fully nested or independent generalization intervals. Multiple candidate comparisons and possible transaction dependence are not accounted for.

## Reproduction and files

The full, runnable scripts, tests, figures, run logs, standalone and executed results-review Jupyter notebook, and complete aggregate CSVs are in the privately delivered `Credit-Fraud_experiment014_logistic_clusters_full_results.zip`. They reproduce the experiment without changing the original finalist notebook. The 699,960-row labels and OOF vectors are in a **different private archive**, `Credit-Fraud_experiment014_private_oof.zip`, which must not be committed.

After applying the private experiment patch at repository root and making the original Kaggle competition ZIP available:

```powershell
conda activate lds1071-fraud
python .\experiments\experiment014\logistic_cluster_ablation.py --data .\playground-series-s6e11.zip --sample-rows 0 --folds 5 --geometry-fit-rows 15000 --dbscan-rows 2300 --C 1 --max-iter 400 --output .\outputs\experiment014\full_699960
python .\experiments\experiment014\bootstrap_ablation.py --input .\outputs\experiment014\full_699960\private_oof_predictions.npz --output .\outputs\experiment014\full_699960 --replicates 1000 --seed 20261124
jupyter lab .\experiments\experiment014\logistic_clustering_review.ipynb
```

All 20 full model fits were verified, all OOF arrays finite and within [0,1], no convergence warnings; synthetic 900-row two-fold contract test and execution of the 15-cell review notebook both passed. Full training dataset SHA256 `d07c8f46b7bba8b076682cf787bbb39e0c46a85ec4b6dd50fe186f322244a344`. Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0.

**Decision:** The results do not justify replacing the better-performing XGBoost finalist or inserting extra clustering into the final project. Preserve as a negative/marginal feature-engineering experiment. Next sequential experiment: `experiment015`, if a new hypothesis warrants it.

**Publication safeguard:** This is a public GitHub repository. Public competition code sharing must also satisfy the competition's Kaggle Notebook/Discussion requirements. This commit contains only text documentation and aggregate statistics, not new executable competition code, raw data, models, or row-level predictions.
