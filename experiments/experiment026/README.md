# experiment026 — Presentaciones y resultados de experiment024

La corrida entregada por el propietario (informe_experiment024_es.zip y notebook ejecutado en commit 4d764657177b13204689675541dd196d74296ba0) confirma 699960 filas train, 299984 test, 40 candidatos, 10 finalistas, XGBoost CUDA, CatBoost GPU y 32 hilos CPU. Ganador nominal Logística + XGBoost | standardized_kmeans_dbscan, AUC OOF 0.9459909936140145, AP 0.507053935766631. Delta contra standardized 0.0000803208773638; no hay IC bootstrap nuevo, score Kaggle ni benchmark de tiempo. El ZIP no incluye summary.csv de los 40 candidatos ni la selección por fold; no se inventan cifras.

Dos fuentes Marp: corta 42 diapositivas y completa 53, con todas las 27 figuras de la corrida más el diagrama del pipeline. Guiones y tema nuevos; fuentes anteriores archivadas. No se reentrenó. Los PNG versionados proceden de las salidas inline del notebook ejecutado (misma corrida y ranking); los PNG del ZIP son las exportaciones de mayor resolución y pueden sustituirlos. Se conservan el top10 y resumen exactos de la fuente y las métricas agregadas de umbrales. Nunca publicar el envío individual.

## Reproducción

Desde la raíz, con Python, Node.js y navegador:

```powershell
git pull --ff-only origin main
.\presentation\build_slides.ps1
```

Para sustituir las figuras inline por las exportaciones originales y recuperar las tablas agregadas originales, ejecutar:

```powershell
.\presentation\build_slides.ps1 -FiguresDirectory "C:\ruta\informe_experiment024_es.zip"
```

El importador valida firma y ranking y sólo copia PNG y agregados. La compilación oficial Marp y revisión visual PDF quedan pendientes: el entorno de edición no dispone de Marp CLI ni acceso a npm. Se detectó que main cambió durante la edición a la revisión ejecutada del propietario; se preserva esa revisión sin modificar el notebook. El hotfix histórico de experiment025 (bbfe751) no es ancestro del nuevo main y no se reincorpora automáticamente. Próximo experimento027 (reservado experiment025 en el historial).
