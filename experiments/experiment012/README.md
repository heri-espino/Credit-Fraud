# experiment012 — Unsupervised projections and clustering features

**Date:** 2026-11-24. **Status:** Two reduced-sample experiments executed; the existing final training/ensemble notebooks were **not** modified. Executable notebooks, scripts, and the interactive dashboard are delivered privately in `Credit-Fraud_experiment012_cluster_dashboard.zip`. This public repository contains the methodological record until corresponding competition code is shared through the competition-associated Kaggle Notebook/Discussion as required.

## Question and rationale

Can new covariates describing a transaction's position relative to clusters discovered without the fraud labels improve the original depth-5 XGBoost classifier? This creates **new predictors**, not synthetic training rows.

**Visual dashboard:** 4 complementary embeddings — PCA, t-SNE, Isomap, FastICA — plus a correlation heatmap, class-conditional ECDFs and K-means/DBSCAN clustering projections. Visualization uses 2,200 deliberately fraud-enriched points (330 fraud = 15%) to make minority patterns visible, whereas the real full train prevalence remains 11,689 / 699,960 (1.67%). DBSCAN/K-means cluster diagnostics use a representative unlabelled random sample, **not** that enriched view. Embedding plots are descriptive and do not establish fraud-class separation or natural group validity.

**Predictive ablation:** For each stratified outer fold, fit preprocessing, robust-scaled 6D PCA geometry and clustering entirely on that fold's training observations. Compare the same XGBoost configuration and folds with (i) original features, (ii) K-means centroid distances/soft memberships, (iii) DBSCAN local kNN/core-neighbor/noise features, and (iv) both. Select K-means k among 3,5,8,12 using training-only silhouette while also recording inertia; select DBSCAN epsilon using training-only kNN-radius quantiles and label-free cluster diagnostics. DBSCAN has no ordinary inductive predict method, so derive distances to training core samples for unseen observations.

### First pilot — 30,000 observations, 3 folds, 180 trees

| Feature set | OOF ROC AUC | Average precision | Δ AUC vs baseline |
|---|---:|---:|---:|
| Original | **0.938588** | **0.461704** | — |
| + K-means | 0.936604 | 0.456546 | −0.001984 |
| + DBSCAN | 0.937427 | 0.460838 | −0.001161 |
| + both | 0.937966 | 0.458093 | −0.000622 |

### Larger pilot — 100,000 observations, 5 folds, 350 trees

| Feature set | OOF ROC AUC | Average precision | Δ AUC vs baseline |
|---|---:|---:|---:|
| Original | 0.942572 | **0.471417** | — |
| + K-means | 0.941714 | 0.463036 | −0.000858 |
| + DBSCAN | **0.942856** | 0.470733 | **+0.000284** |
| + both | 0.941629 | 0.463381 | −0.000943 |

Paired stratified bootstrap, **600 resamples** on 100k OOF predictions, identical resampled observations for every model:

| Δ AUC vs baseline | Observed Δ | 95% percentile interval |
|---|---:|---:|
| DBSCAN features | +0.000284 | [−0.000632, +0.001067] |
| K-means features | −0.000858 | [−0.002317, +0.000565] |
| Both | −0.000943 | [−0.002453, +0.000521] |

**None of the three intervals excludes zero.** K-means silhouette was typically 0.22–0.29 and the selected k changed across folds (12,12,3,3,12), which does not support a stable natural partition. DBSCAN cluster counts and noise rate varied with fold and radius.

## Interpretation

The slightly higher DBSCAN ROC AUC in the larger pilot did **not** improve average precision, did **not** reproduce in the earlier pilot and its paired confidence interval includes zero. The evidence is insufficient to add clustering features to the final notebook. These pilot scores cannot be numerically compared with the earlier 699,960-row OOF benchmark. The paired-bootstrap intervals do not account for post-selection optimism, fold estimation variability, or possible dependence between transactions.

## Reproduction

Extract the privately distributed experiment patch into the **root of this repository** without deleting existing `outputs/` or old experiments. Then run in PowerShell:

```powershell
conda activate lds1071-fraud
python -m pip install -r .\experiments\experiment012\requirements.txt

# Interactive, self-contained dashboard:
python .\experiments\experiment012\build_dashboard.py --data .\playground-series-s6e11.zip --output .\outputs\experiment012\dashboard

# Five-fold pilot:
python .\experiments\experiment012\cluster_feature_experiment.py --data .\playground-series-s6e11.zip --sample-rows 100000 --folds 5 --n-estimators 350 --geometry-fit-rows 15000 --dbscan-rows 2300 --output .\outputs\experiment012\pilot_100000

# Paired uncertainty, no retraining:
python .\experiments\experiment012\bootstrap_ablation.py --input .\outputs\experiment012\pilot_100000\private_oof_predictions.npz --output .\outputs\experiment012\pilot_100000 --replicates 600
```

The two Jupyter notebooks are `experiments/experiment012/dashboard_projections.ipynb` and `experiments/experiment012/clustering_xgboost.ipynb`.

### Verification

Both notebooks were executed end-to-end (clustering notebook with a reduced synthetic execution protocol); separate synthetic unit tests passed; dashboard generated from all 699,960 real labeled records for prevalence, and four class-distribution projections; HTML contents and CSV/PNG outputs checked. Chromium's headless screenshot attempt timed out, so interactive browser rendering was not independently verified. No GPU was available; XGBoost used CPU. Full 699,960-row five-fold feature ablation has **not** run.

### Next

Leave the existing final notebook unchanged; use the experiment as evidence of a tested but unproven feature-engineering hypothesis. Only consider full-data evaluation or alternative density configurations if there is a practical reason to pursue a gain this small. Store original Kaggle data and row-level OOF privately; do not commit to public Git.
