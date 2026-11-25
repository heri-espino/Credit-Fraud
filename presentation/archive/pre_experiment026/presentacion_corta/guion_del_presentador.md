# Guion de presentación · Predicción de fraude · presentación corta revisada

Los textos desarrollan el argumento de cada diapositiva. La estimación bootstrap es condicional a las predicciones OOF y no reemplaza una evaluación independiente.

## Diapositiva 1 — Predicción probabilística de fraude con tarjetas

**Contexto.** Kaggle Playground S6E11 · De los datos y la PCA a la comparación de modelos y ensambles

**Explicación.**  Presentamos el procedimiento completo que lleva a una predicción de probabilidad y a la selección de un modelo. El conjunto es sintético, con variables con significado transaccional.

**Conclusión.** Problema, análisis exploratorio, modelos, validación y selección con incertidumbre explícita.

**Tiempo orientativo:** 0.32 minutos

## Diapositiva 2 — El objetivo: estimar probabilidades, no sólo asignar clases

**Contexto.** El objetivo observado es binario, pero la entrega de Kaggle exige un número entre 0 y 1 para cada operación.

**Explicación.**  Hay una variable respuesta binaria, y=0/1, pero el archivo de envío es id,is_fraud con probabilidades. Técnicamente entrenamos clasificadores probabilísticos, no una regresión lineal que pueda predecir valores negativos o mayores que uno. ROC AUC valora discriminación de rangos; log loss y Brier complementan el análisis de calibración.

**Conclusión.** La tarea es clasificación probabilística: no regresión lineal ordinaria. La calibración importa para interpretar probabilidades, aunque la métrica oficial sea ROC AUC.

**Fórmula:** $$\hat p(x)=P(Y=1\mid X=x)=\frac{1}{1+e^{-f(x)}}$$

**Tiempo orientativo:** 0.66 minutos

## Diapositiva 3 — Inventario del conjunto de datos

**Contexto.** Entrenamiento: 699,960 operaciones; prueba: 299,984. Hay 24 predictores, además del identificador y la etiqueta.

**Explicación.**  Los 24 predictores se clasificaron por tipo mediante inspección de train.csv. Los 13 numéricos incluyen variables temporales y de historial; los cinco categóricos describen la transacción; los seis booleanos funcionan como indicadores de contexto. Nunca utilizar id como predictor sin justificación, ya que podría aprender artefactos del identificador.

**Conclusión.** Los datos mezclan escalas y tipos; por eso el tratamiento debe adaptarse a modelos lineales y árboles.

**Tiempo orientativo:** 0.63 minutos

## Diapositiva 4 — Frecuencia de fraude y valores faltantes

**Contexto.** 

**Explicación.**  La clase positiva representa una pequeña fracción. Se eligió partición estratificada y métricas como ROC AUC y precisión promedio. Se verificó completitud para el conjunto de entrenamiento.

**Conclusión.** 11,689 fraudes frente a 688,271 operaciones legítimas: prevalencia de 1.67%. En train no aparecen valores faltantes.

**Figura:** 01_target_and_missingness.png

**Procedimiento:** Se calculó la distribución de is_fraud y el porcentaje de registros faltantes para cada variable.

**Interpretación:** 11,689 fraudes frente a 688,271 operaciones legítimas: prevalencia de 1.67%. En train no aparecen valores faltantes.

**Limitación:** Predecir siempre «no fraude» daría exactitud alta, pero no permitiría ordenar operaciones de riesgo.

**Tiempo orientativo:** 0.51 minutos

## Diapositiva 5 — EDA: preguntas y análisis realizados

**Contexto.** La exploración no se redujo a una matriz de correlaciones: se examinó la información desde varias perspectivas.

**Explicación.**  Los análisis corresponden a las figuras 01–11 y 20–25. En las siguientes diapositivas mostramos la evidencia más útil para decidir el modelado. En las figuras de densidad con clases balanceadas artificialmente no se debe inferir la prevalencia real.

**Conclusión.** El EDA sirvió para decidir qué transformaciones y modelos merecía la pena comparar; ninguna asociación marginal demuestra causalidad.

**Tiempo orientativo:** 0.58 minutos

## Diapositiva 6 — Distribución condicional: ECDF por clase

**Contexto.** 

**Explicación.**  Se visualizaron distribuciones numéricas originales y por clase, incluyendo las colas. La diferencia entre curvas de distribución no es equivalente a una regla de decisión individual.

**Conclusión.** Las curvas se desplazan de forma diferente según la variable; hay señal marginal, pero las dos clases mantienen áreas de solapamiento.

**Figura:** 21_class_conditional_ecdfs.png

**Procedimiento:** Se comparó la ECDF de predictores numéricos en fraudes y transacciones legítimas, además de histogramas y densidades.

**Interpretación:** Las curvas se desplazan de forma diferente según la variable; hay señal marginal, pero las dos clases mantienen áreas de solapamiento.

**Limitación:** Una ECDF condicionada por clase no indica por sí sola la probabilidad de fraude de una observación.

**Tiempo orientativo:** 0.43 minutos

## Diapositiva 7 — Correlaciones: linealidad y monotonía

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calcularon correlaciones de Pearson y de Spearman para detectar dependencia lineal y monotónica entre predictores.

Se observa lo siguiente: La matriz ayuda a anticipar redundancia y posibles problemas de colinealidad para la regresión logística.

La interpretación debe considerar que Correlaciones pequeñas no descartan relaciones en U ni efectos de interacción; por eso se hicieron gráficos adicionales.

**Conclusión.** La matriz ayuda a anticipar redundancia y posibles problemas de colinealidad para la regresión logística.

**Figura:** 04_pearson_spearman_correlations.png

**Procedimiento:** Se calcularon correlaciones de Pearson y de Spearman para detectar dependencia lineal y monotónica entre predictores.

**Interpretación:** La matriz ayuda a anticipar redundancia y posibles problemas de colinealidad para la regresión logística.

**Limitación:** Correlaciones pequeñas no descartan relaciones en U ni efectos de interacción; por eso se hicieron gráficos adicionales.

**Tiempo orientativo:** 0.44 minutos

## Diapositiva 8 — Categorías y banderas: efectos conjuntos

**Contexto.** 

**Explicación.**  Además de este cruce se calcularon las tasas marginales por categoría y banderas individuales, y se inspeccionó el tamaño de cada subgrupo.

**Conclusión.** La frecuencia de una condición y su tasa de fraude son cuestiones distintas; algunas combinaciones concentran riesgo mayor.

**Figura:** 22_categorical_flag_interactions.png

**Procedimiento:** Se midieron tasas de fraude y tamaños de grupo al cruzar categorías comerciales y de canal con banderas binarias.

**Interpretación:** La frecuencia de una condición y su tasa de fraude son cuestiones distintas; algunas combinaciones concentran riesgo mayor.

**Limitación:** Las celdas con pocos datos tienen más variabilidad: se muestran los conteos antes de interpretar diferencias.

**Tiempo orientativo:** 0.49 minutos

## Diapositiva 9 — Poder discriminante de una sola variable

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Para cada variable se evaluó su capacidad de separar fraudes de operaciones legítimas de forma individual.

Se observa lo siguiente: Algunos predictores tienen señal por sí solos; otros dependen de interacciones con el contexto de la operación.

La interpretación debe considerar que La puntuación univariada no sustituye un modelo multivariado ni mide causalidad.

**Conclusión.** Algunos predictores tienen señal por sí solos; otros dependen de interacciones con el contexto de la operación.

**Figura:** 20_univariate_feature_discrimination.png

**Procedimiento:** Para cada variable se evaluó su capacidad de separar fraudes de operaciones legítimas de forma individual.

**Interpretación:** Algunos predictores tienen señal por sí solos; otros dependen de interacciones con el contexto de la operación.

**Limitación:** La puntuación univariada no sustituye un modelo multivariado ni mide causalidad.

**Tiempo orientativo:** 0.39 minutos

## Diapositiva 10 — Patrones temporales: hora y día

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calculó la tasa de fraude para combinaciones de hora del día y día de la semana.

Se observa lo siguiente: El riesgo puede variar según la combinación temporal y no sólo por la hora considerada de manera aislada.

La interpretación debe considerar que Deben revisarse los conteos en cada celda antes de extrapolar un patrón; no se dispone aquí de secuencia por cliente.

**Conclusión.** El riesgo puede variar según la combinación temporal y no sólo por la hora considerada de manera aislada.

**Figura:** 23_weekly_hourly_fraud_surface.png

**Procedimiento:** Se calculó la tasa de fraude para combinaciones de hora del día y día de la semana.

**Interpretación:** El riesgo puede variar según la combinación temporal y no sólo por la hora considerada de manera aislada.

**Limitación:** Deben revisarse los conteos en cada celda antes de extrapolar un patrón; no se dispone aquí de secuencia por cliente.

**Tiempo orientativo:** 0.39 minutos

## Diapositiva 11 — No linealidad: riesgo por cuantiles

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se agruparon variables continuas por cuantiles y se estimó la tasa de fraude dentro de cada intervalo.

Se observa lo siguiente: Monto, velocidad y riesgo del comercio presentan cambios de pendiente; algunas relaciones no son monotónicas.

La interpretación debe considerar que Un logit aditivo lineal puede ser insuficiente; se probaron splines y árboles como alternativas.

**Conclusión.** Monto, velocidad y riesgo del comercio presentan cambios de pendiente; algunas relaciones no son monotónicas.

**Figura:** 07_nonlinear_binned_fraud_rates.png

**Procedimiento:** Se agruparon variables continuas por cuantiles y se estimó la tasa de fraude dentro de cada intervalo.

**Interpretación:** Monto, velocidad y riesgo del comercio presentan cambios de pendiente; algunas relaciones no son monotónicas.

**Limitación:** Un logit aditivo lineal puede ser insuficiente; se probaron splines y árboles como alternativas.

**Tiempo orientativo:** 0.53 minutos

## Diapositiva 12 — Interacciones entre características

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calcularon tasas de fraude dentro de celdas definidas por pares de variables y se indicó su soporte muestral.

Se observa lo siguiente: Riesgo del comercio y velocidad transaccional muestran un patrón conjunto que no se resume con una correlación.

La interpretación debe considerar que Son tasas marginales condicionadas en dos variables; otros predictores pueden alterar la interpretación.

**Conclusión.** Riesgo del comercio y velocidad transaccional muestran un patrón conjunto que no se resume con una correlación.

**Figura:** 09_bivariate_interaction_heatmaps.png

**Procedimiento:** Se calcularon tasas de fraude dentro de celdas definidas por pares de variables y se indicó su soporte muestral.

**Interpretación:** Riesgo del comercio y velocidad transaccional muestran un patrón conjunto que no se resume con una correlación.

**Limitación:** Son tasas marginales condicionadas en dos variables; otros predictores pueden alterar la interpretación.

**Tiempo orientativo:** 0.52 minutos

## Diapositiva 13 — Valores extremos por rango intercuartílico

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se aplicaron cercas a tres IQR de los cuartiles para localizar colas y valores numéricos extremos.

Se observa lo siguiente: Las transacciones de monto elevado pueden ser legítimas y algunas compras fraudulentas no son extremas.

La interpretación debe considerar que No se eliminaron automáticamente observaciones: una regla de limpieza podría borrar señal predictiva.

**Conclusión.** Las transacciones de monto elevado pueden ser legítimas y algunas compras fraudulentas no son extremas.

**Figura:** 10_univariate_outliers.png

**Procedimiento:** Se aplicaron cercas a tres IQR de los cuartiles para localizar colas y valores numéricos extremos.

**Interpretación:** Las transacciones de monto elevado pueden ser legítimas y algunas compras fraudulentas no son extremas.

**Limitación:** No se eliminaron automáticamente observaciones: una regla de limpieza podría borrar señal predictiva.

**Tiempo orientativo:** 0.42 minutos

## Diapositiva 14 — Detección no supervisada de anomalías

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Isolation Forest asignó puntajes de anomalía sin usar is_fraud; después se comparó la tasa de fraude en los grupos.

Se observa lo siguiente: Los eventos señalados fueron más propensos al fraude dentro de la muestra exploratoria, aunque no coincidían exactamente.

La interpretación debe considerar que Anomalía estadística y fraude no son equivalentes; este diagnóstico no es una validación independiente.

**Conclusión.** Los eventos señalados fueron más propensos al fraude dentro de la muestra exploratoria, aunque no coincidían exactamente.

**Figura:** 11_isolation_forest_anomaly_diagnostics.png

**Procedimiento:** Isolation Forest asignó puntajes de anomalía sin usar is_fraud; después se comparó la tasa de fraude en los grupos.

**Interpretación:** Los eventos señalados fueron más propensos al fraude dentro de la muestra exploratoria, aunque no coincidían exactamente.

**Limitación:** Anomalía estadística y fraude no son equivalentes; este diagnóstico no es una validación independiente.

**Tiempo orientativo:** 0.42 minutos

## Diapositiva 15 — ¿Train y test tienen distribuciones similares?

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se superpusieron ECDF de train y test para revisar cambios de distribución de predictores.

Se observa lo siguiente: Este diagnóstico permite identificar posibles desplazamientos que podrían afectar el desempeño fuera de muestra.

La interpretación debe considerar que Test carece de etiquetas públicas: no se puede medir directamente su ROC AUC antes de la evaluación de Kaggle.

**Conclusión.** Este diagnóstico permite identificar posibles desplazamientos que podrían afectar el desempeño fuera de muestra.

**Figura:** 25_train_test_ecdf_shift.png

**Procedimiento:** Se superpusieron ECDF de train y test para revisar cambios de distribución de predictores.

**Interpretación:** Este diagnóstico permite identificar posibles desplazamientos que podrían afectar el desempeño fuera de muestra.

**Limitación:** Test carece de etiquetas públicas: no se puede medir directamente su ROC AUC antes de la evaluación de Kaggle.

**Tiempo orientativo:** 0.40 minutos

## Diapositiva 16 — Síntesis del EDA: decisiones justificadas

**Contexto.** Las conclusiones del análisis exploratorio se tradujeron en hipótesis de modelado que luego se contrastaron por validación cruzada.

**Explicación.**  También se calcularon diagramas por pares, tasas marginales por canal, tipo de dispositivo y otras categorías, densidades por clase y ECDF. En el EDA no se realizó una selección definitiva de variables por observar la etiqueta en un holdout.

**Conclusión.** Explorar sirve para formular alternativas; el criterio para retenerlas es su desempeño en observaciones no utilizadas en el ajuste.

**Tiempo orientativo:** 0.54 minutos

## Diapositiva 17 — Validación cruzada sin fuga de información

**Contexto.** Los modelos se compararon con cinco folds estratificados y predicciones out-of-fold (OOF).

**Explicación.**  

**Conclusión.** La validación evita optimismo por entrenamiento dentro del fold; seleccionar el máximo entre muchas alternativas aún requiere cautela.

**Tiempo orientativo:** 0.61 minutos

## Diapositiva 18 — PCA mediante SVD: por qué se probó

**Contexto.** Se buscó una representación más compacta conservando al menos el 90% de la varianza de las variables procesadas.

**Explicación.**  

**Conclusión.** Preservar varianza de X no garantiza preservar la señal para predecir Y; la prueba es empírica.

**Fórmula:** $$X_c=U\Sigma V^{T}$$

**Tiempo orientativo:** 0.56 minutos

## Diapositiva 19 — PCA: varianza explicada acumulada

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se proyectaron las variables procesadas sobre componentes principales y se graficó la proporción de varianza retenida.

Se observa lo siguiente: Se evaluó la alternativa que conserva el 90% de varianza; en la comparación OOF no superó a la logística original.

La interpretación debe considerar que Un componente con poca varianza puede seguir teniendo información predictiva; por ello la PCA no fue obligatoria para árboles.

**Conclusión.** Se evaluó la alternativa que conserva el 90% de varianza; en la comparación OOF no superó a la logística original.

**Figura:** 16_pca_explained_variance.png

**Procedimiento:** Se proyectaron las variables procesadas sobre componentes principales y se graficó la proporción de varianza retenida.

**Interpretación:** Se evaluó la alternativa que conserva el 90% de varianza; en la comparación OOF no superó a la logística original.

**Limitación:** Un componente con poca varianza puede seguir teniendo información predictiva; por ello la PCA no fue obligatoria para árboles.

**Tiempo orientativo:** 0.48 minutos

## Diapositiva 20 — Regresión logística: referencia probabilística

**Contexto.** Es un primer clasificador interpretable y eficiente; estima log-odds aditivos y los transforma mediante la sigmoide.

**Explicación.**  

**Conclusión.** No exige normalidad de predictores ni homocedasticidad; sirve como referencia, no como supuesto de que todas las relaciones sean lineales.

**Fórmula:** $$\log\frac{p(x)}{1-p(x)}=\beta_0+\beta^{T}x$$

**Tiempo orientativo:** 0.61 minutos

## Diapositiva 21 — Diagnósticos del modelo logístico

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se verificó la redundancia entre variables mediante VIF y se examinó el posible cambio de distribución entre conjuntos.

Se observa lo siguiente: No se identificaron correlaciones extremas que por sí solas invalidaran el modelo; el tratamiento de categorías evita redundancia exacta.

La interpretación debe considerar que VIF no certifica independencia, ausencia de separación multivariante o linealidad del logit; se complementó con otros diagnósticos.

**Conclusión.** No se identificaron correlaciones extremas que por sí solas invalidaran el modelo; el tratamiento de categorías evita redundancia exacta.

**Figura:** 17_assumptions_vif_and_feature_shift.png

**Procedimiento:** Se verificó la redundancia entre variables mediante VIF y se examinó el posible cambio de distribución entre conjuntos.

**Interpretación:** No se identificaron correlaciones extremas que por sí solas invalidaran el modelo; el tratamiento de categorías evita redundancia exacta.

**Limitación:** VIF no certifica independencia, ausencia de separación multivariante o linealidad del logit; se complementó con otros diagnósticos.

**Tiempo orientativo:** 0.44 minutos

## Diapositiva 22 — Familias de modelos y qué pueden aprender

**Contexto.** Se compararon 19 configuraciones de cinco líneas de modelado con las mismas particiones externas.

**Explicación.**  

**Conclusión.** La comparación combina capacidad predictiva, estabilidad, interpretación y costo de cómputo.

**Tiempo orientativo:** 0.58 minutos

## Diapositiva 23 — Búsqueda de hiperparámetros con GridSearchCV

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se exploraron combinaciones de profundidad, tasa de aprendizaje y regularización para XGBoost y CatBoost mediante CV interno.

Se observa lo siguiente: Cada combinación se evaluó con tres folds internos de la parte de entrenamiento y se conservó la mejor configuración.

La interpretación debe considerar que El gráfico muestra parámetros probados; el XGBoost fijo de referencia no debe confundirse con el XGBoost seleccionado por la búsqueda.

**Conclusión.** Cada combinación se evaluó con tres folds internos de la parte de entrenamiento y se conservó la mejor configuración.

**Figura:** 42_gridsearch_full_parameter_space.png

**Procedimiento:** Se exploraron combinaciones de profundidad, tasa de aprendizaje y regularización para XGBoost y CatBoost mediante CV interno.

**Interpretación:** Cada combinación se evaluó con tres folds internos de la parte de entrenamiento y se conservó la mejor configuración.

**Limitación:** El gráfico muestra parámetros probados; el XGBoost fijo de referencia no debe confundirse con el XGBoost seleccionado por la búsqueda.

**Tiempo orientativo:** 0.46 minutos

## Diapositiva 24 — Comparación de candidatos en cinco folds

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calcularon ROC AUC OOF para todos los candidatos y se graficó la variación de AUC entre folds estratificados.

Se observa lo siguiente: Los métodos basados en boosting estuvieron entre los mejor posicionados y las diferencias entre candidatos superiores fueron pequeñas.

La interpretación debe considerar que El máximo OOF observado puede ser optimista por selección: conviene revisar dispersión entre folds y validación independiente.

**Conclusión.** Los métodos basados en boosting estuvieron entre los mejor posicionados y las diferencias entre candidatos superiores fueron pequeñas.

**Figura:** 12_candidate_scores_and_folds.png

**Procedimiento:** Se calcularon ROC AUC OOF para todos los candidatos y se graficó la variación de AUC entre folds estratificados.

**Interpretación:** Los métodos basados en boosting estuvieron entre los mejor posicionados y las diferencias entre candidatos superiores fueron pequeñas.

**Limitación:** El máximo OOF observado puede ser optimista por selección: conviene revisar dispersión entre folds y validación independiente.

**Tiempo orientativo:** 0.44 minutos

## Diapositiva 25 — ¿Cuánto difieren las predicciones de los modelos?

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calculó la correlación entre los vectores de probabilidades OOF de los distintos candidatos.

Se observa lo siguiente: Una alta correlación sugiere que los modelos clasifican muchas transacciones de forma semejante.

La interpretación debe considerar que Alta correlación de puntajes no implica coincidencia exacta entre los casos de mayor riesgo ni mejora por promediarlos.

**Conclusión.** Una alta correlación sugiere que los modelos clasifican muchas transacciones de forma semejante.

**Figura:** 13_oof_prediction_correlations.png

**Procedimiento:** Se calculó la correlación entre los vectores de probabilidades OOF de los distintos candidatos.

**Interpretación:** Una alta correlación sugiere que los modelos clasifican muchas transacciones de forma semejante.

**Limitación:** Alta correlación de puntajes no implica coincidencia exacta entre los casos de mayor riesgo ni mejora por promediarlos.

**Tiempo orientativo:** 0.40 minutos

## Diapositiva 26 — Desempeño frente a tiempo de entrenamiento

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se contrastó la calidad predictiva con el tiempo utilizado para entrenar y ajustar las alternativas.

Se observa lo siguiente: Los métodos más complejos no aportan necesariamente una mejora proporcional al costo computacional.

La interpretación debe considerar que Los tiempos dependen del hardware y del dispositivo efectivo de CPU/GPU; no son una comparación universal.

**Conclusión.** Los métodos más complejos no aportan necesariamente una mejora proporcional al costo computacional.

**Figura:** 27_performance_vs_training_time.png

**Procedimiento:** Se contrastó la calidad predictiva con el tiempo utilizado para entrenar y ajustar las alternativas.

**Interpretación:** Los métodos más complejos no aportan necesariamente una mejora proporcional al costo computacional.

**Limitación:** Los tiempos dependen del hardware y del dispositivo efectivo de CPU/GPU; no son una comparación universal.

**Tiempo orientativo:** 0.42 minutos

## Diapositiva 27 — Mejor candidato individual: XGBoost

**Contexto.** La referencia individual con puntuación verificada es XGBoost de profundidad 5 y tasa de aprendizaje 0.05.

**Explicación.**  

**Conclusión.** Se conserva como referencia para juzgar si el costo adicional de un ensamble mejora realmente la discriminación.

**Tiempo orientativo:** 0.47 minutos

## Diapositiva 28 — Cuatro estrategias de ensamble

**Contexto.** Se reutilizaron predicciones OOF y modelos por fold, evitando volver a ejecutar toda la búsqueda inicial.

**Explicación.**  

**Conclusión.** Los cuatro mecanismos son diferentes; su valor se decide comparándolos contra el mejor modelo individual.

**Tiempo orientativo:** 0.68 minutos

## Diapositiva 29 — Primer ensamble: promedio de probabilidades

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se construyeron mezclas entre modelos individuales y se promediaron probabilidades de modelos seleccionados.

Se observa lo siguiente: El promedio puede reducir variabilidad, pero combinar modelos similares o de calidad desigual no garantiza mejor ROC AUC.

La interpretación debe considerar que El promedio no es bagging clásico: éste entrena múltiples instancias sobre muestras bootstrap y luego promedia.

**Conclusión.** El promedio puede reducir variabilidad, pero combinar modelos similares o de calidad desigual no garantiza mejor ROC AUC.

**Figura:** 14_ensemble_comparisons.png

**Procedimiento:** Se construyeron mezclas entre modelos individuales y se promediaron probabilidades de modelos seleccionados.

**Interpretación:** El promedio puede reducir variabilidad, pero combinar modelos similares o de calidad desigual no garantiza mejor ROC AUC.

**Limitación:** El promedio no es bagging clásico: éste entrena múltiples instancias sobre muestras bootstrap y luego promedia.

**Tiempo orientativo:** 0.40 minutos

## Diapositiva 30 — Segundo ensamble: corregir el logit con XGBoost

**Contexto.** XGBoost utiliza el puntaje inicial de la regresión logística como base y optimiza la pérdida logística.

**Explicación.**  

**Conclusión.** Se corrige en escala de log-odds y la sigmoide garantiza una probabilidad final entre 0 y 1.

**Fórmula:** $$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$

**Tiempo orientativo:** 0.60 minutos

## Diapositiva 31 — Tercer ensamble: aprender residuos explícitos

**Contexto.** Esta alternativa implementa literalmente la idea de usar los errores de la regresión logística como nueva respuesta.

**Explicación.**  

**Conclusión.** Aprender residuos de probabilidad con pérdida cuadrática no equivale a corregir logits con pérdida logística.

**Fórmula:** $$r_i=y_i-\hat p_{\mathrm{LR}}(x_i)$$

**Tiempo orientativo:** 0.54 minutos

## Diapositiva 32 — Cuarto ensamble: stacking con random forest

**Contexto.** Un segundo clasificador recibe como predictores las probabilidades que generan los modelos base.

**Explicación.**  

**Conclusión.** El bosque aprende cómo combinar predicciones; no recibe los 24 predictores originales.

**Fórmula:** $$z_i=\left(\hat p_1(x_i),\ldots,\hat p_{17}(x_i)\right)$$

**Tiempo orientativo:** 0.60 minutos

## Diapositiva 33 — Comparación final: modelo individual y ensambles

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se calcularon las mismas métricas OOF para el mejor individual y los cuatro ensambles, sobre las mismas transacciones.

Se observa lo siguiente: AUC: offset 0.946205; XGBoost 0.946120; stacking 0.945747; promedio 0.943280; residuos 0.940241.

La interpretación debe considerar que La ventaja del primer método es de 0.000085 sobre el individual; no debe confundirse orden observado con mejora demostrada.

**Conclusión.** AUC: offset 0.946205; XGBoost 0.946120; stacking 0.945747; promedio 0.943280; residuos 0.940241.

**Figura:** 44_resumen_ensambles_es.png

**Procedimiento:** Se calcularon las mismas métricas OOF para el mejor individual y los cuatro ensambles, sobre las mismas transacciones.

**Interpretación:** AUC: offset 0.946205; XGBoost 0.946120; stacking 0.945747; promedio 0.943280; residuos 0.940241.

**Limitación:** La ventaja del primer método es de 0.000085 sobre el individual; no debe confundirse orden observado con mejora demostrada.

**Tiempo orientativo:** 0.50 minutos

## Diapositiva 34 — ROC AUC, precisión promedio y calibración

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se complementó el ordenamiento por ROC AUC con precisión promedio, pérdida logística y error de Brier.

Se observa lo siguiente: El offset también obtuvo AP 0.507424; el stacking fue cercano en AP y Brier, aunque inferior en ROC AUC.

La interpretación debe considerar que ROC AUC mide ranking; log loss y Brier penalizan probabilidades mal ajustadas. Ninguna métrica resume todo el comportamiento.

**Conclusión.** El offset también obtuvo AP 0.507424; el stacking fue cercano en AP y Brier, aunque inferior en ROC AUC.

**Figura:** 46_01_five_way_metric_scorecard.png

**Procedimiento:** Se complementó el ordenamiento por ROC AUC con precisión promedio, pérdida logística y error de Brier.

**Interpretación:** El offset también obtuvo AP 0.507424; el stacking fue cercano en AP y Brier, aunque inferior en ROC AUC.

**Limitación:** ROC AUC mide ranking; log loss y Brier penalizan probabilidades mal ajustadas. Ninguna métrica resume todo el comportamiento.

**Tiempo orientativo:** 0.42 minutos

## Diapositiva 35 — Bootstrap emparejado: magnitud de la diferencia

**Contexto.** 

**Explicación.**  Se realizó el siguiente análisis: Se remuestrearon las mismas transacciones por clase en 600 réplicas; se calculó en cada una la diferencia de AUC.

Se observa lo siguiente: Offset menos XGBoost fijo: +0.000085; intervalo percentil del 95% [−0.000263, +0.000440], que incluye cero.

La interpretación debe considerar que El intervalo es exploratorio: selección OOF previa, posible dependencia entre operaciones y falta de prueba externa.

**Conclusión.** Offset menos XGBoost fijo: +0.000085; intervalo percentil del 95% [−0.000263, +0.000440], que incluye cero.

**Figura:** 50_bootstrap_pareado_auc.png

**Procedimiento:** Se remuestrearon las mismas transacciones por clase en 600 réplicas; se calculó en cada una la diferencia de AUC.

**Interpretación:** Offset menos XGBoost fijo: +0.000085; intervalo percentil del 95% [−0.000263, +0.000440], que incluye cero.

**Limitación:** El intervalo es exploratorio: selección OOF previa, posible dependencia entre operaciones y falta de prueba externa.

**Tiempo orientativo:** 0.66 minutos

## Diapositiva 36 — Conclusión: selección observada y alcance de la evidencia

**Contexto.** La decisión de producción del notebook fue escoger la mayor ROC AUC OOF, pero debemos separar la regla de selección de su evidencia estadística.

**Explicación.**  

**Conclusión.** El experimento justifica mantener ambas alternativas; la mayor AUC observada no es prueba suficiente de superioridad fuera de muestra.

**Tiempo orientativo:** 0.60 minutos