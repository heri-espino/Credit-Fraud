# experiment013 — full 699,960-row clustering feature ablation

**Executed 2026-11-24** on the full Kaggle S6E11 labeled train set. This is the full-data continuation of experiment012, **not** a re-run of the project's final ensemble comparison. Results were generated in an available Linux CPU environment after the self-hosted runner preflight found no Kaggle data in its checkout.

## Fixed protocol

- Dataset: 699,960 transactions; 11,689 frauds; 24 source predictors, excluding `id`.
- Common 5-fold shuffled `StratifiedKFold(random_state=42)` for all candidates; 20 supervised XGBoost fits in total.
- Fixed model: XGBoost with `n_estimators=350`, `max_depth=5`, `learning_rate=0.05`, `min_child_weight=5`, logistic objective, histogram trees, four CPU threads.
- Four feature sets: **baseline**, **+ K-means distances/memberships**, **+ DBSCAN nearest-core/density indicators**, **+ both**. This is feature engineering, *not* synthetic observation generation.
- All transformations and unsupervised hyperparameter choices fit **within each outer training fold**. The supervised model trains using every outer-training row; geometry fits use a reproducible 15,000-row training-only PCA/K-means reference and a 2,300-row training-only DBSCAN reference. Clustering does **not** fit on all ~560k training rows in each fold.
- K-means `k∈{3,5,8,12}` compared via training silhouette/inertia; DBSCAN eps tested at training-only kNN distance quantiles. This preserves the previous pilot's configuration.

## Results — pooled OOF

| Features | ROC AUC | Average precision | Log loss | Brier | Δ AUC |
|---|---:|---:|---:|---:|---:|
| Baseline | 0.94570236 | **0.50090996** | **0.04614440** | **0.01114034** | 0 |
| + DBSCAN | **0.94570502** | 0.50064558 | 0.04615806 | 0.01114135 | +0.00000266 |
| + K-means | 0.94543602 | 0.49856464 | 0.04626607 | 0.01116563 | −0.00026634 |
| + both | 0.94545948 | 0.49866808 | 0.04626507 | 0.01116637 | −0.00024289 |

Training plus unsupervised feature construction completed in **203.59 seconds** with no incomplete folds. All 699,960 OOF entries for all four variants were verified finite and within [0,1]. The selected K-means sizes were [12,12,12,12,8]; the DBSCAN fitted density solutions had two or three clusters per fold.

### Paired stratified bootstrap

1,000 matched, class-stratified resamples of the **same OOF rows**, random seed 20261124. The ROC AUC differences are always relative to the baseline:

| Augmentation | Observed Δ | 95% percentile CI | Fraction of resamples Δ > 0 |
|---|---:|---:|---:|
| DBSCAN | +0.00000266 | **[−0.00013921, +0.00015842]** | 0.514 |
| K-means | −0.00026634 | [−0.00048527, −0.00004689] | 0.007 |
| Combined | −0.00024289 | [−0.00048304, −0.00002497] | 0.017 |

**Conclusion:** DBSCAN is statistically indistinguishable from the unaugmented baseline on conditional OOF resampling and marginally worse on AP/log loss/Brier. K-means-derived features show lower AUC. **Keep the original feature set**; do not modify the finalist notebook to include clustering on these results.

These bootstrap intervals are conditional on predictions already selected and fitted. They do **not** correct for hyperparameter exploration, between-fold estimation, or possible dependence between transactions. The synthetic Kaggle data may not behave like real bank transaction data. The point estimate from experiment012's 100k pilot (+0.000284 for DBSCAN) did not persist on full data (+0.000003).

## Files

Version-controlled aggregate files are under `results/`: `summary.csv`, `fold_metrics.csv`, `cluster_diagnostics.csv`, `paired_auc_bootstrap.csv`, `run_manifest.json`, `environment_provenance.json`.

The full *private* experiment patch with executable scripts, tests, results-only executed Jupyter notebook, figures and run logs is delivered in `Credit-Fraud_experiment013_full_699960_results.zip` in the project conversation. The 699,960-row label/OOF array is **not in Git**; it is saved separately as `Credit-Fraud_experiment013_private_oof.zip`.

Full experimental commands (PowerShell, from repository root, after extracting the private patch and supplying the competition ZIP):

```powershell
conda activate lds1071-fraud
python .\experiments\experiment013\cluster_feature_experiment.py --data .\playground-series-s6e11.zip --sample-rows 0 --folds 5 --n-estimators 350 --jobs 4 --geometry-fit-rows 15000 --dbscan-rows 2300 --output .\outputs\experiment013\full_699960
python .\experiments\experiment013\bootstrap_ablation.py --input .\outputs\experiment013\full_699960\private_oof_predictions.npz --output .\outputs\experiment013\full_699960 --replicates 1000 --seed 20261124
```

The source implementation and outputs are preserved privately because publicly sharing Kaggle competition code also requires sharing it on the contest-associated Kaggle Notebook/Discussion. No original CSV/ZIP, fitted binaries or transaction-level OOF data are committed.

## Runner preflight

A GitHub Actions check did reach **PCAG103A-15** (Windows x64, Conda and NVIDIA-SMI visible), but the runner's fresh checkout did **not** contain the Kaggle archive in the checked locations; the default Python was 3.14.7 with no XGBoost/scikit-learn. Therefore these results were computed locally in the available Linux CPU environment, **not** on the Windows runner. To execute this there, supply an explicit local dataset path and select the correct Conda environment; workflow is now manual-only.

Next sequential experiment ID: **experiment014**, only if a new modeling hypothesis is justified.
