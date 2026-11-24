# AGENTS.md — Credit Fraud

## Repository-first protocol
1. Read `README.md`, `notes/HANDOFF.md`, and the relevant `experiments/experimentNNN/README.md` before changes.
2. Inspect `main`, open PRs and the commit history; do not overwrite other agents' work or merge a PR without explicit authorization.
3. The repository root **is** the project root. Paths copied from the course repo must drop the prefix `final_project/`.
4. Preserve every existing notebook, figure, simulation summary and presentation; archive prior versions before replacing them. Label smoke results distinctly from full-run OOF metrics.
5. Use sequential experiment IDs; the next unallocated ID after this migration is `experiment012`. Every experiment must document what, why, reproduction, results, limitations, next steps.
6. Commit/push completed reproducible work. Do not force-push, commit credentials, raw Kaggle data, OOF/test row-level predictions, or fitted model binaries.

## Statistical contracts
- Binary target is `is_fraud`; `id` is not a predictor. Kaggle requires a probability, primary selection metric ROC AUC.
- Five stratified outer folds; fold-fit imputation, encoding, scaling, spline expansion and PCA to avoid leakage.
- XGBoost/CatBoost may use CUDA when genuinely available, otherwise CPU. Keep nested `GridSearchCV(n_jobs=1)` on one GPU, allowing estimator-level CPU parallelism where safe.
- Blending of probabilities is **not** classical bootstrap bagging. Logistic-offset XGBoost uses LR log-odds as `base_margin`; explicit residual XGBoost regresses `y - p_LR` separately. RF stacking consumes base-model OOF probability columns.
- The random-forest stacking meta-CV on cached OOF features is not fully nested; do not claim an unbiased model comparison or an independently tested Kaggle score.
- Paired stratified bootstrap resamples **identical row indices** for all models; its 600-replicate interval of the logit-offset minus fixed-XGBoost AUC difference includes zero. It does **not** resolve post-selection bias or possible customer/time dependence.
- Fixed-depth XGBoost (`xgb_depth5_lr05`) and `xgb_nested_grid` are distinct. Do not invent an AUC for the latter unless its OOF predictions are available.

## Repository artifacts and runner
- Core notebooks at root: `credit_card_fraud.ipynb`, `ensemble_comparison.ipynb`, `paired_bootstrap_comparison.ipynb`.
- Complete Spanish deck is v10; short Spanish deck is v11. Keep the `fraud-whitegrid` theme and small math consistent with text.
- `.github/workflows/verify-build.yml` is manually dispatched and runs on a self-hosted Windows x64 GitHub Actions runner. It validates/builds, **not trains**. Runner `PCAG103A-15` is a machine name, not automatically a GitHub Actions custom label.
- The local `outputs/` directory is intentionally Git-ignored; model artifacts on the runner's disk are not automatically accessible inside a fresh `GITHUB_WORKSPACE`.
- Publication of competition code from this public repository must satisfy Kaggle's associated competition-public-sharing requirements.


## experiment012 — Exploratory manifold and clustering ablations

A private experiment patch contains `experiments/experiment012/` with the dashboard (PCA, t-SNE, Isomap, FastICA), K-means silhouette/inertia and DBSCAN cluster-sensitivity diagnostics, and a *fold-fit* XGBoost ablation. Two pilots (30k/3fold/180trees; 100k/5fold/350trees) have been **executed**, with bootstrap B=600 on the larger OOF data. Treat results as exploratory: the +0.000284 DBSCAN AUC gain has CI [−0.000632,+0.001067] and slightly worse AP. No changes were made to the final training notebook. Geometric transformations, K selection, DBSCAN radius selection and cluster fitting must remain strictly inside each supervised outer training fold. Do not treat t-SNE/Isomap coordinates as inductively available predictors or use oversampled visualization prevalence for risk estimation. Source/data publication rule remains in force; consult `experiments/experiment012/README.md`. Next experiment index: `experiment013`.


## experiment013 — Full-data clustering test and decision

Completed all 699,960 rows, five stratified folds and four fixed-configuration XGBoost feature sets (20 fits). Derived K-means/DBSCAN features are produced from training-fold-only unsupervised reference samples (15k geometry, 2.3k DBSCAN), never from validation fold labels. Full OOF AUC baseline .94570236; DBSCAN .94570502; K-means .94543602; combined .94545948. Paired bootstrap B=1000 yields DBSCAN Δ+.00000266 CI [−.000139,+.000158], thus **no evidence of improvement**. Keep the existing final classifier unchanged. See `experiments/experiment013/README.md`. Store row-level OOF data only in private local/external archival storage; public Git contains aggregates and documentation. Next experiment number: **experiment014**.

## experiment014 — Logistic regression cluster-feature ablation

Completed 699,960 rows, five stratified folds, 20 L2-logistic fits with baseline/K-means/DBSCAN/combined feature groups. All preprocessors/clusters are fold-fit; k-means uses 15k and DBSCAN 2.3k training-only references per fold. Full OOF AUC values: baseline .941356842, K-means .941511039, DBSCAN .941451258, combined .941559127. Paired 1000-replicate nominal 95% intervals for all AUC gains include zero. XGB exp013 baseline .945702363 still wins. Secondary difference-of-gains intervals are explorative/post-selection and pipelines use different encoding/scaling. See `experiments/experiment014/README.md`. Private ZIP contains scripts and 15-cell review notebook; separate private ZIP contains row-level OOF. Do not change original finalists or publish data. Next experiment number: `experiment015`.

## experiment015 — Logistic-offset clustering features (completed)

Five OOF variants tested on 699,960 rows, five folds with same 42 seed. Two-stage model uses LR logits as XGB `base_margin` at fit *and inference*. Variant `combined_lr_only` adds cluster features **only** in LR and reuses the original XGBoost feature matrix. The other three add features to both stages. Best observed +.000058273 AUC had paired bootstrap 95% CI [−.000127384,+.000237351], no reliable gain. Original finalist unchanged. Full aggregate/fold methodology in `experiments/experiment015/README.md`, executable scripts and executed review notebook available privately; OOF files excluded from public Git. The full run used Linux CPU, not self-hosted Windows runner. Next sequential experiment ID `experiment016`.

## experiment016 — Notebook final en español

La versión final versionada en la raíz (`notebook_final_es.ipynb`) tiene 50 celdas (25 de código), se validó contra el dataset original y la caché OOF, y generó 19 figuras españolas. Los CSV agregados requeridos están versionados en `experiments/experiment016/resultados/`; véase `experiments/experiment016/README.md`. El modo por defecto no reentrena candidatos. El GridSearchCV opcional corresponde a una ejecución *nueva*, no a los resultados históricos.

Bootstrap original del experimento010: B=600, ΔAUC offset vs XGB +.0000846 con intervalo 95% que incluye cero. No se modifica el finalista. El notebook se publicó en GitHub a petición del propietario; queda **pendiente** la publicación correspondiente en Kaggle conforme a sus reglas. No subir OOF/test fila por fila. Próximo experimento: experiment017.

## experiment017 — cinco clusters, búsqueda de profundidad 30 y política de alerta

La notebook principal tiene 54 celdas y Seaborn dark. XGBoost se evaluó con 36 configuraciones de búsqueda incluyendo profundidad 30; las seis combinaciones adicionales no ganaron en ningún pliegue. K-means con k=5 añadió seis características y obtuvo diferencia de ROC AUC +0.000044 (IC 95% bootstrap [-0.000107,+0.000194]), no un resultado concluyente.

La política ilustrativa de recall 98% minimiza alertas falsas dadas las restricciones; sin esa restricción minimizar FN es trivial. No modificar el finalista ni umbralizar la predicción que solicita Kaggle. El registro está en `experiments/experiment017/README.md`, y scripts y figuras reproducibles en el ZIP de la conversación; los OOF/test individuales permanecen privados. Cumplir publicación correspondiente en Kaggle para el código difundido en este repositorio público. Próximo número experiment018.


## experiment018 — Final Spanish notebook, data representations and tuned offset

The final Spanish notebook integrates K-means/DBSCAN, PCA and t-SNE into early representation selection; uses exactly Seaborn `whitegrid`+`dark`; includes 36 XGBoost booster hyperparameter combinations tuned after logistic regression via correct `base_margin` during fit/predict, with a runnable optional script in the owner's experiment018 ZIP. Completed 699,960-row five-fold OOF search with inner 3fold on 36k training-only observations, 4 representations; 2,160 inner XGBoost fits, 20 outer fits. AUC: baseline .94584215, Kmeans .94587012, DBSCAN .94586038, combined .94585803. Paired bootstrap B=1000 Kmeans Δ+.00002797 CI [−.00014967,+.00021260]; no demonstrated improvement. Historic winner .94620475 remains nominal. Tuning source code and private OOF arrays are not Git-hosted; see `experiments/experiment018/README.md`. Next experiment019. No unverified statistical superiority or Kaggle score claims; ensure required Kaggle code cross-publication.


**experiment018 nested-representation selector:** after inner-CV model tuning, choose the LR representation separately by maximum inner AUC within each outer training fold. Fold choices baseline,kmeans,baseline,baseline,baseline; joint OOF AUC .9458559178 vs baseline .9458421547, paired bootstrap 1000 delta +.0000137631 CI [−.0000542282,+.0000775875]. Distinguish this proper foldwise selection from choosing the overall best variant post hoc. New public aggregate CSVs in experiment018/resultados; confidential OOF only in a separate private archive.


## experiment019 — Narrativa final integrada, sin nuevo entrenamiento

El notebook final versionado tiene **66 celdas/33 ejecutables**. Mantener el orden: 1 EDA, 2 representación y K-means/DBSCAN, 3 familias y grillas, 4 selección base logística y búsqueda de corrector XGBoost, 5 ensambles y tiempo, 6 modelo final e incertidumbre y métricas. El máximo aparente del experimento014 para logística combinada no es una ganancia establecida; referencia parsimoniosa original. En experiment018 la selección de representación se efectuó dentro de cada fold externo (originales 4/5). No crear fuga moviendo transformaciones fuera de los folds. Ejecutar OOF loader antes de generación de envío. Mantener `EJECUTAR_BUSQUEDA_HIBRIDA=False` por defecto. Reutilizar agregados existentes; no publicar OOF/test, datos Kaggle o binarios. Ver `experiments/experiment019/README.md`. Próximo experimento: experiment020.


## experiment020 — Revisión de entrega y protocolo común (2026-11-24)

Notebook español de 69 celdas (34 ejecutables), narrativa EDA → representación → familias y grillas → selección logística y corrector XGBoost → selección y evaluación. Se archivó experiment019. Nuevo protocolo: cinco folds externos y tres internos compartidos, hasta 36k filas internas, cuatro representaciones por familia (más PCA/splines para logística), misma grilla de 36 opciones para XGBoost individual y corrector. Selección logística por su propia AUC interna antes de ajustar el corrector. 4 440 ajustes internos de candidatos más 25 externos y auxiliares. **No se ha ejecutado ni validado end-to-end en esta sesión**; no hay resultados nuevos. Por defecto se mantienen métricas históricas con procedencia explícita. Para ejecutar/cargar usar las banderas EJECUTAR_PROTOCOLO_COMUN/CARGAR_PROTOCOLO_COMUN; los resultados privados y nuevos informes se guardan aparte. Ver `experiments/experiment020/README.md`. Próximo experimento: experiment021. No publicar datos o vectores individuales; publicación de código correspondiente en Kaggle sigue pendiente.


## experiment021 — Ensambles y grilla XGBoost común

Sección 3: cuatro familias individuales con selección anidada de representación e hiperparámetros; XGBoost 36 configuraciones por representación. Sección 4: promedio de cuatro familias, bagging bootstrap del XGBoost seleccionado (5 réplicas), stacking XGBoost sobre cuatro probabilidades OOF con cross-fitting dentro de meta-train y corrección de logits de la logística seleccionada. Stacking y offset comparten la grilla de 36 con XGBoost individual, misma semilla y parámetros fijos. La selección previa de bases condiciona el AUC interno del meta-modelo; el outer fold permanece retenido. Ocho candidatos, 4 980 ajustes internos de candidatos más refits/auxiliares. Notebook de 64 celdas/36 código; archivo previo archivado. Checkpoint privado de sección 3 con verificación de IDs y folds; flags EJECUTAR_PROTOCOLO_COMUN, CARGAR_PROTOCOLO_COMUN, REUTILIZAR_INDIVIDUALES. Outputs nuevos en outputs/experiment021 y outputs/informe_ensambles_es. Smoke test sintético en experiments/experiment021/smoke_test.py. **Implementación no ejecutada en esta sesión; no hay nuevas métricas verificadas.** Ejecutar smoke y corrida completa antes de entrega. Ver experiments/experiment021/README.md. Próximo experimento022. No subir predicciones fila a fila ni datos; publicación equivalente en Kaggle pendiente.


## experiment022 — K-means explícito, ranking top 10 y corrección de configuración

Auditoría de la corrida del propietario (commit `7b682cc0c53a331c9f2b18c70a7508b2f31e5b3d`, "ran"): una celda adicional puso EJECUTAR_PROTOCOLO_COMUN=True, pero la siguiente la redefinió False. Se ejecutó modo histórico (37 celdas de código en la revisión del propietario, 5 vectores históricos verificados, envío histórico de 299 984 filas). AUC histórica 0.946205 offset, 0.946120 XGB individual. En exp018, mejor híbrido ajustado K-means en logística 0.945870 vs 0.945842 original; en exp014, mejor logística aislada fue K-means+DBSCAN 0.941559 vs K-means 0.941511. No confundir esas tablas ni atribuirlas a experiment021.

Se eliminó la celda duplicada. El notebook tiene una sola configuración, por defecto EJECUTAR_PROTOCOLO_COMUN=True y EJECUTAR_EXTENSION_TOP10=True. Extension: reajustar los mejores parámetros internos de las 18 combinaciones familia/representación, más offset fijo K-means (36 configuraciones del booster, base logística K-means elegida por AUC interna dentro de cada fold). 27 candidatos en total incluidos los ocho de exp021; se excluyen duplicados exactos OOF/test antes de seleccionar top10. 540 ajustes internos nuevos de booster, 90 refits individuales y 5 refits de híbrido (más logística auxiliar); no repetir búsquedas ya guardadas. Cargar experiment021 completo con CARGAR_PROTOCOLO_COMUN=True y ejecutar extensión; para reproducir todo sin entrenar, EJECUTAR_EXTENSION_TOP10=False. Salidas separadas outputs/experiment022 e informe_top10_es. En modo histórico, top10 descriptivo con procedencia; curvas solo de vectores disponibles. No forzar K-means como ganador. No publicar NPZ. Implementación nueva no ejecutada aquí; smoke test sintético disponible. Próximo experimento023.
