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


## experiment028 — AUC pareado y mapas Seaborn con p-valores originales

Actualiza notebook_inferencia_final_es.ipynb sin alterar entrenamiento ni resultados previos. Recall conservado, DeLong pareado y bootstrap AUC estratificado exacto de ambas clases (2 000 réplicas, semilla 42, hasta 4 hilos, caché por 50); 45 pares por familia, Holm/Bonferroni, diferencias e IC, curvas ROC originales. Estilo seaborn whitegrid/dark/notebook original; mapas de p continuos con escala [0,1], anotaciones y CSV precisos. Salidas outputs/experiment028/figuras y tablas en outputs/experiment028. Inferencia exploratoria; no publicar datos ni NPZ. Sin resultados nuevos hasta ejecutar con predicciones privadas. Ver experiments/experiment028/README.md. Próximo experiment029.


## experiment029 — Inferencia final simplificada de F1

Notebook activo reducido a ocho celdas y dos figuras: dashboard 1×2 p bootstrap y Holm (45 pares), IC 95 % de diferencia F1 contra ganador AUC. Nombres originales completos; umbral cruzado recall 98 % original, 100k bootstrap estratificado de patrones, semilla 42, sin reentrenar. Resultados outputs/experiment029, figuras PNG/PDF, versión anterior archivada. Inferencia exploratoria condicionada; no nuevos resultados sin NPZ privados. Ver experiments/experiment029/README.md. Próximo experiment030.
