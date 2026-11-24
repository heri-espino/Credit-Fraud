---
marp: true
theme: fraud-es
size: 16:9
paginate: true
transition: fade
footer: 'LDS1071 · Predicción de fraude'
title: 'Predicción de fraude · presentación completa'
description: 'Presentación técnica en español a partir de 44 figuras proporcionadas.'
---

<!-- _class: marp-content -->
<div class="marp-tag">PRESENTACIÓN TÉCNICA EN ESPAÑOL</div>

# Predicción de fraude con tarjetas: el proceso completo

Análisis exploratorio · modelos · selección · ensambles · validación

**LDS1071 · Kaggle S6E11 · fuente: notebook y 44 figuras proporcionadas**

---

<!-- _class: marp-content -->
<div class="marp-tag">A · DEFINICIÓN</div>

## Qué problema resolvemos y qué entregamos



<div class="marp-cards"><div class="marp-card"><b>Entrada X</b><p>24 predictores numéricos, categóricos y booleanos; el identificador id se excluye.</p></div><div class="marp-card"><b>Objetivo Y</b><p>Variable binaria is_fraud, con prevalencia aproximada de 1.67%.</p></div><div class="marp-card"><b>Salida</b><p>Una probabilidad o score de fraude para cada fila del test.</p></div><div class="marp-card"><b>Evaluación</b><p>Kaggle usa el área bajo la curva ROC; AP/calibración explican otros aspectos.</p></div></div>

<div class="marp-message">Un buen score ordena; una buena probabilidad también necesita calibración.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">A · DEFINICIÓN</div>

## Datos y desafío estadístico



<div class="marp-cards"><div class="marp-card"><b>Tamaño</b><p>699,960 filas de entrenamiento; 11,689 casos de fraude.</p></div><div class="marp-card"><b>Clases</b><p>688,271 legítimas; ~1.67% positivas.</p></div><div class="marp-card"><b>Validez</b><p>No se observaron datos faltantes en entrenamiento; el id no entra al modelo.</p></div><div class="marp-card"><b>Cuidado</b><p>La exactitud puede ser alta prediciendo todo legítimo: preferir ROC AUC/AP.</p></div></div>

<div class="marp-message">Fraude raro ≠ necesariamente anomalía aislada.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">A · DEFINICIÓN</div>

## Métricas: cada una responde otra pregunta



<div class="marp-cards"><div class="marp-card"><b>ROC AUC</b><p>Probabilidad de que un positivo reciba mayor score que un negativo.</p></div><div class="marp-card"><b>Average precision</b><p>Resume precisión vs recobrado; especialmente informativa con una clase rara.</p></div><div class="marp-card"><b>Log loss / Brier</b><p>Evalúan calidad de probabilidades, no sólo ranking.</p></div><div class="marp-card"><b>Top-k y lift</b><p>Miden cuántos fraudes se capturan al revisar sólo cierta fracción.</p></div></div>

<div class="marp-message">La métrica oficial fija el objetivo; las métricas auxiliares previenen conclusiones incompletas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">A · MÉTODO</div>

## Diseño experimental en siete pasos



<div class="marp-cards"><div class="marp-card"><b>01</b><p>Revisar tipos, distribución, faltantes y relaciones.</p></div><div class="marp-card"><b>02</b><p>Diagnosticar no linealidades, interacciones y anomalías.</p></div><div class="marp-card"><b>03</b><p>Preparar pipelines sin fuga de información.</p></div><div class="marp-card"><b>04</b><p>Comparar familias y configuraciones en 5 folds.</p></div><div class="marp-card"><b>05</b><p>Afinar XGBoost/CatBoost con búsqueda interna.</p></div><div class="marp-card"><b>06</b><p>Evaluar blends y corrección de log-odds.</p></div><div class="marp-card"><b>07</b><p>Elegir estrategia OOF y preparar archivo Kaggle.</p></div></div>

<div class="marp-message">Semilla 42; conservar resultados por fold y por candidato.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">A · MÉTODO</div>

## Validación cruzada sin data leakage



<div class="marp-cards"><div class="marp-card"><b>5 folds estratificados</b><p>Cada fold conserva aproximadamente la proporción de fraude.</p></div><div class="marp-card"><b>Pipeline</b><p>Imputación, escalado, one-hot, splines y PCA se ajustan sólo con train interno.</p></div><div class="marp-card"><b>OOF</b><p>Cada fila obtiene una predicción de un modelo que nunca entrenó con esa fila.</p></div><div class="marp-card"><b>Selección</b><p>Elegir el máximo en las mismas predicciones OOF causa cierto optimismo; un holdout posterior lo reduce.</p></div></div>

<div class="marp-message">El CV permite comparar modelos con exactamente los mismos folds.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">B · ANÁLISIS EXPLORATORIO</div>

## ¿Por qué explorar antes de modelar?



<div class="marp-cards"><div class="marp-card"><b>Calidad</b><p>Detectar valores faltantes, duplicados potenciales y categorías raras.</p></div><div class="marp-card"><b>Geometría</b><p>Identificar colas, cambios de escala, dependencias y separabilidad.</p></div><div class="marp-card"><b>Hipótesis</b><p>Decidir si una frontera lineal puede ser razonable o es necesario introducir no linealidad.</p></div><div class="marp-card"><b>Precaución</b><p>Las asociaciones marginales no prueban efectos ajustados ni causalidad.</p></div></div>

<div class="marp-message">Las figuras de EDA ayudan a formular hipótesis, no reemplazan la validación cruzada.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Balance de clases y completitud

<div class="fig-hero">
  <img src="../../outputs/figures/01_target_and_missingness.png" alt="Balance de clases y completitud" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.<br/><b>Qué aprendimos:</b> La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.<br/><b>Límite:</b> El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Distribuciones numéricas

<div class="fig-hero">
  <img src="../../outputs/figures/02_numeric_distributions.png" alt="Distribuciones numéricas" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.<br/><b>Qué aprendimos:</b> Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.<br/><b>Límite:</b> Una distribución sesgada no determina por sí sola utilidad predictiva.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Distribuciones según la clase

<div class="fig-hero">
  <img src="../../outputs/figures/03_class_conditional_densities.png" alt="Distribuciones según la clase" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.<br/><b>Qué aprendimos:</b> La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.<br/><b>Límite:</b> Las densidades normalizadas por clase no representan la prevalencia real de fraude.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Correlaciones de Pearson y Spearman

<div class="fig-hero">
  <img src="../../outputs/figures/04_pearson_spearman_correlations.png" alt="Correlaciones de Pearson y Spearman" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).<br/><b>Qué aprendimos:</b> Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.<br/><b>Límite:</b> Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Riesgo por categorías

<div class="fig-hero">
  <img src="../../outputs/figures/05_categorical_risks.png" alt="Riesgo por categorías" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se estimó la tasa observada de fraude por categoría y su soporte muestral.<br/><b>Qué aprendimos:</b> Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.<br/><b>Límite:</b> Categorías con pocas observaciones pueden producir tasas muy inestables.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Indicadores booleanos: frecuencia y riesgo

<div class="fig-hero">
  <img src="../../outputs/figures/06_flag_prevalence_vs_fraud.png" alt="Indicadores booleanos: frecuencia y riesgo" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.<br/><b>Qué aprendimos:</b> Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.<br/><b>Límite:</b> La asociación marginal puede desaparecer al ajustar por otros predictores.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">C · NO LINEALIDAD</div>

## De correlaciones a relaciones no lineales



<div class="marp-cards"><div class="marp-card"><b>Problema</b><p>Una baja correlación no descarta una relación en U o interacciones.</p></div><div class="marp-card"><b>Herramienta</b><p>Binning cuantílico de variables, cruce de rangos y tasas condicionadas.</p></div><div class="marp-card"><b>Modelo lineal</b><p>La regresión logística es lineal en βᵀx, no en la probabilidad.</p></div><div class="marp-card"><b>Alternativas</b><p>Splines, árboles, boosted trees y transformación de variables.</p></div></div>

<div class="marp-message">El EDA motivó candidatos adicionales; su valor se decide con CV.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">C · PATRONES Y ANOMALÍAS</div>

## No linealidad de las tasas de fraude

<div class="fig-hero">
  <img src="../../outputs/figures/07_nonlinear_binned_fraud_rates.png" alt="No linealidad de las tasas de fraude" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.<br/><b>Qué aprendimos:</b> Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.<br/><b>Límite:</b> El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">C · PATRONES Y ANOMALÍAS</div>

## Patrones temporales de fraude

<div class="fig-hero">
  <img src="../../outputs/figures/08_time_patterns.png" alt="Patrones temporales de fraude" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se analizaron tasas por hora, día y otras variables temporales disponibles.<br/><b>Qué aprendimos:</b> Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.<br/><b>Límite:</b> La agregación no prueba estabilidad futura ni sustituye una validación temporal.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">C · PATRONES Y ANOMALÍAS</div>

## Interacciones entre variables numéricas

<div class="fig-hero">
  <img src="../../outputs/figures/09_bivariate_interaction_heatmaps.png" alt="Interacciones entre variables numéricas" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.<br/><b>Qué aprendimos:</b> Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.<br/><b>Límite:</b> Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">C · PATRONES Y ANOMALÍAS</div>

## Valores extremos: criterio IQR

<div class="fig-hero">
  <img src="../../outputs/figures/10_univariate_outliers.png" alt="Valores extremos: criterio IQR" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.<br/><b>Qué aprendimos:</b> Los extremos pueden ser transacciones válidas y contener señal de fraude.<br/><b>Límite:</b> Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">C · PATRONES Y ANOMALÍAS</div>

## Anomalías con Isolation Forest

<div class="fig-hero">
  <img src="../../outputs/figures/11_isolation_forest_anomaly_diagnostics.png" alt="Anomalías con Isolation Forest" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.<br/><b>Qué aprendimos:</b> El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.<br/><b>Límite:</b> No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">C · ANOMALÍAS</div>

## Anomalía, outlier y fraude: tres conceptos



<div class="marp-cards"><div class="marp-card"><b>Outlier</b><p>Observación extrema según una variable y una regla estadística.</p></div><div class="marp-card"><b>Anomalía</b><p>Patrón multivariante infrecuente, sin usar etiquetas.</p></div><div class="marp-card"><b>Fraude</b><p>Resultado etiquetado que puede ser típico o atípico.</p></div><div class="marp-card"><b>Decisión EDA</b><p>No borrar transacciones extremas automáticamente; compararlas descriptivamente.</p></div></div>

<div class="marp-message">Eliminar colas puede destruir justamente la señal que queremos detectar.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · PREPROCESAMIENTO</div>

## Pipelines de modelos: decisiones concretas



<div class="marp-cards"><div class="marp-card"><b>Regresión logística</b><p>Estandarización numérica, codificación de categorías y regularización L2.</p></div><div class="marp-card"><b>Logit con splines</b><p>SplineTransformer para importe, velocidad y riesgo del comercio.</p></div><div class="marp-card"><b>Árboles</b><p>Random forest y XGBoost aprenden cortes; no exigir PCA.</p></div><div class="marp-card"><b>CatBoost</b><p>Procesamiento nativo de categorías, con imputación y GPU opcional.</p></div></div>

<div class="marp-message">La transformación se ajusta dentro del fold de entrenamiento.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · DIMENSIONALIDAD</div>

## SVD y PCA: por qué se probaron



<div class="marp-cards"><div class="marp-card"><b>Factorización</b><p>Para Z centrada: Z = UΣVᵀ.</p></div><div class="marp-card"><b>Truncamiento</b><p>Retener k componentes con suma de varianza explicada ≥ 90%.</p></div><div class="marp-card"><b>Hipótesis</b><p>Reducir ruido/colinealidad puede estabilizar un modelo lineal.</p></div><div class="marp-card"><b>Contraargumento</b><p>Una dirección de baja varianza puede predecir muy bien la etiqueta.</p></div></div>

<div class="marp-message">Por eso PCA es candidato experimental, no paso obligatorio.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · LÍNEA BASE</div>

## ¿Por qué regresión logística?



<div class="marp-cards"><div class="marp-card"><b>Modelo</b><p>p(Y=1|x)=1/(1+exp[-(β₀+βᵀx)]).</p></div><div class="marp-card"><b>Eficiencia</b><p>Comparación rápida con un dataset grande.</p></div><div class="marp-card"><b>Interpretabilidad</b><p>Coeficientes describen cambios en log-odds, dados otros predictores.</p></div><div class="marp-card"><b>Diagnóstico</b><p>Una forma funcional simple es una referencia para medir ganancia de modelos complejos.</p></div></div>

<div class="marp-message">L2 ayuda ante correlaciones, pero no “corrige” especificación no lineal.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · AUDITORÍA</div>

## ¿Se satisfacen los supuestos de logit?



<div class="marp-cards"><div class="marp-card"><b>Se cumple</b><p>La respuesta es binaria; hay suficientes fraudes para ajustar el modelo.</p></div><div class="marp-card"><b>En revisión</b><p>Linealidad de log-odds, separación completa multivariante y dependencia entre operaciones.</p></div><div class="marp-card"><b>Se diagnostica</b><p>Colinealidad, convergencia, especificación con splines y calibración OOF.</p></div><div class="marp-card"><b>No se requiere</b><p>Normalidad de predictores ni homocedasticidad de errores Bernoulli.</p></div></div>

<div class="marp-message">La utilidad predictiva no equivale a validez causal de coeficientes.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · ESPECIFICACIÓN</div>

## ¿Qué aporta el spline logístico?



<div class="marp-cards"><div class="marp-card"><b>Modelo original</b><p>f(x)=β₀+Σ βⱼ xⱼ.</p></div><div class="marp-card"><b>Modelo extendido</b><p>f(x)=β₀+Σₖ γₖ Bₖ(x), con funciones base spline.</p></div><div class="marp-card"><b>Ventaja</b><p>Curvatura interpretable y continua sin cambiar la familia logística.</p></div><div class="marp-card"><b>Control</b><p>Colocar los splines dentro del Pipeline y validar con folds idénticos.</p></div></div>

<div class="marp-message">Probar una no linealidad específica es más informativo que añadir complejidad indiscriminada.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · MODELOS</div>

## Random forest: bagging dentro de una familia



<div class="marp-cards"><div class="marp-card"><b>Idea</b><p>Muchos árboles ajustados sobre muestras y subconjuntos aleatorios de variables.</p></div><div class="marp-card"><b>Promedio</b><p>La agregación de árboles reduce varianza frente a un árbol individual.</p></div><div class="marp-card"><b>Fortaleza</b><p>Aprende umbrales e interacciones sin ecuaciones de spline explícitas.</p></div><div class="marp-card"><b>Costo</b><p>Puede consumir memoria y no siempre calibra probabilidades óptimamente.</p></div></div>

<div class="marp-message">Este sí es un mecanismo tipo bagging, a diferencia del blend posterior.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · MODELOS</div>

## XGBoost: árboles que corrigen errores



<div class="marp-cards"><div class="marp-card"><b>Mecanismo</b><p>Se agregan árboles secuenciales guiados por el gradiente de la pérdida.</p></div><div class="marp-card"><b>Regularización</b><p>Profundidad, learning rate, min_child_weight y número de árboles.</p></div><div class="marp-card"><b>Hipótesis</b><p>Capturar no linealidad/interacciones omitidas por logit.</p></div><div class="marp-card"><b>Hardware</b><p>tree_method=&quot;hist&quot;; CUDA si la prueba real detecta GPU, si no CPU.</p></div></div>

<div class="marp-message">Se conserva el mismo esquema de evaluación, sin favorecer a un algoritmo por hardware.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · MODELOS</div>

## CatBoost: otra forma de boosting



<div class="marp-cards"><div class="marp-card"><b>Categorías</b><p>Admite variables categóricas de forma nativa; reduce la necesidad de one-hot.</p></div><div class="marp-card"><b>Control de complejidad</b><p>depth, learning_rate, l2_leaf_reg, iterations.</p></div><div class="marp-card"><b>Comparación</b><p>Candidatos fijos y variantes ajustadas con GridSearchCV.</p></div><div class="marp-card"><b>Hardware</b><p>GPU NVIDIA cuando está disponible; fallback explícito a CPU.</p></div></div>

<div class="marp-message">Diferentes sesgos inductivos merecen comparación directa, no suposiciones de superioridad.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">D · COMPARACIÓN</div>

## Diseño de candidatos e hiperparámetros



<div class="marp-cards"><div class="marp-card"><b>Conjunto</b><p>19 especificaciones propuestas, incluyendo 2 variantes con búsqueda interna.</p></div><div class="marp-card"><b>Evaluación externa</b><p>19 × 5 = 95 evaluaciones de folds externas.</p></div><div class="marp-card"><b>Búsqueda interna</b><p>2 familias × 5 folds × 8 configuraciones × 3 folds = 240 ajustes internos.</p></div><div class="marp-card"><b>Costo total</b><p>Además del refit de las mejores configuraciones y de dos etapas en offset boosting.</p></div></div>

<div class="marp-message">En modo rápido el notebook reduce tanto filas como hiperparámetros; no mezclar esos scores con el full run.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Comparación de candidatos en cinco folds

<div class="fig-hero">
  <img src="../../outputs/figures/12_candidate_scores_and_folds.png" alt="Comparación de candidatos en cinco folds" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se calcularon ROC AUC out-of-fold por candidato y por partición.<br/><b>Qué aprendimos:</b> El desempeño medio debe juzgarse junto con su variación entre particiones y familias.<br/><b>Límite:</b> La elección del máximo dentro del mismo CV introduce optimismo de selección.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Correlación entre modelos

<div class="fig-hero">
  <img src="../../outputs/figures/13_oof_prediction_correlations.png" alt="Correlación entre modelos" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon los vectores de probabilidades OOF de todos los candidatos.<br/><b>Qué aprendimos:</b> Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.<br/><b>Límite:</b> Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Modelo individual frente a combinaciones

<div class="fig-hero">
  <img src="../../outputs/figures/14_ensemble_comparisons.png" alt="Modelo individual frente a combinaciones" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.<br/><b>Qué aprendimos:</b> Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.<br/><b>Límite:</b> El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Curvas ROC y precisión–recobrado

<div class="fig-hero">
  <img src="../../outputs/figures/15_oof_roc_pr_curves.png" alt="Curvas ROC y precisión–recobrado" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.<br/><b>Qué aprendimos:</b> ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.<br/><b>Límite:</b> Ninguna curva fija por sí sola un umbral operativo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## SVD/PCA: 90% de varianza

<div class="fig-hero">
  <img src="../../outputs/figures/16_pca_explained_variance.png" alt="SVD/PCA: 90% de varianza" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.<br/><b>Qué aprendimos:</b> La reducción es una alternativa de representación, no una mejora predictiva garantizada.<br/><b>Límite:</b> La varianza de X y la información predictiva sobre Y son objetivos distintos.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Supuestos logísticos y posibles cambios

<div class="fig-hero">
  <img src="../../outputs/figures/17_assumptions_vif_and_feature_shift.png" alt="Supuestos logísticos y posibles cambios" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.<br/><b>Qué aprendimos:</b> Es necesario separar problemas de especificación, dependencia y cambios de distribución.<br/><b>Límite:</b> Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Diagnóstico de la regresión logística

<div class="fig-hero">
  <img src="../../outputs/figures/18_oof_logistic_assumption_checks.png" alt="Diagnóstico de la regresión logística" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.<br/><b>Qué aprendimos:</b> Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.<br/><b>Límite:</b> Predictores normales y homocedasticidad NO son supuestos requeridos para logit.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Corregir el logit con XGBoost

<div class="fig-hero">
  <img src="../../outputs/figures/19_logistic_offset_boosting_diagnostics.png" alt="Corregir el logit con XGBoost" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.<br/><b>Qué aprendimos:</b> Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.<br/><b>Límite:</b> No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">E · ENSEMBLES</div>

## Blending y bagging: cómo evolucionó la idea inicial



<div class="marp-cards"><div class="marp-card"><b>Propuesta</b><p>Conservar todos los modelos en vez de quedarse solamente con el ganador.</p></div><div class="marp-card"><b>Realización</b><p>Promedio equiponderado de probabilidades OOF y de prueba.</p></div><div class="marp-card"><b>Cuatro estrategias</b><p>Mejor individual; todos; top 3; mejor de cada familia.</p></div><div class="marp-card"><b>Hallazgo metodológico</b><p>Más modelos no implica mejor AUC si sus errores son correlacionados.</p></div></div>

<div class="marp-message">Término preciso de la realización: blending entre familias heterogéneas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">E · ENSEMBLES</div>

## Qué sería stacking clásico



<div class="marp-cards"><div class="marp-card"><b>Nivel 1</b><p>Ajustar modelos base y obtener predicciones OOF de cada uno.</p></div><div class="marp-card"><b>Nivel 2</b><p>Construir matriz Z de scores OOF y entrenar una meta-regresión logística.</p></div><div class="marp-card"><b>Sin fuga</b><p>Las predicciones para entrenar el meta-modelo no pueden ser in-sample.</p></div><div class="marp-card"><b>Estado real</b><p>El notebook no implementó ese meta-learner; sí implementó blending y offset boosting.</p></div></div>

<div class="marp-message">Explicar stacking propuesto sin presentarlo como experimento ya ejecutado.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">E · ENSEMBLES</div>

## Logit + booster de corrección en escala logit



<div class="marp-cards"><div class="marp-card"><b>Primera etapa</b><p>f_LR(x)=β₀+βᵀx; congelar los coeficientes una vez entrenados.</p></div><div class="marp-card"><b>Segunda etapa</b><p>g_XGB(x) aprende correcciones utilizando base_margin=f_LR(x).</p></div><div class="marp-card"><b>Predicción final</b><p>p(x)=σ(f_LR(x)+g_XGB(x)).</p></div><div class="marp-card"><b>Riesgo</b><p>La segunda etapa puede corregir estructura o sobreajustar ruido; comparar en OOF.</p></div></div>

<div class="marp-message">Es una composición aditiva sobre el logit, NO stacking con meta-logit.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">E · ENSEMBLES</div>

## Por qué conservar modelos que no ganaron



<div class="marp-cards"><div class="marp-card"><b>Reproducibilidad</b><p>Cada configuración tiene métricas, folds y predicciones guardadas.</p></div><div class="marp-card"><b>Diversidad</b><p>Un candidato inferior puede complementar a otro si comete errores distintos.</p></div><div class="marp-card"><b>Costo</b><p>Guardar todos permite estudiar correlación y solapamiento de casos top-risk.</p></div><div class="marp-card"><b>Selección</b><p>Elegir blends previamente definidos; no buscar combinaciones infinitas sin validación.</p></div></div>

<div class="marp-message">La selección sobre OOF es exploratoria y no representa una evaluación completamente intacta.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">F · EXPLORACIÓN AMPLIADA</div>

## EDA extendido: qué más investigamos



<div class="marp-cards"><div class="marp-card"><b>Discriminación univariante</b><p>AUC por predictor para priorizar explicaciones.</p></div><div class="marp-card"><b>Subgrupos</b><p>Interacciones entre banderas, categorías y ventanas temporales.</p></div><div class="marp-card"><b>Geometría</b><p>ECDF y dispersión de clases en parejas de variables.</p></div><div class="marp-card"><b>Distribución del test</b><p>Buscar desplazamientos sin conocer las etiquetas de la prueba.</p></div></div>

<div class="marp-message">Cada gráfico sirve para generar preguntas, no para ajustar modelos sobre el test.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Valor discriminativo de cada variable

<div class="fig-hero">
  <img src="../../outputs/figures/20_univariate_feature_discrimination.png" alt="Valor discriminativo de cada variable" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se estimó el AUC de predictores aislados y se compararon señales univariantes.<br/><b>Qué aprendimos:</b> El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.<br/><b>Límite:</b> Un AUC univariante alto no asegura contribución incremental.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Distribuciones acumuladas por clase

<div class="fig-hero">
  <img src="../../outputs/figures/21_class_conditional_ecdfs.png" alt="Distribuciones acumuladas por clase" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.<br/><b>Qué aprendimos:</b> Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.<br/><b>Límite:</b> Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Categorías × indicadores booleanos

<div class="fig-hero">
  <img src="../../outputs/figures/22_categorical_flag_interactions.png" alt="Categorías × indicadores booleanos" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.<br/><b>Qué aprendimos:</b> Una misma bandera puede tener distinta asociación con el fraude según su contexto.<br/><b>Límite:</b> En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Mapa de riesgo por día y hora

<div class="fig-hero">
  <img src="../../outputs/figures/23_weekly_hourly_fraud_surface.png" alt="Mapa de riesgo por día y hora" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.<br/><b>Qué aprendimos:</b> Puede haber concentraciones temporales no captadas por términos horarios aislados.<br/><b>Límite:</b> La composición de transacciones puede explicar parte del efecto observado.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Geometría bivariante por clase

<div class="fig-hero">
  <img src="../../outputs/figures/24_pairwise_class_geometry.png" alt="Geometría bivariante por clase" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.<br/><b>Qué aprendimos:</b> Los patrones de separación multivariada justifican no depender solo de un predictor.<br/><b>Límite:</b> Las muestras de visualización no deben confundirse con la distribución completa.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">F · EDA EXTENDIDO</div>

## Comparación entrenamiento–prueba

<div class="fig-hero">
  <img src="../../outputs/figures/25_train_test_ecdf_shift.png" alt="Comparación entrenamiento–prueba" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.<br/><b>Qué aprendimos:</b> Permite detectar cambios marginales antes de enviar predicciones a Kaggle.<br/><b>Límite:</b> Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">G · EVALUACIÓN</div>

## De la métrica de Kaggle a una operación real



<div class="marp-cards"><div class="marp-card"><b>Competencia</b><p>Optimizar ROC AUC; ranking entre pares de clases.</p></div><div class="marp-card"><b>Evento raro</b><p>Registrar average precision, precisión y recall.</p></div><div class="marp-card"><b>Probabilidades</b><p>Inspeccionar Brier, log loss y curvas de confiabilidad.</p></div><div class="marp-card"><b>Política</b><p>Medir captura y errores al revisar top 1%, 5% o 10%.</p></div></div>

<div class="marp-message">No hay una única métrica que responda todos los usos.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">G · EVALUACIÓN</div>

## Validación de umbrales y presupuesto



<div class="marp-cards"><div class="marp-card"><b>Umbral fijo</b><p>Predecir positivo si p ≥ 0.5: simple pero arbitrario con gran desbalance.</p></div><div class="marp-card"><b>Top k</b><p>Revisar el k% con mayor puntuación: umbral adaptado a capacidad.</p></div><div class="marp-card"><b>Ganancia</b><p>Comparar detecciones acumuladas con selección aleatoria.</p></div><div class="marp-card"><b>Faltan costos</b><p>Para optimizar el umbral de negocio se necesitan costos de falsos positivos/negativos.</p></div></div>

<div class="marp-message">Estas políticas son evaluadas; no deben confundirse con entrenamiento distinto.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Comparación con cuatro métricas

<div class="fig-hero">
  <img src="../../outputs/figures/26_four_metric_model_scorecard.png" alt="Comparación con cuatro métricas" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.<br/><b>Qué aprendimos:</b> La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.<br/><b>Límite:</b> Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento frente a costo computacional

<div class="fig-hero">
  <img src="../../outputs/figures/27_performance_vs_training_time.png" alt="Rendimiento frente a costo computacional" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.<br/><b>Qué aprendimos:</b> Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.<br/><b>Límite:</b> Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Distribuciones de riesgo predicho

<div class="fig-hero">
  <img src="../../outputs/figures/28_oof_score_distributions.png" alt="Distribuciones de riesgo predicho" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.<br/><b>Qué aprendimos:</b> La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.<br/><b>Límite:</b> Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Ganancia acumulada y lift

<div class="fig-hero">
  <img src="../../outputs/figures/29_cumulative_gains_and_lift.png" alt="Ganancia acumulada y lift" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.<br/><b>Qué aprendimos:</b> La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.<br/><b>Límite:</b> Las curvas no incluyen el costo real de las investigaciones o falsos positivos.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Precisión y recobrado con capacidad limitada

<div class="fig-hero">
  <img src="../../outputs/figures/30_precision_recall_at_review_budget.png" alt="Precisión y recobrado con capacidad limitada" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.<br/><b>Qué aprendimos:</b> Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.<br/><b>Límite:</b> La mejor fracción a revisar depende de costos externos ausentes del dataset.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Errores según política de decisión

<div class="fig-hero">
  <img src="../../outputs/figures/31_confusion_matrices_by_policy.png" alt="Errores según política de decisión" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.<br/><b>Qué aprendimos:</b> Un mismo clasificador puede producir decisiones muy distintas según la política.<br/><b>Límite:</b> No se deben comparar matrices sin especificar su regla de umbral.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Confiabilidad de las probabilidades

<div class="fig-hero">
  <img src="../../outputs/figures/32_model_reliability_comparison.png" alt="Confiabilidad de las probabilidades" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.<br/><b>Qué aprendimos:</b> Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.<br/><b>Límite:</b> Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Calibración e incertidumbre

<div class="fig-hero">
  <img src="../../outputs/figures/33_calibration_with_wilson_intervals.png" alt="Calibración e incertidumbre" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.<br/><b>Qué aprendimos:</b> Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.<br/><b>Límite:</b> Los intervalos son descriptivos y dependen del particionado de riesgo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento por canal

<div class="fig-hero">
  <img src="../../outputs/figures/34_subgroups_channel.png" alt="Rendimiento por canal" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se evaluaron métricas OOF desagregadas por canal de transacción.<br/><b>Qué aprendimos:</b> La calidad global puede esconder subgrupos con menos capacidad discriminativa.<br/><b>Límite:</b> Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento por categoría de comercio

<div class="fig-hero">
  <img src="../../outputs/figures/34_subgroups_merchant_category.png" alt="Rendimiento por categoría de comercio" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se comparó ROC AUC y AP por categorías de comercio.<br/><b>Qué aprendimos:</b> Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.<br/><b>Límite:</b> La tasa base difiere entre grupos y afecta de manera importante a AP.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">H · EXPLICABILIDAD</div>

## Interpretabilidad: distinguir asociación y explicación



<div class="marp-cards"><div class="marp-card"><b>Coeficientes</b><p>Signo y magnitud dependen de la codificación y del escalamiento.</p></div><div class="marp-card"><b>Importancia interna</b><p>Gini/ganancia de árbol pueden favorecer variables con características distintas.</p></div><div class="marp-card"><b>Dependencia parcial</b><p>Efecto medio al perturbar una variable dentro de un modelo ya entrenado.</p></div><div class="marp-card"><b>Límite</b><p>Son descripciones predictivas; no identifican causalidad.</p></div></div>

<div class="marp-message">Comparar modelos heterogéneos requiere cuidado con las escalas de importancia.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">H · DECISIÓN</div>

## Selección final: regla programada y evidencia pendiente



<div class="marp-cards"><div class="marp-card"><b>Comparar</b><p>Calcular ROC AUC pooled OOF para cada candidato y cuatro blends.</p></div><div class="marp-card"><b>Elegir</b><p>El notebook selecciona la fila de mayor ROC AUC en ensemble_metrics.csv.</p></div><div class="marp-card"><b>Exportar</b><p>Genera submission.csv con id e is_fraud en el orden exacto del test.</p></div><div class="marp-card"><b>Verificar</b><p>Sin ensemble_metrics.csv ni run_manifest.json del full run no afirmar el ganador numérico exacto.</p></div></div>

<div class="marp-message">La selección usada para generar Kaggle es auditable, pero la estimación seleccionada es optimista.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Coincidencia en el 1% de mayor riesgo

<div class="fig-hero">
  <img src="../../outputs/figures/35_top_risk_set_overlap.png" alt="Coincidencia en el 1% de mayor riesgo" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.<br/><b>Qué aprendimos:</b> Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.<br/><b>Límite:</b> La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Importancia de características

<div class="fig-hero">
  <img src="../../outputs/figures/36_model_feature_importance.png" alt="Importancia de características" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon coeficientes transformados de logit e importancias internas de árboles.<br/><b>Qué aprendimos:</b> Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.<br/><b>Límite:</b> Importancia no significa causalidad y es difícil de comparar entre modelos.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Dependencia parcial: efectos aprendidos

<div class="fig-hero">
  <img src="../../outputs/figures/37_partial_dependence_models.png" alt="Dependencia parcial: efectos aprendidos" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.<br/><b>Qué aprendimos:</b> Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.<br/><b>Límite:</b> Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Cómo cambia el riesgo con el blend

<div class="fig-hero">
  <img src="../../outputs/figures/38_blend_vs_single_predictions.png" alt="Cómo cambia el riesgo con el blend" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se comparó la probabilidad del mejor individuo con la combinación seleccionada.<br/><b>Qué aprendimos:</b> El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.<br/><b>Límite:</b> Menor dispersión no es sinónimo de mejor discriminación ni calibración.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Control de predicciones para Kaggle

<div class="fig-hero">
  <img src="../../outputs/figures/39_submission_probability_sanity.png" alt="Control de predicciones para Kaggle" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.<br/><b>Qué aprendimos:</b> La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.<br/><b>Límite:</b> No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Exploración de hiperparámetros

<div class="fig-hero">
  <img src="../../outputs/figures/40_hyperparameter_effects.png" alt="Exploración de hiperparámetros" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon configuraciones y su puntuación agregada en validación.<br/><b>Qué aprendimos:</b> La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.<br/><b>Límite:</b> Variar varios parámetros a la vez dificulta atribuciones causales.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Estabilidad del ROC AUC por fold

<div class="fig-hero">
  <img src="../../outputs/figures/41_fold_auc_heatmap.png" alt="Estabilidad del ROC AUC por fold" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se representó cada candidato contra las cinco particiones de validación.<br/><b>Qué aprendimos:</b> La comparación pareada muestra si las mejoras persisten o dependen de un fold.<br/><b>Límite:</b> Cinco folds no son cinco experimentos independientes para inferencias fuertes.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Espacio completo de GridSearchCV

<div class="fig-hero">
  <img src="../../outputs/figures/42_gridsearch_full_parameter_space.png" alt="Espacio completo de GridSearchCV" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se registró cada combinación de profundidad, learning rate y regularización explorada.<br/><b>Qué aprendimos:</b> La visualización muestra sensibilidad del ajuste dentro de los folds internos.<br/><b>Límite:</b> El mejor valor interno no garantiza mejora en el fold externo.</div>

---

<!-- _class: marp-figure -->
<div class="marp-tag">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Efecto del ajuste sobre folds externos

<div class="fig-hero">
  <img src="../../outputs/figures/43_nested_gridsearch_outer_results.png" alt="Efecto del ajuste sobre folds externos" />
</div>

<div class="marp-fig-notes"><b>Qué se hizo:</b> Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.<br/><b>Qué aprendimos:</b> La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.<br/><b>Límite:</b> Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">I · CONCLUSIONES</div>

## Qué concluye el proyecto y qué no



<div class="marp-cards"><div class="marp-card"><b>Sí: comparación sistemática</b><p>Muchos métodos y transformaciones juzgados con el mismo protocolo estratificado.</p></div><div class="marp-card"><b>Sí: EDA con hipótesis</b><p>No linealidad, interacciones, anomalías y grupos merecen análisis.</p></div><div class="marp-card"><b>No: superioridad universal</b><p>Un modelo complejo o un blend no gana por definición.</p></div><div class="marp-card"><b>No: inferencia independiente</b><p>El ganador fue seleccionado con resultados OOF usados también para estimar calidad.</p></div></div>

<div class="marp-message">El hallazgo más transferible es el procedimiento de evaluación reproducible.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">I · CONCLUSIONES</div>

## Limitaciones de los resultados disponibles



<div class="marp-cards"><div class="marp-card"><b>Proveniencia de figuras</b><p>Se recibieron 44 PNG; los CSV numéricos de los folds del full run no acompañaban las imágenes.</p></div><div class="marp-card"><b>Optimismo de selección</b><p>Elegir la mejor combinación y reportar su OOF en el mismo conjunto sesga al alza.</p></div><div class="marp-card"><b>Cambio temporal</b><p>No se verificó una prueba temporal ni independencia por cuenta/tarjeta.</p></div><div class="marp-card"><b>GPU y tiempos</b><p>El hardware modifica costo; no comparar tiempos sin informar dispositivo real.</p></div></div>

<div class="marp-message">Las diapositivas describen los gráficos existentes, no inventan un resultado de leaderboard.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">I · CONCLUSIONES</div>

## Trabajo posterior para cerrar la selección



<div class="marp-cards"><div class="marp-card"><b>Reproducir</b><p>Confirmar FAST_DEV_RUN=False y guardar run_manifest.json/ensemble_metrics.csv.</p></div><div class="marp-card"><b>Validar</b><p>Usar holdout intacto o nested CV para evaluación final y diferencias pequeñas.</p></div><div class="marp-card"><b>Calibrar</b><p>Evaluar probabilidades después de elegir el ranking final.</p></div><div class="marp-card"><b>Entregar</b><p>Verificar CSV, versionar artefactos y presentar limitaciones transparentemente.</p></div></div>

<div class="marp-message">Estadística rigurosa = buenos modelos + trazabilidad + afirmaciones proporcionadas.</div>

---

<!-- _class: marp-content -->
<div class="marp-tag">FIN</div>

# Conclusión general

No gana el modelo con más componentes; gana la propuesta que resiste una evaluación transparente.

**EDA → hipótesis → modelos → CV → búsqueda → ensemble → decisión con incertidumbre.**
