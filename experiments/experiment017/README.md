# experiment017 — Cinco clusters K-means, búsqueda XGBoost y decisión de alerta

**Ejecutado:** 24 noviembre 2026. Dataset completo de 699,960 filas, cinco folds estratificados (`random_state=42`). Se preservaron experimentos anteriores.

## Configuración

Se reutilizó la OOF del XGBoost original de experiment013. La nueva versión añade exactamente seis columnas: cinco indicadores de pertenencia a K-means con k=5 y una similitud al centro asignado `exp(-distancia²/escala)`. El escalado, PCA de seis dimensiones y K-means se ajustaron exclusivamente sobre entrenamiento externo (15,000 filas de referencia geométrica); XGBoost entrena con todas las ~560,000 filas de ese pliegue.

XGBoost fijo: 350 árboles, profundidad 5, learning_rate 0.05 y min_child_weight 5. Búsqueda GridSearchCV: `max_depth=[3,5,7,10,15,30]`, `learning_rate=[0.04,0.08]`, `min_child_weight=[5,10,15]`. Son **36 combinaciones** con 3 folds internos sobre 20,000 observaciones del entrenamiento externo y cinco folds externos. Se reutilizaron las evaluaciones internas de 30 configuraciones y se agregaron las seis de profundidad 30 con idénticas particiones. La geometría se ajustó con todo el entrenamiento externo, por lo que su estimación no está totalmente anidada en el CV interno, aunque la evaluación OOF externa no utiliza etiquetas de validación.

## Resultados

| Variante | ROC AUC OOF | Average precision |
|---|---:|---:|
| XGBoost, predictores originales | 0.945702363 | 0.500909959 |
| **XGBoost fijo + 5 grupos** | **0.945746719** | **0.501017810** |
| 5 grupos + GridSearchCV (30) | 0.944886982 | 0.499679004 |
| 5 grupos + GridSearchCV (36) | 0.944886982 | 0.499679004 |

**Ningún fold seleccionó profundidad 30.** Los cinco eligieron profundidad 3, learning_rate 0.04 y min_child_weight 5. Bootstrap estratificado emparejado, B=1000: ΔAUC fijo vs original **+0.000044357**, IC95 **[−0.000107,+0.000194]** (incluye cero). La búsqueda ajustada es peor que la referencia por aproximadamente −0.000815 AUC.

## Política de alertas

Kaggle requiere probabilidades, no etiquetas binarias. Para emitir una alerta se elige aparte un umbral t. Eliminar falsos negativos exclusivamente alerta todas las operaciones, por lo que usamos como ejemplo un objetivo de sensibilidad del 98% y comparamos falsas alarmas. El umbral en cada fold se determina con predicciones OOF de los otros cuatro.

En el mejor XGBoost individual histórico, con umbral 0.50 se observan **8102 FN y 1182 FP**, F1 **0.435897**, accuracy **0.986736**; con recall ~98% (umbral ~0.002388), **233 FN y 306525 FP**, F1 **0.069500**, accuracy **0.561749**. En evaluación cruzada del umbral: **231 FN, 305362 FP, recall 0.980238, F1 0.069758 y accuracy 0.563414**. Es una política exploratoria y genera demasiadas alertas para recomendarla operativamente sin costos explícitos.

El mejor logit-offset tiene ROC AUC superior, pero no la menor tasa de falsas alarmas al 98% de sensibilidad. ROC AUC no depende del umbral. El CSV de Kaggle permanece como `id,is_fraud` con probabilidades sin corte.

## Reproducción

La versión de `notebook_final_es.ipynb` incluye grilla 36, Seaborn dark, figura de candidatos con ROC AUC ampliado y figura de cuatro ensambles solo con ROC AUC. Los CSV agregados están en `results/`; los scripts completos, tests, figuras y resultados se distribuyeron en `Credit-Fraud_experiment017_kmeans5_umbrales.zip`. Las predicciones fila a fila y envíos se conservaron en `Credit-Fraud_experiment017_OOF_PRIVATE.zip` y **no** se suben a Git.

Los 54 componentes del notebook se ejecutaron de inicio a fin. Todo corrió en Linux CPU; no se usó el runner Windows. Los intervalos bootstrap son condicionales a las predicciones OOF y no son validación externa ni corrigen dependencia, búsqueda/selección de modelos o los costos reales de fraude. **Decisión:** conservar el finalista original. Siguiente experimento: experiment018.

El repositorio es público; cualquier código de la competencia difundido públicamente debe compartirse también en el Notebook/Discussion correspondiente de Kaggle conforme a sus reglas. Ese paso permanece pendiente.