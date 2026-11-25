# Reproducción del cuaderno final — experiment024 acelerado

```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
nvidia-smi
python experiments/experiment024/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
Reiniciar kernel y ejecutar todo. Por defecto GPU auto y CPU_JOBS=-1, GRID_JOBS=4. Un ajuste GPU a la vez. Para exigir GPU, DISPOSITIVO_XGB='cuda', DISPOSITIVO_CATBOOST='GPU'. CPU fallback solo durante la prueba inicial. Si RAM saturada, GRID_JOBS=2/1. Si VRAM insuficiente, cambiar dispositivo en una corrida nueva (no mezclar cachés). REANUDAR=True recupera grillas y folds compatibles en outputs/experiment024. Los checkpoints previos de experiment023 permanecen intactos pero no se reutilizan automáticamente. El informe sale en outputs/informe_experiment024_es. Ver [experiment024](experiments/experiment024/README.md).
