# experiment019 — Integración lógica del informe final

**Fecha:** 2026-11-24. **Estado:** revisión narrativa del cuaderno, sin nuevas afirmaciones de desempeño ni reentrenamiento.

## Objetivo

Se reorganizó `notebook_final_es.ipynb` en la siguiente secuencia científica, que sustituye una presentación fragmentada de resultados:

1. EDA: integridad, desbalance, distribuciones, correlaciones, no linealidades, temporalidad, anomalías y train/test.
2. Ingeniería de variables: PCA/SVD, t-SNE descriptivo, K-means y DBSCAN, incluyendo diagnósticos de inercia, silueta y ruido y variante de cinco grupos.
3. Algoritmos y búsqueda: regresión logística, splines, PCA, bosque aleatorio, XGBoost y CatBoost. Se explica **qué representaciones fueron realmente probadas con cada familia**, sin inventar un diseño factorial completo; validación anidada y comparaciones reales de OOF.
4. Selección logística: el mejor valor puntual entre cuatro representaciones del experimento014 fue `combined` con ROC AUC 0.941559, pero su diferencia frente a `baseline` 0.941357 tiene IC95 [-0.000009,+0.000422]. Por parsimonia, se conserva la base original como **referencia**, sin descartar las demás para selección interna.
5. XGBoost posterior a la logística: `base_margin` con logits en fit/predict; 36 configuraciones y cuatro representaciones del experimento018. Cinco folds externos, tres internos sobre una muestra de 36 000 filas de entrenamiento externo por fold. La representación elegida en los folds externos fue original 4 veces y K-means una vez; la selección se hizo por AUC interna, nunca con etiquetas externas.
6. Ensambles y tiempo: promedio, offset, residuos explícitos y stacking RF contra mejor XGBoost individual; ROC AUC vs. segundos de booster por fold, con alcance de los tiempos explícito.
7. Inferencia, selección y diagnóstico: intervalos bootstrap de diferencias, ROC/PR/calibración, políticas de alerta, matriz de confusión con porcentajes, F1 y conclusiones.

**Finalista histórico:** logit corregido con XGBoost, AUC OOF 0.946205 frente a 0.946120 del XGBoost individual. La diferencia +0.000085 y su IC95 [-0.000263,+0.000440] no demuestran superioridad. El experimento018 no mejora significativamente el resultado por cambiar representación.

## Implementación

- 66 celdas, 33 ejecutables. Se preservan íntegramente las funciones de los experimentos anteriores; cambia su ubicación explicativa, y se añaden una tabla y gráfico para elegir la base logística.
- Se arregló el orden de dependencias: primero cargar OOF/test, después construir envío, luego graficar ROC. La bandera opcional `EJECUTAR_BUSQUEDA_HIBRIDA=False` permanece inicializada.
- El modo por defecto **no** reentrena modelos. No se publican modelos `.joblib`, filas Kaggle ni predicciones OOF/test.
- Estructura y etiquetas en español; estilo Seaborn `whitegrid`, paleta `dark`; curvas superpuestas ordenadas y transparencia diferenciada.

## Verificación

La versión local equivalente se ejecutó secuencialmente con el dataset completo de **699 960 filas** y archivos de predicciones OOF de los experimentos anteriores: las 33 celdas ejecutables terminaron sin errores (aproximadamente 26 s), se reconstruyeron **31 figuras** y la salida de Kaggle. Los archivos confidenciales utilizados en esa ejecución no se incorporan al repositorio.

**Observación de procedencia:** las métricas de las tablas provienen de experimentos 013–018 ya ejecutados. No se añade un experimento predictivo nuevo ni se declara una mejoría no verificada.

## Reproducir

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
jupyter lab notebook_final_es.ipynb
```

Para curvas y envío se necesita la caché privada de OOF y test en `outputs/`. Los CSV agregados ya están versionados. Publicación de código en Kaggle Notebook/Discussion sigue pendiente según las reglas del concurso.