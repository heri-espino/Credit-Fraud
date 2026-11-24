# Presentación técnica completa

Diapositivas: **75**. Todas las **44 figuras originales** aparecen una vez y en orden de análisis.

## Contenido
- `deck.md`: fuente editable **compatible con Marp**, en español.
- `slides.html`: archivo HTML autónomo (figuras incorporadas, transición fade, teclado, ampliación y notas con `N`).
- `slides.pdf`: versión 16:9 de 75 páginas, estática, con texto seleccionable.
- `guion_del_presentador.md`: interpretación y guion de la exposición.
- Los PNG originales se encuentran en `../../outputs/figures/` y **no fueron modificados**.

## Abrir la presentación
Abre `slides.html` en un navegador. Usa flechas para avanzar y retroceder, `N` para consultar notas y haz clic sobre una imagen para ampliarla. El PDF no puede mostrar animaciones.

## Exportación con Marp CLI (en PowerShell, desde final_project/presentation/)
```powershell
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_completa\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --template bespoke -o .\presentacion_completa\slides-marp.html
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_completa\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --pdf -o .\presentacion_completa\slides-marp.pdf
```

**Proveniencia de exportación:** los archivos HTML/PDF incluidos fueron construidos con el exportador offline reproducible `build_presentaciones_es.py`, no con Marp CLI. El archivo Markdown sí está preparado para Marp. La apariencia del renderizado de Marp CLI podría variar ligeramente. Para reconstruir los entregables empaquetados, ejecuta `python .\build_presentaciones_es.py`.

## Sobre los resultados
El material usa el notebook y las figuras aportadas por el usuario. El archivo `figures.zip` contenía imágenes, **no** los CSV completos de resultados del entrenamiento definitivo. Por ello se explican tendencias y reglas de decisión sin inventar cuál estrategia exacta ganó el full run. Los resultados de smoke tests anteriores no se presentan como resultados del experimento completo. La regresión logística con correcciones de XGBoost es **offset boosting**; no se afirma que se haya ajustado un meta-modelo de stacking clásico.
