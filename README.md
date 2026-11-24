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


## experiment012 — Interactive manifold dashboard and clustering feature ablation

We added an experimental report at [`experiments/experiment012/README.md`](experiments/experiment012/README.md) covering **PCA, t-SNE, Isomap and FastICA** visualizations plus label-free K-means/DBSCAN features for XGBoost. This was deliberately kept separate from the three canonical modeling/ensemble/bootstrap notebooks.

In the genuine **100,000-row / five-fold / 350-tree pilot**, original XGBoost achieved **ROC AUC 0.942572** and average precision **0.471417**; XGBoost plus DBSCAN features scored **0.942856** and **0.470733** respectively. The +0.000284 ROC AUC difference has a 600-replicate paired-bootstrap interval **[−0.000632, +0.001067]**, so no robust improvement is established. K-means alone and combined with DBSCAN reduced ROC AUC; a separate 30k pilot did not reproduce the DBSCAN gain. **Do not incorporate the clustering features into the final model yet.**

The full experiment notebooks, Python scripts and privately generated dashboard/aggregate figures are available in the owner's experiment012 patch ZIP. Because this repository is public and Kaggle requires publicly shared competition code also to be shared on its competition-associated Kaggle forum/notebook, only the methodological summary is committed here pending that additional publication. The raw data and all row-level OOF files remain local.


## experiment013 — Full-dataset clustering ablation completed

The experiment012 hypothesis has now been evaluated on **all 699,960 labeled rows** with **five stratified folds and 20 identical-configuration XGBoost fits** (four feature sets × five folds). The fold-fit cluster geometry uses smaller training-only references (K-means/PCA: 15k; DBSCAN: 2.3k rows), whereas **every XGBoost uses its full outer training fold**.

| Full 699,960-row OOF feature set | ROC AUC | Average precision |
|---|---:|---:|
| Original features | 0.945702 | **0.500910** |
| + DBSCAN | **0.945705** | 0.500646 |
| + K-means | 0.945436 | 0.498565 |
| + both | 0.945459 | 0.498668 |

**Paired stratified bootstrap, B=1,000:** ΔAUC DBSCAN versus baseline **+0.00000266**, percentile CI 95% **[−0.000139, +0.000158]**; K-means **−0.000266**, CI **[−0.000485, −0.000047]**; both **−0.000243**, CI **[−0.000483, −0.000025]**. DBSCAN is essentially tied, and the original feature set is preferable on average precision, log loss and Brier score. **Do not alter the final modeling notebook to add clustering features.** The complete aggregate results, fold/cluster diagnostics, environment hashes and reproduction instructions are in [`experiments/experiment013/`](experiments/experiment013/).

The full run completed in 203.6 seconds on a separate available Linux CPU environment, **not** `PCAG103A-15`. A successful preflight reached the Windows runner but found neither the Kaggle ZIP in known checkout locations nor the required ML libraries in its default Python. The runner diagnostic is manually triggered at `.github/workflows/experiment012-preflight.yml`; future runner jobs require an explicit local data path and the named Conda environment.

The execution scripts, figures, notebooks and logs are preserved in the private downloadable `Credit-Fraud_experiment013_full_699960_results.zip`; record-level training labels/OOF predictions are preserved **only** in `Credit-Fraud_experiment013_private_oof.zip`. These must not be published as ordinary Git objects. The source remains private pending the Kaggle contest's public-code-sharing requirement.

## experiment014 — Cluster features for logistic regression (full-data experiment)

The experiment013 clustering feature ablation was repeated with **L2-regularized logistic regression**, the **full 699,960-row training data**, and **5 stratified CV folds**. All 20 fits converged. Original features: OOF ROC AUC **0.941356842** (AP **0.486234633**); + K-means **0.941511039**; + DBSCAN **0.941451258**; + both **0.941559127** (AP **0.487348829**). Although all augmentations gained slightly, **1,000 paired bootstrap resamples** yield 95% intervals for each AUC difference that **include zero** (combined: [−0.000009,+0.000422]). The fixed XGBoost baseline from experiment013 remains stronger at **0.945702363 ROC AUC**.

A secondary paired comparison finds that the *change* from added K-means features is more favorable under the logistic pipeline than under XGBoost (combined interaction Δ **+0.000445**, CI [0.000155,0.000768]), but this cross-pipeline result is exploratory because encoding/scaling differ and no independent selection assessment was run. **The final notebook remains unchanged.** See [experiment014](experiments/experiment014/README.md). Executable scripts, figures, tests and review notebook are preserved in the owner's private experiment014 ZIP; individual transaction OOF predictions are in a separate private archive. Competition code is not newly published to the public repo pending Kaggle's matching code-sharing requirement.

## experiment015 — Clusters inside the logistic-offset XGBoost (completed)

Unlike experiments013–014, this experiment **actually refitted the two-stage finalist** and tried K-means/DBSCAN features in its logistic baseline and boosted correction. All **699,960 labeled rows**, **5 stratified folds**, **20 logistic fits and 25 depth-3, 240-tree XGBoost corrections** were evaluated (238.4 seconds, Linux CPU). The matched original hybrid obtained **0.946102351 ROC AUC** (AP **0.507152395**). Adding **both cluster groups only to logistic regression**, while keeping XGBoost on its original features, gave **0.946160624** (AP **0.507244901**), Δ **+0.000058273**. Putting clusters into both stages did not improve performance.

With **1,000 paired, class-stratified OOF bootstrap replicates**, the 95% interval for the apparent best gain was **[−0.000127384,+0.000237351]**, which includes zero. None of the four cluster-augmented intervals excludes zero. The historical previous finalist achieved **0.946204755** in an earlier run and was not demonstrably improved by this CPU re-fit. **Decision: keep the original final model unchanged.** Full aggregate scores, an audit of logistic-stage improvements, fold metrics, manifest and reproducibility notes: [experiment015](experiments/experiment015/README.md). The executable code and the executed 12-cell review notebook are privately delivered in the project ZIP, with transaction-level OOF predictions in a separate private ZIP, pending required Kaggle competition code-sharing compliance.

## experiment016 — Cuaderno final integrado en español

Se consolidó el informe como **notebook_final_es.ipynb**, con 50 celdas y ocho etapas: datos, EDA completo, ingeniería/PCA y clusters, 19 configuraciones candidatas y tuning, cuatro ensambles, bootstrap emparejado, selección y probabilidades de Kaggle. Se producen **19 figuras con títulos, ejes y leyendas en español**.

Se verificó el notebook contra 699,960 filas y las predicciones OOF reales; generó 299,984 probabilidades válidas. Por defecto **reutiliza resultados sin reentrenar** los 19 modelos. Selección nominal: logística corregida con XGBoost (AUC .946205 frente a XGBoost individual .946120), sin superioridad estadística demostrada. Los experimentos 013–015 no cambiaron el finalista.

El ZIP privado Credit-Fraud_notebook_final_es.zip contiene el cuaderno, CSV agregados y figuras. Más detalles en [experiment016](experiments/experiment016/README.md). Este repositorio es público: el código ejecutable se mantiene en el ZIP hasta compartirlo también en el Notebook/Discussion de la competencia de Kaggle, según sus reglas. No publicar datos individuales, OOF/test ni modelos binarios.
