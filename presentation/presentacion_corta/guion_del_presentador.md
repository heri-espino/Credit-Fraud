# Guion · experiment024

No afirmar significancia estadística ni score Kaggle.

## 1. Portada
Presentar el problema antes de revelar el resultado.

## 2. ¿Qué queremos predecir?

Una transacción puede ser legítima o fraudulenta. Buscamos estimar su probabilidad de fraude.

$$\hat p(x)\approx P(Y=1\mid X=x),\quad Y\in\{0,1\}.$$

- **Entrada:** variables observadas de la transacción, sin usar el identificador.
- **Salida:** probabilidad entre 0 y 1 por cada fila de prueba.
- **Objetivo:** maximizar ROC AUC, métrica de Kaggle.
- **Decisión operativa:** convertir la probabilidad en una alerta sólo si se define un umbral.

## 3. ¿Con qué información contamos?

| Conjunto | Observaciones | Etiqueta |
|---|---:|---|
| Entrenamiento | 699 960 | is_fraud (0/1) |
| Prueba | 299 984 | Desconocida |

**24 predictores:** 13 numéricos (monto, saldo, velocidad, riesgo, tiempo, etc.), 5 categóricos (comercio, tarjeta, autenticación, canal y dispositivo) y 6 booleanos (banderas de riesgo). El campo id sólo identifica filas.

## 4. ¿Por qué ROC AUC y no exactitud?

$$\mathrm{AUC}=P(s(X^+)>s(X^-))+\tfrac12 P(s(X^+)=s(X^-)).$$

- **ROC AUC:** capacidad de ordenar fraudes por encima de legítimas.
- **Average precision (AP):** resume precisión–recall; referencia aleatoria = prevalencia.
- **Log loss / Brier:** evalúan probabilidades, no sólo ranking.
- **Recall, precisión y F1:** dependen de un umbral.

La exactitud puede ser engañosa cuando la clase positiva es rara.

## 5. Desbalance y valores faltantes

**Lectura:** Distribución de is_fraud y porcentaje de faltantes.

**Resultado:** 11 689 fraudes (1,67 %) y 688 271 legítimas (98,33 %). No se observan faltantes.

**Alcance:** Predecir siempre legítima da 98,33 % de exactitud pero recall cero.

## 6. Distribuciones numéricas

**Lectura:** Histogramas de seis variables en una muestra.

**Resultado:** Monto, saldo y tiempo presentan asimetrías; velocidad y riesgo tienen otras escalas.

**Alcance:** No se eliminan automáticamente valores extremos.

## 7. Correlación de Spearman

**Lectura:** Asociación monótona de numéricas y booleanas.

**Resultado:** Predominan correlaciones bajas, con asociaciones localizadas.

**Alcance:** No descarta interacciones ni relaciones no monótonas.

## 8. Fraude por categoría y canal

**Lectura:** Tasas por grupo sobre el entrenamiento completo.

**Resultado:** Gift Cards, Crypto Exchange y Gaming muestran tasas superiores a la referencia; los canales varían menos.

**Alcance:** Interpretar con tamaños de grupo; no son efectos causales.

## 9. Relaciones no lineales

**Lectura:** Tasas observadas por doce cuantiles.

**Resultado:** Velocidad y riesgo del comercio muestran aumentos pronunciados en los cuantiles altos.

**Alcance:** La tasa marginal no equivale a la relación multivariable.

## 10. Interacciones entre predictores

**Lectura:** Tasas conjuntas por quintiles.

**Resultado:** La celda de mayor velocidad y riesgo comercial alcanza 9,10 % de fraude.

**Alcance:** Las interacciones motivan árboles; no prueban causalidad.

## 11. Anomalías multivariantes

**Lectura:** Distribución de puntuaciones de Isolation Forest por clase.

**Resultado:** Fraudes tienden a scores de anomalía mayores; existe solapamiento.

**Alcance:** Diagnóstico descriptivo, no predictor del pipeline.

## 12. Del diagnóstico a las hipótesis

- Diferencias de escala → comparar estandarización con datos sin escalar.
- No linealidades e interacciones → comparar logística y árboles.
- Anomalías y vecindades → construir características geométricas mediante clustering.
- Desbalance → estratificación, ROC AUC y métricas de alertas.

**Las decisiones se contrastan mediante validación cruzada; el EDA no demuestra superioridad de ningún modelo.**

## 13. El flujo metodológico del notebook

   

## 14. Imputación, one-hot y estandarización

$$z_j=\frac{x_j-\hat\mu_j}{\hat\sigma_j}.$$

- Numéricas: mediana y escalado opcional.
- Booleanas: 0/1 e imputación por moda.
- Categóricas: moda y one-hot encoding; niveles desconocidos ignorados.
- Raw conserva la escala original de numéricas, pero también usa one-hot.

**Todas las transformaciones se ajustan únicamente en el entrenamiento de cada split.**

## 15. PCA: retener 90 % de la varianza

**Lectura:** Varianza acumulada y proyección ilustrativa en dos dimensiones.

**Resultado:** Las clases se solapan; PCA 90 % permite construir distancias de clustering.

**Alcance:** Se reajusta por split; no es un quinto candidato de representación.

## 16. K-means: distancias a centroides

$$\min_{\mu_1,\ldots,\mu_k}\sum_i\min_j\|z_i-\mu_j\|_2^2.$$

- Geometría PCA sobre datos estandarizados; referencia de hasta 15 000 filas del entrenamiento.
- k = 5, 10 inicializaciones y semilla fija.
- Cinco distancias a centroides y una distancia mínima: **seis nuevas características**.
- Validación y prueba se transforman con centroides ya ajustados.

## 17. DBSCAN: densidad y ruido

$$d_{\rm core}(z)=\min_{c\in\mathcal C}\|z-c\|_2.$$

- Referencia de hasta 2 300 observaciones, min_samples = 5.
- ε: cuantil 90 % de la distancia al quinto vecino de referencia.
- Dos nuevas características: distancia al núcleo más cercano e indicador de distancia mayor que ε.
- Total: seis características K-means + dos DBSCAN.

No se crean transacciones sintéticas ni se eliminan columnas originales.

## 18. Diagnósticos de clustering

**Lectura:** Inercia, silueta y proporción de ruido.

**Resultado:** La inercia decrece con k; la silueta no es monótona. El ruido baja al ampliar ε.

**Alcance:** k=5 y cuantil 0,90 son decisiones fijas, no óptimos demostrados.

## 19. Diseño factorial: cuatro alternativas

| Representación | Escalado | One-hot | K-means + DBSCAN |
|---|:---:|:---:|:---:|
| raw | No | Sí | No |
| standardized | Sí | Sí | No |
| raw_kmeans_dbscan | No | Sí | Sí |
| standardized_kmeans_dbscan | Sí | Sí | Sí |

La geometría para clustering siempre está estandarizada; se escalan las distancias añadidas sólo en las ramas standardized. El indicador de ruido sigue binario.

## 20. Validación cruzada anidada

- **5 folds externos** estratificados: cada operación recibe una predicción fuera de fold (OOF).
- **3 folds internos:** hasta 36 000 filas estratificadas del entrenamiento externo.
- Se reajustan imputación, one-hot, escalado, PCA y clusters dentro de cada split.
- Se eligen parámetros por AUC interna; refit en todo el entrenamiento externo.
- Para test, promedio de cinco probabilidades.

$$\hat p_i^{\rm OOF}=\hat f_{-k(i)}(x_i).$$

El fold externo permanece retenido; la selección final por OOF sigue siendo exploratoria.

## 21. Regresión logística

$$\hat p(x)=\sigma(\beta_0+x^\top\beta),\qquad\sigma(t)=\frac{1}{1+e^{-t}}.$$

- Regularización L2: C ∈ {0,01; 0,1; 1; 10}.
- Ponderación: None o balanced.
- Ocho configuraciones por representación.
- El escalado modifica el condicionamiento y la penalización.

La logística ofrece una base probabilística para la corrección posterior.

## 22. Logística: efecto de la estandarización

**Lectura:** Distribución de AUC interna por representación.

**Resultado:** Las variantes estandarizadas muestran puntuaciones típicas más altas; raw presenta valores bajos dispersos.

**Alcance:** No es el ranking externo OOF.

## 23. Bosque aleatorio: cuatro representaciones

**Lectura:** AUC interna de nueve configuraciones por representación.

**Resultado:** Las ramas sin clusters presentan medianas mayores en esta grilla.

**Alcance:** No demuestra un efecto causal ni sustituye al OOF.

## 24. XGBoost: boosting de árboles

$$F_m(x)=F_{m-1}(x)+\eta h_m(x),\quad \hat p(x)=\sigma(F_M(x)).$$

- 240 árboles; profundidad: 3, 5, 7, 10, 15, 30.
- Tasa de aprendizaje: 0,04; 0,08.
- min_child_weight: 5, 10, 15.

**6 × 2 × 3 = 36 configuraciones**; misma grilla en XGBoost individual, stacking y corrector de logits.

## 25. XGBoost: cuatro representaciones

**Lectura:** 36 configuraciones por representación y fold.

**Resultado:** Amplio solapamiento de distribuciones internas; no se aprecia una ventaja clara del escalado.

**Alcance:** Los árboles pueden ser poco sensibles a escalas monótonas.

## 26. CatBoost: cuatro representaciones

**Lectura:** AUC interna de ocho configuraciones por representación.

**Resultado:** Medianas próximas; con clusters hay mayor dispersión inferior.

**Alcance:** No es una comparación OOF.

## 27. Espacio de búsqueda común

| Familia | Por representación | × 4 representaciones |
|---|---:|---:|
| Logística | 8 | 32 |
| Bosque aleatorio | 9 | 36 |
| XGBoost | 36 | 144 |
| CatBoost | 8 | 32 |
| **Total** | **61** | **244** |

244 × 3 folds internos × 5 externos = **3 660 ajustes internos nominales** de modelos individuales.

## 28. La representación es un hiperparámetro

$$(r^*,\theta^*)=\arg\max_{r,\theta}\frac13\sum_{j=1}^{3}\mathrm{AUC}_j(r,\theta).$$

- Por familia y representación: elegir mejor configuración interna.
- 4 familias × 4 representaciones = 16 candidatos fijos.
- Un selector adaptativo por familia: elige representación y parámetros por fold.
- 16 + 4 = **20 modelos individuales**.

Ninguna etiqueta de validación externa participa en la selección interna.

## 29. Promedio y bagging

$$\hat p_{\rm promedio}=\tfrac14\sum_{j=1}^4\hat p_j,\quad\hat p_{\rm bagging}=\tfrac15\sum_{b=1}^5\hat p_b.$$

- **Promedio:** combinar las cuatro probabilidades de las familias seleccionadas.
- **Bagging:** cinco réplicas bootstrap de XGBoost, con reemplazo, usando parámetros seleccionados.
- Cuatro escenarios fijos y uno adaptativo.
- Reducir varianza no garantiza que aumente AUC.

## 30. Stacking: aprender a combinar probabilidades

$$\hat p_{\rm stack}(x)=g(\hat p_{LR},\hat p_{RF},\hat p_{XGB},\hat p_{CAT}).$$

- El meta-modelo XGBoost recibe cuatro probabilidades.
- Cross-fitting para producir entradas OOF de meta-entrenamiento.
- Meta-validación con bases ajustadas únicamente en meta-entrenamiento.
- Misma grilla de 36 configuraciones.

La selección previa de las bases condiciona la evaluación interna; el fold externo sigue retenido.

## 31. Logística + XGBoost: corregir el logit

$$\hat p(x)=\sigma\big(f_{\rm LR}(x)+g_{\rm XGB}(x)\big).$$

1. Elegir y ajustar la logística mediante AUC interna.
2. Usar su logit como **base_margin** en el ajuste XGBoost.
3. Evaluar las 36 configuraciones del corrector.
4. Pasar también base_margin en predicción; ambas etapas usan la misma representación.

No es stacking de probabilidades ni regresión de residuos explícitos.

## 32. Corrección de logits: búsqueda de 36 boosters

**Lectura:** AUC interna por escenario.

**Resultado:** La rama standardized presenta mediana interna alta; el ranking OOF puede diferir.

**Alcance:** La selección final utiliza AUC OOF.

## 33. 40 candidatos y aceleración

| Grupo | Candidatos |
|---|---:|
| 4 familias × 5 escenarios | 20 |
| 4 ensambles × 5 escenarios | 20 |
| **Total nominal** | **40** |

La corrida confirma XGBoost CUDA, CatBoost GPU, 32 hilos CPU y hasta 4 configuraciones CPU simultáneas. 9 060 ajustes internos nominales antes de reutilización, más auxiliares y refits. No hay benchmark temporal en el ZIP.

## 34. Top 10 por ROC AUC OOF

**Lectura:** Ranking de 40 candidatos nominales, excluyendo duplicados exactos de predicciones.

**Resultado:** Tres correctores logísticos ocupan los primeros lugares; gana standardized_kmeans_dbscan.

**Alcance:** El eje está ampliado. No se dispone de IC nuevo.

## 35. Top 10: valores redondeados

    #  Modelo  Representación  ROC AUC  AP      1  Logística + XGBoost  E + K + D  0,945991  0,507054    2  Logística + XGBoost  Adaptativa  0,945939  0,507165    3  Logística + XGBoost  E  0,945911  0,506537    4  Stacking XGBoost  E  0,944241  0,490959    5  Stacking XGBoost  Adaptativa  0,944197  0,489923    6  Stacking XGBoost  E + K + D  0,944149  0,489329    7  Bagging XGBoost  Raw  0,943996  0,496211    8  Stacking XGBoost  Raw + K + D  0,943960  0,488966    9  CatBoost  Adaptativa  0,943933  0,501852    10  CatBoost  Raw  0,943925  0,501742     E = estandarizada; K = K-means; D = DBSCAN. Fuente: top10.csv. 

## 36. El finalista: ¿cuánto mejora?

 0,945991  ROC AUC OOF  

| Comparación | Diferencia AUC |
|---|---:|
| Contra logística + XGBoost estandarizada sin clusters | +0,000080 |
| Contra logística + XGBoost adaptativa | +0,000052 |

AP = 0,507054 · Log loss = 0,045837 · Brier = 0,011053.

El máximo nominal no demuestra superioridad estadística ni separa la contribución de K-means y DBSCAN.

## 37. ROC y precisión–recall

**Lectura:** Predicciones OOF reales de los diez modelos.

**Resultado:** Las ROC casi coinciden; PR permite examinar la clase rara.

**Alcance:** La referencia PR aleatoria es 1,67 %; AUC no elige umbral.

## 38. Calibración de probabilidades

**Lectura:** Frecuencia observada contra probabilidad media en 15 cuantiles.

**Resultado:** Puntos concentrados en probabilidades bajas; curvas próximas.

**Alcance:** No garantiza calibración en las colas ni estabilidad temporal.

## 39. Tres políticas de alerta del finalista

| Política OOF | Umbral | Recall | Precisión | F1 | FN / FP |
|---|---:|---:|---:|---:|---:|
| 0,50 | 0,5000 | 30,82 % | 75,43 % | 0,4376 | 8 087 / 1 173 |
| Máximo F1 | 0,2510 | 46,11 % | 54,67 % | 0,5003 | 6 299 / 4 469 |
| Recall 98 % | 0,002076 | 98,01 % | 3,59 % | 0,0693 | 233 / 307 241 |

Reducir fraudes omitidos eleva alertas falsas. Umbrales ajustados sobre OOF completo: resultados descriptivos.

## 40. Matriz de confusión: recall cercano al 98 %

**Lectura:** Umbral elegido en otros folds OOF y aplicado al fold retenido.

**Resultado:** 11 455 VP, 234 FN, 305 799 FP y 382 472 VN. Recall 98,00 %; F1 0,06965.

**Alcance:** 44,43 % de legítimas alertadas; no es validación independiente.

## 41. Entrega de probabilidades a Kaggle

- Finalista: Logística + XGBoost | standardized_kmeans_dbscan.
- 299 984 filas de prueba; columnas id,is_fraud.
- Probabilidades finitas entre 0 y 1, sin umbral.
- No hay score confirmado del leaderboard en el ZIP.

El archivo de predicciones individuales permanece privado.

## 42. Conclusiones y trabajo futuro

- Se evaluó el preprocesamiento y la ingeniería como parte del espacio de hiperparámetros.
- Ganador nominal: logística estandarizada + K-means + DBSCAN + XGBoost, AUC 0,945991.
- Tres variantes del corrector ocupan los primeros puestos; la ventaja sobre la estandarizada sin clusters es 0,000080.
- No hay IC nuevo, validación temporal ni score externo confirmado.
- Siguiente paso: bootstrap emparejado, ablación separada K-means/DBSCAN y análisis de costos.

**Selección reproducible; superioridad estadística aún no demostrada.**
