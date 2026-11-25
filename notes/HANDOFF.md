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

### experiment016 — Sincronización solicitada para `git pull` (2026-11-24)

Se añadieron a la raíz `notebook_final_es.ipynb` y `INSTRUCCIONES_ES.md`, junto con el directorio `experiments/experiment016/resultados/` (diccionario, métricas históricas, resumen bootstrap y tabla de cinco estrategias). Todos son textos fuente/estadísticas agregadas; se excluyen datos Kaggle, NPZ con predicciones fila a fila, modelos serializados y figuras regenerables de `outputs/`. El usuario puede hacer `git pull` para recuperar la notebook y ejecutarla en su entorno; para generar un submission se sigue necesitando la caché OOF/test guardada localmente. Dado que el repo es público, queda pendiente compartir este mismo código en el Kaggle Notebook/Discussion de S6E11 conforme a las reglas de publicación.

## experiment017 — Modelo con cinco clusters, profundidad 30 y análisis binario (2026-11-24)

Sobre 699,960 transacciones, cinco folds semilla42: XGBoost fijo + cinco clusters K-means AUC .945746719 (AP .501017810) frente a baseline experiment013 AUC .945702363 (AP .500909959). Bootstrap pareado estratificado B1000 ΔAUC +.000044357, IC95 [-.000107,+.000194]. Grilla previa de 30 parámetros y seis nuevos de profundidad30 (total36), tres folds internos y entrenamiento completo por fold externo: ganador profundidad3, lr.04, min_child_weight5 en todos los folds, AUC .944886982. Geometría PCA/K-means entrenada en cada fold externo, con 15k puntos de referencia.

Notebook final 54 celdas, Seaborn dark, zoom ROC AUC y gráfico de ensambles sólo ROC AUC. Umbral de alerta con criterio ilustrativo de 98% recall: mejor XGBoost individual histórico tuvo FN231, FP305362, F1=.069758, exactitud=.563414, AUC=.946120 con selección cruzada del umbral; el offset logístico retuvo la mayor AUC global .946205. No existe umbral de producción justificado sin costos operativos; Kaggle requiere probabilidades.

Notebook local validada end-to-end; el código final sincronizado a GitHub para git pull. Ejecución en Linux CPU, no runner Windows. Resultados agregados públicos en experiments/experiment017 y scripts/figuras en ZIP, predicciones individuales en ZIP privado. Siguiente experimento018.


## experiment018 — Full nested offset search and final Spanish narrative (2026-11-24)

Completed full 699,960 labeled row, 5 outer folds, 4 LR feature sets (baseline/Kmeans/DBSCAN/combined), XGBoost margin correction grid 36 combinations ([3,5,7,10,15,30] depth × [.04,.08] LR × [5,10,15] min_child_weight), 3 inner folds on a training-only stratified 36k sample per outer fold. Geometry refitted within inner training and outer training; LR logits used as base_margin both fit/predict. 2160 inner boosted fits + 20 outer fits, about 995.8sec on Linux CPU, not Windows runner. All outer-selected depths=3 and learning rates=.04. OOF AUC: baseline .9458421547, Kmeans .9458701219, DBSCAN .9458603846, combined .9458580274. Paired stratified bootstrap 1000, Kmeans Δ+.0000279672 CI [−.0001496728,+.0002126033], DBSCAN Δ+.00001823 CI [−.00012734,+.00015995], both Δ+.00001587 CI [−.00016519,+.00019915]. No significant improvement. Previous nominal best .946204755 from historical experiment remains choice; not independently verified head-to-head against new search. Final notebook 62 cells, includes new bootstrap plot, tSNE replacing FastICA, all Spanish charts, F1/threshold and ROC AUC vs booster time, plus script launch flag default False. Aggregate CSV/manifests committed in experiment018; complete source/figures in private ZIP, OOF vector in separate private ZIP. Kaggle public code cross-publication still pending. Next experiment019.


**experiment018 foldwise data-hyperparameter selection:** the joint selector based *only* on inner AUC per outer fold picked original features in outer folds 1,3,4,5, K-means in fold 2. Reconstructed OOF AUC .9458559178, AP .5058042807; baseline .9458421547. Paired bootstrap B=1000 gives Δ+.0000137631 CI [−.0000542282,+.0000775875], includes zero. New code `joint_selection.py` and `bootstrap_joint.py` are in the private ZIP, with aggregate output committed publicly. This selection is more rigorous than picking max pooled OOF of four variants, but still not independent of prior exploration.


## experiment019 — Reconstrucción de narrativa (2026-11-24)

Reorganizado `notebook_final_es.ipynb` y registrado en `experiments/experiment019/README.md`: 66 celdas, 33 ejecutables, narrativa EDA → clusters y representación → todos los algoritmos y búsqueda → mejor base logística (distinción máximo OOF y parsimonia) → corrección por XGBoost `base_margin` con grilla de 36 → cuatro ensambles → incertidumbre y evaluación ROC/PR/F1. Resultados históricos preservados, sin nuevos ajustes; el selector anidado de representación sigue siendo experiment018 y eligió original 4/5 folds. Se introdujo tabla y figura de selección logística a partir del experimento014, sin afirmar superioridad: AUC 0.941559 combinada vs 0.941357 original, intervalo de la diferencia contiene 0.

Dependencia reparada al mover la carga OOF antes del envío. El equivalente local pasó la ejecución de las 33 celdas sobre 699,960 observaciones con los archivos confidenciales guardados, generando 31 gráficos. Los resultados del finalista son históricos (offset 0.946205, XGB 0.946120, IC95 diferencia incluye cero); no hay mejora demostrada. Las cachés OOF/test nunca se subieron a Git y siguen siendo necesarias para curvas y submission. Código en repositorio público: pendiente publicación equivalente del Notebook/Discussion Kaggle. Próximo número experiment020.


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


## experiment024 — Aceleración GPU/CPU y reutilización de ajustes

Mismo diseño factorial que experiment023, grillas y folds conservados. XGB CUDA y CatBoost GPU con pruebas reales y CPU fallback solo en preflight; CPU_JOBS=-1 y GRID_JOBS=4, presupuesto de hilos dividido, un ajuste GPU a la vez. Matrices y bases de stacking compartidas entre escenarios, offset/bagging adaptativo reutiliza el escenario fijo equivalente. Checkpoints por lote de grilla y por fold/escenario, firma de código, datos, hardware y versiones; outputs nuevos experiment024. No mezclar cachés CPU/GPU o exp023 automáticamente. GPU puede cambiar resultados numéricos, no prometer speedup sin benchmark. Smoke sintético preparado, no ejecutado aquí; no nuevas métricas. Ver `experiments/experiment024/README.md`. Próximo experiment025.


## experiment026 — Resultados experiment024 y Marp

El informe del propietario confirma corrida completa de 40 candidatos, XGBoost CUDA, CatBoost GPU, 32 hilos. Ganador nominal Logística + XGBoost | standardized_kmeans_dbscan, AUC OOF 0.9459909936140145, AP 0.507053935766631; diferencia contra standardized +0.00008032, sin IC nuevo. Top10 y resumen del ZIP y las 27 figuras inline del notebook ejecutado se versionan en experiments/experiment026/resultados/. Las exportaciones de mayor resolución y demás agregados se importan con presentation/import_experiment024.py; no publicar envío Kaggle. Presentaciones actuales 42/53 diapositivas, tema fraud-final-es; fuentes previas archivadas. Compilación oficial pendiente, sin reentrenamiento. Se preservó main del propietario 4d76465; el hotfix histórico bbfe751 (experiment025) quedó fuera de esa rama antes de esta edición. Ver experiments/experiment026/README.md. Próximo experiment027.


## experiment027 — Inferencia pareada de recall del top 10

Nuevo `notebook_inferencia_final_es.ipynb`, sin reentrenar ni alterar notebook final ejecutado. Recupera experiment024 desde NPZ privados, verifica firma/folds y cuatro métricas contra experiment026. Política principal recall 98 % cruzado, sensibilidad umbral 0.50; 45 pares por política, bootstrap conjunto 100k, McNemar exacto bilateral, Holm y Bonferroni, mapas triangulares y magnitud/FPR. Resultados exploratorios condicionados a OOF seleccionadas y umbrales fijos. Salidas outputs/experiment027; nunca publicar datos ni predicciones individuales. Reproducción y smoke en `experiments/experiment027/README.md`. No hay resultados numéricos nuevos sin checkpoints originales. Próximo experiment028.


## experiment028 — AUC pareado y mapas Seaborn con p-valores originales

Actualiza notebook_inferencia_final_es.ipynb sin alterar entrenamiento ni resultados previos. Recall conservado, DeLong pareado y bootstrap AUC estratificado exacto de ambas clases (2 000 réplicas, semilla 42, hasta 4 hilos, caché por 50); 45 pares por familia, Holm/Bonferroni, diferencias e IC, curvas ROC originales. Estilo seaborn whitegrid/dark/notebook original; mapas de p continuos con escala [0,1], anotaciones y CSV precisos. Salidas outputs/experiment028/figuras y tablas en outputs/experiment028. Inferencia exploratoria; no publicar datos ni NPZ. Sin resultados nuevos hasta ejecutar con predicciones privadas. Ver experiments/experiment028/README.md. Próximo experiment029.


## experiment029 — Inferencia final simplificada de F1

Notebook activo reducido a ocho celdas y dos figuras: dashboard 1×2 p bootstrap y Holm (45 pares), IC 95 % de diferencia F1 contra ganador AUC. Nombres originales completos; umbral cruzado recall 98 % original, 100k bootstrap estratificado de patrones, semilla 42, sin reentrenar. Resultados outputs/experiment029, figuras PNG/PDF, versión anterior archivada. Inferencia exploratoria condicionada; no nuevos resultados sin NPZ privados. Ver experiments/experiment029/README.md. Próximo experiment030.
