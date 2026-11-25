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

El cuaderno y los CSV agregados necesarios están versionados en GitHub, mientras que las figuras se regeneran en `outputs/informe_final_es/figuras/` al ejecutar el notebook. El ZIP Credit-Fraud_notebook_final_es.zip sigue disponible como copia independiente. Más detalles en [experiment016](experiments/experiment016/README.md). **Requisito pendiente:** este repositorio es público y Kaggle exige compartir también este código en un Notebook o Discussion asociado a la competencia. El código se publica aquí a petición del propietario; aún debe publicarse su equivalente en Kaggle. No publicar datos individuales, OOF/test ni modelos binarios.

## Descarga directa del notebook final (experiment016)

Tras `git pull`, abra [`notebook_final_es.ipynb`](notebook_final_es.ipynb). Los archivos de métricas, el diccionario y los resultados agregados necesarios están en [`experiments/experiment016/resultados/`](experiments/experiment016/resultados/). `INSTRUCCIONES_ES.md` detalla el entorno y la ubicación de la caché OOF. El directorio `outputs/` se mantiene intencionalmente fuera de Git: conserve su copia local para generar las curvas y la entrega Kaggle sin reentrenamiento.

## experiment017 — XGBoost con cinco grupos y umbrales de alerta

La [notebook final](notebook_final_es.ipynb) contiene ahora **54 celdas**: gráficos en Seaborn `dark`, ROC AUC con escala ampliada, y comparación de ensambles exclusivamente con ROC AUC. La búsqueda de XGBoost usa **36 configuraciones**, incluida profundidad máxima 30, que no fue elegida en ninguno de los cinco pliegues.

Con 699,960 observaciones y cinco pliegues: XGBoost original AUC OOF 0.945702; XGBoost fijo más cinco grupos K-means 0.945747, diferencia +0.000044 e intervalo bootstrap 95% [−0.000107,+0.000194], que incluye cero. El XGBoost seleccionado por la búsqueda de 36 configuraciones alcanzó 0.944887. Los [resultados agregados](experiments/experiment017/results) y el [informe](experiments/experiment017/README.md) están versionados.

El apartado de umbral binario presenta matriz de confusión, falsos negativos, falsas alarmas, F1, precisión, recall, accuracy, curva ROC y AUC. Una política ilustrativa del 98% de recall provoca más de 300,000 falsas alarmas; no es una recomendación de operación bancaria. Las predicciones enviadas a Kaggle siempre son probabilidades, sin umbral.

Para ejecutarlo, `git pull --ff-only origin main`, `conda activate lds1071-fraud`, `jupyter lab notebook_final_es.ipynb`. El ZIP entregado en conversación contiene scripts completos y figuras; OOF/test fila a fila permanece en archivos privados y fuera de Git. Continúa pendiente la publicación equivalente del código en el Notebook/Discussion de Kaggle exigida por el concurso.


## experiment018 — Búsqueda completa de la corrección logística con XGBoost

El cuaderno final en español ahora integra PCA/t-SNE y K-means/DBSCAN **antes** de comparar modelos, gráficos Seaborn `whitegrid` con paleta `dark`, métricas F1 y falsas alarmas, ROC AUC frente a tiempo medido de booster y búsqueda de XGBoost posterior al logit. Se completó una nueva búsqueda sobre **699 960 filas, 5 folds externos, 4 representaciones y 36 parámetros del booster**; tres folds internos por representación sobre un subconjunto de 36 000 transacciones de cada entrenamiento externo. La variante K-means en la logística obtuvo ROC AUC OOF **0.945870** versus **0.945842** con variables originales; Δ +0.000028, IC bootstrap emparejado 95 % **[−0.000150,+0.000213]**. Todos los folds seleccionaron `max_depth=3`, `learning_rate=0.04`; no se demostró mejora y se conserva la elección histórica con AUC 0.946205. Resultados numéricos por fold y bootstrap en [`experiments/experiment018/resultados/`](experiments/experiment018/resultados/); scripts reproducibles y figuras en ZIP privado, sin datos OOF por transacción en Git. El código público debe compartirse también en la competencia Kaggle para cumplir sus reglas.


**Ajuste adicional del experimento018:** al seleccionar la representación *dentro* de cada entrenamiento externo mediante AUC interna, se escogieron variables originales en cuatro folds y K-means en uno. El selector anidado obtuvo AUC OOF **0.945856** frente a 0.945842 de la base sin clusters; Δ+0.000014, IC emparejado 95 % **[−0.000054,+0.000078]**. Las tres tablas agregadas y la figura están documentadas en experiment018; no se ha demostrado una ganancia por la construcción de clusters.


## experiment019 — Cuaderno con secuencia metodológica integrada

`notebook_final_es.ipynb` fue reorganizado como un informe continuo de **66 celdas (33 de código)**: EDA → PCA/t-SNE y K-means/DBSCAN → comparación de algoritmos y grillas → elección justificada de la primera etapa logística → corrección con XGBoost y validación anidada → cuatro ensambles → incertidumbre → evaluación del finalista (ROC, PR, calibración, F1 y matriz de confusión).

La logística con K-means+DBSCAN obtuvo la mayor AUC aislada, **0.941559**, pero su diferencia con la logística original **0.941357** tiene un IC95 que incluye cero; por parsimonia la original queda como base de referencia. En la búsqueda conjunta anidada del experimento018, la representación original se eligió en cuatro folds y K-means en uno. El finalista histórico sigue siendo la logística corregida mediante XGBoost (AUC OOF **0.946205**, ventaja frente al XGBoost individual no demostrada estadísticamente). **No se reentrenaron modelos nuevos** en esta revisión.

El orden de carga de cachés OOF y envío fue corregido; el notebook fue verificado contra el dataset completo y las predicciones guardadas en una ejecución local equivalente (33 celdas, 31 figuras). Véase [experimento019](experiments/experiment019/README.md). Se recupera con `git pull --ff-only origin main`. La publicación equivalente de código de competición en Kaggle continúa pendiente.


## experiment020 — Revisión de entrega y protocolo común (2026-11-24)

Notebook español de 69 celdas (34 ejecutables), narrativa EDA → representación → familias y grillas → selección logística y corrector XGBoost → selección y evaluación. Se archivó experiment019. Nuevo protocolo: cinco folds externos y tres internos compartidos, hasta 36k filas internas, cuatro representaciones por familia (más PCA/splines para logística), misma grilla de 36 opciones para XGBoost individual y corrector. Selección logística por su propia AUC interna antes de ajustar el corrector. 4 440 ajustes internos de candidatos más 25 externos y auxiliares. **No se ha ejecutado ni validado end-to-end en esta sesión**; no hay resultados nuevos. Por defecto se mantienen métricas históricas con procedencia explícita. Para ejecutar/cargar usar las banderas EJECUTAR_PROTOCOLO_COMUN/CARGAR_PROTOCOLO_COMUN; los resultados privados y nuevos informes se guardan aparte. Ver `experiments/experiment020/README.md`. Próximo experimento: experiment021. No publicar datos o vectores individuales; publicación de código correspondiente en Kaggle sigue pendiente.


## experiment021 — Ensambles y grilla XGBoost común

Sección 3: cuatro familias individuales con selección anidada de representación e hiperparámetros; XGBoost 36 configuraciones por representación. Sección 4: promedio de cuatro familias, bagging bootstrap del XGBoost seleccionado (5 réplicas), stacking XGBoost sobre cuatro probabilidades OOF con cross-fitting dentro de meta-train y corrección de logits de la logística seleccionada. Stacking y offset comparten la grilla de 36 con XGBoost individual, misma semilla y parámetros fijos. La selección previa de bases condiciona el AUC interno del meta-modelo; el outer fold permanece retenido. Ocho candidatos, 4 980 ajustes internos de candidatos más refits/auxiliares. Notebook de 64 celdas/36 código; archivo previo archivado. Checkpoint privado de sección 3 con verificación de IDs y folds; flags EJECUTAR_PROTOCOLO_COMUN, CARGAR_PROTOCOLO_COMUN, REUTILIZAR_INDIVIDUALES. Outputs nuevos en outputs/experiment021 y outputs/informe_ensambles_es. Smoke test sintético en experiments/experiment021/smoke_test.py. **Implementación no ejecutada en esta sesión; no hay nuevas métricas verificadas.** Ejecutar smoke y corrida completa antes de entrega. Ver experiments/experiment021/README.md. Próximo experimento022. No subir predicciones fila a fila ni datos; publicación equivalente en Kaggle pendiente.


## experiment022 — K-means explícito, ranking top 10 y corrección de configuración

Auditoría de la corrida del propietario (commit `7b682cc0c53a331c9f2b18c70a7508b2f31e5b3d`, "ran"): una celda adicional puso EJECUTAR_PROTOCOLO_COMUN=True, pero la siguiente la redefinió False. Se ejecutó modo histórico (37 celdas de código en la revisión del propietario, 5 vectores históricos verificados, envío histórico de 299 984 filas). AUC histórica 0.946205 offset, 0.946120 XGB individual. En exp018, mejor híbrido ajustado K-means en logística 0.945870 vs 0.945842 original; en exp014, mejor logística aislada fue K-means+DBSCAN 0.941559 vs K-means 0.941511. No confundir esas tablas ni atribuirlas a experiment021.

Se eliminó la celda duplicada. El notebook tiene una sola configuración, por defecto EJECUTAR_PROTOCOLO_COMUN=True y EJECUTAR_EXTENSION_TOP10=True. Extension: reajustar los mejores parámetros internos de las 18 combinaciones familia/representación, más offset fijo K-means (36 configuraciones del booster, base logística K-means elegida por AUC interna dentro de cada fold). 27 candidatos en total incluidos los ocho de exp021; se excluyen duplicados exactos OOF/test antes de seleccionar top10. 540 ajustes internos nuevos de booster, 90 refits individuales y 5 refits de híbrido (más logística auxiliar); no repetir búsquedas ya guardadas. Cargar experiment021 completo con CARGAR_PROTOCOLO_COMUN=True y ejecutar extensión; para reproducir todo sin entrenar, EJECUTAR_EXTENSION_TOP10=False. Salidas separadas outputs/experiment022 e informe_top10_es. En modo histórico, top10 descriptivo con procedencia; curvas solo de vectores disponibles. No forzar K-means como ganador. No publicar NPZ. Implementación nueva no ejecutada aquí; smoke test sintético disponible. Próximo experimento023.


## experiment023 — Diseño factorial de representación

Objetivo: separar el efecto del escalado y el de las características K-means + DBSCAN en todas las familias. Cuatro representaciones: raw, standardized, raw_kmeans_dbscan y standardized_kmeans_dbscan. Raw significa numéricas imputadas no escaladas, con booleanas 0/1 y one-hot para categorías; no significa alimentar strings al clasificador. Geometría común estandarizada, PCA 90 %, K-means k=5, DBSCAN min_samples=5, cuantil .90 para epsilon. Ocho características derivadas, distancias escaladas solo en la rama standardized; ruido binario. PCA y splines dejan de ser candidatos separados para respetar el diseño de cuatro alternativas.

5 folds externos y 3 internos comunes, muestra interna estratificada de hasta 36k. Grillas por representación: LR 8, RF 9, XGB 36, CatBoost 8 (244 configuraciones por fold, 3 660 ajustes internos). Cuatro familias × cuatro representaciones fijas más cuatro selectores adaptativos = 20 individuales. Cuatro ensambles × cinco escenarios (incluido adaptive) = 20 ensambles. Stacking y offset usan la misma grilla XGB de 36 (5 400 ajustes internos de booster adicionales; más refits, bases auxiliares y cinco réplicas bootstrap). En offset, LR se selecciona por su AUC interna y el corrector emplea su misma representación. En stacking, la elección previa de las bases condiciona la evaluación interna; el fold externo permanece retenido. La selección adaptativa no utiliza AUC externa. El ranking final elimina duplicados exactos OOF/test y selecciona hasta diez; no hay garantía de que el híbrido gane.


Reproducción, checkpoints, limitaciones y estado en `experiments/experiment023/README.md`. El notebook final usa experiment023; código y smoke preparados, no ejecutados en la sesión de edición. No publicar datos ni vectores privados. Próximo experiment024.
