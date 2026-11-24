# experiment001 — Five-fold CV fraud classifier benchmark (smoke test)

## Purpose
Test the complete course-deliverable notebook, including preprocessing, PCA, 5-fold stratified cross-validation, model tuning infrastructure, model blending, diagnostics, and correct Kaggle submission format.

## Dataset and configuration
- Full input: 699,960 labeled training rows, 299,984 unlabeled test rows. Source is Kaggle playground-series-s6e11 and was **not** copied into this experiment folder.
- Smoke test: stratified sample of 15,000 training rows, random seed 42.
- Five stratified folds with shuffle, one hyperparameter candidate per family (four total), shortened random-forest / XGBoost estimator counts for development speed, `N_JOBS=2` for repeatable resource usage.
- Numerical and categorical preprocessing occurs within each fold; `id` excluded. Model types: logistic regression, PCA90 + logistic regression, random forest, XGBoost.
- Python environment: scikit-learn 1.8.0, XGBoost 3.1.3, pandas 2.2.3, NumPy 2.3.5.

## How to reproduce
From `final_project/`, place the user's Kaggle ZIP alongside the notebook or CSVs in `data/`. Temporarily set `FAST_DEV_RUN=True`, `MAX_CANDIDATES_PER_FAMILY=1`, `N_JOBS=2`, and `SAVE_FOLD_MODELS=False` (all in the config cell). Execute **all notebook cells in order**. Restore full-run defaults afterward.

## Results (exploratory; not full competition scores)

| Candidate | OOF ROC AUC | Average precision |
|---|---:|---:|
| Logistic regression | 0.95225 | 0.50886 |
| PCA90 + logistic regression | 0.93247 | 0.45387 |
| Random forest | 0.93707 | 0.37891 |
| XGBoost | 0.94725 | 0.45248 |
| Equal-weight blend, all four | 0.95000 | 0.49577 |

- Diagnostic sample PCA: 24/54 encoded dimensions retained ~90.65% feature variance (not target variance).
- The best-single-model strategy ranked first under ROC AUC on the smoke-test OOF data.
- Three correct-format Kaggle submissions were exported for 299,984 test observations, but **not uploaded** to Kaggle.
- Four candidate result records, twenty CV fold metric records, ensemble evaluations, and run manifest are saved in this folder. **Record-level OOF/test predictions, model binaries, and dataset rows are intentionally excluded from this portable experiment summary.** They remain in the local ignored `outputs/` folder after execution.

## Findings
PCA did not improve logistic ROC AUC in the smoke run; the four-candidate blend did not beat the individual logistic model. The experiment is useful only as a pipeline/infrastructure test, not a reliable ranking for full-scale tuning.

## Limitations
15k versus 699,960 rows; reduced XGBoost/RF tree counts; single candidate per family. Selecting the best on the same OOF folds is optimistic. The complete 11-candidate × five-fold run is not yet executed.

## Next steps
1. Run full data with `FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`; inspect cross-validated results and saved fold pipelines.
2. Avoid public code publication until the notebook is also posted on the competition's Kaggle Notebook/Discussion, as required by competition rules.
3. Preserve experiment001 outputs and create experiment002 for nested CV/untouched holdout/calibration if pursued.
