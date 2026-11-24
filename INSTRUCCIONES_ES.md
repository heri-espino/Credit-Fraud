# Reproducción del cuaderno final — experiment021

Desde la raíz del repositorio, conserve outputs/ y coloque el ZIP oficial de Kaggle o los CSV originales en data/.

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment021/smoke_test.py
jupyter lab notebook_final_es.ipynb
```

Seleccione el kernel Python (LDS1071 Fraud) y configure las banderas de la primera celda:

| Modo | EJECUTAR_PROTOCOLO_COMUN | CARGAR_PROTOCOLO_COMUN | REUTILIZAR_INDIVIDUALES |
|---|---|---|---|
| Histórico (predeterminado) | False | False | False |
| Nuevo entrenamiento completo | True | False | False |
| Reanudar desde sección 3 completa | True | False | True |
| Reproducir experiment021 terminado | False | True | False |

Mantenga EJECUTAR_BUSQUEDA_HIBRIDA=False. Reinicie kernel y ejecute todas las celdas. La sección 3 entrena cuatro modelos individuales; la sección 4 añade promedio, bagging, stacking XGBoost y corrección LR+XGBoost. Los tres boosters usan la misma grilla de 36 combinaciones.

El smoke test usa datos sintéticos y un presupuesto reducido; no se ha ejecutado en esta sesión. El entrenamiento completo también está pendiente. Agregados/checkpoints en outputs/experiment021/; figuras, métricas y envío en outputs/informe_ensambles_es/. Mantenga NPZ privados fuera de Git. Consulte [experiment021](experiments/experiment021/README.md).
