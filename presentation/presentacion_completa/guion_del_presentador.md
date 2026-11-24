# Guion de exposición · Predicción de fraude · presentación completa

**Uso:** el guion complementa las diapositivas sin saturar las imágenes. No son resultados adicionales.

## Diapositiva 01 — Predicción de fraude con tarjetas: el proceso completo

**Mensaje central:** LDS1071 · Kaggle S6E11 · fuente: notebook y 44 figuras proporcionadas

**Guion:** Este material distingue decisiones reproducibles, resultados exploratorios y aquello que requiere comprobación contra archivos CSV del run completo.

## Diapositiva 02 — Qué problema resolvemos y qué entregamos

**Mensaje central:** Un buen score ordena; una buena probabilidad también necesita calibración.

**Guion:** Diferenciar clasificación probabilística, ranking y decisión binaria. El test de Kaggle carece de etiquetas públicas.

## Diapositiva 03 — Datos y desafío estadístico

**Mensaje central:** Fraude raro ≠ necesariamente anomalía aislada.

**Guion:** La ausencia de missing no exime de usar pipelines robustos ante nuevos datos.

## Diapositiva 04 — Métricas: cada una responde otra pregunta

**Mensaje central:** La métrica oficial fija el objetivo; las métricas auxiliares previenen conclusiones incompletas.

**Guion:** No interpretar AUC como probabilidad individual de fraude. AP depende de la prevalencia.

## Diapositiva 05 — Diseño experimental en siete pasos

**Mensaje central:** Semilla 42; conservar resultados por fold y por candidato.

**Guion:** La línea de trabajo preserva trazabilidad y ensayos fallidos, no sólo el mejor modelo.

## Diapositiva 06 — Validación cruzada sin data leakage

**Mensaje central:** El CV permite comparar modelos con exactamente los mismos folds.

**Guion:** Distinguir CV externo de 3-fold CV interno de GridSearchCV. El conjunto test de Kaggle no se usa para entrenar.

## Diapositiva 07 — ¿Por qué explorar antes de modelar?

**Mensaje central:** Las figuras de EDA ayudan a formular hipótesis, no reemplazan la validación cruzada.

**Guion:** 

## Diapositiva 08 — Balance de clases y completitud

**Mensaje central:** La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.

**Guion:** QUÉ SE HIZO: Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.

INTERPRETACIÓN: La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.

LÍMITE: El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.

**Imagen:** `outputs/figures/01_target_and_missingness.png`
**Advertencia:** El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.

## Diapositiva 09 — Distribuciones numéricas

**Mensaje central:** Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.

**Guion:** QUÉ SE HIZO: Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.

INTERPRETACIÓN: Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.

LÍMITE: Una distribución sesgada no determina por sí sola utilidad predictiva.

**Imagen:** `outputs/figures/02_numeric_distributions.png`
**Advertencia:** Una distribución sesgada no determina por sí sola utilidad predictiva.

## Diapositiva 10 — Distribuciones según la clase

**Mensaje central:** La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.

**Guion:** QUÉ SE HIZO: Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.

INTERPRETACIÓN: La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.

LÍMITE: Las densidades normalizadas por clase no representan la prevalencia real de fraude.

**Imagen:** `outputs/figures/03_class_conditional_densities.png`
**Advertencia:** Las densidades normalizadas por clase no representan la prevalencia real de fraude.

## Diapositiva 11 — Correlaciones de Pearson y Spearman

**Mensaje central:** Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.

**Guion:** QUÉ SE HIZO: Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).

INTERPRETACIÓN: Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.

LÍMITE: Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.

**Imagen:** `outputs/figures/04_pearson_spearman_correlations.png`
**Advertencia:** Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.

## Diapositiva 12 — Riesgo por categorías

**Mensaje central:** Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.

**Guion:** QUÉ SE HIZO: Se estimó la tasa observada de fraude por categoría y su soporte muestral.

INTERPRETACIÓN: Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.

LÍMITE: Categorías con pocas observaciones pueden producir tasas muy inestables.

**Imagen:** `outputs/figures/05_categorical_risks.png`
**Advertencia:** Categorías con pocas observaciones pueden producir tasas muy inestables.

## Diapositiva 13 — Indicadores booleanos: frecuencia y riesgo

**Mensaje central:** Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.

**Guion:** QUÉ SE HIZO: Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.

INTERPRETACIÓN: Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.

LÍMITE: La asociación marginal puede desaparecer al ajustar por otros predictores.

**Imagen:** `outputs/figures/06_flag_prevalence_vs_fraud.png`
**Advertencia:** La asociación marginal puede desaparecer al ajustar por otros predictores.

## Diapositiva 14 — De correlaciones a relaciones no lineales

**Mensaje central:** El EDA motivó candidatos adicionales; su valor se decide con CV.

**Guion:** 

## Diapositiva 15 — No linealidad de las tasas de fraude

**Mensaje central:** Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.

**Guion:** QUÉ SE HIZO: Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.

INTERPRETACIÓN: Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.

LÍMITE: El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.

**Imagen:** `outputs/figures/07_nonlinear_binned_fraud_rates.png`
**Advertencia:** El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.

## Diapositiva 16 — Patrones temporales de fraude

**Mensaje central:** Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.

**Guion:** QUÉ SE HIZO: Se analizaron tasas por hora, día y otras variables temporales disponibles.

INTERPRETACIÓN: Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.

LÍMITE: La agregación no prueba estabilidad futura ni sustituye una validación temporal.

**Imagen:** `outputs/figures/08_time_patterns.png`
**Advertencia:** La agregación no prueba estabilidad futura ni sustituye una validación temporal.

## Diapositiva 17 — Interacciones entre variables numéricas

**Mensaje central:** Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.

**Guion:** QUÉ SE HIZO: Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.

INTERPRETACIÓN: Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.

LÍMITE: Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.

**Imagen:** `outputs/figures/09_bivariate_interaction_heatmaps.png`
**Advertencia:** Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.

## Diapositiva 18 — Valores extremos: criterio IQR

**Mensaje central:** Los extremos pueden ser transacciones válidas y contener señal de fraude.

**Guion:** QUÉ SE HIZO: Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.

INTERPRETACIÓN: Los extremos pueden ser transacciones válidas y contener señal de fraude.

LÍMITE: Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.

**Imagen:** `outputs/figures/10_univariate_outliers.png`
**Advertencia:** Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.

## Diapositiva 19 — Anomalías con Isolation Forest

**Mensaje central:** El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.

**Guion:** QUÉ SE HIZO: Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.

INTERPRETACIÓN: El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.

LÍMITE: No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.

**Imagen:** `outputs/figures/11_isolation_forest_anomaly_diagnostics.png`
**Advertencia:** No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.

## Diapositiva 20 — Anomalía, outlier y fraude: tres conceptos

**Mensaje central:** Eliminar colas puede destruir justamente la señal que queremos detectar.

**Guion:** 

## Diapositiva 21 — Pipelines de modelos: decisiones concretas

**Mensaje central:** La transformación se ajusta dentro del fold de entrenamiento.

**Guion:** 

## Diapositiva 22 — SVD y PCA: por qué se probaron

**Mensaje central:** Por eso PCA es candidato experimental, no paso obligatorio.

**Guion:** El objetivo PCA no observa Y; los resultados de clasificación determinan si ayuda.

## Diapositiva 23 — ¿Por qué regresión logística?

**Mensaje central:** L2 ayuda ante correlaciones, pero no “corrige” especificación no lineal.

**Guion:** 

## Diapositiva 24 — ¿Se satisfacen los supuestos de logit?

**Mensaje central:** La utilidad predictiva no equivale a validez causal de coeficientes.

**Guion:** 

## Diapositiva 25 — ¿Qué aporta el spline logístico?

**Mensaje central:** Probar una no linealidad específica es más informativo que añadir complejidad indiscriminada.

**Guion:** 

## Diapositiva 26 — Random forest: bagging dentro de una familia

**Mensaje central:** Este sí es un mecanismo tipo bagging, a diferencia del blend posterior.

**Guion:** 

## Diapositiva 27 — XGBoost: árboles que corrigen errores

**Mensaje central:** Se conserva el mismo esquema de evaluación, sin favorecer a un algoritmo por hardware.

**Guion:** 

## Diapositiva 28 — CatBoost: otra forma de boosting

**Mensaje central:** Diferentes sesgos inductivos merecen comparación directa, no suposiciones de superioridad.

**Guion:** 

## Diapositiva 29 — Diseño de candidatos e hiperparámetros

**Mensaje central:** En modo rápido el notebook reduce tanto filas como hiperparámetros; no mezclar esos scores con el full run.

**Guion:** 

## Diapositiva 30 — Comparación de candidatos en cinco folds

**Mensaje central:** El desempeño medio debe juzgarse junto con su variación entre particiones y familias.

**Guion:** QUÉ SE HIZO: Se calcularon ROC AUC out-of-fold por candidato y por partición.

INTERPRETACIÓN: El desempeño medio debe juzgarse junto con su variación entre particiones y familias.

LÍMITE: La elección del máximo dentro del mismo CV introduce optimismo de selección.

**Imagen:** `outputs/figures/12_candidate_scores_and_folds.png`
**Advertencia:** La elección del máximo dentro del mismo CV introduce optimismo de selección.

## Diapositiva 31 — Correlación entre modelos

**Mensaje central:** Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.

**Guion:** QUÉ SE HIZO: Se compararon los vectores de probabilidades OOF de todos los candidatos.

INTERPRETACIÓN: Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.

LÍMITE: Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.

**Imagen:** `outputs/figures/13_oof_prediction_correlations.png`
**Advertencia:** Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.

## Diapositiva 32 — Modelo individual frente a combinaciones

**Mensaje central:** Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.

**Guion:** QUÉ SE HIZO: Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.

INTERPRETACIÓN: Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.

LÍMITE: El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.

**Imagen:** `outputs/figures/14_ensemble_comparisons.png`
**Advertencia:** El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.

## Diapositiva 33 — Curvas ROC y precisión–recobrado

**Mensaje central:** ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.

**Guion:** QUÉ SE HIZO: Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.

INTERPRETACIÓN: ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.

LÍMITE: Ninguna curva fija por sí sola un umbral operativo.

**Imagen:** `outputs/figures/15_oof_roc_pr_curves.png`
**Advertencia:** Ninguna curva fija por sí sola un umbral operativo.

## Diapositiva 34 — SVD/PCA: 90% de varianza

**Mensaje central:** La reducción es una alternativa de representación, no una mejora predictiva garantizada.

**Guion:** QUÉ SE HIZO: Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.

INTERPRETACIÓN: La reducción es una alternativa de representación, no una mejora predictiva garantizada.

LÍMITE: La varianza de X y la información predictiva sobre Y son objetivos distintos.

**Imagen:** `outputs/figures/16_pca_explained_variance.png`
**Advertencia:** La varianza de X y la información predictiva sobre Y son objetivos distintos.

## Diapositiva 35 — Supuestos logísticos y posibles cambios

**Mensaje central:** Es necesario separar problemas de especificación, dependencia y cambios de distribución.

**Guion:** QUÉ SE HIZO: Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.

INTERPRETACIÓN: Es necesario separar problemas de especificación, dependencia y cambios de distribución.

LÍMITE: Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.

**Imagen:** `outputs/figures/17_assumptions_vif_and_feature_shift.png`
**Advertencia:** Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.

## Diapositiva 36 — Diagnóstico de la regresión logística

**Mensaje central:** Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.

**Guion:** QUÉ SE HIZO: Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.

INTERPRETACIÓN: Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.

LÍMITE: Predictores normales y homocedasticidad NO son supuestos requeridos para logit.

**Imagen:** `outputs/figures/18_oof_logistic_assumption_checks.png`
**Advertencia:** Predictores normales y homocedasticidad NO son supuestos requeridos para logit.

## Diapositiva 37 — Corregir el logit con XGBoost

**Mensaje central:** Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.

**Guion:** QUÉ SE HIZO: Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.

INTERPRETACIÓN: Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.

LÍMITE: No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.

**Imagen:** `outputs/figures/19_logistic_offset_boosting_diagnostics.png`
**Advertencia:** No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.

## Diapositiva 38 — Blending y bagging: cómo evolucionó la idea inicial

**Mensaje central:** Término preciso de la realización: blending entre familias heterogéneas.

**Guion:** 

## Diapositiva 39 — Qué sería stacking clásico

**Mensaje central:** Explicar stacking propuesto sin presentarlo como experimento ya ejecutado.

**Guion:** 

## Diapositiva 40 — Logit + booster de corrección en escala logit

**Mensaje central:** Es una composición aditiva sobre el logit, NO stacking con meta-logit.

**Guion:** 

## Diapositiva 41 — Por qué conservar modelos que no ganaron

**Mensaje central:** La selección sobre OOF es exploratoria y no representa una evaluación completamente intacta.

**Guion:** 

## Diapositiva 42 — EDA extendido: qué más investigamos

**Mensaje central:** Cada gráfico sirve para generar preguntas, no para ajustar modelos sobre el test.

**Guion:** 

## Diapositiva 43 — Valor discriminativo de cada variable

**Mensaje central:** El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.

**Guion:** QUÉ SE HIZO: Se estimó el AUC de predictores aislados y se compararon señales univariantes.

INTERPRETACIÓN: El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.

LÍMITE: Un AUC univariante alto no asegura contribución incremental.

**Imagen:** `outputs/figures/20_univariate_feature_discrimination.png`
**Advertencia:** Un AUC univariante alto no asegura contribución incremental.

## Diapositiva 44 — Distribuciones acumuladas por clase

**Mensaje central:** Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.

**Guion:** QUÉ SE HIZO: Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.

INTERPRETACIÓN: Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.

LÍMITE: Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.

**Imagen:** `outputs/figures/21_class_conditional_ecdfs.png`
**Advertencia:** Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.

## Diapositiva 45 — Categorías × indicadores booleanos

**Mensaje central:** Una misma bandera puede tener distinta asociación con el fraude según su contexto.

**Guion:** QUÉ SE HIZO: Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.

INTERPRETACIÓN: Una misma bandera puede tener distinta asociación con el fraude según su contexto.

LÍMITE: En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.

**Imagen:** `outputs/figures/22_categorical_flag_interactions.png`
**Advertencia:** En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.

## Diapositiva 46 — Mapa de riesgo por día y hora

**Mensaje central:** Puede haber concentraciones temporales no captadas por términos horarios aislados.

**Guion:** QUÉ SE HIZO: Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.

INTERPRETACIÓN: Puede haber concentraciones temporales no captadas por términos horarios aislados.

LÍMITE: La composición de transacciones puede explicar parte del efecto observado.

**Imagen:** `outputs/figures/23_weekly_hourly_fraud_surface.png`
**Advertencia:** La composición de transacciones puede explicar parte del efecto observado.

## Diapositiva 47 — Geometría bivariante por clase

**Mensaje central:** Los patrones de separación multivariada justifican no depender solo de un predictor.

**Guion:** QUÉ SE HIZO: Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.

INTERPRETACIÓN: Los patrones de separación multivariada justifican no depender solo de un predictor.

LÍMITE: Las muestras de visualización no deben confundirse con la distribución completa.

**Imagen:** `outputs/figures/24_pairwise_class_geometry.png`
**Advertencia:** Las muestras de visualización no deben confundirse con la distribución completa.

## Diapositiva 48 — Comparación entrenamiento–prueba

**Mensaje central:** Permite detectar cambios marginales antes de enviar predicciones a Kaggle.

**Guion:** QUÉ SE HIZO: Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.

INTERPRETACIÓN: Permite detectar cambios marginales antes de enviar predicciones a Kaggle.

LÍMITE: Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.

**Imagen:** `outputs/figures/25_train_test_ecdf_shift.png`
**Advertencia:** Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.

## Diapositiva 49 — De la métrica de Kaggle a una operación real

**Mensaje central:** No hay una única métrica que responda todos los usos.

**Guion:** 

## Diapositiva 50 — Validación de umbrales y presupuesto

**Mensaje central:** Estas políticas son evaluadas; no deben confundirse con entrenamiento distinto.

**Guion:** 

## Diapositiva 51 — Comparación con cuatro métricas

**Mensaje central:** La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.

**Guion:** QUÉ SE HIZO: Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.

INTERPRETACIÓN: La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.

LÍMITE: Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.

**Imagen:** `outputs/figures/26_four_metric_model_scorecard.png`
**Advertencia:** Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.

## Diapositiva 52 — Rendimiento frente a costo computacional

**Mensaje central:** Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.

**Guion:** QUÉ SE HIZO: Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.

INTERPRETACIÓN: Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.

LÍMITE: Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.

**Imagen:** `outputs/figures/27_performance_vs_training_time.png`
**Advertencia:** Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.

## Diapositiva 53 — Distribuciones de riesgo predicho

**Mensaje central:** La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.

**Guion:** QUÉ SE HIZO: Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.

INTERPRETACIÓN: La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.

LÍMITE: Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.

**Imagen:** `outputs/figures/28_oof_score_distributions.png`
**Advertencia:** Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.

## Diapositiva 54 — Ganancia acumulada y lift

**Mensaje central:** La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.

**Guion:** QUÉ SE HIZO: Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.

INTERPRETACIÓN: La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.

LÍMITE: Las curvas no incluyen el costo real de las investigaciones o falsos positivos.

**Imagen:** `outputs/figures/29_cumulative_gains_and_lift.png`
**Advertencia:** Las curvas no incluyen el costo real de las investigaciones o falsos positivos.

## Diapositiva 55 — Precisión y recobrado con capacidad limitada

**Mensaje central:** Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.

**Guion:** QUÉ SE HIZO: Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.

INTERPRETACIÓN: Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.

LÍMITE: La mejor fracción a revisar depende de costos externos ausentes del dataset.

**Imagen:** `outputs/figures/30_precision_recall_at_review_budget.png`
**Advertencia:** La mejor fracción a revisar depende de costos externos ausentes del dataset.

## Diapositiva 56 — Errores según política de decisión

**Mensaje central:** Un mismo clasificador puede producir decisiones muy distintas según la política.

**Guion:** QUÉ SE HIZO: Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.

INTERPRETACIÓN: Un mismo clasificador puede producir decisiones muy distintas según la política.

LÍMITE: No se deben comparar matrices sin especificar su regla de umbral.

**Imagen:** `outputs/figures/31_confusion_matrices_by_policy.png`
**Advertencia:** No se deben comparar matrices sin especificar su regla de umbral.

## Diapositiva 57 — Confiabilidad de las probabilidades

**Mensaje central:** Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.

**Guion:** QUÉ SE HIZO: Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.

INTERPRETACIÓN: Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.

LÍMITE: Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.

**Imagen:** `outputs/figures/32_model_reliability_comparison.png`
**Advertencia:** Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.

## Diapositiva 58 — Calibración e incertidumbre

**Mensaje central:** Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.

**Guion:** QUÉ SE HIZO: Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.

INTERPRETACIÓN: Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.

LÍMITE: Los intervalos son descriptivos y dependen del particionado de riesgo.

**Imagen:** `outputs/figures/33_calibration_with_wilson_intervals.png`
**Advertencia:** Los intervalos son descriptivos y dependen del particionado de riesgo.

## Diapositiva 59 — Rendimiento por canal

**Mensaje central:** La calidad global puede esconder subgrupos con menos capacidad discriminativa.

**Guion:** QUÉ SE HIZO: Se evaluaron métricas OOF desagregadas por canal de transacción.

INTERPRETACIÓN: La calidad global puede esconder subgrupos con menos capacidad discriminativa.

LÍMITE: Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.

**Imagen:** `outputs/figures/34_subgroups_channel.png`
**Advertencia:** Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.

## Diapositiva 60 — Rendimiento por categoría de comercio

**Mensaje central:** Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.

**Guion:** QUÉ SE HIZO: Se comparó ROC AUC y AP por categorías de comercio.

INTERPRETACIÓN: Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.

LÍMITE: La tasa base difiere entre grupos y afecta de manera importante a AP.

**Imagen:** `outputs/figures/34_subgroups_merchant_category.png`
**Advertencia:** La tasa base difiere entre grupos y afecta de manera importante a AP.

## Diapositiva 61 — Interpretabilidad: distinguir asociación y explicación

**Mensaje central:** Comparar modelos heterogéneos requiere cuidado con las escalas de importancia.

**Guion:** 

## Diapositiva 62 — Selección final: regla programada y evidencia pendiente

**Mensaje central:** La selección usada para generar Kaggle es auditable, pero la estimación seleccionada es optimista.

**Guion:** 

## Diapositiva 63 — Coincidencia en el 1% de mayor riesgo

**Mensaje central:** Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.

**Guion:** QUÉ SE HIZO: Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.

INTERPRETACIÓN: Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.

LÍMITE: La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.

**Imagen:** `outputs/figures/35_top_risk_set_overlap.png`
**Advertencia:** La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.

## Diapositiva 64 — Importancia de características

**Mensaje central:** Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.

**Guion:** QUÉ SE HIZO: Se compararon coeficientes transformados de logit e importancias internas de árboles.

INTERPRETACIÓN: Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.

LÍMITE: Importancia no significa causalidad y es difícil de comparar entre modelos.

**Imagen:** `outputs/figures/36_model_feature_importance.png`
**Advertencia:** Importancia no significa causalidad y es difícil de comparar entre modelos.

## Diapositiva 65 — Dependencia parcial: efectos aprendidos

**Mensaje central:** Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.

**Guion:** QUÉ SE HIZO: Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.

INTERPRETACIÓN: Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.

LÍMITE: Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.

**Imagen:** `outputs/figures/37_partial_dependence_models.png`
**Advertencia:** Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.

## Diapositiva 66 — Cómo cambia el riesgo con el blend

**Mensaje central:** El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.

**Guion:** QUÉ SE HIZO: Se comparó la probabilidad del mejor individuo con la combinación seleccionada.

INTERPRETACIÓN: El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.

LÍMITE: Menor dispersión no es sinónimo de mejor discriminación ni calibración.

**Imagen:** `outputs/figures/38_blend_vs_single_predictions.png`
**Advertencia:** Menor dispersión no es sinónimo de mejor discriminación ni calibración.

## Diapositiva 67 — Control de predicciones para Kaggle

**Mensaje central:** La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.

**Guion:** QUÉ SE HIZO: Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.

INTERPRETACIÓN: La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.

LÍMITE: No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.

**Imagen:** `outputs/figures/39_submission_probability_sanity.png`
**Advertencia:** No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.

## Diapositiva 68 — Exploración de hiperparámetros

**Mensaje central:** La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.

**Guion:** QUÉ SE HIZO: Se compararon configuraciones y su puntuación agregada en validación.

INTERPRETACIÓN: La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.

LÍMITE: Variar varios parámetros a la vez dificulta atribuciones causales.

**Imagen:** `outputs/figures/40_hyperparameter_effects.png`
**Advertencia:** Variar varios parámetros a la vez dificulta atribuciones causales.

## Diapositiva 69 — Estabilidad del ROC AUC por fold

**Mensaje central:** La comparación pareada muestra si las mejoras persisten o dependen de un fold.

**Guion:** QUÉ SE HIZO: Se representó cada candidato contra las cinco particiones de validación.

INTERPRETACIÓN: La comparación pareada muestra si las mejoras persisten o dependen de un fold.

LÍMITE: Cinco folds no son cinco experimentos independientes para inferencias fuertes.

**Imagen:** `outputs/figures/41_fold_auc_heatmap.png`
**Advertencia:** Cinco folds no son cinco experimentos independientes para inferencias fuertes.

## Diapositiva 70 — Espacio completo de GridSearchCV

**Mensaje central:** La visualización muestra sensibilidad del ajuste dentro de los folds internos.

**Guion:** QUÉ SE HIZO: Se registró cada combinación de profundidad, learning rate y regularización explorada.

INTERPRETACIÓN: La visualización muestra sensibilidad del ajuste dentro de los folds internos.

LÍMITE: El mejor valor interno no garantiza mejora en el fold externo.

**Imagen:** `outputs/figures/42_gridsearch_full_parameter_space.png`
**Advertencia:** El mejor valor interno no garantiza mejora en el fold externo.

## Diapositiva 71 — Efecto del ajuste sobre folds externos

**Mensaje central:** La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.

**Guion:** QUÉ SE HIZO: Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.

INTERPRETACIÓN: La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.

LÍMITE: Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.

**Imagen:** `outputs/figures/43_nested_gridsearch_outer_results.png`
**Advertencia:** Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.

## Diapositiva 72 — Qué concluye el proyecto y qué no

**Mensaje central:** El hallazgo más transferible es el procedimiento de evaluación reproducible.

**Guion:** 

## Diapositiva 73 — Limitaciones de los resultados disponibles

**Mensaje central:** Las diapositivas describen los gráficos existentes, no inventan un resultado de leaderboard.

**Guion:** 

## Diapositiva 74 — Trabajo posterior para cerrar la selección

**Mensaje central:** Estadística rigurosa = buenos modelos + trazabilidad + afirmaciones proporcionadas.

**Guion:** 

## Diapositiva 75 — Conclusión general

**Mensaje central:** EDA → hipótesis → modelos → CV → búsqueda → ensemble → decisión con incertidumbre.

**Guion:** Invitar preguntas sobre PCA, logit, la distinción bagging/blending/stacking y las decisiones de validación.

