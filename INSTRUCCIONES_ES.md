# Reproducción del cuaderno final — experiment022

Conserve los datos y outputs locales. Desde la raíz:
```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
python experiments/experiment022/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
Cambie las banderas **en la única celda de configuración** y reinicie el kernel; no agregue otra celda de configuración antes de ella.

| Modo | EJECUTAR_PROTOCOLO_COMUN | CARGAR_PROTOCOLO_COMUN | REUTILIZAR_INDIVIDUALES | EJECUTAR_EXTENSION_TOP10 |
|---|---|---|---|---|
| Completo desde cero (predeterminado) | True | False | False | True |
| Reanudar después de sección 3 de exp021 | True | False | True | True |
| Exp021 ya completo, ajustar extensión | False | True | False | True |
| Exp021 y exp022 completos, solo gráficos | False | True | False | False |
| Histórico | False | False | False | False |

Mantenga EJECUTAR_BUSQUEDA_HIBRIDA=False y N_BAGGING=5. La extensión evalúa 18 variantes individuales y corrección logística K-means fija además de los ocho candidatos de experiment021. Se ordena por ROC AUC OOF y se comparan los diez mejores distintos. Resultados nuevos en outputs/experiment022/; figuras, top10.csv y envío en outputs/informe_top10_es/. Los NPZ son privados y nunca se suben. El smoke test y la corrida nueva están pendientes de ejecución. Véase [experiment022](experiments/experiment022/README.md).
