# experiment027 — Comparación pareada de recall de los diez finalistas

Objetivo: completar el análisis posterior a experiment024/026 sin reentrenar. El notebook histórico paired_bootstrap_comparison.ipynb queda intacto. Nuevo notebook `notebook_inferencia_final_es.ipynb`. Carga top10.csv y resumen_final.json versionados en experiment026 y los NPZ privados locales de experiment024; verifica firma, índices de los cinco folds (semilla 42), cobertura y AUC/AP/log-loss/Brier originales. Se requiere train.csv original sin reordenar, o ZIP; no se usan datos de test. No se recalcula el hash de datos completo; no se dispone de identificadores por fila en los NPZ.

Política primaria: recall objetivo 98 % con umbral de los otros cuatro folds, exactamente como notebook final. Sensibilidad: umbral 0.50. Se comparan los 45 pares no ordenados por política. Bootstrap pareado de patrones conjuntos de detección en positivos, multinomial exacto en distribución al remuestreo por filas (100 000 réplicas, semilla 20261125, IC percentiles puntuales y p bilateral centrado con +1). McNemar bilateral exacto sobre discordancias como contraste primario. Holm y Bonferroni por separado en cada familia de 45 p-valores (método/política); sensibilidad exploratoria, no control conjunto sobre ambas políticas. Mapas triangulares de p brutos, Holm y Bonferroni, para ambos métodos y políticas; además diferencias en puntos porcentuales e IC frente a M01, y FPR junto con recall. No se confunde igualdad de recall con igualdad de AUC.

## Reproducción

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment027/smoke_test.py
jupyter lab notebook_inferencia_final_es.ipynb
```

Ejecutar todas las celdas. CHECKPOINTS apunta a outputs/experiment024 y puede cambiarse si los archivos se guardaron en otro directorio. Si faltan NPZ recuperar copia privada original; el ZIP de informe agregado no basta. Nunca subir predicciones por fila. Tablas, matrices y figuras PNG/PDF y manifiesto en outputs/experiment027; revisar y versionar únicamente agregados en experiments/experiment027/resultados cuando se disponga de la ejecución real. No sobrescribe resultados anteriores ni presentaciones.

## Limitaciones y estado

Inferencia exploratoria condicionada a OOF y umbrales fijos; selección sobre mismas etiquetas, dependencia por folds solapados y posible dependencia por transacción. Calibración 98 % no plenamente anidada; bootstrap no reajusta umbrales ni modelos. McNemar exacto bajo pares independientes, no garantiza validez confirmatoria en este diseño. IC puntuales no simultáneos. Sin resultados inferenciales nuevos hasta ejecución con predicciones privadas. Próximo experiment028.
