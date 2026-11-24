# Cómo reproducir el cuaderno final

En la raíz de Credit-Fraud, conserve `outputs/` y coloque el ZIP original de Kaggle o los tres CSV en `data/`.

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
jupyter lab notebook_final_es.ipynb
```

Seleccione el kernel Python (LDS1071 Fraud) y use Restart Kernel and Run All Cells.

## Selección del modo
- Histórico (predeterminado): `EJECUTAR_PROTOCOLO_COMUN=False` y `CARGAR_PROTOCOLO_COMUN=False`. Recupera resultados previos, no reentrena. Para las curvas y el envío se requiere `outputs/ensemble_extension/five_way_oof_and_test_predictions.npz` o el ZIP `ensemble_extension.zip`. Figuras y envío en `outputs/informe_final_es/`.
- Nuevo protocolo homogéneo: `EJECUTAR_PROTOCOLO_COMUN=True` y `CARGAR_PROTOCOLO_COMUN=False`. Ejecuta 4 440 ajustes internos de candidatos y 25 externos, más auxiliares. Las métricas nuevas aún no están verificadas. No ejecutar simultáneamente la búsqueda histórica opcional.
- Reutilizar una corrida homogénea completa: `EJECUTAR_PROTOCOLO_COMUN=False` y `CARGAR_PROTOCOLO_COMUN=True`. Verifica IDs y AUC de la caché nueva. Figuras y envío en `outputs/informe_comun_es/`.

Los datos individuales y los archivos NPZ privados se mantienen fuera de Git. Consulte [experiment020](experiments/experiment020/README.md). Antes de entregar el notebook con la nueva metodología, ejecutar y verificar las celdas, las tablas y las figuras, y conservar los agregados. No presentar métricas históricas como resultado del protocolo nuevo.
