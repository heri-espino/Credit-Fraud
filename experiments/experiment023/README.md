# experiment023 — Representación como hiperparámetro factorial

Objetivo: separar el efecto del escalado y el de las características K-means + DBSCAN en todas las familias. Cuatro representaciones: raw, standardized, raw_kmeans_dbscan y standardized_kmeans_dbscan. Raw significa numéricas imputadas no escaladas, con booleanas 0/1 y one-hot para categorías; no significa alimentar strings al clasificador. Geometría común estandarizada, PCA 90 %, K-means k=5, DBSCAN min_samples=5, cuantil .90 para epsilon. Ocho características derivadas, distancias escaladas solo en la rama standardized; ruido binario. PCA y splines dejan de ser candidatos separados para respetar el diseño de cuatro alternativas.

5 folds externos y 3 internos comunes, muestra interna estratificada de hasta 36k. Grillas por representación: LR 8, RF 9, XGB 36, CatBoost 8 (244 configuraciones por fold, 3 660 ajustes internos). Cuatro familias × cuatro representaciones fijas más cuatro selectores adaptativos = 20 individuales. Cuatro ensambles × cinco escenarios (incluido adaptive) = 20 ensambles. Stacking y offset usan la misma grilla XGB de 36 (5 400 ajustes internos de booster adicionales; más refits, bases auxiliares y cinco réplicas bootstrap). En offset, LR se selecciona por su AUC interna y el corrector emplea su misma representación. En stacking, la elección previa de las bases condiciona la evaluación interna; el fold externo permanece retenido. La selección adaptativa no utiliza AUC externa. El ranking final elimina duplicados exactos OOF/test y selecciona hasta diez; no hay garantía de que el híbrido gane.

## Reproducción

Desde la raíz, con el entorno lds1071-fraud y los CSV/ZIP privados:
```powershell
python experiments/experiment023/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
Reiniciar kernel y ejecutar todas las celdas. REANUDAR=True recupera checkpoints por fold de individuales y por escenario/fold de ensambles, verificados por firma de datos/configuración/código; REANUDAR=False vuelve a ajustar y sobrescribe checkpoints. No reutiliza cachés anteriores. Agregados: outputs/experiment023/individual_grid.csv, individual_selected.csv, individual_summary.csv, grid_results.csv, selected_params.csv, summary.csv. Informe y gráficos en outputs/informe_experiment023_es/. Los NPZ y envíos por fila permanecen privados. Se archiva la versión previa y se conserva el SVG metodológico nuevo.

## Estado y próximos pasos

Implementación y prueba sintética preparadas; no ejecutadas sobre datos originales en la sesión de edición. No existen nuevas AUC verificadas. Ejecutar primero el smoke, revisar convergencia de LR raw y tiempo/memoria, luego ejecutar la corrida completa, revisar top 10, guardar agregados y realizar bootstrap exploratorio si se requiere. El conjunto original y predicciones no están en Git. Publicación equivalente en Kaggle pendiente conforme a reglas. Próximo experimento024.
