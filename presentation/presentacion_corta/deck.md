---
marp: true
theme: fraud-es
size: 16:9
paginate: true
transition: fade
footer: 'LDS1071 · Predicción de fraude'
title: 'Selección del modelo de fraude · presentación de 20 minutos'
description: 'Presentación técnica en español a partir de 44 figuras proporcionadas.'
---

<!-- _class: marp-content -->
<div class="marp-tag">PRESENTACIÓN BREVE · 20 MIN</div>

# ¿Cómo seleccionamos un modelo para detectar fraude?

Proyecto final LDS1071 · Kaggle Playground S6E11

**Del análisis exploratorio a una decisión validada con cinco folds.**

---

<!-- _class: marp-content -->
<div class="marp-tag">01 · PROBLEMA</div>

## La pregunta y la ruta experimental

Encontrar una regla que ordene las transacciones desde mayor hasta menor riesgo de fraude.

<div class="marp-cards"><div class="marp-card"><b>1 · Datos</b><p>Describir clases, distribuciones, interacciones y anomalías.</p></div><div class="marp-card"><b>2 · Modelos</b><p>Logit; PCA/splines; random forest; XGBoost y CatBoost.</p></div><div class="marp-card"><b>3 · Validación</b><p>5 folds estratificados; mismo protocolo; GridSearchCV interno.</p></div><div class="marp-card"><b>4 · Decisión</b><p>Probar blends, correcciones logísticas y robustez operativa.</p></div></div>

<div class="marp-message">Criterio oficial: ROC AUC. Métricas de apoyo: AP, log loss, Brier y captura.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">02 · EDA</div>

## El problema: fraude poco frecuente

<div class="fig-hero">
  <img src="../../outputs/figures/01_target_and_missingness.png" alt="El problema: fraude poco frecuente" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.<br/><b>Qué aprendimos:</b> Se requieren validación estratificada y métricas de ranking; accuracy sola no basta.<br/><b>Límite:</b> El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">02 · EDA</div>

## EDA: señal entre las dos clases

<div class="fig-hero">
  <img src="../../outputs/figures/03_class_conditional_densities.png" alt="EDA: señal entre las dos clases" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.<br/><b>Qué aprendimos:</b> Esto motiva modelar simultáneamente características numéricas, categóricas y booleanas.<br/><b>Límite:</b> Las densidades normalizadas por clase no representan la prevalencia real de fraude.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">02 · EDA</div>

## La relación no siempre es lineal

<div class="fig-hero">
  <img src="../../outputs/figures/07_nonlinear_binned_fraud_rates.png" alt="La relación no siempre es lineal" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.<br/><b>Qué aprendimos:</b> Motivación para splines, árboles y boosting frente a logit lineal en log-odds.<br/><b>Límite:</b> El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">02 · EDA</div>

## Interacciones: el riesgo es contextual

<div class="fig-hero">
  <img src="../../outputs/figures/09_bivariate_interaction_heatmaps.png" alt="Interacciones: el riesgo es contextual" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.<br/><b>Qué aprendimos:</b> Un modelo puramente aditivo puede omitir interacciones relevantes.<br/><b>Límite:</b> Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">02 · EDA</div>

## ¿Y las observaciones atípicas?

<div class="fig-hero">
  <img src="../../outputs/figures/11_isolation_forest_anomaly_diagnostics.png" alt="¿Y las observaciones atípicas?" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.<br/><b>Qué aprendimos:</b> Decisión: conservar outliers; una operación rara no es necesariamente un fraude.<br/><b>Límite:</b> No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">03 · METODOLOGÍA</div>

## Preprocesamiento sin fuga de información

En cada fold, todas las transformaciones se ajustan exclusivamente con los datos de entrenamiento.

<div class="marp-cards"><div class="marp-card"><b>Entrada</b><p>Excluir id; separar predictores y etiqueta binaria.</p></div><div class="marp-card"><b>Codificación</b><p>Imputación y one-hot cuando corresponde; CatBoost usa categorías nativas.</p></div><div class="marp-card"><b>Escalamiento</b><p>StandardScaler para logit; PCA sólo como rama experimental.</p></div><div class="marp-card"><b>Predicciones OOF</b><p>Cada observación se predice sin haber entrenado el modelo con ella.</p></div></div>

<div class="marp-message">5-fold StratifiedKFold · seed 42 · métricas y configuraciones guardadas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">03 · MODELOS</div>

## ¿Por qué comenzar con regresión logística?

Es un benchmark reproducible, rápido e interpretable que modela la probabilidad de un evento binario.

<div class="marp-cards"><div class="marp-card"><b>Modelo</b><p>p(x) = σ(β₀ + βᵀx): relación lineal en los log-odds.</p></div><div class="marp-card"><b>Fortalezas</b><p>Regularización L2; probabilidades; coeficientes interpretables en escala transformada.</p></div><div class="marp-card"><b>Limitación</b><p>No aprende interacciones ni curvas arbitrarias sin ingeniería de variables.</p></div><div class="marp-card"><b>Diagnósticos</b><p>Binario ✓; dependencia, linealidad y calibración requieren auditoría.</p></div></div>

<div class="marp-message">Logit estándar y logit con splines: prueba directa de no linealidad.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">03 · MODELOS</div>

## SVD/PCA: ¿reducción útil o pérdida de señal?

<div class="fig-hero">
  <img src="../../outputs/figures/16_pca_explained_variance.png" alt="SVD/PCA: ¿reducción útil o pérdida de señal?" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.<br/><b>Qué aprendimos:</b> Retener 90% de varianza no garantiza retener 90% de señal sobre fraude: se compara mediante CV.<br/><b>Límite:</b> La varianza de X y la información predictiva sobre Y son objetivos distintos.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">03 · MODELOS</div>

## Cinco familias para hipótesis distintas

Todos los modelos compiten con las mismas particiones y el mismo objetivo ROC AUC.

<div class="marp-cards"><div class="marp-card"><b>Logit y splines</b><p>Baselines aditivos; estiman efecto global y curvatura suave.</p></div><div class="marp-card"><b>Random forest</b><p>Bagging de árboles, umbrales e interacciones; baja varianza.</p></div><div class="marp-card"><b>XGBoost</b><p>Boosting secuencial regularizado para capturar errores y patrones complejos.</p></div><div class="marp-card"><b>CatBoost</b><p>Boosting con manejo nativo de variables categóricas y GPU opcional.</p></div></div>

<div class="marp-message">Más complejidad sólo se justifica con mejora fuera de entrenamiento.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">04 · VALIDACIÓN</div>

## Búsqueda de hiperparámetros

<div class="fig-hero">
  <img src="../../outputs/figures/42_gridsearch_full_parameter_space.png" alt="Búsqueda de hiperparámetros" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se registró cada combinación de profundidad, learning rate y regularización explorada.<br/><b>Qué aprendimos:</b> La búsqueda ocurre dentro del entrenamiento de cada fold externo; se evalúa en el fold externo.<br/><b>Límite:</b> El mejor valor interno no garantiza mejora en el fold externo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">04 · RESULTADOS</div>

## ¿Cuál modelo rindió mejor?

<div class="fig-hero">
  <img src="../../outputs/figures/26_four_metric_model_scorecard.png" alt="¿Cuál modelo rindió mejor?" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.<br/><b>Qué aprendimos:</b> No existe un ganador automático por complejidad: evaluar ranking, probabilidad y costo.<br/><b>Límite:</b> Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">05 · ENSEMBLES</div>

## Intento 1: “bagging” de modelos

<div class="fig-hero">
  <img src="../../outputs/figures/14_ensemble_comparisons.png" alt="Intento 1: “bagging” de modelos" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.<br/><b>Qué aprendimos:</b> Nombre exacto: blending; no equivale al bootstrap bagging clásico.<br/><b>Límite:</b> El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">05 · ENSEMBLES</div>

## Intento 2: potenciar los errores de logit

<div class="fig-hero">
  <img src="../../outputs/figures/19_logistic_offset_boosting_diagnostics.png" alt="Intento 2: potenciar los errores de logit" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.<br/><b>Qué aprendimos:</b> p(x)=σ[f_logit(x)+g_XGB(x)]; probar si las correcciones elevan AUC/AP OOF.<br/><b>Límite:</b> No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">05 · ENSEMBLES</div>

## Bagging, blending, stacking: no son lo mismo

La diferencia principal está en cómo se obtienen y combinan las predicciones.

<div class="marp-cards"><div class="marp-card"><b>Bagging</b><p>Mismo algoritmo en muestras bootstrap; agregación de resultados.</p></div><div class="marp-card"><b>Blending realizado</b><p>Promedio de probabilidades de familias y configuraciones diferentes.</p></div><div class="marp-card"><b>Stacking clásico</b><p>Modelo meta que aprende una combinación a partir de predicciones OOF.</p></div><div class="marp-card"><b>Offset boosting realizado</b><p>Árboles que corrigen la salida logit de una regresión logística fija.</p></div></div>

<div class="marp-message">Reportamos lo implementado, sin atribuir al proyecto un meta-learner no ejecutado.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">06 · DECISIÓN</div>

## Fraude capturado bajo un presupuesto

<div class="fig-hero">
  <img src="../../outputs/figures/29_cumulative_gains_and_lift.png" alt="Fraude capturado bajo un presupuesto" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.<br/><b>Qué aprendimos:</b> ROC AUC es el objetivo de Kaggle; captura y precisión describen utilidad operativa.<br/><b>Límite:</b> Las curvas no incluyen el costo real de las investigaciones o falsos positivos.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">06 · DECISIÓN</div>

## ¿Se pueden interpretar como probabilidades?

<div class="fig-hero">
  <img src="../../outputs/figures/32_model_reliability_comparison.png" alt="¿Se pueden interpretar como probabilidades?" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.<br/><b>Qué aprendimos:</b> Un excelente ROC AUC no garantiza calibración; contrastar Brier y log loss.<br/><b>Límite:</b> Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">06 · DECISIÓN</div>

## Decisión final y límite de evidencia

<div class="fig-hero">
  <img src="../../outputs/figures/43_nested_gridsearch_outer_results.png" alt="Decisión final y límite de evidencia" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.<br/><b>Qué aprendimos:</b> No afirmar una superioridad numérica definitiva sin el CSV del run completo ni una validación intacta.<br/><b>Límite:</b> Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">07 · CIERRE</div>

## Conclusión: aprendimos del proceso, no sólo del ranking

Una evaluación justa permite preferir un modelo simple o complejo por evidencia, no por intuición.

<div class="marp-cards"><div class="marp-card"><b>EDA</b><p>Desbalance, no linealidades, interacciones y anomalías sin eliminar datos.</p></div><div class="marp-card"><b>Modelos</b><p>Logit como punto de referencia; PCA, splines, RF, XGBoost y CatBoost contrastados.</p></div><div class="marp-card"><b>Ensembles</b><p>Blend de varios modelos y corrección de log-odds: comparar, no asumir ganancia.</p></div><div class="marp-card"><b>Pendiente</b><p>Confirmar resultados del run definitivo, validar selección y enviar CSV a Kaggle.</p></div></div>

<div class="marp-message">Regla: maximizar ROC AUC OOF; documentar AP, calibración, estabilidad y costos.</div>
