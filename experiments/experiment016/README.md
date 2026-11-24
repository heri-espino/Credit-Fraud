# experiment016 — Cuaderno final unificado en español

**Estado:** preparado y verificado el 24 de noviembre de 2026. El entregable principal es el cuaderno **`notebook_final_es.ipynb` (50 celdas)** distribuido al propietario en el ZIP privado **`Credit-Fraud_notebook_final_es.zip`**. Se preservan los cuadernos originales y experimentos 001–015 sin modificaciones.

## Secuencia del cuaderno

0. Configuración, fuentes, modo de reutilización y trazabilidad.
1. Dataset de Kaggle: 699,960 filas etiquetadas, 299,984 de prueba, 24 predictores (13 numéricos, 5 categóricos y 6 lógicos), 11,689 fraudes.
2. EDA: desbalance, faltantes, distribuciones, correlaciones, riesgo por categoría, tasas por cuantiles, interacciones, patrones temporales, extremos IQR, Isolation Forest y desplazamiento train/test.
3. Ingeniería: codificación por columna, escalado, splines, PCA/SVD con 90% de varianza, FastICA, t-SNE opcional; diagnósticos de K-means (inercia/silueta) y DBSCAN (radio/ruido); ablasiones completas 013–015.
4. Modelos y búsqueda: auditoría de supuestos de regresión logística, **19 especificaciones originales**, GridSearchCV opcional y función autocontenida para ejecutar una búsqueda anidada de cinco folds.
5. Cuatro ensambles y comparación con XGBoost individual: promedio de probabilidades, logística con corrección XGBoost por logit offset, corrección explícita de residuos y stacking con random forest. Se muestran mecanismos implementables y se reutilizan predicciones OOF verificadas.
6. Incertidumbre: bootstrap estratificado emparejado con 600 réplicas (resultados del experimento010; no se inventa una nueva prueba).
7. Decisión, validación y creación de submission `id,is_fraud` **solo** si se dispone de probabilidades reales de prueba.
8. Limitaciones, resultados y catálogo de figuras.

## Resultados históricos reutilizados

| Estrategia | ROC AUC OOF | AP |
|---|---:|---:|
| Logística corregida con XGBoost | **0.946204755** | **0.507424** |
| XGBoost individual, profundidad 5 | 0.946120149 | 0.503585 |
| Stacking con bosque aleatorio | 0.945746947 | 0.506383 |
| Promedio de probabilidades | 0.943280104 | 0.500913 |
| XGBoost sobre residuos explícitos | 0.940240912 | 0.494046 |

La diferencia nominal de +0.000084606 AUC del modelo corregido frente al mejor individual tiene un intervalo emparejado 95% de **[-0.000262587,+0.000439726]**, que incluye 0. El modelo seleccionado por máximo AUC OOF no ha demostrado superioridad estadística. El stacking no fue completamente anidado y hay optimismo de selección. No se confunde el XGBoost fijo `xgb_depth5_lr05` con `xgb_nested_grid`.

Los experimentos de clustering de 699,960 filas no justificaron sustituir el finalista; la ligera ganancia de la logística de primera etapa no sobrevivió consistentemente a la corrección XGBoost.

## Reproducción

Extraer el ZIP privado en la raíz de `Credit-Fraud`, sin borrar `outputs/`; instalar el entorno según README y abrir:

```powershell
conda activate lds1071-fraud
jupyter lab notebook_final_es.ipynb
```

Necesita el ZIP original de Kaggle junto al notebook (o CSV en `data/`) y los CSV agregados incluidos en `experiments/experiment016/resultados/`. Para curvas ROC, calibración y submission requiere `outputs/ensemble_extension/five_way_oof_and_test_predictions.npz` **o** `ensemble_extension.zip`, conservados localmente y excluidos de Git.

El modo predeterminado NO reentrena los 19 candidatos ni los ensambles. `CORRER_BUSQUEDA_DE_EJEMPLO=True` habilita una **búsqueda nueva sobre un subconjunto**, mientras que la función `evaluar_busqueda_anidada` documenta los cinco folds externos si se desea reejecutar.

## Verificación y reglas

- Fuente Jupyter validada: **50 celdas, 25 de código**, todas compiladas y ejecutadas secuencialmente con los datos originales.
- **19 figuras nuevas con títulos, ejes y leyendas en español**; se generó un CSV de 299,984 probabilidades válidas, conservado **privadamente**.
- Los scripts y notebooks históricos, los archivos de Kaggle, los modelos `.joblib` y los vectores OOF/test individuales se conservan en sus destinos anteriores; **no se publican**.
- Repositorio público: antes de subir el código de este nuevo notebook también debe compartirse en el Notebook/Discussion de la competencia, conforme a las reglas de Kaggle. Por ello el notebook ejecutable permanece en el ZIP privado y este directorio contiene documentación/estadísticas agregadas.

**Siguiente experimento:** experiment017, si se requiere una nueva pregunta científica. La versión final del informe ya está lista para uso académico.
