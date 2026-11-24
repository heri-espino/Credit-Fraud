---
marp: true
theme: fraud-whitegrid
size: 16:9
paginate: true
math: mathjax
transition: fade
footer: 'LDS1071 · Predicción de fraude'
title: 'Predicción de fraude · presentación corta revisada'
---

<!-- _class: cover -->
<div class="eyebrow">PROYECTO FINAL · LDS1071</div>

# Predicción probabilística de fraude con tarjetas

Kaggle Playground S6E11 · De los datos y la PCA a la comparación de modelos y ensambles

<div class="thesis">Problema, análisis exploratorio, modelos, validación y selección con incertidumbre explícita.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">01 · PROBLEMA</div>

## El objetivo: estimar probabilidades, no sólo asignar clases

<p class="lead">El objetivo observado es binario, pero la entrega de Kaggle exige un número entre 0 y 1 para cada operación.</p>

$$\hat p(x)=P(Y=1\mid X=x)=\frac{1}{1+e^{-f(x)}}$$


<div class="points"><div class="point"><h3>Respuesta observada</h3><p>is_fraud toma 0 cuando la operación es legítima y 1 cuando se registró como fraude.</p></div><div class="point"><h3>Predicción solicitada</h3><p>Para cada id del test, debemos entregar la probabilidad estimada de fraude; no basta responder «fraude / no fraude».</p></div><div class="point"><h3>Por qué logística</h3><p>Un clasificador probabilístico usa la función sigmoide para transformar un puntaje real en una probabilidad válida.</p></div><div class="point"><h3>Cómo evalúa Kaggle</h3><p>ROC AUC compara el orden de los puntajes entre fraudes y operaciones legítimas; no depende de un umbral de 0.5.</p></div></div>
<div class="takeaway">La tarea es clasificación probabilística: no regresión lineal ordinaria. La calibración importa para interpretar probabilidades, aunque la métrica oficial sea ROC AUC.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">01 · DATOS</div>

## Inventario del conjunto de datos

<p class="lead">Entrenamiento: 699,960 operaciones; prueba: 299,984. Hay 24 predictores, además del identificador y la etiqueta.</p>


<div class="points"><div class="point"><h3>13 numéricos</h3><p>Monto, tiempo desde la compra anterior, transacciones en 24 h, distancia al hogar, antigüedad, edad, saldo, intentos CVV, velocidad y riesgo del comercio, entre otros.</p></div><div class="point"><h3>5 categóricos</h3><p>Categoría del comercio, tipo de tarjeta, método de autenticación, canal de operación y tipo de dispositivo.</p></div><div class="point"><h3>6 booleanos</h3><p>Compra internacional, comercio nuevo, VPN, discordancia de país IP, discordancia de direcciones e intento de estafa generado por IA.</p></div><div class="point"><h3>Preprocesamiento</h3><p>Se excluye id por ser identificador; se codifican categorías y se escalan numéricas sólo cuando el estimador lo requiere.</p></div></div>
<div class="takeaway">Los datos mezclan escalas y tipos; por eso el tratamiento debe adaptarse a modelos lineales y árboles.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Frecuencia de fraude y valores faltantes

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/01_target_and_missingness.png" alt="Frecuencia de fraude y valores faltantes"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calculó la distribución de is_fraud y el porcentaje de registros faltantes para cada variable.</p><h3>RESULTADO</h3><p>11,689 fraudes frente a 688,271 operaciones legítimas: prevalencia de 1.67%. En train no aparecen valores faltantes.</p><h3>ALCANCE</h3><p>Predecir siempre «no fraude» daría exactitud alta, pero no permitiría ordenar operaciones de riesgo.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">02 · EDA</div>

## EDA: preguntas y análisis realizados

<p class="lead">La exploración no se redujo a una matriz de correlaciones: se examinó la información desde varias perspectivas.</p>


<div class="points"><div class="point"><h3>Distribuciones</h3><p>Histogramas, densidades condicionadas por clase y funciones de distribución acumulada (ECDF) para comparar escalas y colas.</p></div><div class="point"><h3>Asociaciones</h3><p>Pearson, Spearman, tasas de fraude por categoría, banderas, curvas por cuantiles y combinaciones de dos predictores.</p></div><div class="point"><h3>Tiempo y geometría</h3><p>Riesgo por hora y día, diagramas por pares y capacidad discriminante marginal de cada variable.</p></div><div class="point"><h3>Anomalías y cambio</h3><p>Valores extremos por IQR, Isolation Forest y comparación entre las distribuciones de entrenamiento y prueba.</p></div></div>
<div class="takeaway">El EDA sirvió para decidir qué transformaciones y modelos merecía la pena comparar; ninguna asociación marginal demuestra causalidad.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Distribución condicional: ECDF por clase

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/21_class_conditional_ecdfs.png" alt="Distribución condicional: ECDF por clase"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se comparó la ECDF de predictores numéricos en fraudes y transacciones legítimas, además de histogramas y densidades.</p><h3>RESULTADO</h3><p>Las curvas se desplazan de forma diferente según la variable; hay señal marginal, pero las dos clases mantienen áreas de solapamiento.</p><h3>ALCANCE</h3><p>Una ECDF condicionada por clase no indica por sí sola la probabilidad de fraude de una observación.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Correlaciones: linealidad y monotonía

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/04_pearson_spearman_correlations.png" alt="Correlaciones: linealidad y monotonía"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon correlaciones de Pearson y de Spearman para detectar dependencia lineal y monotónica entre predictores.</p><h3>RESULTADO</h3><p>La matriz ayuda a anticipar redundancia y posibles problemas de colinealidad para la regresión logística.</p><h3>ALCANCE</h3><p>Correlaciones pequeñas no descartan relaciones en U ni efectos de interacción; por eso se hicieron gráficos adicionales.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Categorías y banderas: efectos conjuntos

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/22_categorical_flag_interactions.png" alt="Categorías y banderas: efectos conjuntos"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se midieron tasas de fraude y tamaños de grupo al cruzar categorías comerciales y de canal con banderas binarias.</p><h3>RESULTADO</h3><p>La frecuencia de una condición y su tasa de fraude son cuestiones distintas; algunas combinaciones concentran riesgo mayor.</p><h3>ALCANCE</h3><p>Las celdas con pocos datos tienen más variabilidad: se muestran los conteos antes de interpretar diferencias.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Poder discriminante de una sola variable

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/20_univariate_feature_discrimination.png" alt="Poder discriminante de una sola variable"/></div><div class="explanation"><h3>MÉTODO</h3><p>Para cada variable se evaluó su capacidad de separar fraudes de operaciones legítimas de forma individual.</p><h3>RESULTADO</h3><p>Algunos predictores tienen señal por sí solos; otros dependen de interacciones con el contexto de la operación.</p><h3>ALCANCE</h3><p>La puntuación univariada no sustituye un modelo multivariado ni mide causalidad.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Patrones temporales: hora y día

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/23_weekly_hourly_fraud_surface.png" alt="Patrones temporales: hora y día"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calculó la tasa de fraude para combinaciones de hora del día y día de la semana.</p><h3>RESULTADO</h3><p>El riesgo puede variar según la combinación temporal y no sólo por la hora considerada de manera aislada.</p><h3>ALCANCE</h3><p>Deben revisarse los conteos en cada celda antes de extrapolar un patrón; no se dispone aquí de secuencia por cliente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## No linealidad: riesgo por cuantiles

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/07_nonlinear_binned_fraud_rates.png" alt="No linealidad: riesgo por cuantiles"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se agruparon variables continuas por cuantiles y se estimó la tasa de fraude dentro de cada intervalo.</p><h3>RESULTADO</h3><p>Monto, velocidad y riesgo del comercio presentan cambios de pendiente; algunas relaciones no son monotónicas.</p><h3>ALCANCE</h3><p>Un logit aditivo lineal puede ser insuficiente; se probaron splines y árboles como alternativas.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Interacciones entre características

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/09_bivariate_interaction_heatmaps.png" alt="Interacciones entre características"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon tasas de fraude dentro de celdas definidas por pares de variables y se indicó su soporte muestral.</p><h3>RESULTADO</h3><p>Riesgo del comercio y velocidad transaccional muestran un patrón conjunto que no se resume con una correlación.</p><h3>ALCANCE</h3><p>Son tasas marginales condicionadas en dos variables; otros predictores pueden alterar la interpretación.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Valores extremos por rango intercuartílico

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/10_univariate_outliers.png" alt="Valores extremos por rango intercuartílico"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se aplicaron cercas a tres IQR de los cuartiles para localizar colas y valores numéricos extremos.</p><h3>RESULTADO</h3><p>Las transacciones de monto elevado pueden ser legítimas y algunas compras fraudulentas no son extremas.</p><h3>ALCANCE</h3><p>No se eliminaron automáticamente observaciones: una regla de limpieza podría borrar señal predictiva.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## Detección no supervisada de anomalías

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/11_isolation_forest_anomaly_diagnostics.png" alt="Detección no supervisada de anomalías"/></div><div class="explanation"><h3>MÉTODO</h3><p>Isolation Forest asignó puntajes de anomalía sin usar is_fraud; después se comparó la tasa de fraude en los grupos.</p><h3>RESULTADO</h3><p>Los eventos señalados fueron más propensos al fraude dentro de la muestra exploratoria, aunque no coincidían exactamente.</p><h3>ALCANCE</h3><p>Anomalía estadística y fraude no son equivalentes; este diagnóstico no es una validación independiente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">02 · EDA</div>

## ¿Train y test tienen distribuciones similares?

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/25_train_test_ecdf_shift.png" alt="¿Train y test tienen distribuciones similares?"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se superpusieron ECDF de train y test para revisar cambios de distribución de predictores.</p><h3>RESULTADO</h3><p>Este diagnóstico permite identificar posibles desplazamientos que podrían afectar el desempeño fuera de muestra.</p><h3>ALCANCE</h3><p>Test carece de etiquetas públicas: no se puede medir directamente su ROC AUC antes de la evaluación de Kaggle.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">02 · EDA</div>

## Síntesis del EDA: decisiones justificadas

<p class="lead">Las conclusiones del análisis exploratorio se tradujeron en hipótesis de modelado que luego se contrastaron por validación cruzada.</p>


<div class="points"><div class="point"><h3>Relaciones no lineales</h3><p>La forma de las curvas motivó logística con splines y árboles de decisión potenciados.</p></div><div class="point"><h3>Interacciones</h3><p>Los mapas de calor y gráficos por pares justificaron probar métodos capaces de capturar combinaciones.</p></div><div class="point"><h3>Colas y rareza</h3><p>Se conservaron valores extremos; se realizaron diagnósticos IQR e Isolation Forest sin tratar automáticamente toda anomalía como fraude.</p></div><div class="point"><h3>Desbalance y desplazamiento</h3><p>La validación fue estratificada; se revisaron métricas de ranking y distribuciones train/test.</p></div></div>
<div class="takeaway">Explorar sirve para formular alternativas; el criterio para retenerlas es su desempeño en observaciones no utilizadas en el ajuste.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">03 · METODOLOGÍA</div>

## Validación cruzada sin fuga de información

<p class="lead">Los modelos se compararon con cinco folds estratificados y predicciones out-of-fold (OOF).</p>


<div class="points"><div class="point"><h3>Cinco particiones</h3><p>Cada observación tiene una predicción producida por un estimador que no la usó para entrenarse.</p></div><div class="point"><h3>Transformaciones dentro del fold</h3><p>Escalado, codificación, splines y PCA se ajustan sólo en el subconjunto de entrenamiento de cada fold.</p></div><div class="point"><h3>GridSearchCV</h3><p>XGBoost y CatBoost usan búsqueda de hiperparámetros en una partición interna del entrenamiento, sin mirar la validación externa.</p></div><div class="point"><h3>Métricas</h3><p>Primaria: ROC AUC OOF. También se guardaron precisión promedio, log loss, Brier y tiempos de ajuste.</p></div></div>
<div class="takeaway">La validación evita optimismo por entrenamiento dentro del fold; seleccionar el máximo entre muchas alternativas aún requiere cautela.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">03 · REDUCCIÓN DE DIMENSIÓN</div>

## PCA mediante SVD: por qué se probó

<p class="lead">Se buscó una representación más compacta conservando al menos el 90% de la varianza de las variables procesadas.</p>

$$X_c=U\Sigma V^{T}$$


<div class="points"><div class="point"><h3>Construcción</h3><p>Tras codificar y escalar, se centra la matriz y se calcula su descomposición en valores singulares (SVD).</p></div><div class="point"><h3>Componentes</h3><p>Las columnas principales de la transformación retienen direcciones con mayor variabilidad en los predictores.</p></div><div class="point"><h3>Elección de k</h3><p>Se toma el número mínimo de componentes cuya varianza explicada acumulada alcanza el 90%.</p></div><div class="point"><h3>Validación</h3><p>La PCA se ajusta dentro de cada fold, y su regresión logística se compara contra la logística sin PCA.</p></div></div>
<div class="takeaway">Preservar varianza de X no garantiza preservar la señal para predecir Y; la prueba es empírica.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">03 · REDUCCIÓN DE DIMENSIÓN</div>

## PCA: varianza explicada acumulada

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/16_pca_explained_variance.png" alt="PCA: varianza explicada acumulada"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se proyectaron las variables procesadas sobre componentes principales y se graficó la proporción de varianza retenida.</p><h3>RESULTADO</h3><p>Se evaluó la alternativa que conserva el 90% de varianza; en la comparación OOF no superó a la logística original.</p><h3>ALCANCE</h3><p>Un componente con poca varianza puede seguir teniendo información predictiva; por ello la PCA no fue obligatoria para árboles.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">04 · MODELOS</div>

## Regresión logística: referencia probabilística

<p class="lead">Es un primer clasificador interpretable y eficiente; estima log-odds aditivos y los transforma mediante la sigmoide.</p>

$$\log\frac{p(x)}{1-p(x)}=\beta_0+\beta^{T}x$$


<div class="points"><div class="point"><h3>Respuesta y salida</h3><p>Aunque la etiqueta de entrenamiento sea 0/1, el modelo produce una probabilidad válida entre 0 y 1.</p></div><div class="point"><h3>Regularización</h3><p>Se utilizó penalización L2 y se ajustó la intensidad C, con las variables numéricas estandarizadas.</p></div><div class="point"><h3>Hipótesis de especificación</h3><p>El logit es aditivo y lineal en la representación dada; por eso se añadió una versión con splines.</p></div><div class="point"><h3>Condiciones a revisar</h3><p>Independencia entre observaciones, colinealidad, separación de clases, convergencia y calibración.</p></div></div>
<div class="takeaway">No exige normalidad de predictores ni homocedasticidad; sirve como referencia, no como supuesto de que todas las relaciones sean lineales.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">04 · MODELOS</div>

## Diagnósticos del modelo logístico

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/17_assumptions_vif_and_feature_shift.png" alt="Diagnósticos del modelo logístico"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se verificó la redundancia entre variables mediante VIF y se examinó el posible cambio de distribución entre conjuntos.</p><h3>RESULTADO</h3><p>No se identificaron correlaciones extremas que por sí solas invalidaran el modelo; el tratamiento de categorías evita redundancia exacta.</p><h3>ALCANCE</h3><p>VIF no certifica independencia, ausencia de separación multivariante o linealidad del logit; se complementó con otros diagnósticos.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">04 · MODELOS</div>

## Familias de modelos y qué pueden aprender

<p class="lead">Se compararon 19 configuraciones de cinco líneas de modelado con las mismas particiones externas.</p>


<div class="points"><div class="point"><h3>Logística y logística con splines</h3><p>Base lineal regularizada y versión flexible para suavizar cambios no lineales.</p></div><div class="point"><h3>Random forest</h3><p>Promedia árboles ajustados sobre muestras aleatorias; aprende interacciones y suele resistir pequeñas perturbaciones.</p></div><div class="point"><h3>XGBoost y CatBoost</h3><p>Boosting de árboles: nuevos árboles corrigen pérdida del conjunto anterior; CatBoost trata categorías de forma especializada.</p></div><div class="point"><h3>Logística + XGBoost</h3><p>Se inicia con los logits de la regresión logística y los árboles aprenden correcciones sobre la pérdida logística.</p></div></div>
<div class="takeaway">La comparación combina capacidad predictiva, estabilidad, interpretación y costo de cómputo.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">04 · AJUSTE</div>

## Búsqueda de hiperparámetros con GridSearchCV

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/42_gridsearch_full_parameter_space.png" alt="Búsqueda de hiperparámetros con GridSearchCV"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se exploraron combinaciones de profundidad, tasa de aprendizaje y regularización para XGBoost y CatBoost mediante CV interno.</p><h3>RESULTADO</h3><p>Cada combinación se evaluó con tres folds internos de la parte de entrenamiento y se conservó la mejor configuración.</p><h3>ALCANCE</h3><p>El gráfico muestra parámetros probados; el XGBoost fijo de referencia no debe confundirse con el XGBoost seleccionado por la búsqueda.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">04 · AJUSTE</div>

## Comparación de candidatos en cinco folds

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/12_candidate_scores_and_folds.png" alt="Comparación de candidatos en cinco folds"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon ROC AUC OOF para todos los candidatos y se graficó la variación de AUC entre folds estratificados.</p><h3>RESULTADO</h3><p>Los métodos basados en boosting estuvieron entre los mejor posicionados y las diferencias entre candidatos superiores fueron pequeñas.</p><h3>ALCANCE</h3><p>El máximo OOF observado puede ser optimista por selección: conviene revisar dispersión entre folds y validación independiente.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">04 · DIAGNÓSTICOS</div>

## ¿Cuánto difieren las predicciones de los modelos?

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/13_oof_prediction_correlations.png" alt="¿Cuánto difieren las predicciones de los modelos?"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calculó la correlación entre los vectores de probabilidades OOF de los distintos candidatos.</p><h3>RESULTADO</h3><p>Una alta correlación sugiere que los modelos clasifican muchas transacciones de forma semejante.</p><h3>ALCANCE</h3><p>Alta correlación de puntajes no implica coincidencia exacta entre los casos de mayor riesgo ni mejora por promediarlos.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">04 · DIAGNÓSTICOS</div>

## Desempeño frente a tiempo de entrenamiento

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/27_performance_vs_training_time.png" alt="Desempeño frente a tiempo de entrenamiento"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se contrastó la calidad predictiva con el tiempo utilizado para entrenar y ajustar las alternativas.</p><h3>RESULTADO</h3><p>Los métodos más complejos no aportan necesariamente una mejora proporcional al costo computacional.</p><h3>ALCANCE</h3><p>Los tiempos dependen del hardware y del dispositivo efectivo de CPU/GPU; no son una comparación universal.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">04 · RESULTADO</div>

## Mejor candidato individual: XGBoost

<p class="lead">La referencia individual con puntuación verificada es XGBoost de profundidad 5 y tasa de aprendizaje 0.05.</p>


<div class="points"><div class="point"><h3>ROC AUC OOF</h3><p>0.946120 sobre las 699,960 operaciones etiquetadas.</p></div><div class="point"><h3>Precisión promedio</h3><p>0.503585 en el mismo conjunto de predicciones OOF.</p></div><div class="point"><h3>Por qué funciona</h3><p>La suma de árboles detecta umbrales e interacciones que una regla lineal no puede representar sin transformaciones.</p></div><div class="point"><h3>Distinción necesaria</h3><p>Ésta es una configuración fija; el vector OOF del XGBoost seleccionado por GridSearchCV no se incluyó en los archivos del segundo experimento.</p></div></div>
<div class="takeaway">Se conserva como referencia para juzgar si el costo adicional de un ensamble mejora realmente la discriminación.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">05 · ENSAMBLES</div>

## Cuatro estrategias de ensamble

<p class="lead">Se reutilizaron predicciones OOF y modelos por fold, evitando volver a ejecutar toda la búsqueda inicial.</p>


<div class="points"><div class="point"><h3>1 · Promedio de probabilidades</h3><p>Blending: media de las predicciones de varios modelos seleccionados; no equivale a bagging sobre remuestreos.</p></div><div class="point"><h3>2 · Corrección del logit</h3><p>Regresión logística seguida de XGBoost que aprende correcciones a los logits usando base_margin.</p></div><div class="point"><h3>3 · Regresión sobre residuos</h3><p>XGBoostRegressor intenta predecir los errores de probabilidad de la regresión logística.</p></div><div class="point"><h3>4 · Stacking con random forest</h3><p>Un bosque meta utiliza como únicas variables las predicciones OOF de 17 modelos base.</p></div></div>
<div class="takeaway">Los cuatro mecanismos son diferentes; su valor se decide comparándolos contra el mejor modelo individual.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">05 · ENSAMBLES</div>

## Primer ensamble: promedio de probabilidades

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/14_ensemble_comparisons.png" alt="Primer ensamble: promedio de probabilidades"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se construyeron mezclas entre modelos individuales y se promediaron probabilidades de modelos seleccionados.</p><h3>RESULTADO</h3><p>El promedio puede reducir variabilidad, pero combinar modelos similares o de calidad desigual no garantiza mejor ROC AUC.</p><h3>ALCANCE</h3><p>El promedio no es bagging clásico: éste entrena múltiples instancias sobre muestras bootstrap y luego promedia.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">05 · ENSAMBLES</div>

## Segundo ensamble: corregir el logit con XGBoost

<p class="lead">XGBoost utiliza el puntaje inicial de la regresión logística como base y optimiza la pérdida logística.</p>

$$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$


<div class="points"><div class="point"><h3>Paso 1 · Modelo inicial</h3><p>Se entrena la regresión logística y se calcula su logit para cada transacción.</p></div><div class="point"><h3>Paso 2 · base_margin</h3><p>XGBoost recibe los logits iniciales, no los residuos como nueva variable respuesta.</p></div><div class="point"><h3>Paso 3 · Árboles correctores</h3><p>La pérdida logística genera gradientes relacionados con y menos la probabilidad actual; los árboles corrigen la predicción.</p></div><div class="point"><h3>Resultado</h3><p>ROC AUC OOF 0.946205, con XGBoost corrector de profundidad 3 y tasa de aprendizaje 0.05.</p></div></div>
<div class="takeaway">Se corrige en escala de log-odds y la sigmoide garantiza una probabilidad final entre 0 y 1.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">05 · ENSAMBLES</div>

## Tercer ensamble: aprender residuos explícitos

<p class="lead">Esta alternativa implementa literalmente la idea de usar los errores de la regresión logística como nueva respuesta.</p>

$$r_i=y_i-\hat p_{\mathrm{LR}}(x_i)$$


<div class="points"><div class="point"><h3>Residuos</h3><p>Para la transacción i se calcula la diferencia entre su etiqueta y la probabilidad logística.</p></div><div class="point"><h3>Modelo corrector</h3><p>Un XGBoost de regresión aprende a predecir esos residuos mediante pérdida cuadrática.</p></div><div class="point"><h3>Probabilidad final</h3><p>Se suma la corrección a la probabilidad logística y se acota el resultado al intervalo [0,1].</p></div><div class="point"><h3>Resultado</h3><p>ROC AUC OOF 0.940241: inferior al offset boosting y al XGBoost individual.</p></div></div>
<div class="takeaway">Aprender residuos de probabilidad con pérdida cuadrática no equivale a corregir logits con pérdida logística.</div>

---

<!-- _class: text-slide -->
<div class="eyebrow">05 · ENSAMBLES</div>

## Cuarto ensamble: stacking con random forest

<p class="lead">Un segundo clasificador recibe como predictores las probabilidades que generan los modelos base.</p>

$$z_i=\left(\hat p_1(x_i),\ldots,\hat p_{17}(x_i)\right)$$


<div class="points"><div class="point"><h3>Matriz meta</h3><p>17 columnas de probabilidades OOF: una por cada candidato utilizado en la primera etapa.</p></div><div class="point"><h3>Meta-modelo</h3><p>Bosque aleatorio de 280 árboles, profundidad máxima 6 y 75 observaciones mínimas por hoja.</p></div><div class="point"><h3>Validación</h3><p>Se hizo otro CV estratificado de cinco folds en la segunda capa; no es un diseño completamente anidado.</p></div><div class="point"><h3>Resultado</h3><p>ROC AUC OOF 0.945747 y precisión promedio 0.506383: competitivo, pero no supera al offset.</p></div></div>
<div class="takeaway">El bosque aprende cómo combinar predicciones; no recibe los 24 predictores originales.</div>

---

<!-- _class: figure-side -->
<div class="eyebrow">06 · RESULTADOS</div>

## Comparación final: modelo individual y ensambles

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/44_resumen_ensambles_es.png" alt="Comparación final: modelo individual y ensambles"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se calcularon las mismas métricas OOF para el mejor individual y los cuatro ensambles, sobre las mismas transacciones.</p><h3>RESULTADO</h3><p>AUC: offset 0.946205; XGBoost 0.946120; stacking 0.945747; promedio 0.943280; residuos 0.940241.</p><h3>ALCANCE</h3><p>La ventaja del primer método es de 0.000085 sobre el individual; no debe confundirse orden observado con mejora demostrada.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">06 · RESULTADOS</div>

## ROC AUC, precisión promedio y calibración

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/46_01_five_way_metric_scorecard.png" alt="ROC AUC, precisión promedio y calibración"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se complementó el ordenamiento por ROC AUC con precisión promedio, pérdida logística y error de Brier.</p><h3>RESULTADO</h3><p>El offset también obtuvo AP 0.507424; el stacking fue cercano en AP y Brier, aunque inferior en ROC AUC.</p><h3>ALCANCE</h3><p>ROC AUC mide ranking; log loss y Brier penalizan probabilidades mal ajustadas. Ninguna métrica resume todo el comportamiento.</p></div></div>

---

<!-- _class: figure-side -->
<div class="eyebrow">06 · INFERENCIA</div>

## Bootstrap emparejado: magnitud de la diferencia

<div class="figure-layout"><div class="plot-panel"><img src="../../outputs/figures/50_bootstrap_pareado_auc.png" alt="Bootstrap emparejado: magnitud de la diferencia"/></div><div class="explanation"><h3>MÉTODO</h3><p>Se remuestrearon las mismas transacciones por clase en 600 réplicas; se calculó en cada una la diferencia de AUC.</p><h3>RESULTADO</h3><p>Offset menos XGBoost fijo: +0.000085; intervalo percentil del 95% [−0.000263, +0.000440], que incluye cero.</p><h3>ALCANCE</h3><p>El intervalo es exploratorio: selección OOF previa, posible dependencia entre operaciones y falta de prueba externa.</p></div></div>

---

<!-- _class: text-slide -->
<div class="eyebrow">07 · CONCLUSIONES</div>

## Conclusión: selección observada y alcance de la evidencia

<p class="lead">La decisión de producción del notebook fue escoger la mayor ROC AUC OOF, pero debemos separar la regla de selección de su evidencia estadística.</p>


<div class="points"><div class="point"><h3>Modelo seleccionado</h3><p>Regresión logística corregida con XGBoost, AUC OOF 0.946205.</p></div><div class="point"><h3>Alternativa casi equivalente</h3><p>XGBoost individual de profundidad 5: AUC 0.946120; diferencia de sólo 0.000085.</p></div><div class="point"><h3>Prueba emparejada</h3><p>El intervalo del 95% contiene cero: no se estableció una ventaja estadísticamente sólida del ensamble.</p></div><div class="point"><h3>Qué falta</h3><p>Verificar el XGBoost de GridSearchCV con su OOF y, en lo posible, evaluar en un conjunto etiquetado independiente.</p></div></div>
<div class="takeaway">El experimento justifica mantener ambas alternativas; la mayor AUC observada no es prueba suficiente de superioridad fuera de muestra.</div>