# Credit Fraud — Kaggle Playground Series S6E11

Reproducible course project on **probabilistic credit-card fraud prediction**. Target: `is_fraud` (0/1); submitted values are probabilities in `[0,1]`. Kaggle evaluates **ROC AUC**, not classification accuracy.

**Canonical repository:** [heri-espino/Credit-Fraud](https://github.com/heri-espino/Credit-Fraud). This repository is the project root; there is **no** nested `final_project/` directory. The initial work originated in `heri-espino/LDS1071-Machine-Learning/final_project`.

## Dataset and results

- Training: **699,960** transactions, **24** predictor variables (13 numerical, 5 categorical, 6 Boolean), plus `id` and `is_fraud`.
- Test: **299,984** transactions, with `id` and the 24 predictors.
- Fraud: **11,689** (1.67%); legitimate: **688,271** (98.33%).
- Five stratified folds; preprocessing and PCA fitted inside each fold. Candidate families: logistic regression, PCA-logistic, spline-logistic, random forest, XGBoost, CatBoost and logistic-offset XGBoost, including nested `GridSearchCV` experiments.
- The follow-up `ensemble_comparison.ipynb` evaluates blending, logistic-offset boosting, explicit residual XGBoost and random-forest stacking against the best standalone candidate.

| Model / strategy | Pooled out-of-fold ROC AUC | Average precision |
|---|---:|---:|
| Logistic regression + XGBoost logit correction | **0.946205** | **0.507424** |
| XGBoost standalone (depth 5, learning rate 0.05) | 0.946120 | 0.503585 |
| Random-forest stacking | 0.945747 | 0.506383 |
| Average-probability blending | 0.943280 | 0.500913 |
| XGBoost correcting explicit probability residuals | 0.940241 | 0.494046 |

The selected logistic-offset model exceeds standalone XGBoost by only **0.0000846 AUC**. A 600-replicate **paired stratified OOF bootstrap** gave a 95% percentile interval of **[−0.000263, 0.000440]** for the difference: this **does not establish** superiority. Model selection used these OOF predictions, so uncertainty remains exploratory. The separately tuned `xgb_nested_grid` candidate should not be confused with the fixed standalone model above.

## Project layout

```text
credit_card_fraud.ipynb               # Full modeling, EDA, CV, hyperparameter searches
ensemble_comparison.ipynb             # Reuses cached model outputs for ensemble comparison
paired_bootstrap_comparison.ipynb     # Reuses OOF vectors; no costly retraining
environment.yml / requirements.txt    # Python 3.11 / Conda / ipykernel
experiments/experiment001–011/        # Sequential research, methods and results
presentation/presentacion_corta/      # Spanish slide source, v11 (36 slides)
presentation/presentacion_completa/   # Spanish slide source, v10 (93 slides)
presentation/themes/fraud-whitegrid.css
presentation/archive/                # Historical source/rendered versions
notes/HANDOFF.md / AGENTS.md          # Reproduction and next-agent instructions
outputs/                              # Local generated products, intentionally ignored
```

**Export note:** the source decks are current; existing historical HTML/PDF files are archived. Run the manual build action or `presentation/build_slides.ps1` to produce fresh HTML/PDF from the present Marp source. The latest source decks may refer to figures present only in your local `outputs/` from the original runs.

## Windows PowerShell / Conda

```powershell
git clone https://github.com/heri-espino/Credit-Fraud.git
Set-Location .\Credit-Fraud
conda env create -f .\environment.yml
conda activate lds1071-fraud
python -m ipykernel install --user --name lds1071-fraud --display-name "Python (LDS1071 Fraud)"
python -m pip check
jupyter lab
```

Select `Python (LDS1071 Fraud)` as kernel. Place `playground-series-s6e11.zip` at the **repository root** (ignored), or the extracted CSV files in `data/`.

**Execution order:** the full training notebook once (or reuse your previously saved `outputs/`); the ensemble notebook only if its required cached models/predictions exist; finally the paired-bootstrap notebook. Check `outputs/all_candidate_predictions.npz` and `outputs/models/logit_C1_fold*.joblib` before restarting training. **Do not re-run** the full expensive modeling experiment just to regenerate slides.

## Self-hosted runner: PCAG103A-15

Your registered Windows x64 runner can run manually dispatched jobs on this repository. The workflow `Verify and build presentations` targets GitHub's automatic labels `self-hosted`, `Windows`, `X64` (the runner's display name is **not** necessarily a label). It does **not** start training, change the Conda environment or submit to Kaggle. It reports availability of Python, Conda and CUDA, checks notebook JSON, and builds Marp HTML/PDF **only if** all local figures can be resolved. Exported files are uploaded as GitHub Actions artifacts, not committed.

From repository **Actions → Verify and build presentations → Run workflow**. To use figures already stored on your workstation, supply their absolute directory path in the optional workflow input. This path is resolved **on the runner machine**, not in GitHub cloud storage. You can also use `presentation/build_slides.ps1 -FiguresDirectory "C:\path\to\outputs\figures"`.

## Publishing, reproducibility and safety

The repository is **public**. The supplied Kaggle competition rules require publicly shared competition code to also be shared on that competition's Kaggle Notebook/Discussion. Verify compliance before distributing new changes. Do **not** commit the raw Kaggle ZIP/CSV, individual transaction OOF/test prediction vectors, `*.joblib` fitted models, credentials, or large private intermediate outputs. Store aggregate results and methodological details in sequential `experiments/`; use Git LFS or documented artifact storage for unsuitable binaries.

The source notebook from the latest clean project package has outputs cleared; older executed notebooks remain available in `experiments/` to preserve provenance. The published presentation exports are **not** claimed to come from the official Marp CLI unless built by that CLI.

See `notes/HANDOFF.md` and `AGENTS.md` before extending the project.
