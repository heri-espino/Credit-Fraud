# Handoff — Experiment001 / Credit-card fraud

## Origin and goal

LDS1071 final Kaggle project. User requested a simple single notebook with EDA, PCA/SVD retaining about 90% feature variance, logistic regression/random forest/XGBoost, hyperparameter tuning, five-fold CV, `n_jobs=-1`, all important metrics, and an ensemble of retained candidate models.

## Dataset inspection (2026-11-22)

- Source: the user's uploaded `playground-series-s6e11.zip`, not checked into the repo.
- `train.csv`: 699,960 rows × 26 columns (24 predictors + `id` + `is_fraud`). `test.csv` matches predictors and `id`.
- Target: 11,689 fraud / 688,271 legitimate (fraud prevalence approximately 1.66995%). No missing training cells.
- Predictors: numerical, bool, and five categorical columns (`merchant_category`, `card_type`, `auth_method`, `channel`, `device_type`).
- The `id` column is excluded as a predictor. Same ordered test ids as `sample_submission.csv`.

## Design

- `experiment001`: diagnostic PCA curve, PCA vs no-PCA logistic regression, random forest, and XGBoost. A small explainable parameter grid (11 candidates) is fitted across **the same** 5 stratified folds.
- Leakage prevention: preprocessing, PCA, and model in a pipeline trained only on each fold's training subset.
- Every candidate retains all five fold metrics, the aggregated OOF prediction and mean test prediction. Fitted fold models are optional (`SAVE_FOLD_MODELS`).
- Evaluate best single candidate, top-three, best-per-family, and all-candidate equal-weight blends. Model selection on OOF scores induces selection optimism; further work should create an untouched holdout/nested CV.
- `n_jobs=-1` within forests and XGBoost only; outer loop sequential to avoid oversubscription.

## Publishing blocker

Repository `heri-espino/LDS1071-Machine-Learning` is **public** (inspected by GitHub connector). The uploaded official rules §3.6 say public competition code must *also* be shared in a competition-associated Kaggle forum/notebook. Until this is done, the notebook must **not** be pushed to GitHub. Avoid any publication of competition record-level data or predictions. GitHub repository had no open PRs when checked.

## Validation

Notebook structurally validated (22 cells, all code cells compile) and executed end-to-end using nbclient. `experiment001/README.md` records the 15,000-row, four-candidate, five-fold smoke results: logistic AUC 0.95225, PCA logistic 0.93247, random forest 0.93707, XGBoost 0.94725, equal-weight blend 0.95000; 299,984-row submissions passed format assertions. The smoke test was performed with model serialization disabled; full-run default now enables fold model persistence. The actual 699,960-row, 55-fit sweep has **not** been run. Never claim a full-data Kaggle ROC AUC from smoke-test scores.

## Next steps

1. Run smoke test with `FAST_DEV_RUN=True`, `MAX_CANDIDATES_PER_FAMILY=1` and verify all cells/exported files.
2. Run with defaults on a suitably provisioned machine, inspecting memory and full CV scores.
3. Publish competition code via Kaggle competition Notebook/Discussion if publication is desired, **then** commit/push project code to the public GitHub repository.
4. Create `experiment002` with separate holdout/nested CV and potentially calibrated weights only after experiment001 is preserved.


## Continuation: visualization extension — experiment002 (2026-11-22)

Expanded the single notebook to 49 cells. Added Seaborn data investigation: class imbalance, distribution comparisons, Pearson/Spearman matrices, grouped categorical/Boolean fraud rates and Wilson 95% intervals, six quantile-binned nonlinear curves, time effects, two pairwise interaction tables with counts, 3×IQR outliers, IsolationForest anomaly scores, and plotted model-selection diagnostics. All generated figures are saved under ignored `outputs/figures/`. Added additive `SplineTransformer` + logistic regression as a fifth model family (13 candidates/65 fits full run). PCA remains separate and fold-safe; no outliers automatically removed. Fixed seeds and user-facing warnings about data-derived choices and selection optimism are preserved.

Validation: all EDA visualizations ran on original 699,960 labeled rows where rates need them (point-level EDA sample at 30,000). Smoke validation ran 5 families × 5 folds on a *temporary* 3,000-row training and 3,000-row test slice with severely shortened tree counts; all downstream plots, predictions, and submission formatting succeeded. These validation numbers are not performance evidence. A previous larger test ran the EDA + 2 logistic models and PCA/RF plus two of five XGBoost folds but exceeded runtime; the reduced validation is the definitive code-path check. Do not claim the full 65-fit experiment or final submission has run.

Full-run next actions: unzip original competition archive by placing it beside the notebook; install `requirements.txt`; use `FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`, `SAVE_FOLD_MODELS` as disk permits, execute all cells, review PCA/no-PCA/spline comparisons and outlier interpretation, and record final OOF metrics. Publication restriction remains in effect until public Kaggle discussion/notebook sharing.

## Continuation: logistic-regression assumptions + offset gradient boosting — experiment003 (2026-11-22)

The 56-cell notebook includes a 10-condition assumptions audit (Section 5.1), including data-dependence uncertainty, linear log-odds doubts, numerical VIF, univariate separation, sampling, calibration, and convergence. To mitigate redundant reference categories in logistic pipelines, `OneHotEncoder(drop='first')` is now used; rerun metrics before interpreting previously recorded smoke estimates. Section 5.2 adds the custom `LogisticOffsetXGBClassifier` with stage-1 L2-logit and stage-2 XGBoost classifier (binary logistic loss) trained with stage-1 logits as `base_margin`, including predict-time offsets. Section 8.4 provides binned OOF residual curves, logit correction profiles, and paired score comparisons. All stage-specific OOF arrays save under local outputs.

Validation: all code cells compile, and a dedicated smoke harness executed five outer folds each for fixed LR, both offset candidates, and a standalone XGB candidate on 6,000 stratified rows, with capped tree counts and no model serialization. Figure 19, two stage-specific `.npz` files, candidate/fold metrics and submissions were verified on this diagnostic subset. Offset depth-2 and depth-3 were worse than LR by 0.00060 and 0.00166 OOF ROC AUC on that subset; not full-data results. Archived test harness and numeric results under `experiments/experiment003/`. Full **15×5** candidate sweep on 699,960 rows remains pending; publication gate applies to all competition code and derivative records.

## Continuation: broad diagnostic visualization — experiment004 (2026-11-22)

The notebook now has 96 cells and 15 candidate configurations × five folds unchanged. It adds six EDA analysis sections (figures 20–25) and fourteen model/ensemble diagnostics plus visualization catalog (figures 26–41, with one doubled subgroup figure). Original experiment001–003 figures and code are preserved. All figures saved under `outputs/figures/`; numerical aggregates saved in `outputs/`. A near-zero negative floating-point error-bar delta for empty fraud bins was fixed by clamping Wilson interval half-widths to zero.

Validation: syntax/nbformat check passed; full-train added EDA 20–25 executed; a targeted five-fold 4,000-row smoke run tested five named model families and generated all added model figures (including importance and PD). Unit smoke used a 400-row Kaggle test **feature** slice only, and no Kaggle submission/leaderboard evaluation. Model smoke ROC AUC: `logit_C1` ≈ 0.930162, `offset_xgb_depth2_lr05` ≈ 0.929897, which should NOT be interpreted as full-data estimates. Detailed scope, plots, aggregate metrics and next steps are archived in `experiments/experiment004/`.

Next: execute the complete 699,960-row 15 × 5 experiment, check figure catalog, score calibration and chosen ensemble before Kaggle submission, then preserve full results as experiment005. Keep Kaggle-public-code sharing restriction in mind; notebook remains out of public GitHub until also published through Kaggle competition.


## experiment005 (2026-11-22): Conda + PowerShell, CatBoost and nested GridSearchCV
- Added `environment.yml` (Python 3.11, pip dependencies, ipykernel) and extended requirements (CatBoost, SciPy, JupyterLab). README contains step-by-step PowerShell setup, kernel registration and GPU troubleshooting.
- Notebook adds CatBoost with a fold-fitted numeric/categorical preprocessor that preserves DataFrame category names; NVIDIA CUDA probe chooses `GPU` if possible, else `CPU`. XGBoost is explicitly CPU with internal threads.
- Added two new CatBoost baseline candidates and two search-tuned candidates `xgb_nested_grid`/`catboost_nested_grid` (19 total, 95 full outer CV fits). The latter perform a 3-fold `GridSearchCV` over 8 candidates, using up to 20,000 observations from each outer train fold, then refit best settings on the **entire** outer train fold. Saves grid tables, best params, inner fit-time, visualizations.
- 240 extra inner fitted pipelines across two tuned families in full mode; reduced modes are available. This is a nested tuning comparison, not a final unbiased competition winner estimate because the overall winning family/blend is selected using OOF scores.
- Exact executable notebook is retained in owner-delivered ZIP, not in the public GitHub repository because of competition public code-sharing requirements. Runtime smoke evidence must be recorded in `experiments/experiment005/README.md`; full dataset training remains to be run.

### experiment005 GPU preference amendment — same experiment, not a new experiment number

The owner requested that **XGBoost GridSearchCV use GPU when possible**. Added notebook flags `XGBOOST_DEVICE='auto'` and `XGBOOST_GPU_ID='0'`; a tiny CUDA fit probes availability and inspects `get_booster().save_config()` because XGBoost may *silently fall back* to CPU if CUDA was requested without a visible device. Resolved backend drives fixed XGB, `grid_xgboost`, and logistic-offset correction stage. CUDA exceptions during an XGB inner search or outer refit trigger CPU retry; CatBoost already has its own device probe/fallback. `GRID_SEARCH_N_JOBS=1` prevents concurrent training on shared VRAM. Search and fold metric files now contain **actual backend** information. `tree_method='hist'` stays enabled for both CPU and CUDA.

Validated notebook compilation plus a 5-fold, 3k-row smoke test covering fixed XGBoost, nested XGBoost grid, fixed and grid-tuned CatBoost, and logistic regression; separate logit-offset-XGB fold smoke also passed. All ran **on CPU** because this runtime has no GPU, verified by XGBoost's actual trained booster configuration. CUDA behavior, performance and Windows Conda installation remain to be tested on an NVIDIA-equipped workstation. Full dataset 19 candidate × 5-fold + 240 inner grid-fit experiment is *not* run. All runnable artifacts and experiment005 smoke aggregates remain in the owner-delivered ZIP; no original competition data or record-level predictions were distributed or committed publicly.
