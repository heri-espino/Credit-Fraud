# experiment029 — Comparación final simplificada de F1

Sustituye la versión extensa de inferencia por un notebook español de ocho celdas, conservando experiment028 en archive. No se modifica la corrida ni se reentrena. Se leen los diez nombres exactos de experiment026 y las predicciones privadas de experiment024, verificando firma, folds y métricas. Política de umbral cruzado con objetivo recall 98 % (la del informe original); se comprueba F1 cruzado si existe el CSV local. F1 agregado, no promedio por fold.

Bootstrap pareado estratificado de positivos y negativos, 100 000 réplicas, semilla 42. Muestreo multinomial conjunto de patrones de decisiones por clase: equivalente en distribución al remuestreo de filas. F1*=2TP*/(n_pos+TP*+FP*). p bilateral centrado con corrección +1; Holm para los 45 pares. IC percentiles puntuales 95 % de diferencia (modelo − referencia, ganador por ROC AUC). Dos figuras exclusivamente: dashboard 1×2 de p originales y Holm con nombres completos, y nueve IC contra la referencia. Estilo Seaborn original. Datos y p-valores no redondeados en CSV. No hay otros contrastes ni figuras en notebook activo.

## Reproducción

```bash
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment029/smoke_test.py
jupyter lab notebook_inferencia_final_es.ipynb
```

Salidas agregadas en outputs/experiment029 y figuras PNG/PDF en figuras/. No publicar predicciones por fila. El contraste e IC son exploratorios condicionados a OOF y umbrales fijos, no capturan incertidumbre de entrenamiento, dependencia entre observaciones ni optimismo de selección. No se dispone de NPZ originales en la sesión de edición; no se reportan p-valores empíricos. Próximo experiment030.
