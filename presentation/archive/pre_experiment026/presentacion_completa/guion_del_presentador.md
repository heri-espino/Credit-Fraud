# Guion de presentación · Predicción de fraude · presentación técnica completa

Los textos desarrollan el argumento de cada diapositiva. La estimación bootstrap es condicional a las predicciones OOF y no reemplaza una evaluación independiente.

## Diapositiva 1 — Predicción de fraude con tarjetas: el proceso completo

**Contexto.** EDA · modelos lineales y árboles · 5-fold CV · cuatro ensambles · resultado final

**Explicación.**  Este material distingue decisiones reproducibles, resultados exploratorios y aquello que requiere comprobación contra archivos CSV del run completo.

**Conclusión.** Se documentan la comparación completa de 19 candidatos y el segundo experimento con modelos guardados.

## Diapositiva 2 — Qué problema resolvemos y qué entregamos

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. Diferenciar clasificación probabilística, ranking y decisión binaria. El test de Kaggle carece de etiquetas públicas.

**Conclusión.** Un buen score ordena; una buena probabilidad también necesita calibración.

## Diapositiva 3 — Datos y desafío estadístico

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. La ausencia de missing no exime de usar pipelines robustos ante nuevos datos.

**Conclusión.** Fraude raro ≠ necesariamente anomalía aislada.

## Diapositiva 4 — Métricas: cada una responde otra pregunta

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. No interpretar AUC como probabilidad individual de fraude. AP depende de la prevalencia.

**Conclusión.** La métrica oficial fija el objetivo; las métricas auxiliares previenen conclusiones incompletas.

**Fórmula:** $$\mathrm{AUC}=P\!\left(s(X^+)>s(X^-)\right)$$

## Diapositiva 5 — Diseño experimental: preparación y comparación

**Contexto.** Primera fase: desde las variables originales hasta un conjunto comparable de modelos.

**Explicación.**  La línea de trabajo preserva trazabilidad y ensayos fallidos, no sólo el mejor modelo.

**Conclusión.** Las primeras decisiones fijan qué se aprende y cómo se evalúa sin fuga de información.

## Diapositiva 6 — Diseño experimental: selección y diagnóstico

**Contexto.** Segunda fase: ajustes internos, comparación de ensambles y seguimiento de resultados.

**Explicación.**  La línea de trabajo preserva trazabilidad y ensayos fallidos, no sólo el mejor modelo.

**Conclusión.** El criterio decisivo es la ROC AUC OOF, complementada por métricas de probabilidad e incertidumbre.

## Diapositiva 7 — Validación cruzada sin data leakage

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. Distinguir CV externo de 3-fold CV interno de GridSearchCV. El conjunto test de Kaggle no se usa para entrenar.

**Conclusión.** El CV permite comparar modelos con exactamente los mismos folds.

## Diapositiva 8 — ¿Por qué explorar antes de modelar?

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Las figuras de EDA ayudan a formular hipótesis, no reemplazan la validación cruzada.

## Diapositiva 9 — Balance de clases y completitud

**Contexto.** Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.

**Explicación.**  QUÉ SE HIZO: Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.

INTERPRETACIÓN: La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.

LÍMITE: El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.

**Conclusión.** La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.

**Figura:** 01_target_and_missingness.png

**Procedimiento:** Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.

**Interpretación:** La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.

**Limitación:** El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.

## Diapositiva 10 — Distribuciones numéricas

**Contexto.** Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.

**Explicación.**  QUÉ SE HIZO: Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.

INTERPRETACIÓN: Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.

LÍMITE: Una distribución sesgada no determina por sí sola utilidad predictiva.

**Conclusión.** Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.

**Figura:** 02_numeric_distributions.png

**Procedimiento:** Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.

**Interpretación:** Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.

**Limitación:** Una distribución sesgada no determina por sí sola utilidad predictiva.

## Diapositiva 11 — Distribuciones según la clase

**Contexto.** Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.

**Explicación.**  QUÉ SE HIZO: Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.

INTERPRETACIÓN: La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.

LÍMITE: Las densidades normalizadas por clase no representan la prevalencia real de fraude.

**Conclusión.** La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.

**Figura:** 03_class_conditional_densities.png

**Procedimiento:** Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.

**Interpretación:** La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.

**Limitación:** Las densidades normalizadas por clase no representan la prevalencia real de fraude.

## Diapositiva 12 — Correlaciones de Pearson y Spearman

**Contexto.** Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).

**Explicación.**  QUÉ SE HIZO: Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).

INTERPRETACIÓN: Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.

LÍMITE: Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.

**Conclusión.** Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.

**Figura:** 04_pearson_spearman_correlations.png

**Procedimiento:** Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).

**Interpretación:** Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.

**Limitación:** Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.

## Diapositiva 13 — Riesgo por categorías

**Contexto.** Se estimó la tasa observada de fraude por categoría y su soporte muestral.

**Explicación.**  QUÉ SE HIZO: Se estimó la tasa observada de fraude por categoría y su soporte muestral.

INTERPRETACIÓN: Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.

LÍMITE: Categorías con pocas observaciones pueden producir tasas muy inestables.

**Conclusión.** Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.

**Figura:** 05_categorical_risks.png

**Procedimiento:** Se estimó la tasa observada de fraude por categoría y su soporte muestral.

**Interpretación:** Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.

**Limitación:** Categorías con pocas observaciones pueden producir tasas muy inestables.

## Diapositiva 14 — Indicadores booleanos: frecuencia y riesgo

**Contexto.** Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.

**Explicación.**  QUÉ SE HIZO: Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.

INTERPRETACIÓN: Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.

LÍMITE: La asociación marginal puede desaparecer al ajustar por otros predictores.

**Conclusión.** Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.

**Figura:** 06_flag_prevalence_vs_fraud.png

**Procedimiento:** Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.

**Interpretación:** Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.

**Limitación:** La asociación marginal puede desaparecer al ajustar por otros predictores.

## Diapositiva 15 — De correlaciones a relaciones no lineales

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** El EDA motivó candidatos adicionales; su valor se decide con CV.

## Diapositiva 16 — No linealidad de las tasas de fraude

**Contexto.** Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.

**Explicación.**  QUÉ SE HIZO: Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.

INTERPRETACIÓN: Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.

LÍMITE: El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.

**Conclusión.** Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.

**Figura:** 07_nonlinear_binned_fraud_rates.png

**Procedimiento:** Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.

**Interpretación:** Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.

**Limitación:** El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.

## Diapositiva 17 — Patrones temporales de fraude

**Contexto.** Se analizaron tasas por hora, día y otras variables temporales disponibles.

**Explicación.**  QUÉ SE HIZO: Se analizaron tasas por hora, día y otras variables temporales disponibles.

INTERPRETACIÓN: Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.

LÍMITE: La agregación no prueba estabilidad futura ni sustituye una validación temporal.

**Conclusión.** Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.

**Figura:** 08_time_patterns.png

**Procedimiento:** Se analizaron tasas por hora, día y otras variables temporales disponibles.

**Interpretación:** Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.

**Limitación:** La agregación no prueba estabilidad futura ni sustituye una validación temporal.

## Diapositiva 18 — Interacciones entre variables numéricas

**Contexto.** Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.

**Explicación.**  QUÉ SE HIZO: Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.

INTERPRETACIÓN: Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.

LÍMITE: Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.

**Conclusión.** Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.

**Figura:** 09_bivariate_interaction_heatmaps.png

**Procedimiento:** Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.

**Interpretación:** Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.

**Limitación:** Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.

## Diapositiva 19 — Valores extremos: criterio IQR

**Contexto.** Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.

**Explicación.**  QUÉ SE HIZO: Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.

INTERPRETACIÓN: Los extremos pueden ser transacciones válidas y contener señal de fraude.

LÍMITE: Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.

**Conclusión.** Los extremos pueden ser transacciones válidas y contener señal de fraude.

**Figura:** 10_univariate_outliers.png

**Procedimiento:** Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.

**Interpretación:** Los extremos pueden ser transacciones válidas y contener señal de fraude.

**Limitación:** Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.

## Diapositiva 20 — Anomalías con Isolation Forest

**Contexto.** Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.

**Explicación.**  QUÉ SE HIZO: Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.

INTERPRETACIÓN: El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.

LÍMITE: No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.

**Conclusión.** El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.

**Figura:** 11_isolation_forest_anomaly_diagnostics.png

**Procedimiento:** Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.

**Interpretación:** El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.

**Limitación:** No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.

## Diapositiva 21 — Anomalía, outlier y fraude: tres conceptos

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Eliminar colas puede destruir justamente la señal que queremos detectar.

## Diapositiva 22 — Pipelines de modelos: decisiones concretas

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** La transformación se ajusta dentro del fold de entrenamiento.

## Diapositiva 23 — SVD y PCA: por qué se probaron

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. El objetivo PCA no observa Y; los resultados de clasificación determinan si ayuda.

**Conclusión.** Por eso PCA es candidato experimental, no paso obligatorio.

**Fórmula:** $$Z=U\Sigma V^\top$$

## Diapositiva 24 — ¿Por qué regresión logística?

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** L2 ayuda ante correlaciones, pero no “corrige” especificación no lineal.

**Fórmula:** $$\hat p(x)=\frac{1}{1+\exp[-(\beta_0+\beta^\top x)]}$$

## Diapositiva 25 — ¿Se satisfacen los supuestos de logit?

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** La utilidad predictiva no equivale a validez causal de coeficientes.

## Diapositiva 26 — ¿Qué aporta el spline logístico?

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Probar una no linealidad específica es más informativo que añadir complejidad indiscriminada.

**Fórmula:** $$f(x)=\beta_0+\sum_{k=1}^{K}\gamma_k B_k(x)$$

## Diapositiva 27 — Random forest: bagging dentro de una familia

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Este sí es un mecanismo tipo bagging, a diferencia del blend posterior.

## Diapositiva 28 — XGBoost: árboles que corrigen errores

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Se conserva el mismo esquema de evaluación, sin favorecer a un algoritmo por hardware.

**Fórmula:** $$f_m(x)=f_{m-1}(x)+\eta h_m(x)$$

## Diapositiva 29 — CatBoost: otra forma de boosting

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Diferentes sesgos inductivos merecen comparación directa, no suposiciones de superioridad.

## Diapositiva 30 — Diseño de candidatos e hiperparámetros

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** En modo rápido el notebook reduce tanto filas como hiperparámetros; no mezclar esos scores con el full run.

## Diapositiva 31 — Comparación de candidatos en cinco folds

**Contexto.** Se calcularon ROC AUC out-of-fold por candidato y por partición.

**Explicación.**  QUÉ SE HIZO: Se calcularon ROC AUC out-of-fold por candidato y por partición.

INTERPRETACIÓN: El desempeño medio debe juzgarse junto con su variación entre particiones y familias.

LÍMITE: La elección del máximo dentro del mismo CV introduce optimismo de selección.

**Conclusión.** El desempeño medio debe juzgarse junto con su variación entre particiones y familias.

**Figura:** 12_candidate_scores_and_folds.png

**Procedimiento:** Se calcularon ROC AUC out-of-fold por candidato y por partición.

**Interpretación:** El desempeño medio debe juzgarse junto con su variación entre particiones y familias.

**Limitación:** La elección del máximo dentro del mismo CV introduce optimismo de selección.

## Diapositiva 32 — Correlación entre modelos

**Contexto.** Se compararon los vectores de probabilidades OOF de todos los candidatos.

**Explicación.**  QUÉ SE HIZO: Se compararon los vectores de probabilidades OOF de todos los candidatos.

INTERPRETACIÓN: Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.

LÍMITE: Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.

**Conclusión.** Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.

**Figura:** 13_oof_prediction_correlations.png

**Procedimiento:** Se compararon los vectores de probabilidades OOF de todos los candidatos.

**Interpretación:** Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.

**Limitación:** Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.

## Diapositiva 33 — Modelo individual frente a combinaciones

**Contexto.** Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.

**Explicación.**  QUÉ SE HIZO: Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.

INTERPRETACIÓN: Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.

LÍMITE: El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.

**Conclusión.** Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.

**Figura:** 14_ensemble_comparisons.png

**Procedimiento:** Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.

**Interpretación:** Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.

**Limitación:** El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.

## Diapositiva 34 — Curvas ROC y precisión–recobrado

**Contexto.** Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.

**Explicación.**  QUÉ SE HIZO: Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.

INTERPRETACIÓN: ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.

LÍMITE: Ninguna curva fija por sí sola un umbral operativo.

**Conclusión.** ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.

**Figura:** 15_oof_roc_pr_curves.png

**Procedimiento:** Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.

**Interpretación:** ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.

**Limitación:** Ninguna curva fija por sí sola un umbral operativo.

## Diapositiva 35 — SVD/PCA: 90% de varianza

**Contexto.** Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.

**Explicación.**  QUÉ SE HIZO: Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.

INTERPRETACIÓN: La reducción es una alternativa de representación, no una mejora predictiva garantizada.

LÍMITE: La varianza de X y la información predictiva sobre Y son objetivos distintos.

**Conclusión.** La reducción es una alternativa de representación, no una mejora predictiva garantizada.

**Figura:** 16_pca_explained_variance.png

**Procedimiento:** Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.

**Interpretación:** La reducción es una alternativa de representación, no una mejora predictiva garantizada.

**Limitación:** La varianza de X y la información predictiva sobre Y son objetivos distintos.

## Diapositiva 36 — Supuestos logísticos y posibles cambios

**Contexto.** Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.

**Explicación.**  QUÉ SE HIZO: Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.

INTERPRETACIÓN: Es necesario separar problemas de especificación, dependencia y cambios de distribución.

LÍMITE: Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.

**Conclusión.** Es necesario separar problemas de especificación, dependencia y cambios de distribución.

**Figura:** 17_assumptions_vif_and_feature_shift.png

**Procedimiento:** Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.

**Interpretación:** Es necesario separar problemas de especificación, dependencia y cambios de distribución.

**Limitación:** Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.

## Diapositiva 37 — Diagnóstico de la regresión logística

**Contexto.** Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.

**Explicación.**  QUÉ SE HIZO: Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.

INTERPRETACIÓN: Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.

LÍMITE: Predictores normales y homocedasticidad NO son supuestos requeridos para logit.

**Conclusión.** Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.

**Figura:** 18_oof_logistic_assumption_checks.png

**Procedimiento:** Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.

**Interpretación:** Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.

**Limitación:** Predictores normales y homocedasticidad NO son supuestos requeridos para logit.

## Diapositiva 38 — Corregir el logit con XGBoost

**Contexto.** Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.

**Explicación.**  QUÉ SE HIZO: Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.

INTERPRETACIÓN: Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.

LÍMITE: No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.

**Conclusión.** Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.

**Figura:** 19_logistic_offset_boosting_diagnostics.png

**Procedimiento:** Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.

**Interpretación:** Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.

**Limitación:** No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.

## Diapositiva 39 — Blending y bagging: cómo evolucionó la idea inicial

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Término preciso de la realización: blending entre familias heterogéneas.

## Diapositiva 40 — Stacking con random forest: segundo experimento

**Contexto.** El stacking sí se implementó posteriormente en un segundo notebook, utilizando sólo probabilidades de modelos base.

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Resultado OOF del stacking: ROC AUC 0.945747; average precision 0.506383.

## Diapositiva 41 — Logit + booster de corrección en escala logit

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Es una composición aditiva sobre el logit, NO stacking con meta-logit.

**Fórmula:** $$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$

## Diapositiva 42 — Por qué conservar modelos que no ganaron

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** La selección sobre OOF es exploratoria y no representa una evaluación completamente intacta.

## Diapositiva 43 — EDA extendido: qué más investigamos

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Cada gráfico sirve para generar preguntas, no para ajustar modelos sobre el test.

## Diapositiva 44 — Valor discriminativo de cada variable

**Contexto.** Se estimó el AUC de predictores aislados y se compararon señales univariantes.

**Explicación.**  QUÉ SE HIZO: Se estimó el AUC de predictores aislados y se compararon señales univariantes.

INTERPRETACIÓN: El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.

LÍMITE: Un AUC univariante alto no asegura contribución incremental.

**Conclusión.** El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.

**Figura:** 20_univariate_feature_discrimination.png

**Procedimiento:** Se estimó el AUC de predictores aislados y se compararon señales univariantes.

**Interpretación:** El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.

**Limitación:** Un AUC univariante alto no asegura contribución incremental.

## Diapositiva 45 — Distribuciones acumuladas por clase

**Contexto.** Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.

**Explicación.**  QUÉ SE HIZO: Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.

INTERPRETACIÓN: Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.

LÍMITE: Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.

**Conclusión.** Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.

**Figura:** 21_class_conditional_ecdfs.png

**Procedimiento:** Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.

**Interpretación:** Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.

**Limitación:** Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.

## Diapositiva 46 — Categorías × indicadores booleanos

**Contexto.** Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.

**Explicación.**  QUÉ SE HIZO: Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.

INTERPRETACIÓN: Una misma bandera puede tener distinta asociación con el fraude según su contexto.

LÍMITE: En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.

**Conclusión.** Una misma bandera puede tener distinta asociación con el fraude según su contexto.

**Figura:** 22_categorical_flag_interactions.png

**Procedimiento:** Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.

**Interpretación:** Una misma bandera puede tener distinta asociación con el fraude según su contexto.

**Limitación:** En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.

## Diapositiva 47 — Mapa de riesgo por día y hora

**Contexto.** Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.

**Explicación.**  QUÉ SE HIZO: Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.

INTERPRETACIÓN: Puede haber concentraciones temporales no captadas por términos horarios aislados.

LÍMITE: La composición de transacciones puede explicar parte del efecto observado.

**Conclusión.** Puede haber concentraciones temporales no captadas por términos horarios aislados.

**Figura:** 23_weekly_hourly_fraud_surface.png

**Procedimiento:** Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.

**Interpretación:** Puede haber concentraciones temporales no captadas por términos horarios aislados.

**Limitación:** La composición de transacciones puede explicar parte del efecto observado.

## Diapositiva 48 — Geometría bivariante por clase

**Contexto.** Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.

**Explicación.**  QUÉ SE HIZO: Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.

INTERPRETACIÓN: Los patrones de separación multivariada justifican no depender solo de un predictor.

LÍMITE: Las muestras de visualización no deben confundirse con la distribución completa.

**Conclusión.** Los patrones de separación multivariada justifican no depender solo de un predictor.

**Figura:** 24_pairwise_class_geometry.png

**Procedimiento:** Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.

**Interpretación:** Los patrones de separación multivariada justifican no depender solo de un predictor.

**Limitación:** Las muestras de visualización no deben confundirse con la distribución completa.

## Diapositiva 49 — Comparación entrenamiento–prueba

**Contexto.** Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.

**Explicación.**  QUÉ SE HIZO: Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.

INTERPRETACIÓN: Permite detectar cambios marginales antes de enviar predicciones a Kaggle.

LÍMITE: Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.

**Conclusión.** Permite detectar cambios marginales antes de enviar predicciones a Kaggle.

**Figura:** 25_train_test_ecdf_shift.png

**Procedimiento:** Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.

**Interpretación:** Permite detectar cambios marginales antes de enviar predicciones a Kaggle.

**Limitación:** Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.

## Diapositiva 50 — De la métrica de Kaggle a una operación real

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** No hay una única métrica que responda todos los usos.

## Diapositiva 51 — Validación de umbrales y presupuesto

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Estas políticas son evaluadas; no deben confundirse con entrenamiento distinto.

## Diapositiva 52 — Comparación con cuatro métricas

**Contexto.** Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.

**Explicación.**  QUÉ SE HIZO: Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.

INTERPRETACIÓN: La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.

LÍMITE: Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.

**Conclusión.** La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.

**Figura:** 26_four_metric_model_scorecard.png

**Procedimiento:** Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.

**Interpretación:** La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.

**Limitación:** Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.

## Diapositiva 53 — Rendimiento frente a costo computacional

**Contexto.** Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.

**Explicación.**  QUÉ SE HIZO: Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.

INTERPRETACIÓN: Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.

LÍMITE: Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.

**Conclusión.** Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.

**Figura:** 27_performance_vs_training_time.png

**Procedimiento:** Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.

**Interpretación:** Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.

**Limitación:** Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.

## Diapositiva 54 — Distribuciones de riesgo predicho

**Contexto.** Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.

**Explicación.**  QUÉ SE HIZO: Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.

INTERPRETACIÓN: La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.

LÍMITE: Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.

**Conclusión.** La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.

**Figura:** 28_oof_score_distributions.png

**Procedimiento:** Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.

**Interpretación:** La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.

**Limitación:** Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.

## Diapositiva 55 — Ganancia acumulada y lift

**Contexto.** Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.

**Explicación.**  QUÉ SE HIZO: Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.

INTERPRETACIÓN: La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.

LÍMITE: Las curvas no incluyen el costo real de las investigaciones o falsos positivos.

**Conclusión.** La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.

**Figura:** 29_cumulative_gains_and_lift.png

**Procedimiento:** Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.

**Interpretación:** La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.

**Limitación:** Las curvas no incluyen el costo real de las investigaciones o falsos positivos.

## Diapositiva 56 — Precisión y recobrado con capacidad limitada

**Contexto.** Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.

**Explicación.**  QUÉ SE HIZO: Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.

INTERPRETACIÓN: Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.

LÍMITE: La mejor fracción a revisar depende de costos externos ausentes del dataset.

**Conclusión.** Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.

**Figura:** 30_precision_recall_at_review_budget.png

**Procedimiento:** Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.

**Interpretación:** Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.

**Limitación:** La mejor fracción a revisar depende de costos externos ausentes del dataset.

## Diapositiva 57 — Errores según política de decisión

**Contexto.** Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.

**Explicación.**  QUÉ SE HIZO: Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.

INTERPRETACIÓN: Un mismo clasificador puede producir decisiones muy distintas según la política.

LÍMITE: No se deben comparar matrices sin especificar su regla de umbral.

**Conclusión.** Un mismo clasificador puede producir decisiones muy distintas según la política.

**Figura:** 31_confusion_matrices_by_policy.png

**Procedimiento:** Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.

**Interpretación:** Un mismo clasificador puede producir decisiones muy distintas según la política.

**Limitación:** No se deben comparar matrices sin especificar su regla de umbral.

## Diapositiva 58 — Confiabilidad de las probabilidades

**Contexto.** Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.

**Explicación.**  QUÉ SE HIZO: Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.

INTERPRETACIÓN: Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.

LÍMITE: Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.

**Conclusión.** Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.

**Figura:** 32_model_reliability_comparison.png

**Procedimiento:** Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.

**Interpretación:** Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.

**Limitación:** Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.

## Diapositiva 59 — Calibración e incertidumbre

**Contexto.** Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.

**Explicación.**  QUÉ SE HIZO: Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.

INTERPRETACIÓN: Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.

LÍMITE: Los intervalos son descriptivos y dependen del particionado de riesgo.

**Conclusión.** Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.

**Figura:** 33_calibration_with_wilson_intervals.png

**Procedimiento:** Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.

**Interpretación:** Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.

**Limitación:** Los intervalos son descriptivos y dependen del particionado de riesgo.

## Diapositiva 60 — Rendimiento por canal

**Contexto.** Se evaluaron métricas OOF desagregadas por canal de transacción.

**Explicación.**  QUÉ SE HIZO: Se evaluaron métricas OOF desagregadas por canal de transacción.

INTERPRETACIÓN: La calidad global puede esconder subgrupos con menos capacidad discriminativa.

LÍMITE: Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.

**Conclusión.** La calidad global puede esconder subgrupos con menos capacidad discriminativa.

**Figura:** 34_subgroups_channel.png

**Procedimiento:** Se evaluaron métricas OOF desagregadas por canal de transacción.

**Interpretación:** La calidad global puede esconder subgrupos con menos capacidad discriminativa.

**Limitación:** Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.

## Diapositiva 61 — Rendimiento por categoría de comercio

**Contexto.** Se comparó ROC AUC y AP por categorías de comercio.

**Explicación.**  QUÉ SE HIZO: Se comparó ROC AUC y AP por categorías de comercio.

INTERPRETACIÓN: Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.

LÍMITE: La tasa base difiere entre grupos y afecta de manera importante a AP.

**Conclusión.** Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.

**Figura:** 34_subgroups_merchant_category.png

**Procedimiento:** Se comparó ROC AUC y AP por categorías de comercio.

**Interpretación:** Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.

**Limitación:** La tasa base difiere entre grupos y afecta de manera importante a AP.

## Diapositiva 62 — Interpretabilidad: distinguir asociación y explicación

**Contexto.** 

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Comparar modelos heterogéneos requiere cuidado con las escalas de importancia.

## Diapositiva 63 — Cómo se cerró la comparación final

**Contexto.** Con la extensión de ensambles se compararon cinco vectores de predicciones OOF de 699,960 observaciones.

**Explicación.** En esta etapa se contrastó una hipótesis concreta del procedimiento; la conclusión se basa en predicciones fuera de fold y no en el ajuste dentro de la muestra. 

**Conclusión.** Ahora contamos con los CSV del experimento final; los valores no proceden de leer el ancho de barras.

## Diapositiva 64 — Coincidencia en el 1% de mayor riesgo

**Contexto.** Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.

**Explicación.**  QUÉ SE HIZO: Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.

INTERPRETACIÓN: Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.

LÍMITE: La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.

**Conclusión.** Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.

**Figura:** 35_top_risk_set_overlap.png

**Procedimiento:** Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.

**Interpretación:** Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.

**Limitación:** La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.

## Diapositiva 65 — Importancia de características

**Contexto.** Se compararon coeficientes transformados de logit e importancias internas de árboles.

**Explicación.**  QUÉ SE HIZO: Se compararon coeficientes transformados de logit e importancias internas de árboles.

INTERPRETACIÓN: Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.

LÍMITE: Importancia no significa causalidad y es difícil de comparar entre modelos.

**Conclusión.** Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.

**Figura:** 36_model_feature_importance.png

**Procedimiento:** Se compararon coeficientes transformados de logit e importancias internas de árboles.

**Interpretación:** Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.

**Limitación:** Importancia no significa causalidad y es difícil de comparar entre modelos.

## Diapositiva 66 — Dependencia parcial: efectos aprendidos

**Contexto.** Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.

**Explicación.**  QUÉ SE HIZO: Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.

INTERPRETACIÓN: Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.

LÍMITE: Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.

**Conclusión.** Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.

**Figura:** 37_partial_dependence_models.png

**Procedimiento:** Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.

**Interpretación:** Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.

**Limitación:** Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.
## Diapositiva 67 — Cómo cambia el riesgo con el blend

**Contexto.** Se comparó la probabilidad del mejor individuo con la combinación seleccionada.

**Explicación.**  QUÉ SE HIZO: Se comparó la probabilidad del mejor individuo con la combinación seleccionada.

INTERPRETACIÓN: El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.

LÍMITE: Menor dispersión no es sinónimo de mejor discriminación ni calibración.

**Conclusión.** El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.

**Figura:** 38_blend_vs_single_predictions.png

**Procedimiento:** Se comparó la probabilidad del mejor individuo con la combinación seleccionada.

**Interpretación:** El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.

**Limitación:** Menor dispersión no es sinónimo de mejor discriminación ni calibración.

## Diapositiva 68 — Control de predicciones para Kaggle

**Contexto.** Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.

**Explicación.**  QUÉ SE HIZO: Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.

INTERPRETACIÓN: La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.

LÍMITE: No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.

**Conclusión.** La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.

**Figura:** 39_submission_probability_sanity.png

**Procedimiento:** Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.

**Interpretación:** La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.

**Limitación:** No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.

## Diapositiva 69 — Exploración de hiperparámetros

**Contexto.** Se compararon configuraciones y su puntuación agregada en validación.

**Explicación.**  QUÉ SE HIZO: Se compararon configuraciones y su puntuación agregada en validación.

INTERPRETACIÓN: La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.

LÍMITE: Variar varios parámetros a la vez dificulta atribuciones causales.

**Conclusión.** La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.

**Figura:** 40_hyperparameter_effects.png

**Procedimiento:** Se compararon configuraciones y su puntuación agregada en validación.

**Interpretación:** La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.

**Limitación:** Variar varios parámetros a la vez dificulta atribuciones causales.

## Diapositiva 70 — Estabilidad del ROC AUC por fold

**Contexto.** Se representó cada candidato contra las cinco particiones de validación.

**Explicación.**  QUÉ SE HIZO: Se representó cada candidato contra las cinco particiones de validación.

INTERPRETACIÓN: La comparación pareada muestra si las mejoras persisten o dependen de un fold.

LÍMITE: Cinco folds no son cinco experimentos independientes para inferencias fuertes.

**Conclusión.** La comparación pareada muestra si las mejoras persisten o dependen de un fold.

**Figura:** 41_fold_auc_heatmap.png

**Procedimiento:** Se representó cada candidato contra las cinco particiones de validación.

**Interpretación:** La comparación pareada muestra si las mejoras persisten o dependen de un fold.

**Limitación:** Cinco folds no son cinco experimentos independientes para inferencias fuertes.

## Diapositiva 71 — Espacio completo de GridSearchCV

**Contexto.** Se registró cada combinación de profundidad, learning rate y regularización explorada.

**Explicación.**  QUÉ SE HIZO: Se registró cada combinación de profundidad, learning rate y regularización explorada.

INTERPRETACIÓN: La visualización muestra sensibilidad del ajuste dentro de los folds internos.

LÍMITE: El mejor valor interno no garantiza mejora en el fold externo.

**Conclusión.** La visualización muestra sensibilidad del ajuste dentro de los folds internos.

**Figura:** 42_gridsearch_full_parameter_space.png

**Procedimiento:** Se registró cada combinación de profundidad, learning rate y regularización explorada.

**Interpretación:** La visualización muestra sensibilidad del ajuste dentro de los folds internos.

**Limitación:** La búsqueda se ajustó en los folds internos. Los resultados exactos del XGBoost de grid sólo se podrán comparar con offset al recuperar el vector OOF original.

## Diapositiva 72 — Efecto del ajuste sobre folds externos

**Contexto.** Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.

**Explicación.**  QUÉ SE HIZO: Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.

INTERPRETACIÓN: La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.

LÍMITE: Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.

**Conclusión.** La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.

**Figura:** 43_nested_gridsearch_outer_results.png

**Procedimiento:** Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.

**Interpretación:** La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.

**Limitación:** La búsqueda se ajustó en los folds internos. Los resultados exactos del XGBoost de grid sólo se podrán comparar con offset al recuperar el vector OOF original.

## Diapositiva 73 — Segundo notebook: aprovechar los modelos ya entrenados

**Contexto.** La extensión reutilizó all_candidate_predictions.npz y los cinco modelos logísticos guardados.

**Explicación.**  Mencionar que los 699,960 registros corresponden al train; el test tiene 299,984 y no posee etiqueta pública.

**Conclusión.** Se conservaron las comparaciones originales y se añadieron los ensambles sin repetir el entrenamiento más costoso.

## Diapositiva 74 — Referencia: el mejor modelo entrenado sin ensamble

**Contexto.** Se tomó el candidato con mayor ROC AUC OOF entre los modelos individuales, no el mejor modelo por intuición.

**Explicación.** La mejor referencia individual en los CSV es un XGBoost fijo. El modelo XGBoost con GridSearchCV fue evaluado en el notebook principal, pero el ZIP de ensambles no contiene sus predicciones para verificar su AUC exacta en esta nueva comparación. 

**Conclusión.** Esta referencia permite medir el beneficio adicional de construir un segundo nivel de aprendizaje.

## Diapositiva 75 — Diseño final: cuatro ensambles frente al mejor individuo

**Contexto.** Las cinco estrategias se compararon en las mismas observaciones y con métricas calculadas sobre probabilidades OOF.

**Explicación.**  

**Conclusión.** Bagging clásico, blending y stacking describen procedimientos distintos; aquí hay cuatro ensambles definidos.

## Diapositiva 76 — E1: promedio de probabilidades

**Contexto.** Se tomaron ocho modelos de familias distintas y se calculó el promedio simple de sus probabilidades.

**Explicación.**  

**Conclusión.** Mezclar predicciones correlacionadas puede reducir el contraste entre operaciones de alto y bajo riesgo.

**Fórmula:** $$\hat p_{\mathrm{blend}}(x)=\frac{1}{8}\sum_{k=1}^{8}\hat p_k(x)$$

## Diapositiva 77 — E2: boosting con logit como condición inicial

**Contexto.** En lugar de sustituir la respuesta por residuos, se proporciona a XGBoost un punto inicial específico por observación.

**Explicación.**  

**Conclusión.** El gradiente corresponde al error de probabilidad inicial; XGBoost también utiliza la curvatura de la pérdida.

**Fórmula:** $$\hat p(x)=\sigma\!\left(f_{\mathrm{LR}}(x)+g_{\mathrm{XGB}}(x)\right)$$

## Diapositiva 78 — E3: XGBoost entrenado sobre residuos explícitos

**Contexto.** Se probó literalmente ajustar un segundo modelo a los errores de probabilidad de la regresión logística.

**Explicación.**  

**Conclusión.** La formulación residual tuvo peor ROC AUC que el modelo individual y que el corrección del logit con XGBoost.

**Fórmula:** $$\hat p(x)=\operatorname{clip}\!\left(\hat p_{\mathrm{LR}}(x)+g(x),0,1\right)$$

## Diapositiva 79 — Por qué E2 y E3 no son equivalentes

**Contexto.** Ambos métodos parten de logit, pero cambian la función objetivo y la escala de la corrección.

**Explicación.**  

**Conclusión.** Los dos experimentos se realizaron; sólo corrección del logit con XGBoost mejoró marginalmente al mejor modelo individual.

## Diapositiva 80 — E4: stacking con random forest

**Contexto.** El bosque no recibe las 24 variables originales: aprende sobre las probabilidades producidas por 17 modelos.

**Explicación.**  

**Conclusión.** El resultado es cercano al mejor XGBoost, con mejor AP, pero ligeramente menor ROC AUC.

**Fórmula:** $$z_i=\left(\hat p_1(x_i),\ldots,\hat p_{17}(x_i)\right)$$

## Diapositiva 81 — Limitación del stacking con OOF reutilizados

**Contexto.** Las probabilidades base de cada fila son OOF, pero la validación del bosque meta no es completamente anidada.

**Explicación.**  

**Conclusión.** La diferencia pequeña entre stacking y el mejor individuo debe leerse con esta reserva.

## Diapositiva 82 — Resultado final: ROC AUC y AP

**Contexto.** 

**Explicación.**  Explicar las posiciones relativas y la escala ampliada de ROC AUC.

**Conclusión.** La comparación directa favorece a logit-offset en AUC y AP; el mejor XGBoost individual queda a 0.000085 de AUC.

**Figura:** 44_resumen_ensambles_es.png

**Procedimiento:** Se compararon las predicciones fuera de fold del mejor modelo individual y de cuatro ensambles.

**Interpretación:** La comparación directa favorece a logit-offset en AUC y AP; el mejor XGBoost individual queda a 0.000085 de AUC.

**Limitación:** Las diferencias son pequeñas y la elección se realizó con las mismas predicciones OOF utilizadas para comparar.

## Diapositiva 83 — Cuatro métricas para cinco métodos

**Contexto.** 

**Explicación.**  Se debe distinguir ranking, precisión de positivos y calidad de probabilidades.

**Conclusión.** Offset boosting obtiene 0.946205 de AUC, 0.507424 de AP, 0.045798 de log loss y 0.011051 de Brier.

**Figura:** 46_01_five_way_metric_scorecard.png

**Procedimiento:** Se calcularon ROC AUC, average precision, log loss y Brier sobre las cinco series de predicciones OOF.

**Interpretación:** Offset boosting obtiene 0.946205 de AUC, 0.507424 de AP, 0.045798 de log loss y 0.011051 de Brier.

**Limitación:** La escala de cada panel es distinta. Comparar magnitudes y no sólo las posiciones de las barras.

## Diapositiva 84 — Curvas ROC y precisión–recobrado

**Contexto.** 

**Explicación.**  Prohibido extrapolar a la muestra privada de test sin etiquetar.

**Conclusión.** Las diferencias son visualmente pequeñas, aun cuando el orden exacto se pueda calcular con seis decimales.

**Figura:** 47_02_roc_precision_recall.png

**Procedimiento:** Se generaron curvas a partir de las predicciones OOF de todos los métodos.

**Interpretación:** Las diferencias son visualmente pequeñas, aun cuando el orden exacto se pueda calcular con seis decimales.

**Limitación:** Estas curvas describen la misma base utilizada para seleccionar el modelo; no corresponden a la prueba privada de Kaggle.

## Diapositiva 85 — Residuos y variables meta del stacking

**Contexto.** 

**Explicación.**  Las importancias no son efectos causales; cada nuevo nivel de complejidad puede sobreajustar.

**Conclusión.** El XGBRegressor hizo correcciones pequeñas en probabilidad; el bosque meta se apoyó más en XGBoost y CatBoost.

**Figura:** 48_03_residual_corrections_and_stacking.png

**Procedimiento:** Se examinó el cambio de probabilidad del modelo residual y las importancias del random forest meta-modelo.

**Interpretación:** El XGBRegressor hizo correcciones pequeñas en probabilidad; el bosque meta se apoyó más en XGBoost y CatBoost.

**Limitación:** Las importancias son descriptivas y no constituyen efectos causales ni garantizan una mejora independiente.

## Diapositiva 86 — Evolución del ROC AUC por fold

**Contexto.** 

**Explicación.**  No tratar cinco folds como cinco repeticiones independientes.

**Conclusión.** Los perfiles de las cinco estrategias siguen un patrón parecido; offset no supera al mejor individuo en todos los folds.

**Figura:** 49_04_fold_stability.png

**Procedimiento:** Se comparó el ROC AUC de cada estrategia por fold original.

**Interpretación:** Los perfiles de las cinco estrategias siguen un patrón parecido; offset no supera al mejor individuo en todos los folds.

**Limitación:** Cinco folds no equivalen a cinco experimentos independientes; las mismas observaciones intervienen en el ajuste de hiperparámetros.

## Diapositiva 87 — Incertidumbre de la diferencia de AUC

**Contexto.** 

**Explicación.**  Estos límites proceden del CSV suministrado; no son evidencia de significancia ni prueba de generalización.

**Conclusión.** El rango exploratorio para offset es [−0.000615, +0.001010]; incluye cero.

**Figura:** 45_diferencias_auc_ensambles_es.png

**Procedimiento:** Se recuperaron los intervalos exploratorios de diferencias emparejadas respecto al mejor XGBoost individual.

**Interpretación:** El rango exploratorio para offset es [−0.000615, +0.001010]; incluye cero.

**Limitación:** Los valores proceden del archivo paired_auc_difference_exploratory.csv; no representan evaluación independiente.

## Diapositiva 88 — Bootstrap emparejado: comparación con el XGBoost individual

**Contexto.** Bootstrap estratificado, 600 réplicas sobre las mismas 699,960 transacciones.

**Explicación.**  Se usan 600 remuestreos pareados de las clases. Es un análisis condicional a la selección previa por OOF; no demuestra generalización ni controla dependencia entre cuentas. El XGBoost ajustado con GridSearchCV requiere la predicción xgb_nested_grid__oof, que no está en el ZIP suministrado.

**Conclusión.** La ganancia de +0.000085 de ROC AUC de la corrección logística no excluye cero.

**Figura:** 50_bootstrap_pareado_auc.png

**Procedimiento:** Se ejecutó un bootstrap emparejado y estratificado con 600 réplicas, usando las mismas filas remuestreadas para todos los métodos. Se preservó el número de fraudes y no fraudes.

**Interpretación:** Diferencia entre corrección del logit y XGBoost individual: +0.000085 de ROC AUC; intervalo percentil del 95%: [−0.000263, +0.000440]. Incluye cero.

**Limitación:** La referencia numérica disponible es el XGBoost fijo de profundidad 5; el XGBoost ajustado con GridSearchCV no está en los archivos OOF recibidos. La nueva notebook lo incluirá cuando recupere sus predicciones.

## Diapositiva 89 — Resultado: ganador según la regla programada

**Contexto.** La regla de selección escoge el mayor ROC AUC OOF entre las cinco estrategias comparadas.

**Explicación.**  

**Conclusión.** La mayor complejidad no produjo una mejora concluyente frente a XGBoost individual.

**Fórmula:** $$\Delta\mathrm{AUC}=0.946205-0.946120=0.000085$$

## Diapositiva 90 — Qué concluye la ejecución completa

**Contexto.** Ahora disponemos del comparativo agregado del experimento con cuatro ensambles.

**Explicación.**  

**Conclusión.** El objetivo no fue demostrar que un ensamble siempre supera al mejor modelo individual.

## Diapositiva 91 — Limitaciones del diseño comparativo

**Contexto.** La extensión sí cuenta con resultados numéricos completos, pero no con una prueba independiente para valorar la selección.

**Explicación.**  

**Conclusión.** Una nueva evaluación independiente permitiría decidir si el segundo modelo aporta valor real.

## Diapositiva 92 — Siguientes pasos de evaluación

**Contexto.** Conservar ambas alternativas: la arquitectura ganadora por OOF y el modelo individual casi equivalente.

**Explicación.**  

**Conclusión.** La comparación es reproducible y su resultado es claro; la magnitud de la mejora exige una validación adicional.

## Diapositiva 93 — Conclusión

**Contexto.** El método elegido es regresión logística corregida con XGBoost por ROC AUC OOF, pero su ventaja es mínima respecto a XGBoost individual.

**Explicación.**  Invitar preguntas sobre PCA, logit, la distinción bagging/blending/stacking y las decisiones de validación.

**Conclusión.** Selección documentada: 0.946205 frente a 0.946120. No se afirma superioridad estadística ni resultado de leaderboard.