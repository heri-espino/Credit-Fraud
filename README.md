# LDS1071 Final Project — Predicting Credit Card Fraud

**Competition:** [Kaggle Playground Series S6E11](https://www.kaggle.com/competitions/playground-series-s6e11) (deadline: 2026-11-30 23:59 UTC).  
**Deliverable:** [credit_card_fraud.ipynb](credit_card_fraud.ipynb) (one Jupyter notebook); `is_fraud` ROC AUC; 5 stratified outer CV folds.  
**Recommended OS:** Windows 10/11, **PowerShell (`pwsh`)**, Miniconda or Anaconda, with an NVIDIA CUDA GPU if available for XGBoost and CatBoost. CPU-only execution is supported.

## 1. Windows PowerShell: create a Conda environment step by step

Open **PowerShell** or **PowerShell 7 (`pwsh`)** and run these commands **from the repository root**, after placing the privately distributed project files under `final_project/`.

### Step 1 — Install/initialize Conda (once per machine)

Install Miniconda or Anaconda if needed, then verify:

```powershell
conda --version
conda init powershell
```

**Close and reopen PowerShell** after `conda init powershell`. If `conda` is not on the PATH, open **Anaconda PowerShell Prompt** first; then initialize your ordinary PowerShell session. Some Windows installations restrict loading PowerShell profile scripts; inspect your execution policy rather than blindly changing system-wide policy.

### Step 2 — Go to the project root

If you already have the course repository, go to it:

```powershell
Set-Location "C:\path\to\LDS1071-Machine-Learning"
Get-ChildItem .\final_project
```

Otherwise, clone the course repository and copy the **private project ZIP** content into `final_project/`. The executable notebook is not yet in the *public* GitHub repository due to the competition code-sharing requirement.

```powershell
git clone https://github.com/heri-espino/LDS1071-Machine-Learning.git
Set-Location .\LDS1071-Machine-Learning
# Copy/extract the privately provided final_project/ files here before proceeding.
```

### Step 3 — Create the named Conda environment

**Recommended, from the root:**

```powershell
conda env create -f .\final_project\environment.yml
conda activate lds1071-fraud
python --version
python -m pip check
```

`environment.yml` installs Python 3.11, `ipykernel`, JupyterLab/Notebook, scikit-learn, XGBoost, CatBoost, Seaborn, and the other dependencies. This is the reproducible environment specification; `requirements.txt` is also provided for pip-only installations.

**Alternative manual method** (instead of the `conda env create` command above):

```powershell
conda create -n lds1071-fraud python=3.11 pip -y
conda activate lds1071-fraud
python -m pip install -r .\final_project\requirements.txt
```

Do **not** use both creation methods for an environment that already exists. To update an existing environment after editing `environment.yml`, use `conda env update -n lds1071-fraud -f .\final_project\environment.yml --prune`.

### Step 4 — Register the notebook kernel (`ipykernel`)

```powershell
python -m ipykernel install --user --name lds1071-fraud --display-name "Python (LDS1071 Fraud)"
jupyter kernelspec list
python -c "import sys, sklearn, xgboost, catboost, seaborn, ipykernel; print(sys.executable); print('sklearn', sklearn.__version__, 'xgboost', xgboost.__version__, 'catboost', catboost.__version__)"
```

In the notebook, choose **Kernel → Change Kernel → Python (LDS1071 Fraud)** (or select this kernel in VS Code's notebook kernel picker). The notebook's metadata already points to `lds1071-fraud`.

### Step 5 — Place the Kaggle input file

The official Kaggle ZIP is **not in Git**. Download/retain `playground-series-s6e11.zip` and place it alongside the notebook:

```text
LDS1071-Machine-Learning/
└── final_project/
    ├── credit_card_fraud.ipynb
    ├── environment.yml
    ├── requirements.txt
    ├── README.md
    ├── playground-series-s6e11.zip     # local only, do not commit
    ├── experiments/                     # reproducible experiment records
    └── outputs/                         # generated; ignored by Git
```

Alternatively extract `train.csv`, `test.csv`, and `sample_submission.csv` into `final_project/data/`.

### Step 6 — Start Jupyter from `final_project/` (important for relative paths)

```powershell
Set-Location .\final_project
jupyter lab credit_card_fraud.ipynb
# Or: jupyter notebook credit_card_fraud.ipynb
```

Select **Python (LDS1071 Fraud)**; first run the setup/data-loading cells, then choose **Restart & Run All**. The default full run is expensive (see below). A short smoke test is recommended first.

### Step 7 — Quick notebook execution test

Change the configuration cell (cell 2, near the top) to:

```python
FAST_DEV_RUN = True
MAX_CANDIDATES_PER_FAMILY = 1
SAVE_FOLD_MODELS = False
RUN_PDP = False
RUN_NESTED_GRID_SEARCH = True
```

Run all cells. Review `outputs/figure_catalog.csv` and `outputs/nested_gridsearch_*.csv`. The smoke-test metrics are **not** final Kaggle metrics. Before the final run, restore:

```python
FAST_DEV_RUN = False
MAX_CANDIDATES_PER_FAMILY = None
SAVE_FOLD_MODELS = True
RUN_PDP = True
RUN_NESTED_GRID_SEARCH = True
```

### Step 8 — Full experiment and submission

The full run uses 699,960 training observations and **19 configurations (95 outer-fold fits)**, including **5 × 3 × 8 = 120 inner search fits per tuned family** (240 inner fits across XGBoost + CatBoost) and 10 outer-fold full-train refits of the chosen grid configurations. Fixed-model outer fits add 85 more. Run time and RAM use depend on the machine. Start by reducing `GRID_SEARCH_TRAIN_ROWS` if necessary. Disable `RUN_NESTED_GRID_SEARCH` if you want the fixed candidate comparisons only.

Outputs include `outputs/candidate_metrics.csv`, `outputs/fold_metrics.csv`, `outputs/nested_gridsearch_cv_results.csv`, `outputs/nested_gridsearch_best_by_fold.csv`, **Seaborn figures** in `outputs/figures/`, and `outputs/submission.csv`. Inspect plots, scores, grid stability and calibration before manually submitting `submission.csv` to Kaggle.

## 2. CPU versus GPU behavior

| Family | Execution | Parallelism / notes |
|---|---|---|
| Logistic regression/PCA/splines | CPU | BLAS limited to avoid oversubscription. |
| Random forest | CPU | `n_jobs=-1` within each fold. |
| XGBoost (fixed, grid-tuned, logistic-offset) | **CUDA GPU preferred**, CPU fallback | `tree_method='hist'`, `device='cuda:0'` after successful GPU probe; otherwise `device='cpu'`. Inspect the **effective** fitted booster device. `n_jobs=-1` enables CPU threads when using CPU; search jobs are sequential. |
| CatBoost (fixed and grid-tuned) | **GPU preferred**, CPU fallback | `task_type='GPU', devices='0'` if a tiny CUDA training probe succeeds; otherwise `task_type='CPU'`. Uses original categorical columns instead of one-hot encoding. |
| `GridSearchCV` | Serial over candidates (`n_jobs=1`) | Prevents XGBoost and CatBoost candidate searches from competing for the same GPU/VRAM. Internal CPU threading remains enabled for CPU fits. |

On Windows, inspect your NVIDIA drivers/device first:

```powershell
nvidia-smi
```

The PyPI XGBoost wheel includes CUDA support on compatible Windows/Linux systems, subject to driver and hardware requirements; a standard CPU-only GPU probe is safe. The notebook uses `XGBOOST_DEVICE='auto'` and `CATBOOST_DEVICE='auto'`, probes CUDA using a **real tiny fit**, and falls back to CPU when unavailable. XGBoost may automatically warn and switch to CPU even when `device='cuda:0'`, so the probe inspects the *trained booster config*. If a later XGBoost GPU fit raises a CUDA-related error (e.g. out-of-memory), its search or fold fit is retried on CPU. For CatBoost GPU the wrapper likewise retries on CPU after a GPU-fit failure. Hardware-specific wall time varies, and CatBoost GPU may not be bitwise deterministic.

To override automatic detection in the notebook:

```python
XGBOOST_DEVICE = 'auto'  # 'auto', 'cuda', 'cpu'; 'cuda' still falls back if not available
XGBOOST_GPU_ID = '0'
CATBOOST_DEVICE = 'auto'  # 'auto', 'GPU', 'CPU'
CATBOOST_GPU_ID = '0'
GRID_SEARCH_N_JOBS = 1    # Keep this at 1 when using a single GPU
```

**Note:** GPU training is not always faster for the 20,000-row inner tuning sample because preprocessing, device transfers and kernel launches add overhead. Compare recorded fit times against a CPU run if optimizing runtime rather than merely enabling acceleration. Use a compatible NVIDIA driver; `nvidia-smi` helps confirm GPU visibility. The CPU fallback should be inspected via the notebook's device summary, rather than inferred from whether the `device` parameter says CUDA.

Relevant docs: [XGBoost GPU](https://xgboost.readthedocs.io/en/release_3.1.0/gpu/index.html), [CatBoost GPU](https://catboost.ai/docs/en/features/training-on-gpu), [CatBoost installation](https://catboost.ai/docs/en/concepts/python-installation), [XGBoost sklearn](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html), [IPython kernels](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

## 3. Notebook sections and experimental design

The same notebook provides EDA, class-conditional distributions, fraud/nonlinear interaction plots, potential outliers, PCA/SVD diagnostics, assumptions for logistic regression, five-fold OOF benchmarking, loss-based boosting over logistic logits, metrics and ROC/PR/threshold plots, group-level evaluation, calibration, importance, partial dependence, model blending, and a Kaggle submission.

**Experiment005** adds (a) fixed CatBoost native categorical models, (b) a **CUDA-preferred** XGBoost `GridSearchCV` pipeline with CPU fallback, (c) a GPU-preferred native categorical CatBoost `GridSearchCV` pipeline, (d) fold-separated inner grid metadata and charts comparing grid candidates with untuned models. All inner searches are trained **exclusively within their respective outer training folds** and tuned pipelines are refitted on their full outer training partitions. Even so, selecting the best *overall family/ensemble* by the same CV scores introduces selection optimism; an untouched test split or fully nested outer selection would be needed for unbiased winner assessment.

### Provenance and version history

- `experiment001`: five-fold baseline and initial model comparison.
- `experiment002`: nonlinear fraud patterns, EDA, anomaly analysis, spline logistic.
- `experiment003`: logit-offset boosted correction and logistic assumptions.
- `experiment004`: expanded EDA, model plots, lift, calibration, feature importance.
- `experiment005`: Conda + PowerShell setup, CatBoost GPU/CPU fallback, nested `GridSearchCV`, and model selection diagnostics.

**Source of truth:** the shipped `credit_card_fraud.ipynb` + `requirements.txt`/`environment.yml`. Experiment records are stored in numbered `experiments/` directories. Generated training outputs and the original competition CSV/ZIP are excluded from sharing.

## 4. Publication and data safeguards

This GitHub repo is **public**. Kaggle rules require publicly shared competition code to **also** be shared through the competition-associated Kaggle Notebook/Discussion. Therefore the executable notebook is intentionally delivered in the private project ZIP instead of being pushed publicly to GitHub until that publication condition is satisfied. Do not commit Kaggle input CSVs, record-level OOF/test predictions, model binaries, credentials, or local `outputs/`. The documentation scaffold in GitHub can be maintained independently of the notebook source.

## 5. Troubleshooting

- **`conda` not recognized:** use Anaconda PowerShell Prompt; run `conda init powershell`, then reopen the shell.
- **Jupyter says `ModuleNotFoundError: catboost`:** notebook uses the wrong kernel. Switch to **Python (LDS1071 Fraud)**, confirm `sys.executable`, or rerun the install command in the activated environment.
- **GPU unavailable for XGBoost or CatBoost:** inspect `nvidia-smi` and the notebook's actual-device probe; leave `XGBOOST_DEVICE='auto'` and `CATBOOST_DEVICE='auto'` to fall back, or force CPU. CUDA wheels need compatible NVIDIA drivers; macOS typically uses CPU.
- **GPU memory exhausted:** avoid running grid jobs concurrently; keep `GRID_SEARCH_N_JOBS=1`. The XGBoost CUDA-issue handler retries affected search/outer-fold fits on CPU and reports their effective devices. You can also reduce `GRID_SEARCH_TRAIN_ROWS`.
- **Memory pressure or long training:** reduce `GRID_SEARCH_TRAIN_ROWS`, disable `RUN_PDP`, use `SAVE_FOLD_MODELS=False`, or set `RUN_NESTED_GRID_SEARCH=False` for a fixed-model run. Keep `GRID_SEARCH_N_JOBS=1` when using a single GPU.
- **Notebook cannot find CSVs:** launch Jupyter from `final_project/` and place `playground-series-s6e11.zip` beside `credit_card_fraud.ipynb`.
- **Need a new environment after changes:** use `conda env update` as described above, then restart the kernel.
#   C r e d i t - F r a u d  
 