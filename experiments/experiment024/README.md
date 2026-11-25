# experiment024 — Aceleración del protocolo factorial (sin reducir las grillas)

## Qué y por qué
experiment023 es el protocolo de referencia: cuatro representaciones, cuatro familias, cinco folds externos, tres internos, hasta 36k filas internas, 36 configuraciones XGBoost, 240 árboles/iteraciones, 40 candidatos nominales, top 10 por AUC OOF. El cuello de botella es la ejecución serial de 9 060 ajustes internos nominales más refits y bases de stacking. Se mantiene el diseño estadístico y se optimiza la ejecución:

- XGBoost `tree_method='hist', device='cuda'` y CatBoost `task_type='GPU', devices='0'` si la prueba de ajuste/predicción CUDA tiene éxito. XGBoost verifica el dispositivo realmente activo, ya que puede caer a CPU automáticamente. Se puede exigir GPU o elegir CPU por biblioteca. Auto usa CPU si la prueba falla; un fallo durante un ajuste posterior no se oculta ni cambia silenciosamente de dispositivo.
- CPU_JOBS=-1 usa todos los núcleos lógicos disponibles (joblib.cpu_count); GRID_JOBS=4 evalúa hasta cuatro configuraciones CPU en paralelo con memoria compartida y presupuesto de hilos repartido. RF, XGB CPU y CatBoost CPU reciben los hilos asignados; BLAS limitado para evitar sobresuscripción. Ajustes GPU en serie. Las matrices geométricas se construyen en CPU, con paralelismo acotado.
- Stacking: las mismas matrices se reutilizan entre escenarios para cada split; se ajusta cada combinación familia/representación/parámetros una vez por split, y se conservan solo probabilidades. El entrenamiento externo usa una única matriz por representación compartida entre ensambles. Offset y bagging adaptativos reutilizan resultados de escenario fijo si la base y configuración coinciden. Se conservan sus filas de grilla para auditoría, aunque no sean nuevos ajustes físicos. Se mantienen las semillas y los límites de cada fold.
- Checkpoints atómicos por lote de configuraciones y por fold/escenario; reanudar sin repetir grillas completadas. Los cross-fits auxiliares y refits no terminados pueden repetirse. Firma de datos, grillas, fuente del motor, dispositivos, número de hilos y versiones. Los checkpoints experiment023 se preservan y no se mezclan automáticamente; el motor nuevo usa outputs/experiment024. Cambiar hardware/parámetros/versión requiere otro directorio o reiniciar con REANUDAR=False.

## Cómo reproducir
```powershell
git pull --ff-only origin main
conda activate lds1071-fraud
nvidia-smi
python experiments/experiment024/smoke_test.py
jupyter lab notebook_final_es.ipynb
```
Configuración predeterminada: REANUDAR=True, CPU_JOBS=-1, GRID_JOBS=4, DISPOSITIVO_XGB='auto', DISPOSITIVO_CATBOOST='auto'. Para exigir GPU, 'cuda' y 'GPU' respectivamente. Si CUDA falla en la prueba, auto cae a CPU; si falla en entrenamiento (p. ej. profundidad 30 y VRAM), conservar outputs existentes y escoger CPU en nueva corrida/directorio. Reducir GRID_JOBS a 2/1 si RAM o CPU saturadas. Verificar GPU durante entrenamiento con nvidia-smi -l 2. Se mantienen todos los 36 candidatos, incluso profundidad 30; no se promete aceleración concreta sin medir. Para medir y comparar, ejecutar con datos, versiones y dispositivos registrados; hardware.json guarda la configuración. Las bibliotecas pueden tener defaults diferentes en GPU y CPU (especialmente CatBoost) y el orden de sumas GPU no es determinista; no se espera igualdad bit a bit. No interpretar cambio de AUC como resultado exclusivo de optimización.

## Resultados, estado y próximos pasos
No se ejecutaron los ajustes completos ni la prueba sintética en el entorno de edición; CUDA real debe verificarse en el equipo del propietario. Se conserva el módulo, documentación y notebook exp023 en el repositorio (snapshot en archive/). Agregados en outputs/experiment024, gráficos y envío en outputs/informe_experiment024_es; archivos privados no se publican. La prueba sintética fuerza CPU, comprueba grillas, paralelismo, checkpoints y 40 candidatos. El siguiente paso es ejecutar smoke, verificar el hardware impreso, medir el tiempo por etapa y completar el ranking. Próximo experiment025. Publicación equivalente en Kaggle pendiente.
