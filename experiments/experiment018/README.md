# experiment018 — Búsqueda anidada de corrección XGBoost con decisiones de representación

**Objetivo:** integrar, antes de la selección final, cuatro representaciones de la primera etapa logística y una grilla explícita de 36 configuraciones del booster corrector. El experimento no inventa observaciones: K-means y DBSCAN solo construyen características adicionales.

## Protocolo

- Datos completos: 699 960 transacciones, 5 folds externos estratificados con semilla 42.
- **Hiperparámetro de representación:** original / K-means / DBSCAN / K-means+DBSCAN, aplicados a **la regresión logística**. XGBoost corrector recibe los predictores originales para aislar esta elección, ya que experiment015 no mostró ventajas de introducir agrupamientos en ambos niveles.
- Dentro de cada fold externo: muestra estratificada de 36 000 filas de entrenamiento (sin observaciones de validación externa), 3 folds internos; cada división refita imputación, codificación, escalado, PCA y K-means/DBSCAN, y logística. Posteriormente se evalúan **36** combinaciones de profundidad `[3,5,7,10,15,30]`, learning rate `[.04,.08]`, min_child_weight `[5,10,15]` con 240 árboles, subsample=.85 y colsample_bytree=.85.
- XGBoost recibe el logit de la regresión logística mediante `base_margin` **tanto en el ajuste como en la predicción**. Se ejecuta una búsqueda de grilla equivalente a GridSearchCV, con caché limitada a las mismas divisiones internas; no se debe usar GridSearchCV directo sin un estimador que propague el margen a predict_proba.
- Se reentrenan en los 559 968 registros externos de entrenamiento la representación, la logística y la corrección XGBoost con los mejores parámetros elegidos internamente. Las predicciones de los cinco folds se integran en un vector OOF por variante, sin reutilizar las etiquetas de validación para seleccionar clusters o parámetros.
- Los resultados de experimentos 013–017 son referencias históricas **no intercambiables** con los nuevos OOF de esta búsqueda.
- Los OOF por fila se guardan localmente, fuera de Git. Los CSV agregados, manifiesto, resultados de bootstrap, tests y gráficas se preservan para la reproducción.

## Conclusión provisional

El notebook final **no** cambia automáticamente el finalista del experimento016. La selección debe basarse en los resultados completos y su incertidumbre, no en los primeros folds. Se conservan 0.946205 OOF ROC AUC para la corrección logística histórica y 0.946120 para el mejor XGBoost individual original; su diferencia +0.000085 tuvo un IC 95 % emparejado que incluyó cero.

## Tiempo computacional

`tiempos_historicos.csv` preserva tiempos **medidos de ajuste del booster** por fold de los experimentos 013 y 015. Estos tiempos **excluyen** el ajuste logístico, la construcción de variables y las búsquedas, por lo que **no representan costos totales de pipeline**. La figura solo compara este costo parcial correctamente etiquetado.

## Publicación

La publicación del código ejecutable en un repositorio público debe satisfacer además las reglas de divulgación de código de la competencia Kaggle. Los scripts completos y los datos por observación se entregan de manera separada, no se mezclan con los resultados agregados del repositorio.
