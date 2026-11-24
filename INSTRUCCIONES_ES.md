# Cómo abrir el cuaderno final

1. Extraiga el ZIP **dentro de la raíz** de `Credit-Fraud` sin borrar `outputs/`, las figuras o los modelos anteriores.
2. Verifique que `experiments/experiment016/resultados/` y `notebook_final_es.ipynb` estén en las rutas indicadas.
3. Coloque `playground-series-s6e11.zip` en la raíz o los CSV originales en `data/`.
4. Active el entorno existente y abra Jupyter:

```powershell
conda activate lds1071-fraud
python -m ipykernel install --user --name lds1071-fraud --display-name "Python (LDS1071 Fraud)"
jupyter lab notebook_final_es.ipynb
```

5. Seleccione `Python (LDS1071 Fraud)` y ejecute **Restart Kernel and Run All Cells**.
6. Las nuevas figuras se guardan bajo `outputs/informe_final_es/figuras/`.

**Configuración inicial:** `CORRER_BUSQUEDA_DE_EJEMPLO=False` y `MOSTRAR_TSNE=False`. Los resultados de modelos y ensambles que ya están entrenados se recuperan, sin volver a realizar los cientos de entrenamientos originales. La t-SNE opcional puede activarse con `MOSTRAR_TSNE=True`.

**Para crear `outputs/informe_final_es/envio_final_kaggle.csv`:** mantenga el archivo `outputs/ensemble_extension/five_way_oof_and_test_predictions.npz` que ya generó en su estación Windows, o coloque en la raíz el ZIP `ensemble_extension.zip` con ese archivo. El cuaderno valida los `id`, el orden y las probabilidades antes de exportar.

**Resultados:** modelo nominalmente elegido por ROC AUC OOF = regresión logística corregida con XGBoost. Su diferencia frente al mejor XGBoost individual es pequeña y su intervalo de confianza emparejado incluye cero.