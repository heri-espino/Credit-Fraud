# experiment005 — Conda + nested XGBoost/CatBoost GridSearchCV (GPU preference)

## Goal

Make a reproducible course deliverable on Windows using Conda + PowerShell + `ipykernel`, extend the fraud-classifier benchmarking notebook with native-categorical CatBoost, and compare a prespecified 3-fold scikit-learn GridSearchCV for **XGBoost and CatBoost** inside five outer stratified folds. The owner additionally requested GPU acceleration for XGBoost when available. The notebook provides a CUDA probe and verified CPU fallback for **both** families; CUDA was unavailable in the validation environment.

## Methods

- The training input is Kaggle's original `playground-series-s6e11.zip`, which is **not** redistributed.
- Five shuffled stratified outer folds use identical indices across candidates. All learned preprocessing is inside each pipeline. Test labels remain unavailable; `id` is excluded as a predictor.
- Inner tuning is a maximum 20,000-row stratified subset **only from the respective outer training fold**. `GridSearchCV` tests 8 combinations × 3 inner folds per tuned family in the full run, optimizes ROC AUC, and keeps inner AP/time/grid results. The best configuration is fit on the full outer training fold, then evaluated on the held-out fold.
- Total planned full run: 19 candidate specifications × 5 outer folds = **95 outer fits**, including 10 selected grid-model refits; two grid searches cost **240 inner fits** beyond the outer fits. No full-data results exist yet.
- `XGBOOST_DEVICE='auto'` tries `tree_method='hist', device='cuda:0'`; a tiny actual fit is checked using XGBoost's trained booster config, since the requested device can otherwise be misleading. `CATBOOST_DEVICE='auto'` similarly probes native categorical GPU fit. Both fall back to CPU on GPU unavailability. XGBoost CUDA runtime errors during a grid/outer fit trigger a CPU retry.
- `GRID_SEARCH_N_JOBS=1` keeps GPU candidate fits serial to prevent VRAM contention. Other CPU-friendly learners may use internal `n_jobs=-1`.

## Validation (CPU hardware only; five-fold reduced-sample smoke)

- Notebook passes `nbformat.validate` and compiles all 100 cells' Python code.
- Fixed-seed stratified **3,000-row** development sample, five outer CV folds, only five representative families (logistic, fixed XGB, fixed CatBoost, nested-grid XGB, nested-grid CatBoost). CatBoost/boosted tree counts were shortened. Grid searches used two depth candidates × two inner folds on up to 1,200 rows per outer fold.
- All **25 outer fits** passed; the grid summary has **20 inner candidate entries**. The tested XGBoost booster explicitly reported **`cpu`** after the CUDA availability probe found no visible GPU; CatBoost reported CPU too. These checks establish the fallback and output schema; **GPU execution is not verified**.
- A separate five-fold 3k-row smoke test of `offset_xgb_depth2_lr05` also passed on CPU.
- ROC AUC and average precision are preliminary and **must not be presented as full-data estimates or Kaggle scores**:

| candidate            |   roc_auc |   average_precision |
|:---------------------|----------:|--------------------:|
| logit_C1             |   0.92982 |             0.44426 |
| xgb_depth3_lr08      |   0.81593 |             0.12987 |
| catboost_depth5_lr06 |   0.91997 |             0.38652 |
| xgb_nested_grid      |   0.91254 |             0.28644 |
| catboost_nested_grid |   0.91594 |             0.34160 |

## Archived files

- `smoke_test.py`: relative-path five-fold validation harness; run from the project environment with `python .\experiments\experiment005\smoke_test.py` from `final_project/` after copying Kaggle ZIP there.
- `smoke_candidate_metrics.csv`, `smoke_fold_metrics.csv`: OOF summary and fold-level metrics, including effective `model_device`.
- `smoke_nested_gridsearch_cv_results.csv`, `smoke_nested_gridsearch_best_by_fold.csv`, `smoke_nested_gridsearch_parameter_summary.csv`: searched configurations and selected parameters.
- `smoke_figures/42_*` and `43_*`: Seaborn grid exploration and held-out fold comparisons generated during the smoke test.
- `smoke_offset_candidate_metrics.csv`: separate offset-boosting training-path validation.

## Limitations and next actions

1. Test on the owner's NVIDIA workstation using `nvidia-smi` and confirm notebook device probe shows CUDA rather than CPU; compare timing and GPU VRAM usage.
2. Run default full configuration (`FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`); monitor disk, GPU memory, runtime, fold variability and overfitting. Consider allocating a held-out split to reduce selection optimism.
3. Review OOF ROC AUC, average precision, calibration, and the full GridSearchCV surface before selecting an ensemble. Produce valid `id,is_fraud` CSV submission without leaking labels.
4. Preserve all aggregate results and figures as **experiment006** if a new full-data experiment is performed. Keep raw records, model binaries, row-level predictions and all competition code private until public Kaggle sharing rules are satisfied.
