"""Build two Spanish-language Marp-compatible presentations with standalone HTML and PDF.

Run: python build_presentaciones_es.py
Inputs: ../outputs/figures/*.png (44 preserved original figures)
Offline renderer follows the same structured slide data as the Marp Markdown export.
It does not claim that offline HTML/PDF were exported with marp-cli.
"""
from __future__ import annotations
from pathlib import Path
import base64, hashlib, html, io, json, math, re, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
FIG=ROOT.parent/'outputs'/'figures'
SHORT=ROOT/'presentacion_corta'
FULL=ROOT/'presentacion_completa'
for dest in (SHORT,FULL):dest.mkdir(exist_ok=True,parents=True)

# Each record: file, Spanish title, how it was made, evidence/interpretation, limitation, chapter.
FIGURES=[
('01_target_and_missingness.png','Balance de clases y completitud','Se cuantificó la frecuencia de fraude y se revisaron valores faltantes por variable.','La clase positiva es poco frecuente: la exactitud global sería una guía engañosa.','El desequilibrio exige estratificación y métricas de ranking; no implica aplicar sobremuestreo automáticamente.',1),
('02_numeric_distributions.png','Distribuciones numéricas','Se trazaron histogramas y distribuciones marginales para revisar escala, asimetría y colas.','Los predictores presentan escalas distintas y algunos valores extremos; conviene estandarizar para modelos lineales.','Una distribución sesgada no determina por sí sola utilidad predictiva.',1),
('03_class_conditional_densities.png','Distribuciones según la clase','Se compararon densidades de variables numéricas separando fraudes y operaciones legítimas.','La superposición entre las dos clases motiva combinar variables; la separación parcial sugiere señal disponible.','Las densidades normalizadas por clase no representan la prevalencia real de fraude.',1),
('04_pearson_spearman_correlations.png','Correlaciones de Pearson y Spearman','Se comparó asociación lineal (Pearson) y asociación monótona de rangos (Spearman).','Las matrices permiten detectar redundancias y relaciones que no son exactamente lineales.','Correlación no implica causalidad; ninguna de las dos detecta todas las dependencias no monótonas.',1),
('05_categorical_risks.png','Riesgo por categorías','Se estimó la tasa observada de fraude por categoría y su soporte muestral.','Algunas categorías presentan niveles de riesgo diferentes, lo que justifica incluirlas en el modelado.','Categorías con pocas observaciones pueden producir tasas muy inestables.',1),
('06_flag_prevalence_vs_fraud.png','Indicadores booleanos: frecuencia y riesgo','Se contrastó qué tan frecuente es cada bandera con la tasa de fraude asociada.','Una bandera poco frecuente puede resultar informativa si aumenta considerablemente el riesgo condicional.','La asociación marginal puede desaparecer al ajustar por otros predictores.',1),
('07_nonlinear_binned_fraud_rates.png','No linealidad de las tasas de fraude','Las variables continuas se dividieron en intervalos cuantílicos y se calculó la tasa observada de fraude.','Las curvas muestran perfiles curvos y, en algunos casos, no monótonos; motivan splines y modelos de árboles.','El agrupamiento por intervalos no demuestra efectos causales ni linealidad condicional.',2),
('08_time_patterns.png','Patrones temporales de fraude','Se analizaron tasas por hora, día y otras variables temporales disponibles.','Puede existir estacionalidad del riesgo y ser útil un modelo que capture efectos temporales.','La agregación no prueba estabilidad futura ni sustituye una validación temporal.',2),
('09_bivariate_interaction_heatmaps.png','Interacciones entre variables numéricas','Se cruzaron intervalos de dos predictores y se estimó la tasa de fraude de cada celda.','Combinaciones de riesgo elevado pueden mostrar intensificación no explicada por cada variable por separado.','Se debe revisar el número de transacciones por celda para evitar conclusiones por ruido.',2),
('10_univariate_outliers.png','Valores extremos: criterio IQR','Se utilizaron cercas basadas en el rango intercuartílico para caracterizar extremos marginales.','Los extremos pueden ser transacciones válidas y contener señal de fraude.','Un outlier no es sinónimo de fraude ni justifica eliminar datos automáticamente.',2),
('11_isolation_forest_anomaly_diagnostics.png','Anomalías con Isolation Forest','Se ajustó un detector no supervisado a una muestra y se contrastaron las anomalías con la etiqueta.','El enriquecimiento de fraude entre transacciones anómalas sugiere una señal descriptiva adicional.','No equivale a rendimiento validado de un detector supervisado; el parámetro contamination no es la prevalencia.',2),
('12_candidate_scores_and_folds.png','Comparación de candidatos en cinco folds','Se calcularon ROC AUC out-of-fold por candidato y por partición.','El desempeño medio debe juzgarse junto con su variación entre particiones y familias.','La elección del máximo dentro del mismo CV introduce optimismo de selección.',3),
('13_oof_prediction_correlations.png','Correlación entre modelos','Se compararon los vectores de probabilidades OOF de todos los candidatos.','Correlaciones elevadas indican que muchos modelos ordenan de manera semejante a las transacciones.','Correlación de probabilidades no garantiza coincidencia en el 1% de mayor riesgo.',3),
('14_ensemble_comparisons.png','Modelo individual frente a combinaciones','Se compararon el mejor individuo, top 3, uno por familia y todos los candidatos.','Agregar todos los modelos no garantiza mejora; se necesita medir el beneficio incremental del blend.','El blend seleccionado con los mismos OOF debe validarse en una muestra independiente.',3),
('15_oof_roc_pr_curves.png','Curvas ROC y precisión–recobrado','Se trazaron curvas ROC y precision–recall con predicciones fuera de fold.','ROC AUC mide ordenamiento; average precision pone atención en el desempeño con eventos raros.','Ninguna curva fija por sí sola un umbral operativo.',3),
('16_pca_explained_variance.png','SVD/PCA: 90% de varianza','Se proyectaron variables procesadas sobre componentes principales y se acumuló la varianza explicada.','La reducción es una alternativa de representación, no una mejora predictiva garantizada.','La varianza de X y la información predictiva sobre Y son objetivos distintos.',3),
('17_assumptions_vif_and_feature_shift.png','Supuestos logísticos y posibles cambios','Se revisaron indicadores de colinealidad y desplazamientos entre variables y muestras.','Es necesario separar problemas de especificación, dependencia y cambios de distribución.','Los diagnósticos no certifican por completo independencia ni ausencia de separación multivariante.',3),
('18_oof_logistic_assumption_checks.png','Diagnóstico de la regresión logística','Se compararon especificaciones lineales/no lineales, residuos agregados y calibración OOF.','Un modelo lineal en log-odds puede describir bien el ranking y aun así mostrar mala calibración.','Predictores normales y homocedasticidad NO son supuestos requeridos para logit.',3),
('19_logistic_offset_boosting_diagnostics.png','Corregir el logit con XGBoost','Se entrenó primero logit y después XGBoost con los logits iniciales como base_margin.','Las correcciones aprenden estructura residual; su utilidad se juzga mediante OOF ROC AUC y AP.','No es stacking clásico ni prueba automática de mejora; puede sobreajustar ruido.',3),
('20_univariate_feature_discrimination.png','Valor discriminativo de cada variable','Se estimó el AUC de predictores aislados y se compararon señales univariantes.','El análisis ayuda a seleccionar variables para estudio, no a reemplazar un modelo conjunto.','Un AUC univariante alto no asegura contribución incremental.',4),
('21_class_conditional_ecdfs.png','Distribuciones acumuladas por clase','Se trazaron funciones de distribución empírica condicionadas a fraude/no fraude.','Las diferencias en cuantiles complementan las densidades y pueden revelar cambios de cola.','Muestras equilibradas para visualizar no deben usarse para estimar prevalencia poblacional.',4),
('22_categorical_flag_interactions.png','Categorías × indicadores booleanos','Se cruzaron categorías e indicadores y se cuantificaron tasas y tamaños de celda.','Una misma bandera puede tener distinta asociación con el fraude según su contexto.','En celdas pequeñas, las tasas necesitan intervalos de incertidumbre.',4),
('23_weekly_hourly_fraud_surface.png','Mapa de riesgo por día y hora','Se representaron superficies de fraude por hora y día para buscar patrones conjuntos.','Puede haber concentraciones temporales no captadas por términos horarios aislados.','La composición de transacciones puede explicar parte del efecto observado.',4),
('24_pairwise_class_geometry.png','Geometría bivariante por clase','Se exploraron dispersiones y contornos de parejas de variables con clases diferenciadas.','Los patrones de separación multivariada justifican no depender solo de un predictor.','Las muestras de visualización no deben confundirse con la distribución completa.',4),
('25_train_test_ecdf_shift.png','Comparación entrenamiento–prueba','Se contrastaron ECDF de predictores entre entrenamiento y test sin usar etiquetas del test.','Permite detectar cambios marginales antes de enviar predicciones a Kaggle.','Igualdad de ECDF marginal no garantiza ausencia de cambio conjunto o de etiquetas.',4),
('26_four_metric_model_scorecard.png','Comparación con cuatro métricas','Se midieron ROC AUC, average precision, log loss y Brier por candidato con OOF.','La mejor discriminación no implica automáticamente las mejores probabilidades calibradas.','Optimizar varias métricas simultáneamente exige priorizar el objetivo oficial.',5),
('27_performance_vs_training_time.png','Rendimiento frente a costo computacional','Se cruzó calidad predictiva con tiempo de entrenamiento de los modelos.','Una mejora muy pequeña puede no compensar grandes costos de búsqueda o ajuste.','Los tiempos dependen del hardware y del uso efectivo de CPU/GPU.',5),
('28_oof_score_distributions.png','Distribuciones de riesgo predicho','Se compararon puntuaciones OOF de positivos y negativos por familia de modelos.','La separación entre distribuciones refleja discriminación; sigue existiendo solapamiento.','Una probabilidad extrema puede deberse a sobreconfianza, no necesariamente a certeza.',5),
('29_cumulative_gains_and_lift.png','Ganancia acumulada y lift','Se ordenaron transacciones por probabilidad para medir fraudes capturados a distintos presupuestos.','La pregunta operativa es cuántos fraudes detectamos al revisar un porcentaje limitado.','Las curvas no incluyen el costo real de las investigaciones o falsos positivos.',5),
('30_precision_recall_at_review_budget.png','Precisión y recobrado con capacidad limitada','Se evaluó la precisión y el recall al investigar las transacciones de mayor puntaje.','Es más operativo que fijar 0.5 cuando la prevalencia es aproximadamente 1.67%.','La mejor fracción a revisar depende de costos externos ausentes del dataset.',5),
('31_confusion_matrices_by_policy.png','Errores según política de decisión','Se compararon matrices de confusión con umbral 0.5 y revisión del 1% de mayor riesgo.','Un mismo clasificador puede producir decisiones muy distintas según la política.','No se deben comparar matrices sin especificar su regla de umbral.',5),
('32_model_reliability_comparison.png','Confiabilidad de las probabilidades','Se comparó probabilidad predicha con tasa observada en intervalos de riesgo.','Una buena curva ROC no garantiza que una predicción de 10% signifique 10% de fraudes.','Calibrar probabilidades debe evitar reutilizar las mismas etiquetas de evaluación.',5),
('33_calibration_with_wilson_intervals.png','Calibración e incertidumbre','Se calcularon tasas por intervalos de riesgo y bandas binomiales tipo Wilson.','Los intervalos hacen visible la incertidumbre, especialmente en bins pequeños.','Los intervalos son descriptivos y dependen del particionado de riesgo.',5),
('34_subgroups_channel.png','Rendimiento por canal','Se evaluaron métricas OOF desagregadas por canal de transacción.','La calidad global puede esconder subgrupos con menos capacidad discriminativa.','Se necesitan suficientes positivos y negativos para interpretar AUC por grupo.',5),
('34_subgroups_merchant_category.png','Rendimiento por categoría de comercio','Se comparó ROC AUC y AP por categorías de comercio.','Los errores pueden concentrarse en segmentos particulares y justificar auditoría adicional.','La tasa base difiere entre grupos y afecta de manera importante a AP.',5),
('35_top_risk_set_overlap.png','Coincidencia en el 1% de mayor riesgo','Se calculó la superposición de conjuntos de transacciones con el 1% de mayor puntuación.','Dos modelos muy correlacionados pueden elegir operaciones diferentes para investigar.','La superposición depende del presupuesto elegido y no da una métrica de calidad aislada.',6),
('36_model_feature_importance.png','Importancia de características','Se compararon coeficientes transformados de logit e importancias internas de árboles.','Las medidas ayudan a explicar el comportamiento de cada familia bajo distintas escalas.','Importancia no significa causalidad y es difícil de comparar entre modelos.',6),
('37_partial_dependence_models.png','Dependencia parcial: efectos aprendidos','Se varió cada variable de interés mientras se promediaba la respuesta de modelos ajustados.','Permite visualizar cómo el logit, los splines y los árboles cambian la puntuación con cada entrada.','Puede evaluar combinaciones de variables poco realistas cuando hay correlaciones.',6),
('38_blend_vs_single_predictions.png','Cómo cambia el riesgo con el blend','Se comparó la probabilidad del mejor individuo con la combinación seleccionada.','El promedio puede suavizar puntuaciones extremas y cambiar el orden de casos difíciles.','Menor dispersión no es sinónimo de mejor discriminación ni calibración.',6),
('39_submission_probability_sanity.png','Control de predicciones para Kaggle','Se cotejaron distribuciones y cuantiles de riesgo OOF frente a test no etiquetado.','La revisión detecta puntuaciones inválidas o desplazamientos muy grandes.','No ofrece una medida de rendimiento, pues las etiquetas de test son desconocidas.',6),
('40_hyperparameter_effects.png','Exploración de hiperparámetros','Se compararon configuraciones y su puntuación agregada en validación.','La profundidad y el learning rate controlan capacidad y riesgo de sobreajuste.','Variar varios parámetros a la vez dificulta atribuciones causales.',6),
('41_fold_auc_heatmap.png','Estabilidad del ROC AUC por fold','Se representó cada candidato contra las cinco particiones de validación.','La comparación pareada muestra si las mejoras persisten o dependen de un fold.','Cinco folds no son cinco experimentos independientes para inferencias fuertes.',6),
('42_gridsearch_full_parameter_space.png','Espacio completo de GridSearchCV','Se registró cada combinación de profundidad, learning rate y regularización explorada.','La visualización muestra sensibilidad del ajuste dentro de los folds internos.','El mejor valor interno no garantiza mejora en el fold externo.',6),
('43_nested_gridsearch_outer_results.png','Efecto del ajuste sobre folds externos','Se compararon XGBoost y CatBoost fijos frente a variantes con búsqueda interna.','La validación externa es el criterio correcto para juzgar si la búsqueda realmente ayudó.','Se debe distinguir el costo de GPU/CPU y no convertir diferencias pequeñas en certezas.',6),
]
assert len(FIGURES)==44 and len({r[0] for r in FIGURES})==44
for filename,*_ in FIGURES:assert (FIG/filename).exists(), filename
F={x[0]:x for x in FIGURES}

S=[];L=[]
def slide(title,lead='',cards=None,fig=None,kind='concept',tag='',message='',notes='',duration=0.8,body=None):
 return dict(title=title,lead=lead,cards=cards or [],figure=fig,kind=kind,tag=tag,message=message,notes=notes,duration=duration,body=body)
def card(h,t):return (h,t)
def add_short(**kwargs):S.append(slide(**kwargs))
def add_full(**kwargs):L.append(slide(**kwargs))

# ------------------------- SHORT VERSION: 20 slides -------------------------
add_short(title='¿Cómo seleccionamos un modelo para detectar fraude?',lead='Proyecto final LDS1071 · Kaggle Playground S6E11',kind='cover',tag='PRESENTACIÓN BREVE · 20 MIN',message='Del análisis exploratorio a una decisión validada con cinco folds.',notes='Presentar problema, objetivo oficial ROC AUC y la idea central: comparar hipótesis simples y complejas, no elegir complejidad por intuición.',duration=.5)
add_short(title='La pregunta y la ruta experimental',tag='01 · PROBLEMA',kind='flow',lead='Encontrar una regla que ordene las transacciones desde mayor hasta menor riesgo de fraude.',cards=[card('1 · Datos','Describir clases, distribuciones, interacciones y anomalías.'),card('2 · Modelos','Logit; PCA/splines; random forest; XGBoost y CatBoost.'),card('3 · Validación','5 folds estratificados; mismo protocolo; GridSearchCV interno.'),card('4 · Decisión','Probar blends, correcciones logísticas y robustez operativa.')],message='Criterio oficial: ROC AUC. Métricas de apoyo: AP, log loss, Brier y captura.',notes='Este diagrama resume lo que se hizo, no una lista de modelos arbitraria. Cada familia contrasta una hipótesis diferente sobre la relación entre X y fraude.',duration=.85)
add_short(title='El problema: fraude poco frecuente',tag='02 · EDA',kind='figure',fig='01_target_and_missingness.png',lead='699,960 operaciones etiquetadas · 11,689 fraudes · prevalencia cercana a 1.67%.',message='Se requieren validación estratificada y métricas de ranking; accuracy sola no basta.',notes='Destacar el denominador: un clasificador que predice siempre “no fraude” tendría alta accuracy y utilidad nula. No se eliminaron las observaciones raras por sistema.',duration=.9)
add_short(title='EDA: señal entre las dos clases',tag='02 · EDA',kind='figure',fig='03_class_conditional_densities.png',lead='Las distribuciones de fraude y no fraude se superponen: ningún predictor basta por sí solo.',message='Esto motiva modelar simultáneamente características numéricas, categóricas y booleanas.',notes='Explicar que se usaron densidades condicionadas para comparar forma, no para inferir prevalencias. Evitar causalidad.',duration=.85)
add_short(title='La relación no siempre es lineal',tag='02 · EDA',kind='figure',fig='07_nonlinear_binned_fraud_rates.png',lead='Tasas de fraude por cuantiles: se observan curvas y cambios de pendiente.',message='Motivación para splines, árboles y boosting frente a logit lineal en log-odds.',notes='Explicar binning y tasas marginales. Ejemplificar el cambio con el importe, velocidad y puntuación de riesgo del comercio. Las curvas no son efectos parciales.',duration=1)
add_short(title='Interacciones: el riesgo es contextual',tag='02 · EDA',kind='figure',fig='09_bivariate_interaction_heatmaps.png',lead='Combinaciones de dos características pueden concentrar tasas de fraude elevadas.',message='Un modelo puramente aditivo puede omitir interacciones relevantes.',notes='Explicar cómo se construye el heatmap: cruzar quintiles e indicar número de transacciones por celda. Interacción descriptiva no causal.',duration=.9)
add_short(title='¿Y las observaciones atípicas?',tag='02 · EDA',kind='figure',fig='11_isolation_forest_anomaly_diagnostics.png',lead='Extremos IQR + Isolation Forest para explorar anomalías sin utilizar las etiquetas para detectarlas.',message='Decisión: conservar outliers; una operación rara no es necesariamente un fraude.',notes='Diferenciar detección no supervisada y clasificación supervisada. Evitar presentar la tasa de anómalos como una estimación validada.',duration=.75)
add_short(title='Preprocesamiento sin fuga de información',tag='03 · METODOLOGÍA',kind='flow',lead='En cada fold, todas las transformaciones se ajustan exclusivamente con los datos de entrenamiento.',cards=[card('Entrada','Excluir id; separar predictores y etiqueta binaria.'),card('Codificación','Imputación y one-hot cuando corresponde; CatBoost usa categorías nativas.'),card('Escalamiento','StandardScaler para logit; PCA sólo como rama experimental.'),card('Predicciones OOF','Cada observación se predice sin haber entrenado el modelo con ella.')],message='5-fold StratifiedKFold · seed 42 · métricas y configuraciones guardadas.',notes='Explicar por qué PCA, imputación y escalado deben vivir dentro del Pipeline y no ajustarse una vez en todo el dataset.',duration=1)
add_short(title='¿Por qué comenzar con regresión logística?',tag='03 · MODELOS',kind='concept',lead='Es un benchmark reproducible, rápido e interpretable que modela la probabilidad de un evento binario.',cards=[card('Modelo','p(x) = σ(β₀ + βᵀx): relación lineal en los log-odds.'),card('Fortalezas','Regularización L2; probabilidades; coeficientes interpretables en escala transformada.'),card('Limitación','No aprende interacciones ni curvas arbitrarias sin ingeniería de variables.'),card('Diagnósticos','Binario ✓; dependencia, linealidad y calibración requieren auditoría.')],message='Logit estándar y logit con splines: prueba directa de no linealidad.',notes='Aclarar que no se necesita normalidad de X ni varianza constante. Añadir distinción entre supuestos de estimación e idoneidad predictiva.',duration=1)
add_short(title='SVD/PCA: ¿reducción útil o pérdida de señal?',tag='03 · MODELOS',kind='figure',fig='16_pca_explained_variance.png',lead='Se propuso conservar componentes que explican aproximadamente el 90% de la varianza de X.',message='Retener 90% de varianza no garantiza retener 90% de señal sobre fraude: se compara mediante CV.',notes='SVD de matriz estandarizada, X = UΣVᵀ. Contrastar logit con y sin PCA; PCA no debe imponerse a los árboles.',duration=.8)
add_short(title='Cinco familias para hipótesis distintas',tag='03 · MODELOS',kind='concept',lead='Todos los modelos compiten con las mismas particiones y el mismo objetivo ROC AUC.',cards=[card('Logit y splines','Baselines aditivos; estiman efecto global y curvatura suave.'),card('Random forest','Bagging de árboles, umbrales e interacciones; baja varianza.'),card('XGBoost','Boosting secuencial regularizado para capturar errores y patrones complejos.'),card('CatBoost','Boosting con manejo nativo de variables categóricas y GPU opcional.')],message='Más complejidad sólo se justifica con mejora fuera de entrenamiento.',notes='Separar bagging interno de random forest de la combinación posterior de modelos heterogéneos.',duration=.85)
add_short(title='Búsqueda de hiperparámetros',tag='04 · VALIDACIÓN',kind='figure',fig='42_gridsearch_full_parameter_space.png',lead='GridSearchCV de XGBoost/CatBoost: profundidad, learning rate y regularización.',message='La búsqueda ocurre dentro del entrenamiento de cada fold externo; se evalúa en el fold externo.',notes='Describir 8 combinaciones × 3 folds internos por familia y hasta 20k filas para tuning por fold externo. Reajuste en el train externo completo.',duration=.95)
add_short(title='¿Cuál modelo rindió mejor?',tag='04 · RESULTADOS',kind='figure',fig='26_four_metric_model_scorecard.png',lead='ROC AUC, average precision, log loss y Brier se comparan sobre predicciones OOF.',message='No existe un ganador automático por complejidad: evaluar ranking, probabilidad y costo.',notes='La imagen permite comparación visual, pero los CSV crudos del full run no se recibieron junto a figuras; no dar décimas inventadas. Selección oficial por ROC AUC.',duration=.85)
add_short(title='Intento 1: “bagging” de modelos',tag='05 · ENSEMBLES',kind='figure',fig='14_ensemble_comparisons.png',lead='Se guardaron TODOS los candidatos y se promediaron probabilidades: top 3, uno por familia y todos.',message='Nombre exacto: blending; no equivale al bootstrap bagging clásico.',notes='Mostrar que el promedio de todos no garantiza superar al mejor individuo. Explicar correlación entre predicciones y por qué diversidad importa.',duration=.85)
add_short(title='Intento 2: potenciar los errores de logit',tag='05 · ENSEMBLES',kind='figure',fig='19_logistic_offset_boosting_diagnostics.png',lead='Logit base + XGBoost que corrige los logits usando base_margin.',message='p(x)=σ[f_logit(x)+g_XGB(x)]; probar si las correcciones elevan AUC/AP OOF.',notes='Esto NO es stacking clásico. No se entrenó una meta-regresión logística con predicciones de varios modelos; para eso harían falta predicciones OOF de nivel 1 y otro proceso de evaluación.',duration=1.05)
add_short(title='Bagging, blending, stacking: no son lo mismo',tag='05 · ENSEMBLES',kind='concept',lead='La diferencia principal está en cómo se obtienen y combinan las predicciones.',cards=[card('Bagging','Mismo algoritmo en muestras bootstrap; agregación de resultados.'),card('Blending realizado','Promedio de probabilidades de familias y configuraciones diferentes.'),card('Stacking clásico','Modelo meta que aprende una combinación a partir de predicciones OOF.'),card('Offset boosting realizado','Árboles que corrigen la salida logit de una regresión logística fija.')],message='Reportamos lo implementado, sin atribuir al proyecto un meta-learner no ejecutado.',notes='Esta diapositiva es crucial para rigor conceptual. La idea original de bagging evolucionó a blends; la idea de stacking evolucionó a corrección en escala de log-odds.',duration=1.05)
add_short(title='Fraude capturado bajo un presupuesto',tag='06 · DECISIÓN',kind='figure',fig='29_cumulative_gains_and_lift.png',lead='Se ordenan transacciones por score y se mide qué fracción de fraudes cae en el top k%.',message='ROC AUC es el objetivo de Kaggle; captura y precisión describen utilidad operativa.',notes='Explicar lift como captura relativa a selección aleatoria. Para decidir umbral de producción faltan costos reales de revisión.',duration=.9)
add_short(title='¿Se pueden interpretar como probabilidades?',tag='06 · DECISIÓN',kind='figure',fig='32_model_reliability_comparison.png',lead='Calibración: comparar la probabilidad predicha con la frecuencia de fraude observada.',message='Un excelente ROC AUC no garantiza calibración; contrastar Brier y log loss.',notes='Diferenciar ordenar de estimar probabilidad real. Clases muy desbalanceadas hacen importantes estas gráficas.',duration=.75)
add_short(title='Decisión final y límite de evidencia',tag='06 · DECISIÓN',kind='figure',fig='43_nested_gridsearch_outer_results.png',lead='La decisión implementada es seleccionar por ROC AUC OOF entre el mejor individuo y blends predefinidos.',message='No afirmar una superioridad numérica definitiva sin el CSV del run completo ni una validación intacta.',notes='La figura compara resultados de tuning externo; no demuestra que GridSearchCV siempre ayude. La selección de blend sobre los mismos OOF genera optimismo. Para reproducir la selección exacta: consultar ensemble_metrics.csv y run_manifest.json del run real.',duration=1.1)
add_short(title='Conclusión: aprendimos del proceso, no sólo del ranking',tag='07 · CIERRE',kind='concept',lead='Una evaluación justa permite preferir un modelo simple o complejo por evidencia, no por intuición.',cards=[card('EDA','Desbalance, no linealidades, interacciones y anomalías sin eliminar datos.'),card('Modelos','Logit como punto de referencia; PCA, splines, RF, XGBoost y CatBoost contrastados.'),card('Ensembles','Blend de varios modelos y corrección de log-odds: comparar, no asumir ganancia.'),card('Pendiente','Confirmar resultados del run definitivo, validar selección y enviar CSV a Kaggle.')],message='Regla: maximizar ROC AUC OOF; documentar AP, calibración, estabilidad y costos.',notes='Cerrar con tres aprendizajes y reconocer limitación de selección. La prueba no etiquetada de Kaggle no permite verificar AUC offline.',duration=.65)
assert len(S)==20

# -------------------- FULL VERSION: preserve every supplied figure --------------------
add_full(title='Predicción de fraude con tarjetas: el proceso completo',lead='Análisis exploratorio · modelos · selección · ensambles · validación',kind='cover',tag='PRESENTACIÓN TÉCNICA EN ESPAÑOL',message='LDS1071 · Kaggle S6E11 · fuente: notebook y 44 figuras proporcionadas',notes='Este material distingue decisiones reproducibles, resultados exploratorios y aquello que requiere comprobación contra archivos CSV del run completo.')
add_full(title='Qué problema resolvemos y qué entregamos',tag='A · DEFINICIÓN',cards=[card('Entrada X','24 predictores numéricos, categóricos y booleanos; el identificador id se excluye.'),card('Objetivo Y','Variable binaria is_fraud, con prevalencia aproximada de 1.67%.'),card('Salida','Una probabilidad o score de fraude para cada fila del test.'),card('Evaluación','Kaggle usa el área bajo la curva ROC; AP/calibración explican otros aspectos.')],message='Un buen score ordena; una buena probabilidad también necesita calibración.',notes='Diferenciar clasificación probabilística, ranking y decisión binaria. El test de Kaggle carece de etiquetas públicas.')
add_full(title='Datos y desafío estadístico',tag='A · DEFINICIÓN',cards=[card('Tamaño','699,960 filas de entrenamiento; 11,689 casos de fraude.'),card('Clases','688,271 legítimas; ~1.67% positivas.'),card('Validez','No se observaron datos faltantes en entrenamiento; el id no entra al modelo.'),card('Cuidado','La exactitud puede ser alta prediciendo todo legítimo: preferir ROC AUC/AP.')],message='Fraude raro ≠ necesariamente anomalía aislada.',notes='La ausencia de missing no exime de usar pipelines robustos ante nuevos datos.')
add_full(title='Métricas: cada una responde otra pregunta',tag='A · DEFINICIÓN',cards=[card('ROC AUC','Probabilidad de que un positivo reciba mayor score que un negativo.'),card('Average precision','Resume precisión vs recobrado; especialmente informativa con una clase rara.'),card('Log loss / Brier','Evalúan calidad de probabilidades, no sólo ranking.'),card('Top-k y lift','Miden cuántos fraudes se capturan al revisar sólo cierta fracción.')],message='La métrica oficial fija el objetivo; las métricas auxiliares previenen conclusiones incompletas.',notes='No interpretar AUC como probabilidad individual de fraude. AP depende de la prevalencia.')
add_full(title='Diseño experimental en siete pasos',tag='A · MÉTODO',kind='flow',cards=[card('01','Revisar tipos, distribución, faltantes y relaciones.'),card('02','Diagnosticar no linealidades, interacciones y anomalías.'),card('03','Preparar pipelines sin fuga de información.'),card('04','Comparar familias y configuraciones en 5 folds.'),card('05','Afinar XGBoost/CatBoost con búsqueda interna.'),card('06','Evaluar blends y corrección de log-odds.'),card('07','Elegir estrategia OOF y preparar archivo Kaggle.')],message='Semilla 42; conservar resultados por fold y por candidato.',notes='La línea de trabajo preserva trazabilidad y ensayos fallidos, no sólo el mejor modelo.')
add_full(title='Validación cruzada sin data leakage',tag='A · MÉTODO',cards=[card('5 folds estratificados','Cada fold conserva aproximadamente la proporción de fraude.'),card('Pipeline','Imputación, escalado, one-hot, splines y PCA se ajustan sólo con train interno.'),card('OOF','Cada fila obtiene una predicción de un modelo que nunca entrenó con esa fila.'),card('Selección','Elegir el máximo en las mismas predicciones OOF causa cierto optimismo; un holdout posterior lo reduce.')],message='El CV permite comparar modelos con exactamente los mismos folds.',notes='Distinguir CV externo de 3-fold CV interno de GridSearchCV. El conjunto test de Kaggle no se usa para entrenar.')
add_full(title='¿Por qué explorar antes de modelar?',tag='B · ANÁLISIS EXPLORATORIO',cards=[card('Calidad','Detectar valores faltantes, duplicados potenciales y categorías raras.'),card('Geometría','Identificar colas, cambios de escala, dependencias y separabilidad.'),card('Hipótesis','Decidir si una frontera lineal puede ser razonable o es necesario introducir no linealidad.'),card('Precaución','Las asociaciones marginales no prueban efectos ajustados ni causalidad.')],message='Las figuras de EDA ayudan a formular hipótesis, no reemplazan la validación cruzada.')

def fig_full(fn,tag=None):
 file,title,method,interp,caveat,chapter=F[fn]
 return slide(title=title,lead=method,fig=fn,kind='figure',tag=tag or f'FIGURA · BLOQUE {chapter}',message=interp,notes=f'QUÉ SE HIZO: {method}\n\nINTERPRETACIÓN: {interp}\n\nLÍMITE: {caveat}',duration=.8)
for rec in FIGURES[:6]: L.append(fig_full(rec[0], 'B · DISTRIBUCIONES Y ASOCIACIONES'))
add_full(title='De correlaciones a relaciones no lineales',tag='C · NO LINEALIDAD',cards=[card('Problema','Una baja correlación no descarta una relación en U o interacciones.'),card('Herramienta','Binning cuantílico de variables, cruce de rangos y tasas condicionadas.'),card('Modelo lineal','La regresión logística es lineal en βᵀx, no en la probabilidad.'),card('Alternativas','Splines, árboles, boosted trees y transformación de variables.')],message='El EDA motivó candidatos adicionales; su valor se decide con CV.')
for rec in FIGURES[6:11]:L.append(fig_full(rec[0],'C · PATRONES Y ANOMALÍAS'))
add_full(title='Anomalía, outlier y fraude: tres conceptos',tag='C · ANOMALÍAS',cards=[card('Outlier','Observación extrema según una variable y una regla estadística.'),card('Anomalía','Patrón multivariante infrecuente, sin usar etiquetas.'),card('Fraude','Resultado etiquetado que puede ser típico o atípico.'),card('Decisión EDA','No borrar transacciones extremas automáticamente; compararlas descriptivamente.')],message='Eliminar colas puede destruir justamente la señal que queremos detectar.')
add_full(title='Pipelines de modelos: decisiones concretas',tag='D · PREPROCESAMIENTO',cards=[card('Regresión logística','Estandarización numérica, codificación de categorías y regularización L2.'),card('Logit con splines','SplineTransformer para importe, velocidad y riesgo del comercio.'),card('Árboles','Random forest y XGBoost aprenden cortes; no exigir PCA.'),card('CatBoost','Procesamiento nativo de categorías, con imputación y GPU opcional.')],message='La transformación se ajusta dentro del fold de entrenamiento.')
add_full(title='SVD y PCA: por qué se probaron',tag='D · DIMENSIONALIDAD',cards=[card('Factorización','Para Z centrada: Z = UΣVᵀ.'),card('Truncamiento','Retener k componentes con suma de varianza explicada ≥ 90%.'),card('Hipótesis','Reducir ruido/colinealidad puede estabilizar un modelo lineal.'),card('Contraargumento','Una dirección de baja varianza puede predecir muy bien la etiqueta.')],message='Por eso PCA es candidato experimental, no paso obligatorio.',notes='El objetivo PCA no observa Y; los resultados de clasificación determinan si ayuda.')
add_full(title='¿Por qué regresión logística?',tag='D · LÍNEA BASE',cards=[card('Modelo','p(Y=1|x)=1/(1+exp[-(β₀+βᵀx)]).'),card('Eficiencia','Comparación rápida con un dataset grande.'),card('Interpretabilidad','Coeficientes describen cambios en log-odds, dados otros predictores.'),card('Diagnóstico','Una forma funcional simple es una referencia para medir ganancia de modelos complejos.')],message='L2 ayuda ante correlaciones, pero no “corrige” especificación no lineal.')
add_full(title='¿Se satisfacen los supuestos de logit?',tag='D · AUDITORÍA',cards=[card('Se cumple','La respuesta es binaria; hay suficientes fraudes para ajustar el modelo.'),card('En revisión','Linealidad de log-odds, separación completa multivariante y dependencia entre operaciones.'),card('Se diagnostica','Colinealidad, convergencia, especificación con splines y calibración OOF.'),card('No se requiere','Normalidad de predictores ni homocedasticidad de errores Bernoulli.')],message='La utilidad predictiva no equivale a validez causal de coeficientes.')
add_full(title='¿Qué aporta el spline logístico?',tag='D · ESPECIFICACIÓN',cards=[card('Modelo original','f(x)=β₀+Σ βⱼ xⱼ.'),card('Modelo extendido','f(x)=β₀+Σₖ γₖ Bₖ(x), con funciones base spline.'),card('Ventaja','Curvatura interpretable y continua sin cambiar la familia logística.'),card('Control','Colocar los splines dentro del Pipeline y validar con folds idénticos.')],message='Probar una no linealidad específica es más informativo que añadir complejidad indiscriminada.')
add_full(title='Random forest: bagging dentro de una familia',tag='D · MODELOS',cards=[card('Idea','Muchos árboles ajustados sobre muestras y subconjuntos aleatorios de variables.'),card('Promedio','La agregación de árboles reduce varianza frente a un árbol individual.'),card('Fortaleza','Aprende umbrales e interacciones sin ecuaciones de spline explícitas.'),card('Costo','Puede consumir memoria y no siempre calibra probabilidades óptimamente.')],message='Este sí es un mecanismo tipo bagging, a diferencia del blend posterior.')
add_full(title='XGBoost: árboles que corrigen errores',tag='D · MODELOS',cards=[card('Mecanismo','Se agregan árboles secuenciales guiados por el gradiente de la pérdida.'),card('Regularización','Profundidad, learning rate, min_child_weight y número de árboles.'),card('Hipótesis','Capturar no linealidad/interacciones omitidas por logit.'),card('Hardware','tree_method="hist"; CUDA si la prueba real detecta GPU, si no CPU.')],message='Se conserva el mismo esquema de evaluación, sin favorecer a un algoritmo por hardware.')
add_full(title='CatBoost: otra forma de boosting',tag='D · MODELOS',cards=[card('Categorías','Admite variables categóricas de forma nativa; reduce la necesidad de one-hot.'),card('Control de complejidad','depth, learning_rate, l2_leaf_reg, iterations.'),card('Comparación','Candidatos fijos y variantes ajustadas con GridSearchCV.'),card('Hardware','GPU NVIDIA cuando está disponible; fallback explícito a CPU.')],message='Diferentes sesgos inductivos merecen comparación directa, no suposiciones de superioridad.')
add_full(title='Diseño de candidatos e hiperparámetros',tag='D · COMPARACIÓN',cards=[card('Conjunto','19 especificaciones propuestas, incluyendo 2 variantes con búsqueda interna.'),card('Evaluación externa','19 × 5 = 95 evaluaciones de folds externas.'),card('Búsqueda interna','2 familias × 5 folds × 8 configuraciones × 3 folds = 240 ajustes internos.'),card('Costo total','Además del refit de las mejores configuraciones y de dos etapas en offset boosting.')],message='En modo rápido el notebook reduce tanto filas como hiperparámetros; no mezclar esos scores con el full run.')
for rec in FIGURES[11:19]:L.append(fig_full(rec[0],'D · CANDIDATOS Y DIAGNÓSTICOS'))
add_full(title='Blending y bagging: cómo evolucionó la idea inicial',tag='E · ENSEMBLES',cards=[card('Propuesta','Conservar todos los modelos en vez de quedarse solamente con el ganador.'),card('Realización','Promedio equiponderado de probabilidades OOF y de prueba.'),card('Cuatro estrategias','Mejor individual; todos; top 3; mejor de cada familia.'),card('Hallazgo metodológico','Más modelos no implica mejor AUC si sus errores son correlacionados.')],message='Término preciso de la realización: blending entre familias heterogéneas.')
add_full(title='Qué sería stacking clásico',tag='E · ENSEMBLES',cards=[card('Nivel 1','Ajustar modelos base y obtener predicciones OOF de cada uno.'),card('Nivel 2','Construir matriz Z de scores OOF y entrenar una meta-regresión logística.'),card('Sin fuga','Las predicciones para entrenar el meta-modelo no pueden ser in-sample.'),card('Estado real','El notebook no implementó ese meta-learner; sí implementó blending y offset boosting.')],message='Explicar stacking propuesto sin presentarlo como experimento ya ejecutado.')
add_full(title='Logit + booster de corrección en escala logit',tag='E · ENSEMBLES',cards=[card('Primera etapa','f_LR(x)=β₀+βᵀx; congelar los coeficientes una vez entrenados.'),card('Segunda etapa','g_XGB(x) aprende correcciones utilizando base_margin=f_LR(x).'),card('Predicción final','p(x)=σ(f_LR(x)+g_XGB(x)).'),card('Riesgo','La segunda etapa puede corregir estructura o sobreajustar ruido; comparar en OOF.')],message='Es una composición aditiva sobre el logit, NO stacking con meta-logit.')
add_full(title='Por qué conservar modelos que no ganaron',tag='E · ENSEMBLES',cards=[card('Reproducibilidad','Cada configuración tiene métricas, folds y predicciones guardadas.'),card('Diversidad','Un candidato inferior puede complementar a otro si comete errores distintos.'),card('Costo','Guardar todos permite estudiar correlación y solapamiento de casos top-risk.'),card('Selección','Elegir blends previamente definidos; no buscar combinaciones infinitas sin validación.')],message='La selección sobre OOF es exploratoria y no representa una evaluación completamente intacta.')
add_full(title='EDA extendido: qué más investigamos',tag='F · EXPLORACIÓN AMPLIADA',cards=[card('Discriminación univariante','AUC por predictor para priorizar explicaciones.'),card('Subgrupos','Interacciones entre banderas, categorías y ventanas temporales.'),card('Geometría','ECDF y dispersión de clases en parejas de variables.'),card('Distribución del test','Buscar desplazamientos sin conocer las etiquetas de la prueba.')],message='Cada gráfico sirve para generar preguntas, no para ajustar modelos sobre el test.')
for rec in FIGURES[19:25]:L.append(fig_full(rec[0],'F · EDA EXTENDIDO'))
add_full(title='De la métrica de Kaggle a una operación real',tag='G · EVALUACIÓN',cards=[card('Competencia','Optimizar ROC AUC; ranking entre pares de clases.'),card('Evento raro','Registrar average precision, precisión y recall.'),card('Probabilidades','Inspeccionar Brier, log loss y curvas de confiabilidad.'),card('Política','Medir captura y errores al revisar top 1%, 5% o 10%.')],message='No hay una única métrica que responda todos los usos.')
add_full(title='Validación de umbrales y presupuesto',tag='G · EVALUACIÓN',cards=[card('Umbral fijo','Predecir positivo si p ≥ 0.5: simple pero arbitrario con gran desbalance.'),card('Top k','Revisar el k% con mayor puntuación: umbral adaptado a capacidad.'),card('Ganancia','Comparar detecciones acumuladas con selección aleatoria.'),card('Faltan costos','Para optimizar el umbral de negocio se necesitan costos de falsos positivos/negativos.')],message='Estas políticas son evaluadas; no deben confundirse con entrenamiento distinto.')
for rec in FIGURES[25:35]:L.append(fig_full(rec[0],'G · MÉTRICAS, CALIBRACIÓN Y SUBGRUPOS'))
add_full(title='Interpretabilidad: distinguir asociación y explicación',tag='H · EXPLICABILIDAD',cards=[card('Coeficientes','Signo y magnitud dependen de la codificación y del escalamiento.'),card('Importancia interna','Gini/ganancia de árbol pueden favorecer variables con características distintas.'),card('Dependencia parcial','Efecto medio al perturbar una variable dentro de un modelo ya entrenado.'),card('Límite','Son descripciones predictivas; no identifican causalidad.')],message='Comparar modelos heterogéneos requiere cuidado con las escalas de importancia.')
add_full(title='Selección final: regla programada y evidencia pendiente',tag='H · DECISIÓN',cards=[card('Comparar','Calcular ROC AUC pooled OOF para cada candidato y cuatro blends.'),card('Elegir','El notebook selecciona la fila de mayor ROC AUC en ensemble_metrics.csv.'),card('Exportar','Genera submission.csv con id e is_fraud en el orden exacto del test.'),card('Verificar','Sin ensemble_metrics.csv ni run_manifest.json del full run no afirmar el ganador numérico exacto.')],message='La selección usada para generar Kaggle es auditable, pero la estimación seleccionada es optimista.')
for rec in FIGURES[35:]:L.append(fig_full(rec[0],'H · INTERPRETACIÓN, BLENDING Y TUNING'))
add_full(title='Qué concluye el proyecto y qué no',tag='I · CONCLUSIONES',cards=[card('Sí: comparación sistemática','Muchos métodos y transformaciones juzgados con el mismo protocolo estratificado.'),card('Sí: EDA con hipótesis','No linealidad, interacciones, anomalías y grupos merecen análisis.'),card('No: superioridad universal','Un modelo complejo o un blend no gana por definición.'),card('No: inferencia independiente','El ganador fue seleccionado con resultados OOF usados también para estimar calidad.')],message='El hallazgo más transferible es el procedimiento de evaluación reproducible.')
add_full(title='Limitaciones de los resultados disponibles',tag='I · CONCLUSIONES',cards=[card('Proveniencia de figuras','Se recibieron 44 PNG; los CSV numéricos de los folds del full run no acompañaban las imágenes.'),card('Optimismo de selección','Elegir la mejor combinación y reportar su OOF en el mismo conjunto sesga al alza.'),card('Cambio temporal','No se verificó una prueba temporal ni independencia por cuenta/tarjeta.'),card('GPU y tiempos','El hardware modifica costo; no comparar tiempos sin informar dispositivo real.')],message='Las diapositivas describen los gráficos existentes, no inventan un resultado de leaderboard.')
add_full(title='Trabajo posterior para cerrar la selección',tag='I · CONCLUSIONES',cards=[card('Reproducir','Confirmar FAST_DEV_RUN=False y guardar run_manifest.json/ensemble_metrics.csv.'),card('Validar','Usar holdout intacto o nested CV para evaluación final y diferencias pequeñas.'),card('Calibrar','Evaluar probabilidades después de elegir el ranking final.'),card('Entregar','Verificar CSV, versionar artefactos y presentar limitaciones transparentemente.')],message='Estadística rigurosa = buenos modelos + trazabilidad + afirmaciones proporcionadas.')
add_full(title='Conclusión general',lead='No gana el modelo con más componentes; gana la propuesta que resiste una evaluación transparente.',tag='FIN',kind='closing',message='EDA → hipótesis → modelos → CV → búsqueda → ensemble → decisión con incertidumbre.',notes='Invitar preguntas sobre PCA, logit, la distinción bagging/blending/stacking y las decisiones de validación.')
assert sum(s['kind']=='figure' for s in L)==44

# ------------------------------- OUTPUT EXPORT --------------------------------
COL={'bg':'#F8FAFC','ink':'#203149','muted':'#5F7185','teal':'#1B8C8B','coral':'#C36B77','blue':'#607DA5','line':'#DBE4EC','paper':'#FFFFFF','card':'#F3F7F9'}

def esc(s):return html.escape(str(s),quote=True)
def marp_slide(obj):
 k=obj['kind'];title=obj['title'];tag=obj.get('tag','');lead=obj.get('lead','');msg=obj.get('message','')
 if k in ('cover','closing'):
  body=f'<div class="marp-tag">{esc(tag)}</div>\n\n# {title}\n\n{lead}\n\n**{msg}**'
 elif k=='figure':
  name=obj['figure']; f=F[name];body=f'<div class="marp-tag">{esc(tag)}</div>\n\n## {esc(title)}\n\n<div class="fig-hero">\n  <img src="../../outputs/figures/{esc(name)}" alt="{esc(title)}" />\n</div>\n\n<div class="marp-fig-notes"><b>Qué se hizo:</b> {esc(f[2])}<br/><b>Qué aprendimos:</b> {esc(msg)}<br/><b>Límite:</b> {esc(f[4])}</div>'
 else:
  cards=''.join(f'<div class="marp-card"><b>{esc(h)}</b><p>{esc(t)}</p></div>' for h,t in obj['cards'])
  body=f'<div class="marp-tag">{esc(tag)}</div>\n\n## {esc(title)}\n\n{esc(lead)}\n\n<div class="marp-cards">{cards}</div>\n\n<div class="marp-message">{esc(msg)}</div>'
 return f'<!-- _class: {"marp-figure" if k=="figure" else "marp-content"} -->\n'+body

def generate_marp(deck,dest,deckname):
 head=f'''---
marp: true
theme: fraud-es
size: 16:9
paginate: true
transition: fade
footer: 'LDS1071 · Predicción de fraude'
title: '{deckname}'
description: 'Presentación técnica en español a partir de 44 figuras proporcionadas.'
---

'''
 md=head+('\n\n---\n\n').join(marp_slide(s) for s in deck)+'\n'
 (dest/'deck.md').write_text(md,encoding='utf8')

# Keep Marp source genuinely editable, with minimal dedicated CSS theme.
THEME='''/* @theme fraud-es */
@import 'default';
:root { --ink:#203149; --muted:#5F7185; --teal:#1B8C8B; --coral:#C36B77; }
section { background:#F8FAFC; color:var(--ink); font-family:'Aptos','Inter','Arial',sans-serif; padding:38px 58px; border-top:8px solid var(--teal); }
h1,h2 { color:var(--ink); font-weight:750; letter-spacing:-.02em; }
h1 { font-size:2.35em; } h2 { font-size:1.65em; margin:14px 0 10px; }
.marp-tag { color:var(--teal); text-transform:uppercase; font-size:.55em; font-weight:800; letter-spacing:.14em; }
.marp-cards { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-top:20px; }
.marp-card { background:white; border:1px solid #DBE4EC; border-radius:10px; padding:16px 18px; font-size:.67em; min-height:102px; }
.marp-card b { color:var(--teal); } .marp-card p { margin:8px 0 0; line-height:1.4; }
.marp-message { margin-top:16px; padding:12px 16px; font-size:.61em; border-left:4px solid var(--coral); background:#FFF8F7; }
.fig-hero { height:450px; background:white; display:flex; align-items:center; justify-content:center; border:1px solid #DBE4EC; border-radius:10px; padding:9px; }
.fig-hero img { max-width:100%; max-height:100%; object-fit:contain; }
.marp-fig-notes { font-size:.44em; line-height:1.32; margin-top:12px; color:#42566B; }
.marp-fig-notes b { color:var(--teal); }
footer { font-size:12px; color:#718498; }
'''

# Offline standalone HTML renderer: speaker notes available via N, zoom via figure click.
def generate_html(deck,dest,name):
 parts=[]; allfiles=set()
 for ix,s in enumerate(deck,1):
  kind=s['kind']; content='';tag=esc(s['tag']);title=esc(s['title']);lead=esc(s['lead']);msg=esc(s['message'])
  if kind in ('cover','closing'):
   content=f'<div class="hero"><div class="tag">{tag}</div><h1>{title}</h1><p>{lead}</p><div class="hero-strip">{msg}</div></div>'
  elif kind=='figure':
   namefig=s['figure'];allfiles.add(namefig);f=F[namefig]
   uri='data:image/png;base64,'+base64.b64encode((FIG/namefig).read_bytes()).decode('ascii')
   content=(f'<div class="top"><span class="tag">{tag}</span><span class="page">FIGURA {namefig[:2]}</span></div><h2>{title}</h2>'
    f'<div class="visual"><img src="{uri}" alt="{title}" loading="lazy"/></div>'
    f'<div class="notes-grid"><div><strong>Qué se hizo</strong><span>{esc(f[2])}</span></div>'
    f'<div><strong>Lectura</strong><span>{msg}</span></div><div><strong>Precaución</strong><span>{esc(f[4])}</span></div></div>')
  else:
   cards=''.join('<div class="infobox"><h3>'+esc(h)+'</h3><p>'+esc(t)+'</p></div>' for h,t in s['cards'])
   content=f'<div class="tag">{tag}</div><h2>{title}</h2><p class="lede">{lead}</p><div class="card-grid">{cards}</div><div class="takeaway">{msg}</div>'
  parts.append(f'<section class="slide {kind}" data-note="{esc(s["notes"])}">{content}<div class="footer">LDS1071 · Predicción de fraude <b>{ix:02d} / {len(deck):02d}</b></div></section>')
 doc='''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>'''+esc(name)+'''</title><style>
:root{--bg:#F8FAFC;--ink:#203149;--muted:#5F7185;--teal:#1B8C8B;--coral:#C36B77;--line:#DBE4EC;--card:#FFFFFF}*{box-sizing:border-box}body{margin:0;background:#0D1826;color:var(--ink);font-family:Inter,Aptos,Arial,sans-serif;overflow:hidden}.stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:12px}.deck{position:relative;aspect-ratio:16/9;width:min(98vw,calc(97vh * 16 / 9));background:var(--bg);box-shadow:0 20px 75px #0008;overflow:hidden;border-radius:6px}.slide{position:absolute;inset:0;padding:3.7% 5.0% 3.6%;background:linear-gradient(180deg,#F7FAFC,#FCFDFE);border-top:7px solid var(--teal);opacity:0;visibility:hidden;transform:translateX(12px);transition:opacity .38s ease, transform .38s ease,visibility .38s}.slide.active{opacity:1;visibility:visible;transform:none;z-index:2}.tag{font-size:clamp(10px,1.03vw,18px);color:var(--teal);font-weight:800;letter-spacing:.16em;text-transform:uppercase}.top{display:flex;justify-content:space-between}.page{color:var(--muted);font-size:clamp(10px,.85vw,16px)}h1{font-size:clamp(31px,4.1vw,73px);line-height:1.09;letter-spacing:-.047em;margin:34px 0 16px}h2{font-size:clamp(27px,2.7vw,49px);line-height:1.12;letter-spacing:-.035em;margin:15px 0 9px}.lede{font-size:clamp(14px,1.28vw,24px);color:var(--muted);margin:0 0 15px;line-height:1.42;max-width:92%}.card-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}.infobox{background:white;border:1px solid var(--line);border-radius:10px;padding:14px 20px;min-height:108px;box-shadow:0 1px 4px #2341}.infobox h3{font-size:clamp(14px,1.16vw,23px);color:var(--teal);margin:0 0 7px}.infobox p{font-size:clamp(12px,.98vw,19px);line-height:1.33;color:#384C62;margin:0}.takeaway{position:absolute;bottom:6.2%;left:5%;right:5%;background:#FFF8F6;border-left:4px solid var(--coral);padding:13px 17px;font-weight:600;color:#5F4251;font-size:clamp(11px,1.06vw,21px)}.footer{position:absolute;bottom:2.4%;left:5%;right:5%;display:flex;justify-content:space-between;color:#8393A2;font-size:clamp(10px,.75vw,15px)}.hero{height:100%;display:flex;flex-direction:column;justify-content:center}.hero p{font-size:clamp(18px,1.7vw,31px);color:#526A7F;max-width:90%;line-height:1.45}.hero-strip{margin-top:45px;border-left:5px solid var(--coral);background:white;padding:18px 23px;font-size:clamp(16px,1.35vw,25px);max-width:90%}.figure h2{font-size:clamp(25px,2.25vw,42px)}.visual{height:56%;display:flex;align-items:center;justify-content:center;background:white;border:1px solid var(--line);border-radius:9px;padding:7px;margin-top:9px}.visual img{max-height:100%;max-width:100%;width:auto;object-fit:contain;cursor:zoom-in}.notes-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:13px}.notes-grid>div{padding:10px 12px;background:#F1F6F8;border-left:3px solid var(--teal);display:flex;flex-direction:column;gap:5px;min-height:71px}.notes-grid>div:last-child{background:#FFF8F6;border-color:var(--coral)}.notes-grid strong{font-size:clamp(10px,.84vw,16px);color:#147E7D}.notes-grid span{font-size:clamp(10px,.79vw,15px);line-height:1.24;color:#30445A}.deck .slide.flow .card-grid{grid-template-columns:repeat(2,1fr)}.counter{position:fixed;right:20px;bottom:16px;color:#fff9;font-size:14px}.controls{position:fixed;bottom:16px;left:18px;display:flex;gap:8px;z-index:15}.controls button{background:#F0F5FA;color:#172B3C;border:0;border-radius:20px;padding:8px 14px;font-weight:700;cursor:pointer}.notes-pane{position:fixed;left:3vw;right:3vw;bottom:4vw;padding:15px 18px;background:#10283F;color:white;z-index:20;border:1px solid #89A9C7;border-radius:9px;font-size:18px;line-height:1.4;display:none;white-space:pre-wrap;max-height:30vh;overflow:auto}.notes-pane.visible{display:block}.modal{position:fixed;inset:0;z-index:30;background:rgba(4,11,20,.94);display:none;align-items:center;justify-content:center;padding:12px}.modal.visible{display:flex}.modal img{max-width:98vw;max-height:96vh;object-fit:contain}.hint{position:fixed;right:17px;top:12px;color:#DFE7EF;font-size:12px}@media(prefers-reduced-motion:reduce){.slide{transition:none}}
</style></head><body><div class="stage"><main class="deck">'''+''.join(parts)+'''</main></div><div class="controls"><button id="prev">◀</button><button id="next">▶</button><button id="notes">Notas (N)</button></div><div class="counter" id="counter"></div><div class="hint">← / → navegar · N notas · clic ampliar</div><aside class="notes-pane" id="notespane"></aside><div class="modal" id="modal"><img alt="Figura ampliada"/></div><script>
const slides=[...document.querySelectorAll('.slide')];let idx=0;const note=document.getElementById('notespane');function show(i){idx=(i+slides.length)%slides.length;slides.forEach((s,j)=>s.classList.toggle('active',j===idx));document.getElementById('counter').textContent=(idx+1)+' / '+slides.length;note.textContent=slides[idx].dataset.note||'Sin notas adicionales';history.replaceState(null,'','#'+(idx+1));}function move(k){show(idx+k)}document.getElementById('prev').onclick=()=>move(-1);document.getElementById('next').onclick=()=>move(1);document.getElementById('notes').onclick=()=>note.classList.toggle('visible');document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();move(1)}if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();move(-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key==='n'||e.key==='N')note.classList.toggle('visible');if(e.key==='Escape'){document.getElementById('modal').classList.remove('visible');note.classList.remove('visible')}});document.querySelectorAll('.visual img').forEach(im=>im.onclick=()=>{document.querySelector('#modal img').src=im.src;document.getElementById('modal').classList.add('visible')});document.getElementById('modal').onclick=()=>document.getElementById('modal').classList.remove('visible');const initial=parseInt(location.hash.slice(1));show(Number.isInteger(initial)?Math.max(0,Math.min(slides.length-1,initial-1)):0);
</script></body></html>'''
 (dest/'slides.html').write_text(doc,encoding='utf8')

# PDF renderer using ReportLab with registered Unicode-supporting fonts.
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(REG).exists():
 pdfmetrics.registerFont(TTFont('FraudSans',REG));pdfmetrics.registerFont(TTFont('FraudSansBold',BOLD))
else:
 REG='';print('Warning: no Unicode font located')
FN='FraudSans' if REG else 'Helvetica'
FB='FraudSansBold' if REG else 'Helvetica-Bold'
W,H=960,540
C={k:HexColor(v) for k,v in COL.items()}

def paragraph(pdf,body,x,top,maxw,maxh,size=14,bold=False,color=None,leading=None,minsize=8.5):
 if not body:return 0
 fname=FB if bold else FN;val=esc(body).replace('\n','<br/>')
 f=size
 while True:
  st=ParagraphStyle('a',fontName=fname,fontSize=f,leading=leading or 1.34*f,textColor=color or C['ink'])
  p=Paragraph(val,st);w,h=p.wrap(maxw,900)
  if h<=maxh or f<=minsize:break
  f-=.4
 p.drawOn(pdf,x,top-h)
 return h

def pdf_box(pdf,x,y,w,h,fill='paper',line=True,r=9):
 pdf.setFillColor(C[fill]);pdf.setStrokeColor(C['line'] if line else C[fill]);pdf.roundRect(x,y,w,h,r,stroke=1 if line else 0,fill=1)

def image_fit(pdf,p,x,y,w,h):
 im=Image.open(p).convert('RGB');a,b=im.size
 scale=min((w-12)/a,(h-12)/b)
 rw,rh=a*scale,b*scale
 pdf.drawImage(ImageReader(im),x+(w-rw)/2,y+(h-rh)/2,rw,rh,mask='auto')

def title_pdf(pdf,s,x,y,maxw,fontsize=28):
 text=str(s);size=fontsize
 while pdfmetrics.stringWidth(text,FB,size)>maxw and size>17:size-=.5
 pdf.setFillColor(C['ink']);pdf.setFont(FB,size);pdf.drawString(x,y,text)

def export_pdf(deck,dest,name):
 pdf=canvas.Canvas(str(dest/'slides.pdf'),pagesize=(W,H),pageCompression=1)
 pdf.setTitle(name);pdf.setAuthor('Proyecto LDS1071');pdf.setSubject('Presentación en español: análisis de fraude con tarjetas')
 for ix,s in enumerate(deck,1):
  kind=s['kind'];pdf.setFillColor(C['bg']);pdf.rect(0,0,W,H,fill=1,stroke=0)
  pdf.setFillColor(C['teal']);pdf.rect(0,533,740,7,fill=1,stroke=0)
  pdf.setFillColor(C['coral']);pdf.rect(740,533,220,7,fill=1,stroke=0)
  pdf.setFillColor(C['muted']);pdf.setFont(FN,9)
  pdf.drawString(41,13,'LDS1071  ·  PREDICCIÓN DE FRAUDE')
  pdf.drawRightString(W-42,13,f'{ix:02d} / {len(deck):02d}')
  tag=s['tag'].upper();pdf.setFillColor(C['teal']);pdf.setFont(FB,11);pdf.drawString(42,498,tag[:80])
  if kind in ('cover','closing'):
   # Cover uses wrapped title for long Spanish text.
   p=paragraph(pdf,s['title'],54,420,843,150,size=47,bold=True,minsize=30)
   paragraph(pdf,s['lead'],55,295,820,85,size=21)
   pdf_box(pdf,54,115,835,76,fill='paper')
   pdf.setFillColor(C['coral']);pdf.rect(54,115,5,76,fill=1,stroke=0)
   paragraph(pdf,s['message'],72,174,795,51,size=17,bold=True)
  elif kind=='figure':
   f=F[s['figure']]
   paragraph(pdf,s['title'],42,475,868,50,size=25,bold=True,minsize=17)
   # Original aspect kept intact; all figures use the same large image panel.
   pdf_box(pdf,42,151,876,274,fill='paper')
   image_fit(pdf,FIG/s['figure'],45,154,870,268)
   # Three small narrative panels: no text beyond minimum font.
   cards=[('QUÉ SE HIZO',f[2]),('INTERPRETACIÓN',s['message']),('LÍMITE',f[4])]
   for j,(heading,body) in enumerate(cards):
    x=42+j*293
    pdf_box(pdf,x,38,284,104,fill='paper' if j!=2 else 'card',line=True,r=6)
    pdf.setFillColor(C['teal'] if j!=2 else C['coral']);pdf.setFont(FB,9.4);pdf.drawString(x+11,126,heading)
    paragraph(pdf,body,x+11,115,262,67,size=10.5,minsize=8.5)
  else:
   paragraph(pdf,s['title'],44,470,861,61,size=29,bold=True,minsize=21)
   paragraph(pdf,s['lead'],44,417,855,53,size=15.5)
   cs=s['cards'];rows=math.ceil(len(cs)/2); cols=2
   # Two by up to four rows. For 7 steps tighten cards.
   top=358;bottom=94;gap=11
   rowheight=(top-bottom-(rows-1)*gap)/rows
   for j,(heading,body) in enumerate(cs):
    r,col=divmod(j,2);x=44+col*442;y=top-(r+1)*rowheight-r*gap
    pdf_box(pdf,x,y,429,rowheight,fill='paper')
    pdf.setFillColor(C['teal']);pdf.setFont(FB,11);pdf.drawString(x+14,y+rowheight-23,heading[:55])
    paragraph(pdf,body,x+14,y+rowheight-34,400,rowheight-42,size=12.8,minsize=9.5)
   pdf_box(pdf,45,39,870,44,fill='card',line=False,r=4)
   pdf.setFillColor(C['coral']);pdf.rect(45,39,4,44,fill=1,stroke=0)
   paragraph(pdf,s['message'],58,72,839,30,size=12.4,minsize=10)
  pdf.showPage()
 pdf.save()


def export_notes(deck,dest,deckname):
 parts=[f'# Guion de exposición · {deckname}','','**Uso:** el guion complementa las diapositivas sin saturar las imágenes. No son resultados adicionales.','']
 for i,s in enumerate(deck,1):
  parts += [f'## Diapositiva {i:02d} — {s["title"]}', '',f'**Mensaje central:** {s["message"]}', '',f'**Guion:** {s["notes"] or s["lead"]}', '']
  if s['kind']=='figure':parts += [f'**Imagen:** `outputs/figures/{s["figure"]}`', f'**Advertencia:** {F[s["figure"]][4]}','']
  if deck is S:parts += [f'**Tiempo previsto:** {s["duration"]:.2f} minutos','']
 (dest/'guion_del_presentador.md').write_text('\n'.join(parts)+'\n',encoding='utf8')

def write_doc(dest,deck,kind):
 title='Presentación breve (máximo 20 minutos)' if kind=='corta' else 'Presentación técnica completa'
 duration=sum(s['duration'] for s in deck) if kind=='corta' else None
 txt=f'''# {title}

Diapositivas: **{len(deck)}**. {'Tiempo objetivo: **'+str(round(duration,1))+' minutos** incluyendo transición entre temas.' if duration is not None else 'Todas las **44 figuras originales** aparecen una vez y en orden de análisis.'}

## Contenido
- `deck.md`: fuente editable **compatible con Marp**, en español.
- `slides.html`: archivo HTML autónomo (figuras incorporadas, transición fade, teclado, ampliación y notas con `N`).
- `slides.pdf`: versión 16:9 de {len(deck)} páginas, estática, con texto seleccionable.
- `guion_del_presentador.md`: interpretación y guion de la exposición.
- Los PNG originales se encuentran en `../../outputs/figures/` y **no fueron modificados**.

## Abrir la presentación
Abre `slides.html` en un navegador. Usa flechas para avanzar y retroceder, `N` para consultar notas y haz clic sobre una imagen para ampliarla. El PDF no puede mostrar animaciones.

## Exportación con Marp CLI (en PowerShell, desde final_project/presentation/)
```powershell
npx --yes @marp-team/marp-cli@4.5.1 .\\{dest.name}\\deck.md --theme-set .\\themes\\fraud-es.css --allow-local-files --template bespoke -o .\\{dest.name}\\slides-marp.html
npx --yes @marp-team/marp-cli@4.5.1 .\\{dest.name}\\deck.md --theme-set .\\themes\\fraud-es.css --allow-local-files --pdf -o .\\{dest.name}\\slides-marp.pdf
```

**Proveniencia de exportación:** los archivos HTML/PDF incluidos fueron construidos con el exportador offline reproducible `build_presentaciones_es.py`, no con Marp CLI. El archivo Markdown sí está preparado para Marp. La apariencia del renderizado de Marp CLI podría variar ligeramente. Para reconstruir los entregables empaquetados, ejecuta `python .\\build_presentaciones_es.py`.

## Sobre los resultados
El material usa el notebook y las figuras aportadas por el usuario. El archivo `figures.zip` contenía imágenes, **no** los CSV completos de resultados del entrenamiento definitivo. Por ello se explican tendencias y reglas de decisión sin inventar cuál estrategia exacta ganó el full run. Los resultados de smoke tests anteriores no se presentan como resultados del experimento completo. La regresión logística con correcciones de XGBoost es **offset boosting**; no se afirma que se haya ajustado un meta-modelo de stacking clásico.
'''
 (dest/'README.md').write_text(txt,encoding='utf8')

for deck,dest,nm,kind in [(S,SHORT,'Selección del modelo de fraude · presentación de 20 minutos','corta'),(L,FULL,'Predicción de fraude · presentación completa','completa')]:
 generate_marp(deck,dest,nm)
 generate_html(deck,dest,nm)
 export_pdf(deck,dest,nm)
 export_notes(deck,dest,nm)
 write_doc(dest,deck,kind)
 (dest/'slides_metadata.json').write_text(json.dumps(deck,ensure_ascii=False,indent=2),encoding='utf8')
 print(kind,'slides:',len(deck),'figures:',sum(s['kind']=='figure' for s in deck),'html MiB:',round((dest/'slides.html').stat().st_size/1024**2,1),'pdf MiB:',round((dest/'slides.pdf').stat().st_size/1024**2,1))

(ROOT/'themes'/'fraud-es.css').write_text(THEME,encoding='utf8')
print('Short timing minutes:',sum(s['duration'] for s in S))
