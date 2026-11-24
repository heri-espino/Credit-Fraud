# Guion de exposición · Selección del modelo de fraude · presentación de 20 minutos

**Uso:** el guion complementa las diapositivas sin saturar las imágenes. No son resultados adicionales.

## Diapositiva 01 — ¿Cómo seleccionamos un modelo para detectar fraude?

**Mensaje central:** Del análisis exploratorio a una decisión validada con cinco folds.

**Guion:** Presentar problema, objetivo oficial ROC AUC y la idea central: comparar hipótesis simples y complejas, no elegir complejidad por intuición.

**Tiempo previsto:** 0.50 minutos

## Diapositiva 02 — La pregunta y la ruta experimental

**Mensaje central:** Criterio oficial: ROC AUC. Métricas de apoyo: AP, log loss, Brier y captura.

**Guion:** Este diagrama resume lo que se hizo, no una lista de modelos arbitraria. Cada familia contrasta una hipótesis diferente sobre la relación entre X y fraude.

**Tiempo previsto:** 0.85 minutos

## Diapositiva 03 — El problema: fraude poco frecuente

**Mensaje central:** Se requieren validación estratificada y métricas de ranking; accuracy sola no basta.

**Guion:** Destacar el denominador: un clasificador que predice siempre “no fraude” tendría alta accuracy y utilidad nula. No se eliminaron las observaciones raras por sistema.

**Imagen:** `outputs/figures/01_target_and_missingness.png`
**Advertencia:** El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.

**Tiempo previsto:** 0.90 minutos

## Diapositiva 04 — EDA: señal entre las dos clases

**Mensaje central:** Esto motiva modelar simultáneamente características numéricas, categóricas y booleanas.

**Guion:** Explicar que se usaron densidades condicionadas para comparar forma, no para inferir prevalencias. Evitar causalidad.

**Imagen:** `outputs/figures/03_class_conditional_densities.png`
**Advertencia:** Las densidades normalizadas por clase no representan la prevalencia real de fraude.

**Tiempo previsto:** 0.85 minutos

## Diapositiva 05 — La relación no siempre es lineal

**Mensaje central:** Motivación para splines, árboles y boosting frente a logit lineal en log-odds.

**Guion:** Explicar binning y tasas marginales. Ejemplificar el cambio con el importe, velocidad y puntuación de riesgo del comercio. Las curvas no son efectos parciales.

**Imagen:** `outputs/figures/07_nonlinear_binned_fraud_rates.png`
**Advertencia:** El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.

**Tiempo previsto:** 1.00 minutos

## Diapositiva 06 — Interacciones: el riesgo es contextual

**Mensaje central:** Un modelo puramente aditivo puede omitir interacciones relevantes.

**Guion:** Explicar cómo se construye el heatmap: cruzar quintiles e indicar número de transacciones por celda. Interacción descriptiva no causal.

**Imagen:** `outputs/figures/09_bivariate_interaction_heatmaps.png`
**Advertencia:** Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.

**Tiempo previsto:** 0.90 minutos

## Diapositiva 07 — ¿Y las observaciones atípicas?

**Mensaje central:** Decisión: conservar outliers; una operación rara no es necesariamente un fraude.

**Guion:** Diferenciar detección no supervisada y clasificación supervisada. Evitar presentar la tasa de anómalos como una estimación validada.

**Imagen:** `outputs/figures/11_isolation_forest_anomaly_diagnostics.png`
**Advertencia:** No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.

**Tiempo previsto:** 0.75 minutos

## Diapositiva 08 — Preprocesamiento sin fuga de información

**Mensaje central:** 5-fold StratifiedKFold · seed 42 · métricas y configuraciones guardadas.

**Guion:** Explicar por qué PCA, imputación y escalado deben vivir dentro del Pipeline y no ajustarse una vez en todo el dataset.

**Tiempo previsto:** 1.00 minutos

## Diapositiva 09 — ¿Por qué comenzar con regresión logística?

**Mensaje central:** Logit estándar y logit con splines: prueba directa de no linealidad.

**Guion:** Aclarar que no se necesita normalidad de X ni varianza constante. Añadir distinción entre supuestos de estimación e idoneidad predictiva.

**Tiempo previsto:** 1.00 minutos

## Diapositiva 10 — SVD/PCA: ¿reducción útil o pérdida de señal?

**Mensaje central:** Retener 90% de varianza no garantiza retener 90% de señal sobre fraude: se compara mediante CV.

**Guion:** SVD de matriz estandarizada, X = UΣVᵀ. Contrastar logit con y sin PCA; PCA no debe imponerse a los árboles.

**Imagen:** `outputs/figures/16_pca_explained_variance.png`
**Advertencia:** La varianza de X y la información predictiva sobre Y son objetivos distintos.

**Tiempo previsto:** 0.80 minutos

## Diapositiva 11 — Cinco familias para hipótesis distintas

**Mensaje central:** Más complejidad sólo se justifica con mejora fuera de entrenamiento.

**Guion:** Separar bagging interno de random forest de la combinación posterior de modelos heterogéneos.

**Tiempo previsto:** 0.85 minutos

## Diapositiva 12 — Búsqueda de hiperparámetros

**Mensaje central:** La búsqueda ocurre dentro del entrenamiento de cada fold externo; se evalúa en el fold externo.

**Guion:** Describir 8 combinaciones × 3 folds internos por familia y hasta 20k filas para tuning por fold externo. Reajuste en el train externo completo.

**Imagen:** `outputs/figures/42_gridsearch_full_parameter_space.png`
**Advertencia:** El mejor valor interno no garantiza mejora en el fold externo.

**Tiempo previsto:** 0.95 minutos

## Diapositiva 13 — ¿Cuál modelo rindió mejor?

**Mensaje central:** No existe un ganador automático por complejidad: evaluar ranking, probabilidad y costo.

**Guion:** La imagen permite comparación visual, pero los CSV crudos del full run no se recibieron junto a figuras; no dar décimas inventadas. Selección oficial por ROC AUC.

**Imagen:** `outputs/figures/26_four_metric_model_scorecard.png`
**Advertencia:** Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.

**Tiempo previsto:** 0.85 minutos

## Diapositiva 14 — Intento 1: “bagging” de modelos

**Mensaje central:** Nombre exacto: blending; no equivale al bootstrap bagging clásico.

**Guion:** Mostrar que el promedio de todos no garantiza superar al mejor individuo. Explicar correlación entre predicciones y por qué diversidad importa.

**Imagen:** `outputs/figures/14_ensemble_comparisons.png`
**Advertencia:** El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.

**Tiempo previsto:** 0.85 minutos

## Diapositiva 15 — Intento 2: potenciar los errores de logit

**Mensaje central:** p(x)=σ[f_logit(x)+g_XGB(x)]; probar si las correcciones elevan AUC/AP OOF.

**Guion:** Esto NO es stacking clásico. No se entrenó una meta-regresión logística con predicciones de varios modelos; para eso harían falta predicciones OOF de nivel 1 y otro proceso de evaluación.

**Imagen:** `outputs/figures/19_logistic_offset_boosting_diagnostics.png`
**Advertencia:** No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.

**Tiempo previsto:** 1.05 minutos

## Diapositiva 16 — Bagging, blending, stacking: no son lo mismo

**Mensaje central:** Reportamos lo implementado, sin atribuir al proyecto un meta-learner no ejecutado.

**Guion:** Esta diapositiva es crucial para rigor conceptual. La idea original de bagging evolucionó a blends; la idea de stacking evolucionó a corrección en escala de log-odds.

**Tiempo previsto:** 1.05 minutos

## Diapositiva 17 — Fraude capturado bajo un presupuesto

**Mensaje central:** ROC AUC es el objetivo de Kaggle; captura y precisión describen utilidad operativa.

**Guion:** Explicar lift como captura relativa a selección aleatoria. Para decidir umbral de producción faltan costos reales de revisión.

**Imagen:** `outputs/figures/29_cumulative_gains_and_lift.png`
**Advertencia:** Las curvas no incluyen el costo real de las investigaciones o falsos positivos.

**Tiempo previsto:** 0.90 minutos

## Diapositiva 18 — ¿Se pueden interpretar como probabilidades?

**Mensaje central:** Un excelente ROC AUC no garantiza calibración; contrastar Brier y log loss.

**Guion:** Diferenciar ordenar de estimar probabilidad real. Clases muy desbalanceadas hacen importantes estas gráficas.

**Imagen:** `outputs/figures/32_model_reliability_comparison.png`
**Advertencia:** Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.

**Tiempo previsto:** 0.75 minutos

## Diapositiva 19 — Decisión final y límite de evidencia

**Mensaje central:** No afirmar una superioridad numérica definitiva sin el CSV del run completo ni una validación intacta.

**Guion:** La figura compara resultados de tuning externo; no demuestra que GridSearchCV siempre ayude. La selección de blend sobre los mismos OOF genera optimismo. Para reproducir la selección exacta: consultar ensemble_metrics.csv y run_manifest.json del run real.

**Imagen:** `outputs/figures/43_nested_gridsearch_outer_results.png`
**Advertencia:** Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.

**Tiempo previsto:** 1.10 minutos

## Diapositiva 20 — Conclusión: aprendimos del proceso, no sólo del ranking

**Mensaje central:** Regla: maximizar ROC AUC OOF; documentar AP, calibración, estabilidad y costos.

**Guion:** Cerrar con tres aprendizajes y reconocer limitación de selección. La prueba no etiquetada de Kaggle no permite verificar AUC offline.

**Tiempo previsto:** 0.65 minutos

