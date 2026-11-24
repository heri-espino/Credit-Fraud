# experiment020 — Protocolo homogéneo y revisión de entrega

**Estado:** código y narrativa revisados; **nuevo entrenamiento completo pendiente**, no hay nuevas métricas verificadas. No confundir con experiment019, que sí se ejecutó con las cachés históricas. Archivo anterior: `archive/notebook_final_es_experiment019.ipynb`.

## Pregunta y diseño

Comparar logística, bosque aleatorio, XGBoost y CatBoost con el mismo procedimiento: cinco folds externos estratificados (semilla 42), muestra estratificada de hasta 36 000 filas de cada entrenamiento externo, tres folds internos idénticos, selección por ROC AUC medio, reajuste de cada ganador con todo el entrenamiento externo. Se evalúan original, K-means, DBSCAN y ambos en cada familia, más PCA 90 % y splines para logística. Todas las transformaciones se ajustan solo con entrenamiento de cada split. La geometría nueva utiliza PCA de referencia, cinco centroides y radio DBSCAN por percentil 90 de distancia al quinto vecino. CatBoost emplea matriz codificada común, no las categorías nativas de la corrida histórica.

| Familia | Configuraciones por representación | Representaciones | Configuraciones por fold |
|---|---:|---:|---:|
| Logística | 8 | 6 | 48 |
| Bosque aleatorio | 9 | 4 | 36 |
| XGBoost | 36 | 4 | 144 |
| CatBoost | 8 | 4 | 32 |
| Logística + XGBoost | 36 | 1 seleccionada | 36 |

Total: 296 configuraciones por fold, 4 440 ajustes internos supervisados de candidatos y 25 ajustes externos, más reajustes auxiliares de la logística y geometría. XGBoost independiente y corrector tienen idénticos parámetros fijos y grilla. El corrector usa predictores originales y logits de la logística seleccionada (base_margin en fit/predict). El ganador logístico se escoge por AUC logística interna, no por AUC OOF ni por rendimiento del corrector. Se reutilizan los mismos splits internos al ajustar el corrector; los scores internos son de selección, no de evaluación independiente. Los modelos finales se comparan por AUC OOF; el máximo observado conserva sesgo de selección.

## Reproducción

1. `git pull --ff-only origin main`; activar `lds1071-fraud`; abrir `notebook_final_es.ipynb` con datos originales disponibles.
2. Por defecto las dos banderas del protocolo común son False, por lo que se reproducen los resultados históricos. Para correr el nuevo protocolo: `EJECUTAR_PROTOCOLO_COMUN=True`, `CARGAR_PROTOCOLO_COMUN=False`. Ejecutar desde un kernel reiniciado.
3. Para reconstruir después sin reentrenar: invertir las dos banderas. Se comprueban IDs, etiquetas, tamaños, finitud, rango de probabilidades y AUC.
4. Los agregados de la nueva ejecución (`summary.csv`, `grid_results.csv`, `selected_params.csv`) se guardan en `outputs/experiment020/`; los datos individuales en `predictions_PRIVATE.npz` deben permanecer privados. Las figuras y envío nuevos van a `outputs/informe_comun_es/`, separados del histórico.

## Verificación y próximos pasos

Se verificó el JSON del notebook versionado, su orden de 69 celdas (34 ejecutables), identificadores únicos, rutas y configuración; no se ejecutó Python ni el entrenamiento en esta sesión. No hay acceso a datos Kaggle ni cachés locales en el entorno de edición. El código nuevo necesita una ejecución de prueba y después la ejecución completa antes de calificar la entrega como final. No afirmar una nueva AUC, que se hizo un diseño factorial histórico, ni superioridad estadística. No subir el NPZ privado. Tras ejecutar, preservar agregados, revisar curvas y enviar el notebook ejecutado; mantener publicación equivalente en Kaggle conforme a sus reglas.
