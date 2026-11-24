# experiment018 — Búsqueda anidada de corrección XGBoost con decisiones de representación

**Objetivo:** integrar, antes de la selección final, cuatro representaciones de la primera etapa logística y una grilla explícita de 36 configuraciones del booster corrector. El experimento no inventa observaciones: K-means y DBSCAN solo construyen características adicionales.

## Protocolo

- Datos completos: 699 960 transacciones, 5 folds externos estratificados con semilla 42.
- **Hiperparámetro de representación:** original / K-means / DBSCAN / K-means+DBSCAN, aplicados a **la regresión logística**. XGBoost corrector recibe los predictores originales para aislar esta elección, ya que experiment015 no mostró ventajas de introducir agrupamientos en ambos niveles.
- Dentro de cada fold externo: muestra estratificada de 36 000 filas de entrenamiento (sin observaciones de validación externa), 3 folds internos; cada división refita imputación, codificación, escalado, PCA y K-means/DBSCAN, y logística. Posteriormente se evalúan **36** combinaciones de profundidad `[3,5,7,10,15,30]`, learning rate `[.04,.08]`, min_child_weight `[5,10,15]` con 240 árboles, subsample=.85 y colsample_bytree=.85.
- XGBoost recibe el logit de la regresión logística mediante `base_margin` **tanto en el ajuste como en la predicción**. Se ejecuta una búsqueda de grilla equivalente a GridSearchCV, con caché limitada a las mismas divisiones internas; no se debe usar GridSearchCV directo sin un estimador que propague el margen a predict_proba.
- Se reentrenan en los 559 968 registros externos de entrenamiento la representación, la logística y la corrección XGBoost con los mejores parámetros elegidos internamente. Las predicciones de los cinco folds se integran en un vector OOF por variante, sin reutilizar las etiquetas de validación para seleccionar clusters o parámetros.
- Los resultados de experimentos 013–017 son referencias históricas **no intercambiables** con los nuevos OOF de esta búsqueda.
- Los OOF por fila se guardan localmente, fuera de Git. Los CSV agregados, manifiesto, resultados de bootstrap, tests y gráficas se preservan para la reproducción.

## Conclusión provisional

El notebook final **no** cambia automáticamente el finalista del experimento016. La selección debe basarse en los resultados completos y su incertidumbre, no en los primeros folds. Se conservan 0.946205 OOF ROC AUC para la corrección logística histórica y 0.946120 para el mejor XGBoost individual original; su diferencia +0.000085 tuvo un IC 95 % emparejado que incluyó cero.

## Tiempo computacional

`tiempos_historicos.csv` preserva tiempos **medidos de ajuste del booster** por fold de los experimentos 013 y 015. Estos tiempos **excluyen** el ajuste logístico, la construcción de variables y las búsquedas, por lo que **no representan costos totales de pipeline**. La figura solo compara este costo parcial correctamente etiquetado.

## Publicación

La publicación del código ejecutable en un repositorio público debe satisfacer además las reglas de divulgación de código de la competencia Kaggle. Los scripts completos y los datos por observación se entregan de manera separada, no se mezclan con los resultados agregados del repositorio.



## Ejecutado: resultados completos (24 de noviembre de 2026)

**Se concluyó el experimento sobre los 699 960 registros.** Se probaron cuatro representaciones de la regresión logística por cinco pliegues externos. En cada pliegue se ejecutaron tres particiones internas sobre 36 000 registros de entrenamiento para seleccionar entre 36 combinaciones del corrector XGBoost, dando 2 160 ajustes internos y 20 finales. El tiempo total fue ~995.8 segundos en Linux CPU. La búsqueda interna **no** utilizó el conjunto completo de ~560 000 registros de cada entrenamiento externo; los modelos finales **sí** se ajustaron en dicho conjunto.

| Representación de la logística | ROC AUC OOF | Precisión promedio |
|---|---:|---:|
| K-means | **0.945870122** | **0.505842779** |
| DBSCAN | 0.945860385 | 0.505404729 |
| K-means y DBSCAN | 0.945858027 | 0.505836662 |
| Variables originales | 0.945842155 | 0.505781679 |

En los veinte ajustes finales se eligió **profundidad 3, tasa de aprendizaje 0.04**; `min_child_weight` osciló entre 5, 10 y 15. El bootstrap emparejado estratificado (B=1 000, semilla 20261124) dio ΔAUC K-means vs originales **+0.000027967**, IC percentil 95 % **[−0.000149673,+0.000212603]**; DBSCAN Δ+0.000018230 IC [−0.000127343,+0.000159947]; ambas Δ+0.000015873 IC [−0.000165187,+0.000199146]. Todos incluyen cero. Se conserva el modelo histórico seleccionado (AUC 0.946205) como referencia nominal, **sin contrastar directamente dos corridas de configuración distinta**.

Los archivos `resultados/summary.csv`, `best_inner_params.csv`, `outer_fold_metrics.csv`, `training_times.csv`, `paired_auc_bootstrap.csv` y `manifest.json` están versionados. El paquete privado `Credit-Fraud_experiment018_final_es.zip` contiene scripts completos y 29+ figuras. Las OOF por transacción se guardan separadamente, no en el Git público.

Reproducir en PowerShell, tras extraer el ZIP privado en la raíz del repositorio y aportar el archivo Kaggle:

```powershell
conda activate lds1071-fraud
python experiments/experiment018/test_tuning.py
python experiments/experiment018/tuning_offset.py --data playground-series-s6e11.zip --output outputs/experiment018/full_699960 --inner-rows 36000 --outer-folds 5 --inner-folds 3 --n-estimators 240 --jobs 4
python experiments/experiment018/bootstrap_offset.py --input outputs/experiment018/full_699960/private_oof_predictions.npz --output outputs/experiment018/full_699960 --replicates 1000
jupyter lab notebook_final_es.ipynb
```

El código de la competencia publicado en GitHub requiere publicación equivalente en Kaggle conforme a las reglas. Próximo experimento: `experiment019`.


## Selección conjunta anidada de la representación

Una evaluación adicional reconstruyó el **hiperparámetro de representación** con la máxima AUC interna en cada fold externo, sin usar etiquetas de ese fold: originales en los folds 1,3,4,5 y K-means en el 2. El selector produjo ROC AUC **0.945855918**, AP 0.505804281, Δ +0.000013763 sobre la alternativa original. Un bootstrap emparejado estratificado B=1000 dio IC 95 % **[−0.000054228,+0.000077588]**, que incluye cero. Se registran `joint_selected_fold_choices.csv`, `joint_selected_summary.csv` y `joint_selected_bootstrap.csv`. Esto elimina la confusión entre **selección en los folds internos** y **elección del máximo sobre OOF externas**. No se modifica el finalista de entrega.
