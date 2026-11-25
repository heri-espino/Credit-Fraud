# Reproducción del cuaderno final — experiment024 acelerado

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
nvidia-smi
python experiments/experiment024/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
Reiniciar kernel y ejecutar todo. Por defecto GPU auto y CPU_JOBS=-1, GRID_JOBS=4. Un ajuste GPU a la vez. Para exigir GPU, DISPOSITIVO_XGB='cuda', DISPOSITIVO_CATBOOST='GPU'. CPU fallback solo durante la prueba inicial. Si RAM saturada, GRID_JOBS=2/1. Si VRAM insuficiente, cambiar dispositivo en una corrida nueva (no mezclar cachés). REANUDAR=True recupera grillas y folds compatibles en outputs/experiment024. Los checkpoints previos de experiment023 permanecen intactos pero no se reutilizan automáticamente. El informe sale en outputs/informe_experiment024_es. Ver [experiment024](experiments/experiment024/README.md).


## experiment027 — Inferencia pareada de recall del top 10

Nuevo `notebook_inferencia_final_es.ipynb`, sin reentrenar ni alterar notebook final ejecutado. Recupera experiment024 desde NPZ privados, verifica firma/folds y cuatro métricas contra experiment026. Política principal recall 98 % cruzado, sensibilidad umbral 0.50; 45 pares por política, bootstrap conjunto 100k, McNemar exacto bilateral, Holm y Bonferroni, mapas triangulares y magnitud/FPR. Resultados exploratorios condicionados a OOF seleccionadas y umbrales fijos. Salidas outputs/experiment027; nunca publicar datos ni predicciones individuales. Reproducción y smoke en `experiments/experiment027/README.md`. No hay resultados numéricos nuevos sin checkpoints originales. Próximo experiment028.
