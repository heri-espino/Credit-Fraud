# experiment028 — Inferencia ROC AUC y mapas de calor con valores originales

Extiende experiment027 en el mismo notebook final español. Se conserva la fuente anterior en archive y no se modifica notebook_final_es.ipynb ni su ejecución. Se mantiene toda la inferencia de recall (semilla y B originales), se adopta la configuración visual original (seaborn whitegrid, dark, notebook, 110/150 dpi, títulos semibold), con un directorio de salida separado outputs/experiment028/figuras. Los mapas muestran directamente matrices de p-valores continuos con escala lineal común 0–1, anotaciones 4 cifras significativas y asteriscos p≤0.05; CSV sin redondeo. No se binariza el color. Las diferencias e IC conservan el signo fila menos columna.

ROC AUC: se usan todas las probabilidades OOF originales verificadas contra experiment026. DeLong pareado bilateral (componentes estructurales, empates 1/2, covarianza conjunta) y bootstrap estratificado pareado exacto de ambas clases mediante multiplicidades y sumas acumuladas sobre negativos ordenados. 2 000 réplicas por defecto, semilla 42, hasta 4 hilos CPU, progreso y checkpoints atómicos cada 50, determinismo por réplica independiente del orden de ejecución. Se conserva el mismo índice de remuestreo para todos los modelos. Holm y Bonferroni separados por familia de 45 pares, IC puntuales percentiles y DeLong; curvas ROC originales con AUC a nueve decimales. El mínimo p bootstrap es 1/(B+1), por lo que DeLong permite mayor resolución en colas. Aumentar B_AUC si se necesita y conservar firma; si se reduce B borrar/renombrar caché. REANUDAR=False elimina únicamente caché AUC de este experimento. No hace falta GPU ni reentrenar.

## Reproducción
```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment027/smoke_test.py
python experiments/experiment028/smoke_test.py
jupyter lab notebook_inferencia_final_es.ipynb
```
Ejecutar todo con NPZ privados originales de exp024 y train.csv/ZIP original sin reordenar. Tablas y matrices CSV y manifiesto en outputs/experiment028, figuras PNG/PDF en figuras/. No subir NPZ ni predicciones fila a fila. Los resultados numéricos nuevos requieren esos archivos privados; no se simulan. Inferencia condicional exploratoria, no corrige selección sobre las mismas OOF, solapamiento de entrenamiento ni dependencia potencial por cliente/tiempo. No interpretar diferencia de AUC como prueba de igualdad de curvas completas. Próximo experiment029.
