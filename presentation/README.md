# Presentaciones del proyecto final — fraude con tarjeta

Esta carpeta conserva la primera presentación (`deck.md`, `slides.html`, `slides.pdf`) y agrega **dos nuevas presentaciones en español**.

## 1. Presentación corta: máximo 20 minutos

- Ruta: `presentacion_corta/`
- **20 diapositivas**, con un guion planificado de **17.55 minutos**, más transiciones/preguntas.
- Presenta el proceso completo de selección: desbalance, EDA, no linealidad, outliers, modelos lineales, PCA, random forest, XGBoost/CatBoost, CV, GridSearchCV, blending, offset boosting, métricas de negocio y límites de decisión.
- Incluye 13 figuras seleccionadas de las 44 originales.
- Entregables: `deck.md`, `slides.html`, `slides.pdf` y `guion_del_presentador.md`.

## 2. Presentación completa

- Ruta: `presentacion_completa/`
- **75 diapositivas**, con las **44 figuras** originales, cada una explicada.
- Incluye fundamento matemático, supuestos de regresión logística, justificación de cada modelo, prevención de leakage, búsqueda anidada, distinción bagging/blending/stacking, corrección del logit, estabilidad por folds, calibración y límites de resultados.
- Entregables: `deck.md`, `slides.html`, `slides.pdf`, `guion_del_presentador.md`.

## Compilación y requisitos

Los HTML/PDF se prepararon mediante un renderizador Python/ReportLab local; el Markdown sigue el formato Marp y puede recompilarse con Marp CLI. El PDF es estático; las transiciones sólo existen en HTML. La carpeta `themes/` incluye el tema `fraud-es.css`.

**Opción offline**, en PowerShell desde `final_project/presentation/`:

```powershell
conda activate lds1071-fraud
python -m pip install Pillow reportlab
python .\build_presentaciones_es.py
```

**Marp CLI oficial** para cada presentación:

```powershell
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_corta\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --template bespoke -o .\presentacion_corta\slides-marp.html
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_corta\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --pdf -o .\presentacion_corta\slides-marp.pdf
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_completa\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --template bespoke -o .\presentacion_completa\slides-marp.html
npx --yes @marp-team/marp-cli@4.5.1 .\presentacion_completa\deck.md --theme-set .\themes\fraud-es.css --allow-local-files --pdf -o .\presentacion_completa\slides-marp.pdf
```

Al abrir `slides.html`: flechas de dirección para cambiar de diapositiva; `N` para consultar notas; clic en figura para ampliarla; `Escape` para cerrar. Los HTML contienen las imágenes incorporadas y no necesitan archivos externos.

## Precisión metodológica

- La combinación de probabilidades implementada es **blending**, no bootstrap bagging clásico (aunque RandomForest sí combina árboles mediante un mecanismo de tipo bagging).
- El experimento `LogisticOffsetXGBClassifier` implementa **offset boosting**: logit base más correcciones XGBoost a los log-odds; no es stacking clásico con meta-regresión logística.
- Un meta-modelo de stacking sobre predicciones OOF se menciona como una alternativa metodológica, **no como un entrenamiento ya realizado**.
- `figures.zip` contenía sólo imágenes y no los CSV de métricas definitivas. No se atribuyen ganadores exactos ni puntajes de test que no puedan verificarse. Para cerrar la narrativa cuantitativa, adjuntar los artefactos del run completo `outputs/ensemble_metrics.csv`, `candidate_metrics.csv`, `fold_metrics.csv` y `run_manifest.json` (sin datos por transacción).
- Se preservan los 44 PNGs de `../outputs/figures/` sin alteraciones.

## Restricción de publicación

El proyecto está basado en la competencia Kaggle S6E11. No publicar notebooks, código de competencia o archivos derivados públicamente en GitHub antes de cumplir las reglas de compartición pública correspondientes de Kaggle. El ZIP se entrega de manera privada al propietario.
