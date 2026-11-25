# Reproducción del cuaderno final — experiment023

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment023/smoke_test.py
jupyter lab notebook_final_es.ipynb
```

Reiniciar el kernel y ejecutar todo. Única opción de ejecución: REANUDAR=True (predeterminada) recupera checkpoints compatibles; False vuelve a entrenar. No se mezclan resultados históricos. Cuatro representaciones para todos los modelos, 40 candidatos nominales, top 10 por AUC OOF. Los archivos privados se guardan en outputs/experiment023; informe en outputs/informe_experiment023_es. La corrida completa y smoke aún deben ejecutarse. Véase [experiment023](experiments/experiment023/README.md).
