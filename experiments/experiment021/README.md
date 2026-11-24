# experiment021 — Ensambles con XGBoost y grilla común

**Estado:** implementación versionada. No se ha ejecutado el entrenamiento completo ni el smoke test en esta sesión. Las métricas de experiment019/020 no son resultados de este protocolo.

## Diseño

Sección 3: logística, bosque aleatorio, XGBoost y CatBoost, cinco folds externos estratificados, 3 internos sobre hasta 36 000 filas de entrenamiento externo, cuatro representaciones por familia (más PCA y splines para logística). XGBoost: 36 configuraciones por representación, 144 por fold externo. Se conservan probabilidades externas y de prueba de cada fold.

Sección 4: (1) promedio uniforme de las cuatro familias, sin nuevos ajustes; (2) bagging clásico del XGBoost seleccionado con 5 réplicas bootstrap de filas de entrenamiento, preprocesamiento fijo de ese fold; (3) stacking XGBoost sobre cuatro columnas de probabilidades; (4) corrección de logits XGBoost de la mejor logística por su propia AUC interna. Los tres boosters comparten exactamente la grilla depth=[3,5,7,10,15,30], eta=[.04,.08], child=[5,10,15], 240 árboles, subsample=.85 y colsample=.85.

Stacking: para cada split interno meta, construir OOF de bases dentro del meta-train mediante 2 folds y ajustar bases en meta-train para producir meta-val. Los parámetros de bases son los seleccionados previamente dentro del entrenamiento externo, por lo que la AUC interna del meta-modelo es condicional y no independiente de la selección previa. Para refit final, generar 3-fold OOF de bases en todo el outer train, ajustar meta y predecir con las columnas externas de sección 3. No se usan etiquetas del outer val en entrenamiento ni selección. Offset: base_margin en fit y predict; selección de LR antes del corrector.

260 configuraciones individuales por fold + 36 stacking + 36 offset = 332 configuraciones por fold, 4 980 ajustes internos de candidatos (3 900 individuales, 540 stacking y 540 offset), más ajustes de bases para cross-fitting, refits y 25 réplicas bootstrap de bagging con valor predeterminado. Los ocho candidatos se comparan por ROC AUC OOF. El máximo observado no equivale a una evaluación independiente.

## Reproducción

Desde la raíz y con el entorno lds1071-fraud activo:
```powershell
git pull --ff-only origin main
python experiments/experiment021/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
El smoke test usa datos sintéticos, grillas y árboles reducidos después de comprobar las 36 configuraciones reales; compila todas las celdas, verifica las 8 probabilidades y el checkpoint. No sustituye la ejecución completa.

Configurar `EJECUTAR_PROTOCOLO_COMUN=True`, `CARGAR_PROTOCOLO_COMUN=False`, `REUTILIZAR_INDIVIDUALES=False` y `EJECUTAR_BUSQUEDA_HIBRIDA=False`. Restart Kernel and Run All. Después de completar sección 3, se guarda el checkpoint privado; para repetir sección 4 sin entrenar las bases de nuevo, use `REUTILIZAR_INDIVIDUALES=True` junto con EJECUTAR=True. Al terminar toda la corrida use EJECUTAR=False, CARGAR=True, REUTILIZAR=False para regenerar figuras sin entrenamiento. El modo histórico por defecto mantiene ambos flags de ejecución/carga False.

Outputs: `outputs/experiment021/` (agregados grid_results.csv, selected_params.csv, summary.csv, individual_grid.csv, individual_selected.csv; NPZ privados), `outputs/informe_ensambles_es/` (figuras, métricas de alerta y envio_final_kaggle.csv). Cache verifica IDs y etiquetas; no subir NPZ ni datos de Kaggle. El notebook anterior está archivado íntegramente.

## Verificación y próximos pasos

Se inspeccionó el notebook JSON y el flujo de dependencias en GitHub, se añadió smoke test reproducible. No se dispone de Python conectado al repositorio ni de datos privados en esta sesión; ejecutar el smoke test y la corrida completa, revisar los agregados y conservarlos en el repositorio sin archivos privados. No afirmar resultados nuevos hasta ejecutar. Publicación equivalente en Kaggle pendiente según reglas del concurso. Próximo experimento: experiment022.
