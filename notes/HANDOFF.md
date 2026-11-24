# Agent handoff — Credit Fraud, migration of experiment011 sources

## Verified current state
The dedicated repository `heri-espino/Credit-Fraud` originally contained the main modeling notebook, ensemble notebook, experiments 001–005 and an earlier 20/75-slide Spanish presentation. This migration aligns it with the most recent privately distributed work through **experiment011** while preserving the older artifacts as historic versions.

- Latest clean main notebook: 100 cells; CatBoost, XGBoost CUDA fallback, nested parameter grids, OOF evaluation.
- Ensemble extension: 22 cells; cached fold logistic models/predictions, 4 strategies compared with best standalone.
- Paired bootstrap: 12 cells; requires `experiments/experiment010/bootstrap_core.py`, cached OOF predictions and Kaggle labels on the owner's PC.
- Short deck v11: 36 Spanish slides, 21 figures, EDA/PCA and probabilistic target explanation, planned 18.1 minutes.
- Long deck v10: 93 Spanish slides, 51 figures and extensive statistical methodology.
- Latest OOF AUCs: offset XGB .9462047549947218; XGB standalone .9461201492641279; RF stack .9457469470932846; probability blend .9432801044177533; explicit residual .9402409115631302.
- Paired bootstrap (B=600; seed=20261123): offset-minus-fixed-XGB delta 0.0000846057306, 95% CI [-0.0002625875,0.0004397256].
- The tuned `xgb_nested_grid` OOF vector has **not** been provided in the ensemble ZIP; re-run only the bootstrap notebook when it is available from `outputs/all_candidate_predictions.npz`.

## Machine and workflows
Owner reported an idle self-hosted **Windows X64** runner `PCAG103A-15`. A read-only, manually dispatched workflow is installed to lint notebooks, inspect CUDA/Conda and compile presentation outputs when local figure inputs are supplied. No execution of the 699,960-row modeling run is triggered automatically. The runner's working directory is not equivalent to the previously used local project directory; cached model files must be supplied separately if reused in Actions.

## Reproducibility and caveats
The official competition dataset, trained fold binaries and per-transaction predictions are not committed. Existing older executed notebook binary content remains as a historical archive reference. Presentation PDF/HTML in the historic archive reflect **earlier versions**; the current Marp Markdown sources are canonical, and freshly built outputs are workflow artifacts.

The public GitHub repository previously already held competition modeling source. Verify required corresponding Kaggle public Notebook/Discussion publication before further code distribution. Avoid false claims of independent statistical significance; the bootstrap still uses models selected on OOF data. Do not change old experiments or PRs without review.

## Next actions
1. On the Windows workstation, restore `outputs/` from the previous run without deleting local fitted models.
2. Verify `outputs/all_candidate_predictions.npz`, `outputs/ensemble_extension/five_way_oof_and_test_predictions.npz`, the original labeled CSV/ZIP, and optionally the `xgb_nested_grid` OOF column.
3. Run the `paired_bootstrap_comparison.ipynb` only if updated comparisons are required.
4. Use Actions manual workflow with figure directory to compile latest HTML/PDF. Keep generated files as artifacts or use Git LFS/external storage, not ordinary repeated large Git blobs.
5. Record any new analyses as `experiment012`.


## experiment012 — Dashboard and fold-leakage-safe clustering features (2026-11-24)

Executed PCA/t-SNE/Isomap/FastICA dashboard over a deliberately 15%-fraud-enhanced 2,200-row **display sample**, retaining the real 1.67% base rate in summary metrics; added a separate 7k representative unlabeled clustering diagnostic and feature distributions. Tested K-means centroid distances/soft memberships and DBSCAN kNN/core distances/noise features as new covariates for the previously selected fixed depth-5 XGBoost configuration. All clustering decisions were made within outer training folds. Pilots: 30k, 3 folds, 180 trees (original AUC .938588; all augmentations worse); 100k, 5 folds, 350 trees (original .942572; DBSCAN .942856; K-means .941714; both .941629). DBSCAN average precision .470733 versus baseline .471417. Paired bootstrap B=600 gave ΔAUC DBSCAN +.000284, CI [−.000632,+.001067]. No established improvement; user-facing final notebooks remain unchanged.

Reproducible scripts/notebooks, dashboard HTML and aggregate results are delivered in the owner's private `Credit-Fraud_experiment012_cluster_dashboard.zip`, which excludes Kaggle data and row-level OOF arrays. Two synthetic unit tests and both notebook execution paths passed; HTML build passed structural checks but Chromium screenshot timed out. Record/method are at `experiments/experiment012/README.md`. This public GitHub update contains documentation only until Kaggle's corresponding code-publication requirement is fulfilled. Preserve all previous experiments and runner configuration.


## experiment013 — Full 699,960-row XGBoost cluster-feature ablation (2026-11-24)

Actual full-data 5-fold training completed: 4 variants × 5 held-out folds, 350 XGBoost trees, max_depth=5, learning_rate=0.05, min_child_weight=5. Full OOF AUC: baseline **.9457023626**, DBSCAN **.9457050194**, K-means **.9454360212**, combined **.9454594775**. AP: baseline **.5009099588** highest; DBSCAN .5006455843; K-means .4985646416; combined .4986680849. All 699,960 OOF records per model validated, 20 fold-metric rows and training-only cluster geometry diagnostics preserved. K chosen by silhouette [12,12,12,12,8]. Training runtime 203.59 seconds on Linux CPU. Paired stratified bootstrap (B=1000, seed=20261124) DBSCAN Δ+.0000026567, 95% CI [−.0001392108,+.0001584177]; K-means Δ−.0002663414 CI [−.0004852698,−.0000468889]; combined Δ−.0002428851 CI [−.0004830440,−.0000249722]. This resolves the prior 100k pilot's inconclusive +.000284 DBSCAN signal: no meaningful gain on full data. Do not add these features to the final notebook.

Checked the user’s Windows GitHub Actions runner `PCAG103A-15`: job reached the machine, but GitHub checkout did not find the competition archive, and default Python 3.14.7 lacked sklearn/XGBoost (Conda and NVIDIA tools exist). Therefore executed the complete experiment in the available local Linux CPU container; **do not claim the Windows runner performed the full training**. Preflight workflow was made manual-only after testing.

Aggregate results/manifest/versions and README were committed to `experiments/experiment013/`; executable code and figures are in `Credit-Fraud_experiment013_full_699960_results.zip`; private row-level OOF arrays are separately in `Credit-Fraud_experiment013_private_oof.zip`. Synthetic geometry tests, tie-aware weighted AUC/paired-bootstrap tests and an executed 11-cell results-review notebook passed. Next planned experiment index: `experiment014`; only pursue a genuinely new hypothesis with independent verification.

## experiment014 — 699,960-row logistic cluster-feature ablation (2026-11-24)

Ran full five-fold CV, identical fold split seed 42 and fold-only K-means/DBSCAN geometry as experiment013, replacing XGB with `LogisticRegression(C=1,L2,lbfgs)` with appropriate fold-only original-feature standardization and reference-onehot, and fold-only scaling of derived features. All 20 models converged; 699,960 finite OOF probabilities per candidate. Pooled AUC baseline .941356842, +KMeans .941511039, +DBSCAN .941451258, +combined .941559127; AP baseline .486234633, combined .487348829. Paired stratified bootstrap B=1000: combined AUC gain +.000202285, CI [−.000009261,+.000422475]; KMeans +.000154197 CI [−.000027990,+.000359717]; DBSCAN +.000094416 CI [−.000067751,+.000253895]. None excludes 0. Secondary paired comparison of differences in clustering-induced gains LR minus XGB: combined +.00044517 CI [+.00015503,+.00076789], but this is conditional, post-selection, and pipelines differ in scaling/encoding. XGBoost exp013 original AUC .945702 still higher than all logistic variants. No changes to finalized notebook.

Full scripts, tests, 15-cell results-review notebook (executed), figures, aggregate CSV/JSON and logs preserved in user's `Credit-Fraud_experiment014_logistic_clusters_full_results.zip`; original row-level labels and OOF stored separately in `Credit-Fraud_experiment014_private_oof.zip`. Verified full training runtime ~143 s Linux CPU (not Windows runner), synthetic 900-row contract tests, OOF integrity, 1000 bootstrap, and notebook execution. Github includes documentation/aggregate metrics only due Kaggle public-sharing rules. Next experiment ID `experiment015`.

## experiment015 — Full two-stage logistic-offset XGBoost with cluster features (2026-11-24)

Different from standalone experiments013/014, this completed five-fold OOF run evaluates actual LR logit offsets passed to depth-3, 240-tree XGBoost at training and inference. All 699,960 rows scored once per hybrid variant. Baseline offset ROC AUC .946102351; combined clusters only in LR .946160624 (Δ +.000058273); DBSCAN in both .946065957; both cluster groups in both .945986981; K-means in both .945969872. Stage-only LR original .941356842 vs LR combined .941549671. Paired stratified bootstrap B=1000 Δ combined-LR-only vs original +.000058273 CI [−.000127384,+.000237351] includes zero; other intervals also include zero. No established improvement. Historical original finalist .946204755 comes from a different execution and should not be confused with the matched CPU baseline here. Keep final notebook unchanged.

Completed 20 LR + 25 XGB fitted corrections, 5 folds (all out-of-fold probabilities finite), 238.4 seconds in Linux CPU container, not PCAG103A-15. Synthetic contract test verified `base_margin` semantics and tie-aware weighted AUC; 12-cell review notebook executed. All code, figures, full metrics/logs/manifest in private `Credit-Fraud_experiment015_hybrid_clustering_full_results.zip`; raw row-level labels/OOF vectors only in private `Credit-Fraud_experiment015_PRIVATE_OOF.zip`. Public GitHub retains only aggregate CSV records and documentation pending Kaggle code-publication compliance. See `experiments/experiment015/README.md`; next `experiment016`.

## experiment016 — Cuaderno final consolidado (2026-11-24)

ZIP privado Credit-Fraud_notebook_final_es.zip: notebook_final_es.ipynb (50 celdas, 25 ejecutables), 19 gráficos Seaborn/Matplotlib en español, datos agregados verificados de los experimentos 008/010/013/014/015, diccionario de variables e instrucciones PowerShell. Contiene EDA completo, PCA/SVD 90%, FastICA y t-SNE opcional, K-means/DBSCAN, supuestos logísticos, 19 candidatos con búsqueda anidada documentada, cuatro ensambles, bootstrap y decisión. No reentrena los modelos originales por defecto.

Validación: las 25 celdas de código ejecutadas secuencialmente sobre 699,960 observaciones con caché OOF; 19 gráficos y CSV de 299,984 filas generado y mantenido privadamente. Offset XGB AUC .946204755, XGB fijo .946120149; Δ+.000084606, IC95 B=600 [-.000262587,+.000439726]; no diferencia fiable. Los experiments 013–015 quedan preservados y no justifican cambiar finalista.

Solo documentación en repositorio público hasta que el código fuente pueda publicarse también en Kaggle conforme a las reglas. Ver experiments/experiment016/README.md. Próximo experimento experiment017.
