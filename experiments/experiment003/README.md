# experiment003 — Logistic regression with XGBoost logit-offset correction

## Research question
Does a shallow XGBoost model initialized with **logistic regression logits** improve OOF credit-fraud ranking (Kaggle ROC AUC), average precision, log loss, or probability calibration over standard logistic regression and standalone XGBoost? This extends the earlier exploratory nonlinearity and assumption checks without overwriting experiments 001/002.

## Algorithm
Each of five stratified outer folds independently fits the numeric/categorical preprocessor, then L2-logistic regression to the *training* fold. `XGBClassifier.fit` receives the logistic `decision_function` **logits** of the same training rows as `base_margin` under `objective='binary:logistic'`; validation and test `predict_proba` must receive the matching logistic logits as their own `base_margin`. The training correction is fitted sequentially on the training fold only, with the logistic component frozen. The corrected model uses `sigmoid(LR_logit + tree_correction)`; it is **not** a probability average, ordinary regression on binary residuals, or bootstrap bagging. Report assumptions audited in notebook Section 5.1, and sequential-boosting details in Section 5.2.

## Reproduction
From the folder `final_project/`, with the original Kaggle `playground-series-s6e11.zip` beside the notebook, install `pip install -r requirements.txt` and run `credit_card_fraud.ipynb` (all cells). For quick smoke execution, configure:

```python
FAST_DEV_RUN = True
DEV_SAMPLE_SIZE = 6000
MAX_CANDIDATES_PER_FAMILY = 1  # for a minimal run; see below for exact smoke candidates
SAVE_FOLD_MODELS = False
```

**Exact archived smoke comparison:** 6,000 stratified rows, shared 5 folds, seed 42, `n_jobs=2` for the test machine, candidate names `logit_C1`, `offset_xgb_depth2_lr05`, `offset_xgb_depth3_lr05`, and `xgb_depth3_lr08` (filtered after building candidates). Development mode caps offset-tree counts at **45** and standalone XGBoost at **70**; the full-run grid instead uses offset models (160 depth-2 trees and 240 depth-3 trees) plus the earlier models. This distinction is essential when interpreting the scores. The scratch test harness `test_offset_boost.py` in this package reproduces the exact selection and metrics without executing EDA figures. It reads the private dataset at runtime, rather than bundling the dataset.

## Observations (SMOKE ONLY: not full-data or leaderboard estimates)

| Model | OOF ROC AUC | OOF average precision | OOF log loss | OOF Brier |
|---|---:|---:|---:|---:|
| L2 logistic `logit_C1` | 0.941169 | 0.497645 | 0.046494 | 0.011254 |
| Offset XGB depth 2 | 0.940566 | 0.489127 | 0.047091 | 0.011376 |
| Offset XGB depth 3 | 0.939514 | 0.481798 | 0.047366 | 0.011411 |
| Standalone XGB depth 3 | 0.919934 | 0.307894 | 0.056035 | 0.013576 |

Neither tested offset model improved ROC AUC, average precision, log loss, or Brier in this small smoke run. See CSVs for all fold-level comparisons and `figures/19_logistic_offset_boosting_diagnostics.png` for the binned residual and logit correction figures. No data or model artifacts were sent to Kaggle or GitHub.

## Limitations
- Only 6,000 of 699,960 labeled rows were used in this smoke test; fraud events are correspondingly few.
- The corrected gradient-boosted model is still allowed to overfit; lower training residuals are not guaranteed to improve validation scores.
- Baseline and correction share each fold's fitted preprocessing; **no validation labels** entered their fit, but selecting a winner based on OOF scores remains statistically optimistic.
- Logistic assumptions are reviewed in the notebook; the boosted correction relaxes linear log-odds but not sampling independence, dataset shift or leakage concerns.
- For the full sweep there are **15 candidates × 5 folds = 75 fits** (some candidates contain two sequential estimators). The full sweep has NOT been run.

## Next actions
1. Run all 15 candidates on the full training set with `FAST_DEV_RUN=False`, `MAX_CANDIDATES_PER_FAMILY=None`.
2. Compare fixed baseline LR versus two offset candidates and standalone XGB using paired folds; investigate mean/std across folds and bootstrap uncertainty on an independent holdout if available.
3. Retain results, model artifacts and figures with sequential experiment documentation; do not push competition code publicly without complying with Kaggle's public sharing rule.
