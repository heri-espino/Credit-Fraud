# experiment022 — Corrección de ejecución y comparación top 10


## experiment022 — K-means explícito, ranking top 10 y corrección de configuración

Auditoría de la corrida del propietario (commit `7b682cc0c53a331c9f2b18c70a7508b2f31e5b3d`, "ran"): una celda adicional puso EJECUTAR_PROTOCOLO_COMUN=True, pero la siguiente la redefinió False. Se ejecutó modo histórico (37 celdas de código en la revisión del propietario, 5 vectores históricos verificados, envío histórico de 299 984 filas). AUC histórica 0.946205 offset, 0.946120 XGB individual. En exp018, mejor híbrido ajustado K-means en logística 0.945870 vs 0.945842 original; en exp014, mejor logística aislada fue K-means+DBSCAN 0.941559 vs K-means 0.941511. No confundir esas tablas ni atribuirlas a experiment021.

Se eliminó la celda duplicada. El notebook tiene una sola configuración, por defecto EJECUTAR_PROTOCOLO_COMUN=True y EJECUTAR_EXTENSION_TOP10=True. Extension: reajustar los mejores parámetros internos de las 18 combinaciones familia/representación, más offset fijo K-means (36 configuraciones del booster, base logística K-means elegida por AUC interna dentro de cada fold). 27 candidatos en total incluidos los ocho de exp021; se excluyen duplicados exactos OOF/test antes de seleccionar top10. 540 ajustes internos nuevos de booster, 90 refits individuales y 5 refits de híbrido (más logística auxiliar); no repetir búsquedas ya guardadas. Cargar experiment021 completo con CARGAR_PROTOCOLO_COMUN=True y ejecutar extensión; para reproducir todo sin entrenar, EJECUTAR_EXTENSION_TOP10=False. Salidas separadas outputs/experiment022 e informe_top10_es. En modo histórico, top10 descriptivo con procedencia; curvas solo de vectores disponibles. No forzar K-means como ganador. No publicar NPZ. Implementación nueva no ejecutada aquí; smoke test sintético disponible. Próximo experimento023.

## Reproducción

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment022/smoke_test.py
jupyter lab notebook_final_es.ipynb
```

Configure únicamente la celda inicial de configuración. Reinicie kernel y ejecute todo. Para una corrida completa desde cero: EJECUTAR_PROTOCOLO_COMUN=True, CARGAR_PROTOCOLO_COMUN=False, REUTILIZAR_INDIVIDUALES=False, EJECUTAR_EXTENSION_TOP10=True. Si solo se completó sección 3 de experiment021, use REUTILIZAR_INDIVIDUALES=True. Si ya se completó experiment021, configure EJECUTAR_PROTOCOLO_COMUN=False, CARGAR_PROTOCOLO_COMUN=True, REUTILIZAR_INDIVIDUALES=False y EJECUTAR_EXTENSION_TOP10=True. Una vez terminada la extensión, cambie EJECUTAR_EXTENSION_TOP10=False para cargarla sin entrenar. Para reproducir los históricos, EJECUTAR_PROTOCOLO_COMUN=False y CARGAR_PROTOCOLO_COMUN=False.

Resultados: outputs/experiment022/summary_all.csv, selected_all.csv, summary_extension.csv, grid_offset_kmeans.csv y selected_extension.csv. outputs/informe_top10_es/top10.csv, figuras ROC/PR, calibración, matrices de confusión y envío. extension_PRIVATE.npz contiene predicciones por fila e IDs y no se publica. El ranking nuevo usa OOF de todos los candidatos, no AUC internas. El corrector fijo conserva K-means en la base logística en todos los folds, y usa los predictores originales para el booster; se distingue del selector adaptativo. La mayor AUC observada no demuestra superioridad estadística.

## Estado

La corrida histórica se verificó mediante outputs reales del notebook en el commit "ran". El código nuevo no se ejecutó ni se verificó con los datos privados en esta sesión. Se añadió smoke test sintético de sintaxis, grilla, refits, caché y ranking. El notebook previo sin outputs se archivó en archive/; el commit original conserva la corrida. Tras ejecutar preservar agregados, revisar resultados y cumplir publicación equivalente en Kaggle. No duplicar datos privados ni resultados individuales en Git.
