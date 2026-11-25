# Presentaciones Marp actuales · experiment024

- [Corta](presentacion_corta/deck.md): 42 diapositivas.
- [Completa](presentacion_completa/deck.md): 53 diapositivas, 27 figuras más diagrama del pipeline.

Orden: problema y datos → EDA → preprocesamiento → geometría y clusters → diseño factorial → validación y grillas → ensambles → top 10 → ROC/PR/calibración → umbrales → conclusiones. Guiones actualizados, tema fraud-final-es, formato 16:9. Fuentes anteriores en archive/pre_experiment026.

## Compilar sin reentrenar

Desde la raíz, con Python, Node.js y navegador:

```powershell
.\presentation\build_slides.ps1
```

Las 27 figuras inline del notebook ejecutado se versionan en experiments/experiment026/resultados/figuras, por lo que no se requiere el informe ZIP para compilar. Para recuperar los PNG de mayor resolución del ZIP y sus tablas agregadas:

```powershell
.\presentation\build_slides.ps1 -FiguresDirectory "C:\ruta\informe_experiment024_es.zip"
```

También se acepta el directorio del informe, outputs/ o el ZIP depurado. El importador verifica firma y top10 exacto y copia sólo PNG y agregados; nunca el envío Kaggle. HTML/PDF oficiales en presentation/dist. No se han compilado aquí. build_presentaciones_es.py es un generador histórico: no usar para regenerar las fuentes nuevas.
