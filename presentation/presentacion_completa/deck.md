---
marp: true
theme: fraud-whitegrid
size: 16:9
paginate: true
math: mathjax
transition: fade
footer: 'LDS1071 · Predicción de fraude'
title: 'Predicción de fraude · presentación técnica completa'
---

<!-- _class: cover -->
<div class="eyebrow">PRESENTACIÓN TÉCNICA EN ESPAÑOL</div>

# Predicción de fraude con tarjetas: el proceso completo

EDA · modelos lineales y árboles · 5-fold CV · cuatro ensambles · resultado final

<div class="thesis">Se documentan la comparación completa de 19 candidatos y el segundo experimento con modelos guardados.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · DEFINICIÓN</div>

## Qué problema resolvemos y qué entregamos

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Entrada X</h3><p>24 predictores numéricos, categóricos y booleanos; el identificador id se excluye.</p></div><div class="point"><h3>Objetivo Y</h3><p>Variable binaria is_fraud, con prevalencia aproximada de 1.67%.</p></div><div class="point"><h3>Salida</h3><p>Una probabilidad o score de fraude para cada fila del test.</p></div><div class="point"><h3>Evaluación</h3><p>Kaggle usa el área bajo la curva ROC; AP/calibración explican otros aspectos.</p></div></div>
<div class="takeaway">Un buen score ordena; una buena probabilidad también necesita calibración.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · DEFINICIÓN</div>

## Datos y desafío estadístico

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Tamaño</h3><p>699,960 filas de entrenamiento; 11,689 casos de fraude.</p></div><div class="point"><h3>Clases</h3><p>688,271 legítimas; ~1.67% positivas.</p></div><div class="point"><h3>Validez</h3><p>No se observaron datos faltantes en entrenamiento; el id no entra al modelo.</p></div><div class="point"><h3>Cuidado</h3><p>La exactitud puede ser alta prediciendo todo legítimo: preferir ROC AUC/AP.</p></div></div>
<div class="takeaway">Fraude raro ≠ necesariamente anomalía aislada.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · DEFINICIÓN</div>

## Métricas: cada una responde otra pregunta

<p class="lead"></p>

$$\mathrm{AUC}=P\!\left(s(X^+)>s(X^-)\right)$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>ROC AUC</h3><p>Probabilidad de que un positivo reciba mayor score que un negativo.</p></div><div class="point"><h3>Average precision</h3><p>Resume precisión vs recobrado; especialmente informativa con una clase rara.</p></div><div class="point"><h3>Log loss / Brier</h3><p>Evalúan calidad de probabilidades, no sólo ranking.</p></div><div class="point"><h3>Top-k y lift</h3><p>Miden cuántos fraudes se capturan al revisar sólo cierta fracción.</p></div></div>
<div class="takeaway">La métrica oficial fija el objetivo; las métricas auxiliares previenen conclusiones incompletas.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · MÉTODO</div>

## Diseño experimental: preparación y comparación

<p class="lead">Primera fase: desde las variables originales hasta un conjunto comparable de modelos.</p>


<div class="points"><div class="point"><h3>01</h3><p>Revisar tipos, distribución, faltantes y relaciones.</p></div><div class="point"><h3>02</h3><p>Diagnosticar no linealidades, interacciones y anomalías.</p></div><div class="point"><h3>03</h3><p>Preparar pipelines sin fuga de información.</p></div><div class="point"><h3>04</h3><p>Comparar familias y configuraciones en 5 folds.</p></div></div>
<div class="takeaway">Las primeras decisiones fijan qué se aprende y cómo se evalúa sin fuga de información.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · MÉTODO</div>

## Diseño experimental: selección y diagnóstico

<p class="lead">Segunda fase: ajustes internos, comparación de ensambles y seguimiento de resultados.</p>


<div class="points"><div class="point"><h3>05</h3><p>Afinar XGBoost/CatBoost con búsqueda interna.</p></div><div class="point"><h3>06</h3><p>Evaluar blends y corrección de log-odds.</p></div><div class="point"><h3>07</h3><p>Elegir estrategia OOF y preparar archivo Kaggle.</p></div></div>
<div class="takeaway">El criterio decisivo es la ROC AUC OOF, complementada por métricas de probabilidad e incertidumbre.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">A · MÉTODO</div>

## Validación cruzada sin data leakage

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>5 folds estratificados</h3><p>Cada fold conserva aproximadamente la proporción de fraude.</p></div><div class="point"><h3>Pipeline</h3><p>Imputación, escalado, one-hot, splines y PCA se ajustan sólo con train interno.</p></div><div class="point"><h3>OOF</h3><p>Cada fila obtiene una predicción de un modelo que nunca entrenó con esa fila.</p></div><div class="point"><h3>Selección</h3><p>Elegir el máximo en las mismas predicciones OOF causa cierto optimismo; un holdout posterior lo reduce.</p></div></div>
<div class="takeaway">El CV permite comparar modelos con exactamente los mismos folds.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">B · ANÁLISIS EXPLORATORIO</div>

## ¿Por qué explorar antes de modelar?

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Calidad</h3><p>Detectar valores faltantes, duplicados potenciales y categorías raras.</p></div><div class="point"><h3>Geometría</h3><p>Identificar colas, cambios de escala, dependencias y separabilidad.</p></div><div class="point"><h3>Hipótesis</h3><p>Decidir si una frontera lineal puede ser razonable o es necesario introducir no linealidad.</p></div><div class="point"><h3>Precaución</h3><p>Las asociaciones marginales no prueban efectos ajustados ni causalidad.</p></div></div>
<div class="takeaway">Las figuras de EDA ayudan a formular hipótesis, no reemplazan la validación cruzada.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Balance de clases y completitud

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/01_target_and_missingness.png" alt="Balance de clases y completitud"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.</p><h3>RESULTADO</h3><p>La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.</p><h3>ALCANCE</h3><p>El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Distribuciones numéricas

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/02_numeric_distributions.png" alt="Distribuciones numéricas"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.</p><h3>RESULTADO</h3><p>Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.</p><h3>ALCANCE</h3><p>Una distribución sesgada no determina por sí sola utilidad predictiva.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Distribuciones según la clase

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/03_class_conditional_densities.png" alt="Distribuciones según la clase"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.</p><h3>RESULTADO</h3><p>La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.</p><h3>ALCANCE</h3><p>Las densidades normalizadas por clase no representan la prevalencia real de fraude.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Correlaciones de Pearson y Spearman

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/04_pearson_spearman_correlations.png" alt="Correlaciones de Pearson y Spearman"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).</p><h3>RESULTADO</h3><p>Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.</p><h3>ALCANCE</h3><p>Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Riesgo por categorías

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/05_categorical_risks.png" alt="Riesgo por categorías"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se estimó la tasa observada de fraude por categoría y su soporte muestral.</p><h3>RESULTADO</h3><p>Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.</p><h3>ALCANCE</h3><p>Categorías con pocas observaciones pueden producir tasas muy inestables.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">B · DISTRIBUCIONES Y ASOCIACIONES</div>

## Indicadores booleanos: frecuencia y riesgo

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/06_flag_prevalence_vs_fraud.png" alt="Indicadores booleanos: frecuencia y riesgo"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.</p><h3>RESULTADO</h3><p>Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.</p><h3>ALCANCE</h3><p>La asociación marginal puede desaparecer al ajustar por otros predictores.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">C · NO LINEALIDAD</div>

## De correlaciones a relaciones no lineales

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Problema</h3><p>Una correlación baja no descarta una relación en U ni interacciones entre predictores.</p></div><div class="point"><h3>Herramienta</h3><p>Binning cuantílico de variables, cruce de rangos y tasas condicionadas.</p></div><div class="point"><h3>Modelo lineal</h3><p>La regresión logística es lineal en βᵀx, no en la probabilidad.</p></div><div class="point"><h3>Alternativas</h3><p>Splines, árboles, boosted trees y transformación de variables.</p></div></div>
<div class="takeaway">El EDA motivó candidatos adicionales; su valor se decide con CV.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">C · PATRONES Y ANOMALÍAS</div>

## No linealidad de las tasas de fraude

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/07_nonlinear_binned_fraud_rates.png" alt="No linealidad de las tasas de fraude"/></div><div class="explanation"><h3>MÉTODO</h3><p>Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.</p><h3>RESULTADO</h3><p>Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.</p><h3>ALCANCE</h3><p>El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">C · PATRONES Y ANOMALÍAS</div>

## Patrones temporales de fraude

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/08_time_patterns.png" alt="Patrones temporales de fraude"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se analizaron tasas por hora, día y otras variables temporales disponibles.</p><h3>RESULTADO</h3><p>Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.</p><h3>ALCANCE</h3><p>La agregación no prueba estabilidad futura ni sustituye una validación temporal.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">C · PATRONES Y ANOMALÍAS</div>

## Interacciones entre variables numéricas

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/09_bivariate_interaction_heatmaps.png" alt="Interacciones entre variables numéricas"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.</p><h3>RESULTADO</h3><p>Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.</p><h3>ALCANCE</h3><p>Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">C · PATRONES Y ANOMALÍAS</div>

## Valores extremos: criterio IQR

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/10_univariate_outliers.png" alt="Valores extremos: criterio IQR"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.</p><h3>RESULTADO</h3><p>Los extremos pueden ser transacciones válidas y contener señal de fraude.</p><h3>ALCANCE</h3><p>Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">C · PATRONES Y ANOMALÍAS</div>

## Anomalías con Isolation Forest

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/11_isolation_forest_anomaly_diagnostics.png" alt="Anomalías con Isolation Forest"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.</p><h3>RESULTADO</h3><p>El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.</p><h3>ALCANCE</h3><p>No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">C · ANOMALÍAS</div>

## Anomalía, outlier y fraude: tres conceptos

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Outlier</h3><p>Observación extrema según una variable y una regla estadística.</p></div><div class="point"><h3>Anomalía</h3><p>Patrón multivariante infrecuente, sin usar etiquetas.</p></div><div class="point"><h3>Fraude</h3><p>Resultado etiquetado que puede ser típico o atípico.</p></div><div class="point"><h3>Decisión EDA</h3><p>No borrar transacciones extremas automáticamente; compararlas descriptivamente.</p></div></div>
<div class="takeaway">Eliminar colas puede destruir justamente la señal que queremos detectar.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · PREPROCESAMIENTO</div>

## Pipelines de modelos: decisiones concretas

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Regresión logística</h3><p>Estandarización numérica, codificación de categorías y regularización L2.</p></div><div class="point"><h3>Logit con splines</h3><p>SplineTransformer para importe, velocidad y riesgo del comercio.</p></div><div class="point"><h3>Árboles</h3><p>Random forest y XGBoost aprenden cortes; no exigir PCA.</p></div><div class="point"><h3>CatBoost</h3><p>Procesamiento nativo de categorías, con imputación y GPU opcional.</p></div></div>
<div class="takeaway">La transformación se ajusta dentro del fold de entrenamiento.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · DIMENSIONALIDAD</div>

## SVD y PCA: por qué se probaron

<p class="lead"></p>

$$Z=U\Sigma V^\top$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Factorización</h3><p>La matriz centrada se descompone en vectores singulares y valores singulares.</p></div><div class="point"><h3>Truncamiento</h3><p>Conservar el menor número de componentes cuya varianza acumulada alcance el 90%.</p></div><div class="point"><h3>Hipótesis</h3><p>Reducir ruido/colinealidad puede estabilizar un modelo lineal.</p></div><div class="point"><h3>Contraargumento</h3><p>Una dirección de baja varianza puede predecir muy bien la etiqueta.</p></div></div>
<div class="takeaway">Por eso PCA es candidato experimental, no paso obligatorio.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · LÍNEA BASE</div>

## ¿Por qué regresión logística?

<p class="lead"></p>

$$\hat p(x)=\frac{1}{1+\exp[-(\beta_0+\beta^\top x)]}$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Modelo</h3><p>La función sigmoide transforma la combinación lineal en una probabilidad.</p></div><div class="point"><h3>Eficiencia</h3><p>Comparación rápida con un dataset grande.</p></div><div class="point"><h3>Interpretabilidad</h3><p>Coeficientes describen cambios en log-odds, dados otros predictores.</p></div><div class="point"><h3>Diagnóstico</h3><p>Una forma funcional simple es una referencia para medir ganancia de modelos complejos.</p></div></div>
<div class="takeaway">L2 ayuda ante correlaciones, pero no “corrige” especificación no lineal.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · AUDITORÍA</div>

## ¿Se satisfacen los supuestos de logit?

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Se cumple</h3><p>La respuesta es binaria; hay suficientes fraudes para ajustar el modelo.</p></div><div class="point"><h3>En revisión</h3><p>Linealidad de log-odds, separación completa multivariante y dependencia entre operaciones.</p></div><div class="point"><h3>Se diagnostica</h3><p>Colinealidad, convergencia, especificación con splines y calibración OOF.</p></div><div class="point"><h3>No se requiere</h3><p>Normalidad de predictores ni homocedasticidad de errores Bernoulli.</p></div></div>
<div class="takeaway">La utilidad predictiva no equivale a validez causal de coeficientes.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · ESPECIFICACIÓN</div>

## ¿Qué aporta el spline logístico?

<p class="lead"></p>

$$f(x)=\beta_0+\sum_{k=1}^{K}\gamma_k B_k(x)$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Modelo original</h3><p>La especificación original contiene solamente términos lineales aditivos.</p></div><div class="point"><h3>Modelo extendido</h3><p>La especificación ampliada sustituye términos lineales por una combinación de funciones base spline.</p></div><div class="point"><h3>Ventaja</h3><p>Curvatura interpretable y continua sin cambiar la familia logística.</p></div><div class="point"><h3>Control</h3><p>Colocar los splines dentro del Pipeline y validar con folds idénticos.</p></div></div>
<div class="takeaway">Probar una no linealidad específica es más informativo que añadir complejidad indiscriminada.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · MODELOS</div>

## Random forest: bagging dentro de una familia

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Idea</h3><p>Muchos árboles ajustados sobre muestras y subconjuntos aleatorios de variables.</p></div><div class="point"><h3>Promedio</h3><p>La agregación de árboles reduce varianza frente a un árbol individual.</p></div><div class="point"><h3>Fortaleza</h3><p>Aprende umbrales e interacciones sin ecuaciones de spline explícitas.</p></div><div class="point"><h3>Costo</h3><p>Puede consumir memoria y no siempre calibra probabilidades óptimamente.</p></div></div>
<div class="takeaway">Este sí es un mecanismo tipo bagging, a diferencia del blend posterior.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · MODELOS</div>

## XGBoost: árboles que corrigen errores

<p class="lead"></p>

$$f_m(x)=f_{m-1}(x)+\eta h_m(x)$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Mecanismo</h3><p>Se agregan árboles secuenciales guiados por el gradiente de la pérdida.</p></div><div class="point"><h3>Regularización</h3><p>Profundidad, learning rate, min_child_weight y número de árboles.</p></div><div class="point"><h3>Hipótesis</h3><p>Capturar no linealidad/interacciones omitidas por logit.</p></div><div class="point"><h3>Hardware</h3><p>tree_method=&quot;hist&quot;; CUDA si la prueba real detecta GPU, si no CPU.</p></div></div>
<div class="takeaway">Se conserva el mismo esquema de evaluación, sin favorecer a un algoritmo por hardware.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · MODELOS</div>

## CatBoost: otra forma de boosting

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Categorías</h3><p>Admite variables categóricas de forma nativa; reduce la necesidad de one-hot.</p></div><div class="point"><h3>Control de complejidad</h3><p>depth, learning_rate, l2_leaf_reg, iterations.</p></div><div class="point"><h3>Comparación</h3><p>Candidatos fijos y variantes ajustadas con GridSearchCV.</p></div><div class="point"><h3>Hardware</h3><p>GPU NVIDIA cuando está disponible; fallback explícito a CPU.</p></div></div>
<div class="takeaway">Diferentes sesgos inductivos merecen comparación directa, no suposiciones de superioridad.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">D · COMPARACIÓN</div>

## Diseño de candidatos e hiperparámetros

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Conjunto</h3><p>19 especificaciones propuestas, incluyendo 2 variantes con búsqueda interna.</p></div><div class="point"><h3>Evaluación externa</h3><p>19 × 5 = 95 evaluaciones de folds externas.</p></div><div class="point"><h3>Búsqueda interna</h3><p>2 familias × 5 folds × 8 configuraciones × 3 folds = 240 ajustes internos.</p></div><div class="point"><h3>Costo total</h3><p>Además del refit de las mejores configuraciones y de dos etapas en corrección del logit con XGBoost.</p></div></div>
<div class="takeaway">En modo rápido el notebook reduce tanto filas como hiperparámetros; no mezclar esos scores con el full run.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Comparación de candidatos en cinco folds

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/12_candidate_scores_and_folds.png" alt="Comparación de candidatos en cinco folds"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon ROC AUC out-of-fold por candidato y por partición.</p><h3>RESULTADO</h3><p>El desempeño medio debe juzgarse junto con su variación entre particiones y familias.</p><h3>ALCANCE</h3><p>La elección del máximo dentro del mismo CV introduce optimismo de selección.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Correlación entre modelos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/13_oof_prediction_correlations.png" alt="Correlación entre modelos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon los vectores de probabilidades OOF de todos los candidatos.</p><h3>RESULTADO</h3><p>Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.</p><h3>ALCANCE</h3><p>Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Modelo individual frente a combinaciones

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/14_ensemble_comparisons.png" alt="Modelo individual frente a combinaciones"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.</p><h3>RESULTADO</h3><p>Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.</p><h3>ALCANCE</h3><p>El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Curvas ROC y precisión–recobrado

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/15_oof_roc_pr_curves.png" alt="Curvas ROC y precisión–recobrado"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.</p><h3>RESULTADO</h3><p>ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.</p><h3>ALCANCE</h3><p>Ninguna curva fija por sí sola un umbral operativo.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## SVD/PCA: 90% de varianza

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/16_pca_explained_variance.png" alt="SVD/PCA: 90% de varianza"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.</p><h3>RESULTADO</h3><p>La reducción es una alternativa de representación, no una mejora predictiva garantizada.</p><h3>ALCANCE</h3><p>La varianza de X y la información predictiva sobre Y son objetivos distintos.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Supuestos logísticos y posibles cambios

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/17_assumptions_vif_and_feature_shift.png" alt="Supuestos logísticos y posibles cambios"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.</p><h3>RESULTADO</h3><p>Es necesario separar problemas de especificación, dependencia y cambios de distribución.</p><h3>ALCANCE</h3><p>Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Diagnóstico de la regresión logística

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/18_oof_logistic_assumption_checks.png" alt="Diagnóstico de la regresión logística"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.</p><h3>RESULTADO</h3><p>Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.</p><h3>ALCANCE</h3><p>Predictores normales y homocedasticidad NO son supuestos requeridos para logit.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">D · CANDIDATOS Y DIAGNÓSTICOS</div>

## Corregir el logit con XGBoost

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/19_logistic_offset_boosting_diagnostics.png" alt="Corregir el logit con XGBoost"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.</p><h3>RESULTADO</h3><p>Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.</p><h3>ALCANCE</h3><p>No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">E · ENSEMBLES</div>

## Blending y bagging: cómo evolucionó la idea inicial

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Propuesta</h3><p>Conservar todos los modelos en vez de quedarse solamente con el ganador.</p></div><div class="point"><h3>Realización</h3><p>Promedio equiponderado de probabilidades OOF y de prueba.</p></div><div class="point"><h3>Cuatro estrategias</h3><p>Mejor individual; todos; top 3; mejor de cada familia.</p></div><div class="point"><h3>Hallazgo metodológico</h3><p>Más modelos no implica mejor AUC si sus errores son correlacionados.</p></div></div>
<div class="takeaway">Término preciso de la realización: blending entre familias heterogéneas.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">E · ENSEMBLES</div>

## Stacking con random forest: segundo experimento

<p class="lead">El stacking sí se implementó posteriormente en un segundo notebook, utilizando sólo probabilidades de modelos base.</p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Matriz de nivel 2</h3><p>Se concatenaron 17 columnas de probabilidades OOF de candidatos ya entrenados.</p></div><div class="point"><h3>Meta-modelo</h3><p>RandomForestClassifier: 280 árboles, max_depth=6, min_samples_leaf=75.</p></div><div class="point"><h3>Evaluación</h3><p>Se creó otro esquema de cinco folds para generar predicciones meta-OOF.</p></div><div class="point"><h3>Restricción</h3><p>No fue nested CV completo: los modelos base usaron etiquetas de otros folds meta en entrenamiento.</p></div></div>
<div class="takeaway">Resultado OOF del stacking: ROC AUC 0.945747; average precision 0.506383.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">E · ENSEMBLES</div>

## Logit + booster de corrección en escala logit

<p class="lead"></p>

$$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Primera etapa</h3><p>Se ajustan los coeficientes de la regresión logística y se mantienen fijos en la segunda etapa.</p></div><div class="point"><h3>Segunda etapa</h3><p>XGBoost recibe el logit como condición inicial mediante `base_margin` y aprende correcciones.</p></div><div class="point"><h3>Predicción final</h3><p>La sigmoide transforma la suma de logit inicial y corrección en una probabilidad.</p></div><div class="point"><h3>Riesgo</h3><p>La segunda etapa puede corregir estructura o sobreajustar ruido; comparar en OOF.</p></div></div>
<div class="takeaway">Es una composición aditiva sobre el logit, NO stacking con meta-logit.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">E · ENSEMBLES</div>

## Por qué conservar modelos que no ganaron

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Reproducibilidad</h3><p>Cada configuración tiene métricas, folds y predicciones guardadas.</p></div><div class="point"><h3>Diversidad</h3><p>Un candidato inferior puede complementar a otro si comete errores distintos.</p></div><div class="point"><h3>Costo</h3><p>Guardar todos permite estudiar correlación y solapamiento de casos top-risk.</p></div><div class="point"><h3>Selección</h3><p>Elegir blends previamente definidos; no buscar combinaciones infinitas sin validación.</p></div></div>
<div class="takeaway">La selección sobre OOF es exploratoria y no representa una evaluación completamente intacta.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">F · EXPLORACIÓN AMPLIADA</div>

## EDA extendido: qué más investigamos

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Discriminación univariante</h3><p>AUC por predictor para priorizar explicaciones.</p></div><div class="point"><h3>Subgrupos</h3><p>Interacciones entre banderas, categorías y ventanas temporales.</p></div><div class="point"><h3>Geometría</h3><p>ECDF y dispersión de clases en parejas de variables.</p></div><div class="point"><h3>Distribución del test</h3><p>Buscar desplazamientos sin conocer las etiquetas de la prueba.</p></div></div>
<div class="takeaway">Cada gráfico sirve para generar preguntas, no para ajustar modelos sobre el test.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Valor discriminativo de cada variable

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/20_univariate_feature_discrimination.png" alt="Valor discriminativo de cada variable"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se estimó el AUC de predictores aislados y se compararon señales univariantes.</p><h3>RESULTADO</h3><p>El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.</p><h3>ALCANCE</h3><p>Un AUC univariante alto no asegura contribución incremental.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Distribuciones acumuladas por clase

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/21_class_conditional_ecdfs.png" alt="Distribuciones acumuladas por clase"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.</p><h3>RESULTADO</h3><p>Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.</p><h3>ALCANCE</h3><p>Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Categorías × indicadores booleanos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/22_categorical_flag_interactions.png" alt="Categorías × indicadores booleanos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.</p><h3>RESULTADO</h3><p>Una misma bandera puede tener distinta asociación con el fraude según su contexto.</p><h3>ALCANCE</h3><p>En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Mapa de riesgo por día y hora

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/23_weekly_hourly_fraud_surface.png" alt="Mapa de riesgo por día y hora"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.</p><h3>RESULTADO</h3><p>Puede haber concentraciones temporales no captadas por términos horarios aislados.</p><h3>ALCANCE</h3><p>La composición de transacciones puede explicar parte del efecto observado.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Geometría bivariante por clase

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/24_pairwise_class_geometry.png" alt="Geometría bivariante por clase"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.</p><h3>RESULTADO</h3><p>Los patrones de separación multivariada justifican no depender solo de un predictor.</p><h3>ALCANCE</h3><p>Las muestras de visualización no deben confundirse con la distribución completa.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">F · EDA EXTENDIDO</div>

## Comparación entrenamiento–prueba

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/25_train_test_ecdf_shift.png" alt="Comparación entrenamiento–prueba"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.</p><h3>RESULTADO</h3><p>Permite detectar cambios marginales antes de enviar predicciones a Kaggle.</p><h3>ALCANCE</h3><p>Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">G · EVALUACIÓN</div>

## De la métrica de Kaggle a una operación real

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Competencia</h3><p>Optimizar ROC AUC; ranking entre pares de clases.</p></div><div class="point"><h3>Evento raro</h3><p>Registrar average precision, precisión y recall.</p></div><div class="point"><h3>Probabilidades</h3><p>Inspeccionar Brier, log loss y curvas de confiabilidad.</p></div><div class="point"><h3>Política</h3><p>Medir captura y errores al revisar top 1%, 5% o 10%.</p></div></div>
<div class="takeaway">No hay una única métrica que responda todos los usos.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">G · EVALUACIÓN</div>

## Validación de umbrales y presupuesto

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Umbral fijo</h3><p>Un umbral de 0.5 es sencillo, pero arbitrario ante una prevalencia de fraude baja.</p></div><div class="point"><h3>Top k</h3><p>Revisar el k% con mayor puntuación: umbral adaptado a capacidad.</p></div><div class="point"><h3>Ganancia</h3><p>Comparar detecciones acumuladas con selección aleatoria.</p></div><div class="point"><h3>Faltan costos</h3><p>Para optimizar el umbral de negocio se necesitan costos de falsos positivos/negativos.</p></div></div>
<div class="takeaway">Estas políticas son evaluadas; no deben confundirse con entrenamiento distinto.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Comparación con cuatro métricas

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/26_four_metric_model_scorecard.png" alt="Comparación con cuatro métricas"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.</p><h3>RESULTADO</h3><p>La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.</p><h3>ALCANCE</h3><p>Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento frente a costo computacional

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/27_performance_vs_training_time.png" alt="Rendimiento frente a costo computacional"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.</p><h3>RESULTADO</h3><p>Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.</p><h3>ALCANCE</h3><p>Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Distribuciones de riesgo predicho

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/28_oof_score_distributions.png" alt="Distribuciones de riesgo predicho"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.</p><h3>RESULTADO</h3><p>La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.</p><h3>ALCANCE</h3><p>Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Ganancia acumulada y lift

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/29_cumulative_gains_and_lift.png" alt="Ganancia acumulada y lift"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.</p><h3>RESULTADO</h3><p>La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.</p><h3>ALCANCE</h3><p>Las curvas no incluyen el costo real de las investigaciones o falsos positivos.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Precisión y recobrado con capacidad limitada

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/30_precision_recall_at_review_budget.png" alt="Precisión y recobrado con capacidad limitada"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.</p><h3>RESULTADO</h3><p>Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.</p><h3>ALCANCE</h3><p>La mejor fracción a revisar depende de costos externos ausentes del dataset.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Errores según política de decisión

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/31_confusion_matrices_by_policy.png" alt="Errores según política de decisión"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.</p><h3>RESULTADO</h3><p>Un mismo clasificador puede producir decisiones muy distintas según la política.</p><h3>ALCANCE</h3><p>No se deben comparar matrices sin especificar su regla de umbral.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Confiabilidad de las probabilidades

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/32_model_reliability_comparison.png" alt="Confiabilidad de las probabilidades"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.</p><h3>RESULTADO</h3><p>Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.</p><h3>ALCANCE</h3><p>Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Calibración e incertidumbre

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/33_calibration_with_wilson_intervals.png" alt="Calibración e incertidumbre"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.</p><h3>RESULTADO</h3><p>Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.</p><h3>ALCANCE</h3><p>Los intervalos son descriptivos y dependen del particionado de riesgo.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento por canal

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/34_subgroups_channel.png" alt="Rendimiento por canal"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se evaluaron métricas OOF desagregadas por canal de transacción.</p><h3>RESULTADO</h3><p>La calidad global puede esconder subgrupos con menos capacidad discriminativa.</p><h3>ALCANCE</h3><p>Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS</div>

## Rendimiento por categoría de comercio

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/34_subgroups_merchant_category.png" alt="Rendimiento por categoría de comercio"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó ROC AUC y AP por categorías de comercio.</p><h3>RESULTADO</h3><p>Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.</p><h3>ALCANCE</h3><p>La tasa base difiere entre grupos y afecta de manera importante a AP.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">H · EXPLICABILIDAD</div>

## Interpretabilidad: distinguir asociación y explicación

<p class="lead"></p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Coeficientes</h3><p>Signo y magnitud dependen de la codificación y del escalamiento.</p></div><div class="point"><h3>Importancia interna</h3><p>Gini/ganancia de árbol pueden favorecer variables con características distintas.</p></div><div class="point"><h3>Dependencia parcial</h3><p>Efecto medio al perturbar una variable dentro de un modelo ya entrenado.</p></div><div class="point"><h3>Límite</h3><p>Son descripciones predictivas; no identifican causalidad.</p></div></div>
<div class="takeaway">Comparar modelos heterogéneos requiere cuidado con las escalas de importancia.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">H · DECISIÓN</div>

## Cómo se cerró la comparación final

<p class="lead">Con la extensión de ensambles se compararon cinco vectores de predicciones OOF de 699,960 observaciones.</p>

<p class="context">En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra.</p>
<div class="points"><div class="point"><h3>Referencia individual</h3><p>XGBoost XGBoost individual (profundidad 5; tasa 0.05): ROC AUC 0.946120.</p></div><div class="point"><h3>Criterio</h3><p>Seleccionar el mayor ROC AUC pooled entre cuatro ensambles y el mejor individuo.</p></div><div class="point"><h3>Seleccionado</h3><p>Logit-offset xgb profundidad 3, learning rate 0.05: ROC AUC 0.946205.</p></div><div class="point"><h3>Incertidumbre</h3><p>La diferencia +0.000085 no demuestra superioridad fuera de muestra.</p></div></div>
<div class="takeaway">Ahora contamos con los CSV del experimento final; los valores no proceden de leer el ancho de barras.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Coincidencia en el 1% de mayor riesgo

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/35_top_risk_set_overlap.png" alt="Coincidencia en el 1% de mayor riesgo"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.</p><h3>RESULTADO</h3><p>Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.</p><h3>ALCANCE</h3><p>La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Importancia de características

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/36_model_feature_importance.png" alt="Importancia de características"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon coeficientes transformados de logit e importancias internas de árboles.</p><h3>RESULTADO</h3><p>Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.</p><h3>ALCANCE</h3><p>Importancia no significa causalidad y es difícil de comparar entre modelos.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Dependencia parcial: efectos aprendidos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/37_partial_dependence_models.png" alt="Dependencia parcial: efectos aprendidos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.</p><h3>RESULTADO</h3><p>Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.</p><h3>ALCANCE</h3><p>Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Cómo cambia el riesgo con el blend

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/38_blend_vs_single_predictions.png" alt="Cómo cambia el riesgo con el blend"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó la probabilidad del mejor individuo con la combinación seleccionada.</p><h3>RESULTADO</h3><p>El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.</p><h3>ALCANCE</h3><p>Menor dispersión no es sinónimo de mejor discriminación ni calibración.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Control de predicciones para Kaggle

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/39_submission_probability_sanity.png" alt="Control de predicciones para Kaggle"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.</p><h3>RESULTADO</h3><p>La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.</p><h3>ALCANCE</h3><p>No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Exploración de hiperparámetros

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/40_hyperparameter_effects.png" alt="Exploración de hiperparámetros"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon configuraciones y su puntuación agregada en validación.</p><h3>RESULTADO</h3><p>La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.</p><h3>ALCANCE</h3><p>Variar varios parámetros a la vez dificulta atribuciones causales.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Estabilidad del ROC AUC por fold

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/41_fold_auc_heatmap.png" alt="Estabilidad del ROC AUC por fold"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se representó cada candidato contra las cinco particiones de validación.</p><h3>RESULTADO</h3><p>La comparación pareada muestra si las mejoras persisten o dependen de un fold.</p><h3>ALCANCE</h3><p>Cinco folds no son cinco experimentos independientes para inferencias fuertes.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Espacio completo de GridSearchCV

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/42_gridsearch_full_parameter_space.png" alt="Espacio completo de GridSearchCV"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se registró cada combinación de profundidad, learning rate y regularización explorada.</p><h3>RESULTADO</h3><p>La visualización muestra sensibilidad del ajuste dentro de los folds internos.</p><h3>ALCANCE</h3><p>La búsqueda se ajustó en los folds internos. Los resultados exactos del XGBoost de grid sólo se podrán comparar con offset al recuperar el vector OOF original.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">H · INTERPRETACIÓN, BLENDING Y TUNING</div>

## Efecto del ajuste sobre folds externos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/43_nested_gridsearch_outer_results.png" alt="Efecto del ajuste sobre folds externos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.</p><h3>RESULTADO</h3><p>La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.</p><h3>ALCANCE</h3><p>La búsqueda se ajustó en los folds internos. Los resultados exactos del XGBoost de grid sólo se podrán comparar con offset al recuperar el vector OOF original.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## Segundo notebook: aprovechar los modelos ya entrenados

<p class="lead">La extensión reutilizó all_candidate_predictions.npz y los cinco modelos logísticos guardados.</p>


<div class="points"><div class="point"><h3>Predicciones base</h3><p>19 candidatos evaluados con cinco folds en el entrenamiento original.</p></div><div class="point"><h3>Archivos reutilizados</h3><p>OOF por candidato, probabilidades de test, métricas, manifiesto y modelos logísticos por fold.</p></div><div class="point"><h3>Entrenamiento nuevo</h3><p>Sólo XGBRegressor sobre residuos y RandomForestClassifier como meta-modelo.</p></div><div class="point"><h3>Salida</h3><p>five_way_comparison.csv, métricas por fold, gráficas y archivos de envío.</p></div></div>
<div class="takeaway">Se conservaron las comparaciones originales y se añadieron los ensambles sin repetir el entrenamiento más costoso.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## Referencia: el mejor modelo entrenado sin ensamble

<p class="lead">Se tomó el candidato con mayor ROC AUC OOF entre los modelos individuales, no el mejor modelo por intuición.</p>

<p class="context">La mejor referencia individual en los CSV es un XGBoost fijo. El modelo XGBoost con GridSearchCV fue evaluado en el notebook principal, pero el ZIP de ensambles no contiene sus predicciones para verificar su AUC exacta en esta nueva comparación.</p>
<div class="points"><div class="point"><h3>Identificador</h3><p>XGBoost individual (profundidad 5; tasa 0.05): XGBoost de profundidad 5 y learning rate 0.05.</p></div><div class="point"><h3>ROC AUC</h3><p>0.946120.</p></div><div class="point"><h3>Average precision</h3><p>0.503585.</p></div><div class="point"><h3>Log loss y Brier</h3><p>0.046003 y 0.011104, respectivamente.</p></div></div>
<div class="takeaway">Esta referencia permite medir el beneficio adicional de construir un segundo nivel de aprendizaje.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## Diseño final: cuatro ensambles frente al mejor individuo

<p class="lead">Las cinco estrategias se compararon en las mismas observaciones y con métricas calculadas sobre probabilidades OOF.</p>


<div class="points"><div class="point"><h3>E1 · Promedio</h3><p>Promedio sin pesos de los mejores candidatos por familia; no requiere ajuste adicional.</p></div><div class="point"><h3>E2 · Logit-offset</h3><p>XGBoost continúa desde los logits del modelo logístico con la pérdida de clasificación.</p></div><div class="point"><h3>E3 · Residuos</h3><p>XGBRegressor ajustado a y−p_logit; se suma la predicción residual y se recorta.</p></div><div class="point"><h3>E4 · Stacking RF</h3><p>Random forest entrenado sobre probabilidades OOF de 17 candidatos.</p></div></div>
<div class="takeaway">Bagging clásico, blending y stacking describen procedimientos distintos; aquí hay cuatro ensambles definidos.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## E1: promedio de probabilidades

<p class="lead">Se tomaron ocho modelos de familias distintas y se calculó el promedio simple de sus probabilidades.</p>

$$\hat p_{\mathrm{blend}}(x)=\frac{1}{8}\sum_{k=1}^{8}\hat p_k(x)$$


<div class="points"><div class="point"><h3>Definición</h3><p>Se calcula el promedio aritmético de las ocho probabilidades seleccionadas.</p></div><div class="point"><h3>ROC AUC</h3><p>0.943280 (−0.002840 frente al mejor individuo).</p></div><div class="point"><h3>Average precision</h3><p>0.500913.</p></div><div class="point"><h3>Resultado</h3><p>No mejoró el ranking; log loss 0.067322 y Brier 0.013587.</p></div></div>
<div class="takeaway">Mezclar predicciones correlacionadas puede reducir el contraste entre operaciones de alto y bajo riesgo.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## E2: boosting con logit como condición inicial

<p class="lead">En lugar de sustituir la respuesta por residuos, se proporciona a XGBoost un punto inicial específico por observación.</p>

$$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$


<div class="points"><div class="point"><h3>Primera etapa</h3><p>La primera etapa estima el logaritmo de las razones de probabilidad de fraude.</p></div><div class="point"><h3>Entrenamiento</h3><p>XGBoost parte de los logits iniciales y mantiene la etiqueta binaria en la pérdida logística.</p></div><div class="point"><h3>Corrección</h3><p>La probabilidad final se obtiene aplicando la sigmoide a la suma de ambas etapas.</p></div><div class="point"><h3>Resultado</h3><p>ROC AUC 0.946205; AP 0.507424; log loss 0.045798; Brier 0.011051.</p></div></div>
<div class="takeaway">El gradiente corresponde al error de probabilidad inicial; XGBoost también utiliza la curvatura de la pérdida.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## E3: XGBoost entrenado sobre residuos explícitos

<p class="lead">Se probó literalmente ajustar un segundo modelo a los errores de probabilidad de la regresión logística.</p>

$$\hat p(x)=\operatorname{clip}\!\left(\hat p_{\mathrm{LR}}(x)+g(x),0,1\right)$$


<div class="points"><div class="point"><h3>Objetivo</h3><p>La nueva respuesta es la diferencia entre la etiqueta observada y la probabilidad logística.</p></div><div class="point"><h3>Modelo corrector</h3><p>XGBRegressor con pérdida cuadrática sobre los residuos.</p></div><div class="point"><h3>Salida</h3><p>clip[p_LR(x)+g(x),0,1], para mantener una escala probabilística válida.</p></div><div class="point"><h3>Rendimiento</h3><p>ROC AUC 0.940241; AP 0.494046; log loss 0.047860.</p></div></div>
<div class="takeaway">La formulación residual tuvo peor ROC AUC que el modelo individual y que el corrección del logit con XGBoost.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## Por qué E2 y E3 no son equivalentes

<p class="lead">Ambos métodos parten de logit, pero cambian la función objetivo y la escala de la corrección.</p>


<div class="points"><div class="point"><h3>Offset: variable respuesta</h3><p>Se conserva una respuesta binaria, y el booster minimiza pérdida logística.</p></div><div class="point"><h3>Offset: escala</h3><p>Suma árboles al logit; la sigmoide asegura que 0&lt;p&lt;1.</p></div><div class="point"><h3>Residuo: variable respuesta</h3><p>La respuesta pasa a ser el error de probabilidad, y se minimiza su error cuadrático.</p></div><div class="point"><h3>Residuo: escala</h3><p>La corrección se suma a probabilidades y luego se trunca, alterando potencialmente la ordenación.</p></div></div>
<div class="takeaway">Los dos experimentos se realizaron; sólo corrección del logit con XGBoost mejoró marginalmente al mejor modelo individual.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## E4: stacking con random forest

<p class="lead">El bosque no recibe las 24 variables originales: aprende sobre las probabilidades producidas por 17 modelos.</p>

$$z_i=\left(\hat p_1(x_i),\ldots,\hat p_{17}(x_i)\right)$$


<div class="points"><div class="point"><h3>Matriz meta</h3><p>La matriz meta contiene 699,960 observaciones y 17 columnas de probabilidades fuera de fold.</p></div><div class="point"><h3>Modelo</h3><p>280 árboles, profundidad 6, hojas de al menos 75 observaciones.</p></div><div class="point"><h3>Meta-OOF</h3><p>Nueva división estratificada en cinco folds para evaluar las predicciones de nivel 2.</p></div><div class="point"><h3>Rendimiento</h3><p>ROC AUC 0.945747; average precision 0.506383; Brier 0.011057.</p></div></div>
<div class="takeaway">El resultado es cercano al mejor XGBoost, con mejor AP, pero ligeramente menor ROC AUC.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">J · ENSAMBLES FINALES</div>

## Limitación del stacking con OOF reutilizados

<p class="lead">Las probabilidades base de cada fila son OOF, pero la validación del bosque meta no es completamente anidada.</p>


<div class="points"><div class="point"><h3>Lo que sí se evita</h3><p>Cada predicción base de entrenamiento se calculó sin entrenar ese modelo con su propia etiqueta.</p></div><div class="point"><h3>Lo que permanece</h3><p>La base de los folds meta puede haber usado las etiquetas de las filas meta-val en otras particiones.</p></div><div class="point"><h3>Consecuencia</h3><p>Las métricas meta-OOF podrían ser optimistas con respecto a una evaluación externa.</p></div><div class="point"><h3>Validación requerida</h3><p>Separar un conjunto intacto antes de entrenar todos los niveles, o efectuar nested CV de ambos niveles.</p></div></div>
<div class="takeaway">La diferencia pequeña entre stacking y el mejor individuo debe leerse con esta reserva.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Resultado final: ROC AUC y AP

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/44_resumen_ensambles_es.png" alt="Resultado final: ROC AUC y AP"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se compararon las predicciones fuera de fold del mejor modelo individual y de cuatro ensambles.</p><h3>RESULTADO</h3><p>La comparación directa favorece a logit-offset en AUC y AP; el mejor XGBoost individual queda a 0.000085 de AUC.</p><h3>ALCANCE</h3><p>Las diferencias son pequeñas y la elección se realizó con las mismas predicciones OOF utilizadas para comparar.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Cuatro métricas para cinco métodos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/46_01_five_way_metric_scorecard.png" alt="Cuatro métricas para cinco métodos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon ROC AUC, average precision, log loss y Brier sobre las cinco series de predicciones OOF.</p><h3>RESULTADO</h3><p>Offset boosting obtiene 0.946205 de AUC, 0.507424 de AP, 0.045798 de log loss y 0.011051 de Brier.</p><h3>ALCANCE</h3><p>La escala de cada panel es distinta. Comparar magnitudes y no sólo las posiciones de las barras.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Curvas ROC y precisión–recobrado

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/47_02_roc_precision_recall.png" alt="Curvas ROC y precisión–recobrado"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se generaron curvas a partir de las predicciones OOF de todos los métodos.</p><h3>RESULTADO</h3><p>Las diferencias son visualmente pequeñas, aun cuando el orden exacto se pueda calcular con seis decimales.</p><h3>ALCANCE</h3><p>Estas curvas describen la misma base utilizada para seleccionar el modelo; no corresponden a la prueba privada de Kaggle.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Residuos y variables meta del stacking

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/48_03_residual_corrections_and_stacking.png" alt="Residuos y variables meta del stacking"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se examinó el cambio de probabilidad del modelo residual y las importancias del random forest meta-modelo.</p><h3>RESULTADO</h3><p>El XGBRegressor hizo correcciones pequeñas en probabilidad; el bosque meta se apoyó más en XGBoost y CatBoost.</p><h3>ALCANCE</h3><p>Las importancias son descriptivas y no constituyen efectos causales ni garantizan una mejora independiente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Evolución del ROC AUC por fold

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/49_04_fold_stability.png" alt="Evolución del ROC AUC por fold"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó el ROC AUC de cada estrategia por fold original.</p><h3>RESULTADO</h3><p>Los perfiles de las cinco estrategias siguen un patrón parecido; offset no supera al mejor individuo en todos los folds.</p><h3>ALCANCE</h3><p>Cinco folds no equivalen a cinco experimentos independientes; las mismas observaciones intervienen en el ajuste de hiperparámetros.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Incertidumbre de la diferencia de AUC

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/45_diferencias_auc_ensambles_es.png" alt="Incertidumbre de la diferencia de AUC"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se recuperaron los intervalos exploratorios de diferencias emparejadas respecto al mejor XGBoost individual.</p><h3>RESULTADO</h3><p>El rango exploratorio para offset es [−0.000615, +0.001010]; incluye cero.</p><h3>ALCANCE</h3><p>Los valores proceden del archivo paired_auc_difference_exploratory.csv; no representan evaluación independiente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">K · ROBUSTEZ ESTADÍSTICA</div>

## Bootstrap emparejado: comparación con el XGBoost individual

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/50_bootstrap_pareado_auc.png" alt="Bootstrap emparejado: comparación con el XGBoost individual"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se ejecutó un bootstrap emparejado y estratificado con 600 réplicas, usando las mismas filas remuestreadas para todos los métodos. Se preservó el número de fraudes y no fraudes.</p><h3>RESULTADO</h3><p>Diferencia entre corrección del logit y XGBoost individual: +0.000085 de ROC AUC; intervalo percentil del 95%: [−0.000263, +0.000440]. Incluye cero.</p><h3>ALCANCE</h3><p>La referencia numérica disponible es el XGBoost fijo de profundidad 5; el XGBoost ajustado con GridSearchCV no está en los archivos OOF recibidos. La nueva notebook lo incluirá cuando recupere sus predicciones.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">K · RESULTADOS DEL ENSAMBLE</div>

## Resultado: ganador según la regla programada

<p class="lead">La regla de selección escoge el mayor ROC AUC OOF entre las cinco estrategias comparadas.</p>

$$\Delta\mathrm{AUC}=0.946205-0.946120=0.000085$$


<div class="points"><div class="point"><h3>Modelo elegido</h3><p>regresión logística corregida con XGBoost (profundidad 3; tasa 0.05).</p></div><div class="point"><h3>Ganancia observada</h3><p>La diferencia observada de ROC AUC es positiva y muy pequeña: 0.000085.</p></div><div class="point"><h3>Desempeño alternativo</h3><p>Stacking: 0.945747 ROC AUC y 0.506383 de AP.</p></div><div class="point"><h3>Interpretación</h3><p>La elección es válida como salida del experimento, pero la mejora puede no generalizar.</p></div></div>
<div class="takeaway">La mayor complejidad no produjo una mejora concluyente frente a XGBoost individual.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">I · CONCLUSIONES</div>

## Qué concluye la ejecución completa

<p class="lead">Ahora disponemos del comparativo agregado del experimento con cuatro ensambles.</p>


<div class="points"><div class="point"><h3>Criterio de selección</h3><p>AUC OOF máximo: 0.946205 para logit-offset.</p></div><div class="point"><h3>Base individual</h3><p>0.946120 para XGBoost profundidad 5: diferencia +0.000085.</p></div><div class="point"><h3>Alternativa de segundo nivel</h3><p>Stacking RF: 0.945747 de ROC AUC; su AP 0.506383 es elevada.</p></div><div class="point"><h3>Interpretación prudente</h3><p>El rango de diferencia offset–individuo contiene cero; no hay superioridad establecida.</p></div></div>
<div class="takeaway">El objetivo no fue demostrar que un ensamble siempre supera al mejor modelo individual.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">I · CONCLUSIONES</div>
## Limitaciones del diseño comparativo

<p class="lead">La extensión sí cuenta con resultados numéricos completos, pero no con una prueba independiente para valorar la selección.</p>


<div class="points"><div class="point"><h3>Selección sobre OOF</h3><p>Se compararon y seleccionaron modelos empleando los mismos resultados fuera de fold.</p></div><div class="point"><h3>Meta-validación</h3><p>El stacking reutiliza predicciones OOF; su validación de nivel 2 no es completamente anidada.</p></div><div class="point"><h3>Dependencia temporal</h3><p>No se verificó independencia entre transacciones de la misma cuenta ni estabilidad temporal.</p></div><div class="point"><h3>Diferencias diminutas</h3><p>La ganancia de ROC AUC 0.000085 es menor que la incertidumbre exploratoria reportada.</p></div></div>
<div class="takeaway">Una nueva evaluación independiente permitiría decidir si el segundo modelo aporta valor real.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">I · CONCLUSIONES</div>

## Siguientes pasos de evaluación

<p class="lead">Conservar ambas alternativas: la arquitectura ganadora por OOF y el modelo individual casi equivalente.</p>


<div class="points"><div class="point"><h3>Prueba independiente</h3><p>Reservar datos externos o usar validación temporal cuando la estructura de clientes lo permita.</p></div><div class="point"><h3>Stacking anidado</h3><p>Entrenar modelos base dentro de cada fold externo antes de ajustar el meta-modelo.</p></div><div class="point"><h3>Prueba de incertidumbre</h3><p>Evaluar diferencias emparejadas en datos que no participaron en la selección.</p></div><div class="point"><h3>Calibración y costo</h3><p>Elegir umbrales de revisión según costos operativos, no por la ROC AUC solamente.</p></div></div>
<div class="takeaway">La comparación es reproducible y su resultado es claro; la magnitud de la mejora exige una validación adicional.</div>

---

<!-- _class: cover -->
<div class="eyebrow">FIN</div>

# Conclusión

El método elegido es regresión logística corregida con XGBoost por ROC AUC OOF, pero su ventaja es mínima respecto a XGBoost individual.

<div class="thesis">Selección documentada: 0.946205 frente a 0.946120. No se afirma superioridad estadística ni resultado de leaderboard.</div>