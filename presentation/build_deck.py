from pathlib import Path
import json, html, re, base64, textwrap, subprocess, os, sys

PRE=Path(__file__).resolve().parent
PROJECT=PRE.parent
FIG=PROJECT/'outputs'/'figures'
PRE.mkdir(exist_ok=True)
(PRE/'themes').mkdir(exist_ok=True)

chapters=[
 ('01','DATA FOUNDATIONS','Understand the class balance, feature types, distributions and measured associations.', ['Prevalence and missingness','Marginal distributions','Correlation and subgroup structure']),
 ('02','NONLINEARITY & ANOMALIES','Look beyond linear assumptions without confusing atypical behavior with fraudulent behavior.',['Binned risk curves','Temporal and feature interactions','Extreme values versus actual fraud']),
 ('03','MODEL DEVELOPMENT','Compare linear baselines, dimensionality reduction, boosted corrections and probability blends.',['Five-fold out-of-fold evaluation','PCA and assumptions','Offset boosting and ensemble diagnostics']),
 ('04','DEEPER DATA EXPLORATION','Inspect individual-feature discrimination, joint patterns, and possible train-test shift.',['ECDF and single-feature AUC','Conditional interactions','Unlabeled distribution shift']),
 ('05','PREDICTIVE PERFORMANCE','Evaluate ranking, calibration, workload, subgroup behavior, and the cost of training.',['ROC AUC and average precision','Calibration versus discrimination','Review capacity and subgroup robustness']),
 ('06','INTERPRETATION & TUNING','Explain what models learn, whether blending helps, and how to interpret grid-search results.',['Feature importance and partial dependence','Hyperparameter and fold stability','Outer-fold evidence for tuning']),
]

# Each record: image identifier, title, what it shows, how to read it, interpretive caution, chapter number.
rows=[
 ('01_target_and_missingness.png','Fraud prevalence and completeness','Quantify the rare positive class and inspect missing-value counts before modeling.','Accuracy alone is inadequate under strong imbalance; use ranking and precision-recall metrics.','Verify the competition target and input schema; missingness is data quality, not model quality.',1),
 ('02_numeric_distributions.png','Numerical feature distributions','Compare scales, tails, discreteness and potential heavy skew across numerical variables.','Long-tailed variables motivate robust plots, transformations or nonlinear modeling.','Distributional shape does not itself prove fraud discrimination.',1),
 ('03_class_conditional_densities.png','Distributions conditioned on fraud status','Compare selected numerical densities between legitimate and fraudulent transactions.','Separation indicates candidate signal, while overlap suggests the need for joint models.','Class-normalized densities conceal the underlying prevalence difference.',1),
 ('04_pearson_spearman_correlations.png','Pearson versus Spearman correlation','Compare linear correlation with rank/monotonic association among features.','Different matrices indicate relationships that may not be captured by linear correlation alone.','Correlation is not causation; feature dependence can destabilize interpretation.',1),
 ('05_categorical_risks.png','Fraud prevalence across categories','Compare base rates by categorical groups while checking category frequencies.','High-rate categories may be informative, especially when supported by many observations.','Tiny groups can show unstable rates; inspect support and confidence intervals.',1),
 ('06_flag_prevalence_vs_fraud.png','Boolean flags: frequency versus risk','Contrast how common each Boolean flag is with its conditional fraud rate.','A rare flag can be highly discriminative; prevalence and risk answer different questions.','A high marginal fraud rate need not persist after adjusting for other variables.',1),
 ('07_nonlinear_binned_fraud_rates.png','Quantile-binned fraud-rate curves','Estimate observed fraud probabilities across ordered feature bins.','Curved or nonmonotone rates motivate splines and boosted trees beyond a linear logit.','Binning and sparse tails introduce uncertainty; curves are descriptive.',2),
 ('08_time_patterns.png','Transaction timing and fraud','Compare fraud rates by hour and day, with uncertainty information where available.','Temporal changes can improve features or motivate periodic transformations.','These are aggregated clock patterns, not temporal leakage tests.',2),
 ('09_bivariate_interaction_heatmaps.png','Joint numerical risk surfaces','Study the joint variation in fraud rates for pairs of numeric predictors.','A strong high-high cell can signal interactions that additive linear models miss.','Cells with low support can exaggerate apparent contrasts.',2),
 ('10_univariate_outliers.png','Univariate outlier fences','Count extreme observations using robust, IQR-based thresholds.','Unusual values deserve inspection but are not automatically recording errors.','Unsupervised fences do not identify fraud labels or causality.',2),
 ('11_isolation_forest_anomaly_diagnostics.png','Isolation Forest anomaly scores','Compare anomaly scores with empirical fraud prevalence on the diagnostic sample.','Anomaly enrichment can reveal useful risk prioritization signals.','In-sample associations do not establish independent fraud-detection performance.',2),
 ('12_candidate_scores_and_folds.png','Candidate ROC AUC and fold variation','Rank modeling specifications by pooled out-of-fold ROC AUC and inspect fold variability.','Read pooled score together with the spread across five validation folds.','Selection and reported performance on the same OOF predictions can be optimistic.',3),
 ('13_oof_prediction_correlations.png','Correlation among model predictions','Measure redundancy among candidate probability scores.','Highly correlated models contribute less diversity to naive probability averaging.','High correlation does not imply identical ranking of the top-risk transactions.',3),
 ('14_ensemble_comparisons.png','Single models versus probability blends','Compare best single model, top-k blend, family representatives and all-candidate blend.','More members do not guarantee higher ROC AUC or average precision.','Blend membership selected on OOF results requires fresh evaluation for unbiased claims.',3),
 ('15_oof_roc_pr_curves.png','ROC and precision–recall curves','Inspect discrimination over many thresholds instead of one arbitrary cutoff.','ROC AUC measures ranking; precision–recall is highly sensitive to fraud rarity.','Threshold-free metrics do not choose a deployment threshold.',3),
 ('16_pca_explained_variance.png','How many principal components explain 90%?','Use singular values/eigenvalues to inspect retained feature variance.','High explained input variance does not necessarily preserve rare-class discrimination.','Fit PCA only inside CV training folds to avoid leakage.',3),
 ('17_assumptions_vif_and_feature_shift.png','Logistic assumptions and feature shift','Inspect multicollinearity diagnostics and exploratory feature-shift measures.','Reference-category encoding limits exact dummy redundancy; regularization improves stability.','A low VIF does not verify independence or correct logit specification.',3),
 ('18_oof_logistic_assumption_checks.png','OOF logistic diagnostics','Compare logistic residual behavior, calibration and convergence information.','A nonlinear residual pattern motivates a more flexible conditional probability model.','Descriptive out-of-fold checks do not verify all statistical assumptions.',3),
 ('19_logistic_offset_boosting_diagnostics.png','Gradient boosting as a logit correction','Compare baseline logistic results with XGBoost that adds nonlinear log-odds corrections.','The boosted stage models corrections rather than replacing the linear baseline.','Only held-out metrics can establish whether the added flexibility helps.',3),
 ('20_univariate_feature_discrimination.png','Predictive ability of individual features','Rank single predictors by univariate discrimination and direction of association.','Strong individual signals help explain candidate selection and model interpretation.','Univariate AUC ignores interactions and redundant information.',4),
 ('21_class_conditional_ecdfs.png','Empirical CDFs by outcome','Compare cumulative numerical distributions for legitimate and fraud cases.','Widening ECDF gaps highlight thresholds or ranges with class separation.','Do not interpret class-normalized curves as population fraud probabilities.',4),
 ('22_categorical_flag_interactions.png','Categorical × Boolean interactions','Compare conditional fraud rates and support across joint feature groups.','Interactions can expose differences hidden in one-feature plots.','Sparse combinations should be interpreted with support counts in view.',4),
 ('23_weekly_hourly_fraud_surface.png','Hour-of-week risk heatmaps','Visualize fraud rate and observation counts jointly across time coordinates.','Rate patterns are more credible where sample support is substantial.','No causal or temporal stability guarantee follows from one observed period.',4),
 ('24_pairwise_class_geometry.png','Fraud geometry in two dimensions','Inspect selected feature pairs for overlap, clusters and unusual regions.','Nonlinear class boundaries may explain why trees compete with additive models.','Plotting subsamples can distort apparent density and class composition.',4),
 ('25_train_test_ecdf_shift.png','Train–test distribution comparisons','Compare unlabeled feature distributions between training and test splits.','A visible shift warns that held-out CV may not exactly match test conditions.','Without test labels, score deterioration cannot be quantified directly.',4),
 ('26_four_metric_model_scorecard.png','A four-metric model scorecard','Compare ROC AUC, average precision, log loss and Brier loss.','Ranking quality and probability quality need not order models identically.','Choose a primary metric before interpreting many scores.',5),
 ('27_performance_vs_training_time.png','Predictive quality versus compute cost','Plot candidate performance against wall-clock training expense.','Small gains may not justify large computation on a teaching project.','Times depend on hardware, device, threading and cache state.',5),
 ('28_oof_score_distributions.png','Predicted-risk distributions by class','Compare predicted fraud probabilities for legitimate and fraud cases.','Overlap reveals unavoidable false positives and false negatives at any cutoff.','These are out-of-fold scores, not deployment calibration guarantees.',5),
 ('29_cumulative_gains_and_lift.png','Cumulative gains and lift','Measure how many fraud cases are captured within the highest-ranked transactions.','Lift compares model-guided review against random screening at the same budget.','Operational usefulness depends on review costs and achievable capacity.',5),
 ('30_precision_recall_at_review_budget.png','Precision and recall at limited review budget','Examine quality as the fraction of investigated transactions increases.','Fraud screening is a ranking-and-capacity problem, not only 0.5 classification.','Selecting capacity using the same OOF labels can induce optimism.',5),
 ('31_confusion_matrices_by_policy.png','Confusion matrices under two decision rules','Contrast fixed 0.5 probability threshold with an intervention budget (top 1%).','Threshold selection materially changes precision, recall and false alarms.','Never transfer a threshold across populations without validation.',5),
 ('32_model_reliability_comparison.png','Reliability diagrams across models','Compare observed fraud frequency against predicted risk by score bin.','A model may rank well but still misstate absolute risk.','Rare-event bins require caution, especially near extreme predicted risks.',5),
 ('33_calibration_with_wilson_intervals.png','Calibration uncertainty intervals','Plot uncertainty around observed bin-level fraud rates.','Wide intervals reveal where limited positive counts weaken conclusions.','Intervals summarize within-bin sampling variation, not all sources of model uncertainty.',5),
 ('34_subgroups_channel.png','Model quality across channels','Compare discrimination by transaction channel for selected candidates.','Subgroup metrics can reveal heterogeneous predictive behavior.','Subgroup sample sizes and fraud counts determine precision.',5),
 ('34_subgroups_merchant_category.png','Model quality across merchant categories','Examine predictive quality across major merchant groups.','A strong global score can conceal weaker performance in some subgroups.','Small subgroup differences may be sampling noise; avoid overinterpretation.',5),
 ('35_top_risk_set_overlap.png','Agreement among the top 1% riskiest cases','Use Jaccard overlap to compare models on transactions that actually trigger review.','Highly correlated overall predictions may still disagree at the operational margin.','The most useful diversity depends on labeling costs and error consequences.',5),
 ('36_model_feature_importance.png','Logistic coefficients and tree importances','Contrast coefficient-based linear interpretation with tree feature importance.','Importance notions are model-specific and not on a common causal scale.','Correlated features and encoding influence apparent importance.',6),
 ('37_partial_dependence_models.png','Partial dependence: learned nonlinear response','Compare average predicted response while varying selected features.','Different shapes help explain disagreements between linear, spline and tree models.','Marginal interventions can evaluate unrealistic correlated-feature combinations.',6),
 ('38_blend_vs_single_predictions.png','How blending changes individual scores','Compare selected ensemble predictions against the leading single model.','Blending can alter risk ordering even when overall metrics barely change.','A change in predicted probability is not evidence of better calibration.',6),
 ('39_submission_probability_sanity.png','Unlabeled Kaggle submission diagnostics','Inspect distribution, extremes and rank behavior of final test probabilities.','Sanity checks can catch invalid ranges or suspicious collapse of risk scores.','Unlabeled test plots cannot estimate true predictive accuracy.',6),
 ('40_hyperparameter_effects.png','Effects of model hyperparameters','Compare model families, regularization and capacity settings.','Tree depth, leaf size and learning rate trade expressivity against variance.','These are tested configurations, not a continuous optimization landscape.',6),
 ('41_fold_auc_heatmap.png','Fold-by-fold ROC AUC stability','Compare candidate scores across common validation folds.','Consistent differences are more persuasive than single pooled-rank changes.','Five folds do not fully quantify sampling uncertainty.',6),
 ('42_gridsearch_full_parameter_space.png','Inner grid search: every tested configuration','Visualize scikit-learn GridSearchCV scores across the XGBoost/CatBoost candidate grid.','Grid-search performance selects configurations inside the training data only.','Best inner-CV score is not the unbiased estimate of final test performance.',6),
 ('43_nested_gridsearch_outer_results.png','Did tuning help on held-out outer folds?','Compare fixed and tuned families on untouched outer folds, including search cost.','Use outer-fold results, not the best inner score, to judge tuning benefits.','Compute-time comparisons are device-dependent; finite-fold differences remain uncertain.',6)
]
assert len(rows)==44
assert all((FIG / r[0]).exists() for r in rows)

# Style matching clean Seaborn visuals, built for both Marp and HTML/PDF export.
css=r'''/* @theme fraud-minimal */
@import 'default';
:root { --ink:#1d3147; --muted:#66768a; --navy:#263d58; --teal:#238d93; --coral:#cf6e74; --paper:#f6f8fa; --line:#dde4ea; }
section {
  width:1280px; height:720px; padding:38px 52px 25px;
  background:#fbfcfd; color:var(--ink);
  font-family:"Aptos","Inter","Segoe UI",Arial,sans-serif;
  font-size:23px; line-height:1.3; overflow:hidden;
  position:relative; box-sizing:border-box;
}
section::before { content:""; display:block; position:absolute; top:0; left:0; right:0; height:8px;
  background:linear-gradient(90deg,var(--teal) 0%, #5a91ad 60%, var(--coral) 100%); }
section h1,section h2,section h3 { color:var(--navy); font-weight:760; letter-spacing:-.027em; }
section h1 { font-size:36px; line-height:1.1; margin:10px 0 14px; }
section p { margin:.4em 0; }
.eyebrow { color:var(--teal); font-size:13px; letter-spacing:.2em; font-weight:760; text-transform:uppercase; }
.fig-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.fig-number { color:#a1aebc; font-size:15px; font-weight:700; letter-spacing:.045em; }
.fig-title { font-size:31px; line-height:1.07; margin:5px 0 12px; }
.figure-wrap { border:1px solid var(--line); background:white; border-radius:14px; width:100%; height:455px; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.figure-wrap img { display:block; max-width:100%; max-height:444px; object-fit:contain; }
.figure-wrap.tall { width:74%; height:540px; }
.figure-wrap.tall img { max-height:526px; max-width:100%; }
.figure-body { display:flex; gap:15px; align-items:stretch; }
.fig-sidebar { width:26%; font-size:17px; display:flex; flex-direction:column; justify-content:center; gap:22px; padding:12px; }
.note-card { background:#f3f7f9; border-left:4px solid var(--teal); padding:10px 14px; border-radius:4px; }
.note-card.secondary { border-left-color:var(--coral); background:#fff7f6; }
.note-label { color:var(--teal); text-transform:uppercase; letter-spacing:.1em; font-weight:760; font-size:11px; display:block; margin-bottom:5px; }
.note-card.secondary .note-label { color:#b65d65; }
.bottom-notes { display:grid; grid-template-columns: 1.05fr 1fr; gap:16px; margin-top:10px; font-size:17px; line-height:1.18; }
.bottom-notes .note-card { min-height:57px; }
.fig-meta { font-size:12px; color:#8493a4; position:absolute; bottom:12px; left:52px; }
.slide-counter { position:absolute; bottom:12px; right:50px; font-size:12px; color:#91a2b3; letter-spacing:.08em; }
section.cover,section.chapter,section.closing { background:#f7f9fb; }
section.cover::before,section.chapter::before,section.closing::before { height:12px; }
.cover-inner { margin-top:100px; }
.cover h1 { font-size:76px; line-height:1.04; margin:18px 0 18px; max-width:1000px; }
.cover-sub { color:#586b80; font-size:27px; max-width:880px; }
.chip-row { display:flex; gap:14px; margin-top:68px; }
.chip { border:1px solid #dce5ed; background:white; border-radius:11px; padding:13px 20px; font-size:15px; color:#64798e; }
.chip strong { color:var(--navy); font-size:24px; display:block; }
.chapter-inner { margin-top:125px; }
.chapter-num { font-size:16px; color:var(--teal); letter-spacing:.25em; font-weight:800; }
.chapter h1 { font-size:67px; line-height:1.04; margin:18px 0; max-width:990px; }
.chapter-sub { max-width:900px; color:var(--muted); font-size:26px; }
.chapter-points { margin-top:32px; display:flex; gap:15px; }
.chapter-points span { background:white; padding:13px 15px; border-radius:8px; border:1px solid #dbe3ea; font-size:18px; }
section.content h1 { font-size:46px; margin:16px 0 30px; }
.content-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:24px; }
.content-box { background:#fff; border:1px solid var(--line); border-radius:14px; padding:28px; min-height:125px; }
.content-box b { display:block; color:var(--teal); margin-bottom:10px; }
.content-box p { color:#586b80; font-size:20px; }
.strip { font-size:23px; color:#496277; border-left:5px solid var(--coral); padding-left:20px; margin-top:30px; }
section.content .small { font-size:17px; color:var(--muted); }

/* Browser-specific navigation is added in the HTML wrapper, never printed. */
body.deck-viewer { margin:0; background:#e9eef2; overflow:hidden; font-family:Arial,sans-serif; }
.deck-stage { height:100vh; width:100vw; display:flex; align-items:center; justify-content:center; }
.deck-shell { transform-origin:center center; width:1280px; height:720px; flex:0 0 auto; }
.deck-shell > section { display:none; box-shadow:0 12px 54px rgba(17,39,61,.14); }
.deck-shell > section.active { display:block; }
.deck-nav { position:fixed; z-index:100; bottom:18px; left:50%; transform:translateX(-50%); border-radius:50px; background:rgba(27,48,70,.84); color:white; font-size:14px; padding:6px 16px; display:flex; align-items:center; gap:16px; backdrop-filter:blur(6px); }
.deck-nav button { font-family:inherit; cursor:pointer; border:0; color:white; font-size:20px; background:none; padding:2px 6px; }
.deck-nav button:hover { color:#9adddc; }
#slideStatus { min-width:75px; text-align:center; letter-spacing:.03em; }
.zoom-indicator {display:none; position:fixed; right:23px; bottom:23px; color:#4d6174; font-size:13px; opacity:.55;}
section.figure-slide .figure-wrap img {cursor:zoom-in;}
#zoomLayer { display:none; position:fixed; z-index:999; inset:0; background:rgba(10,19,28,.94); align-items:center; justify-content:center; padding:22px; box-sizing:border-box; }
#zoomLayer.open { display:flex; }
#zoomLayer img { max-width:96vw; max-height:94vh; object-fit:contain; }
#zoomLayer button { position:fixed; right:25px; top:16px; border:0; background:transparent; color:white; cursor:pointer; font-size:30px; }
@media (prefers-reduced-motion:no-preference) {
::view-transition-old(root) {animation: 220ms ease both fadeSlideOld;}
::view-transition-new(root) {animation: 270ms ease both fadeSlideNew;}
@keyframes fadeSlideOld {to{opacity:0; transform:translateX(-16px)}}
@keyframes fadeSlideNew {from{opacity:0;transform:translateX(16px)} to{opacity:1;transform:translateX(0)}}
}
@page { size: 13.333333in 7.5in; margin:0; }
@media print {
 html,body { width:1280px; height:auto !important; margin:0 !important; overflow:visible !important; background:white !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
 .deck-stage,.deck-shell { width:1280px !important; height:auto !important; transform:none !important; display:block !important; margin:0 !important; padding:0 !important; }
 .deck-shell > section, .deck-shell > section.active {display:block !important; width:1280px; height:720px; margin:0; box-shadow:none; break-after:page; page-break-after:always; print-color-adjust:exact; -webkit-print-color-adjust:exact;}
 .deck-nav,.zoom-indicator,#zoomLayer {display:none !important;}
}
'''
(PRE/'themes'/'fraud-minimal.css').write_text(css,encoding='utf-8')

esc=html.escape
slides=[]
fig_manifest=[]
def add(body,cls,kind,figure=None,title=None):
 slides.append(dict(body=body,cls=cls,kind=kind,figure=figure,title=title))

add('''<div class="cover-inner"><div class="eyebrow">LDS1071 · MACHINE LEARNING · FINAL PROJECT</div>
<h1>Predicting<br>Credit Card Fraud</h1>
<div class="cover-sub">A visual investigation of rare-event classification, model selection, calibration and cross-validated risk ranking.</div>
<div class="chip-row"><div class="chip"><strong>699,960</strong>labeled transactions</div><div class="chip"><strong>1.67%</strong>fraud prevalence</div><div class="chip"><strong>44</strong>supplied analytical figures</div><div class="chip"><strong>ROC AUC</strong>competition objective</div></div>
</div>''','cover','cover',title='Credit Card Fraud — visual report')

add('''<div class="eyebrow">RESEARCH QUESTION</div><h1>What must a useful fraud model do?</h1>
<div class="content-grid">
<div class="content-box"><b>01 · Rank</b><p>Assign higher scores to fraudulent transactions than to legitimate ones.</p></div>
<div class="content-box"><b>02 · Detect</b><p>Capture rare fraud cases within a constrained review budget.</p></div>
<div class="content-box"><b>03 · Quantify</b><p>Produce interpretable risk estimates, not only class predictions.</p></div>
<div class="content-box"><b>04 · Generalize</b><p>Retain performance across folds, customer contexts and transaction subgroups.</p></div>
</div><div class="strip">Kaggle scores probabilistic predictions using ROC AUC. Operational review needs more than that single metric.</div>''','content','intro',title='Study objectives')

add('''<div class="eyebrow">ANALYSIS MAP</div><h1>From descriptive patterns to evidence</h1>
<div class="content-grid">
<div class="content-box"><b>Part I · Data</b><p>Prevalence, distributions, correlations and category effects.</p></div>
<div class="content-box"><b>Part II · Nonlinearity</b><p>Curvature, temporal behavior and extreme observations.</p></div>
<div class="content-box"><b>Part III · Models</b><p>Logistic regression, PCA, random forests, XGBoost, CatBoost and ensembles.</p></div>
<div class="content-box"><b>Part IV · Decisions</b><p>Calibration, review budgets, subgroup checks and hyperparameter searches.</p></div>
</div><p class="small">Every figure in the supplied outputs/figures archive is presented on its own slide, in numbered order.</p>''','content','intro',title='Presentation roadmap')

add('''<div class="eyebrow">DESIGN & VALIDATION</div><h1>A five-fold experimental protocol</h1>
<div class="content-grid">
<div class="content-box"><b>Outer folds</b><p>Stratified 5-fold out-of-fold predictions supply a common comparison set.</p></div>
<div class="content-box"><b>Within-fold preprocessing</b><p>Encoding, scaling, imputation and PCA must be fitted only to training partitions.</p></div>
<div class="content-box"><b>Nested tuning</b><p>GridSearchCV selects boosting parameters within outer training data, then evaluates on untouched outer folds.</p></div>
<div class="content-box"><b>Primary and supporting scores</b><p>ROC AUC; average precision, log loss, Brier score, calibration and review-budget metrics.</p></div>
</div><div class="strip">The supplied figure images are the evidence for this presentation; raw fold data were not included in the uploaded figures archive.</div>''','content','intro',title='Validation design')

for ci,(chapter_number,chapter_title,chapter_sub,points) in enumerate(chapters,1):
 add(f'<div class="chapter-inner"><div class="chapter-num">SECTION {chapter_number} / 06</div><h1>{esc(chapter_title)}</h1><div class="chapter-sub">{esc(chapter_sub)}</div><div class="chapter-points">'+''.join(f'<span>{esc(p)}</span>' for p in points)+'</div></div>','chapter','section',title=chapter_title)
 for fname,title,description,insight,caveat,group in rows:
  if group != ci: continue
  stem=fname[:2]
  p=FIG/fname
  from PIL import Image
  w,h=Image.open(p).size
  tall=w/h <1.30
  image_html=f'<img src="../outputs/figures/{esc(fname)}" alt="{esc(title)}" data-figure="{esc(fname)}" />'
  if tall:
   core=f'''<div class="figure-body"><div class="figure-wrap tall">{image_html}</div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>{esc(description)}</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>{esc(insight)} {esc(caveat)}</div></div></div>'''
  else:
   core=f'''<div class="figure-wrap">{image_html}</div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>{esc(description)}</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>{esc(insight)} {esc(caveat)}</div></div>'''
  body=f'''<div class="fig-head"><span class="eyebrow">{chapter_number} · {esc(chapter_title)}</span><span class="fig-number">FIGURE {len(fig_manifest)+1:02d} / 44 · SOURCE {stem}</span></div>
<h1 class="fig-title">{esc(title)}</h1>{core}<div class="fig-meta">Source: supplied outputs/figures/{esc(fname)}</div>'''
  add(body,'figure-slide','figure',figure=fname,title=title)
  fig_manifest.append({'file':fname,'title':title,'slide_number':len(slides),'chapter':chapter_title,'read':description,'interpret':insight,'limitation':caveat,'pixels':[w,h]})

add('''<div class="eyebrow">SYNTHESIS</div><h1>What the 44 figures establish</h1>
<div class="content-grid">
<div class="content-box"><b>Fraud is rare and structured</b><p>Risk varies across feature values, time periods and feature combinations.</p></div>
<div class="content-box"><b>Linear is a useful benchmark</b><p>Logistic regression offers an interpretable log-odds starting point; splines and trees relax additivity.</p></div>
<div class="content-box"><b>Evaluation is multidimensional</b><p>ROC AUC, precision-recall, calibration and operational review budgets answer different questions.</p></div>
<div class="content-box"><b>Tuning needs honest validation</b><p>The performance of a tuned model must be judged on outer held-out folds, not its best inner score.</p></div>
</div>''','content','conclusion',title='Synthesis')
add('''<div class="eyebrow">THESIS · ANTITHESIS · SYNTHESIS</div><h1>Why not just pick the largest ROC AUC?</h1>
<div class="content-grid">
<div class="content-box"><b>Thesis</b><p>A high ROC AUC means useful ranking for Kaggle's objective.</p></div>
<div class="content-box"><b>Antithesis</b><p>The same model can be miscalibrated, expensive to train, unstable across folds, or unhelpful at an actual review budget.</p></div>
<div class="content-box"><b>Synthesis</b><p>Use ROC AUC to rank candidates, then stress-test calibration, rare-event precision, stability, subgroup behavior and cost.</p></div>
<div class="content-box"><b>Selection rule</b><p>Prefer a simpler model if added complexity or tuning brings no convincing held-out improvement.</p></div>
</div>''','content','conclusion',title='Model selection decision')
add('''<div class="eyebrow">VALIDITY & UNCERTAINTY</div><h1>Limits of what these plots can prove</h1>
<div class="content-grid">
<div class="content-box"><b>Observational, often synthetic</b><p>Descriptive differences do not identify causal drivers of fraud.</p></div>
<div class="content-box"><b>Selection optimism</b><p>Using the same out-of-fold labels to choose a winning candidate or blend can inflate reported success.</p></div>
<div class="content-box"><b>Unknown provenance of image-only results</b><p>Numerical claims require the saved fold CSVs, configurations, hardware logs and sample counts.</p></div>
<div class="content-box"><b>External validity</b><p>Unlabeled Kaggle test results and possible train–test shift limit generalization claims.</p></div>
</div>''','content','conclusion',title='Limitations')
add('''<div class="eyebrow">REPRODUCIBILITY & NEXT STEPS</div><h1>From a visual report to a defensible submission</h1>
<div class="content-grid">
<div class="content-box"><b>Reproduce</b><p>Run final_project/credit_card_fraud.ipynb with the project Conda environment; record versions, seed and device.</p></div>
<div class="content-box"><b>Archive</b><p>Keep OOF predictions, fold metrics, complete hyperparameter searches, figure catalog and model configurations.</p></div>
<div class="content-box"><b>Validate again</b><p>Use a fresh holdout or nested evaluation if choosing the final blend based on many OOF candidates.</p></div>
<div class="content-box"><b>Submit</b><p>Verify probability bounds and id order; submit the selected id,is_fraud CSV and record public leaderboard feedback separately.</p></div>
</div><div class="strip">The PDF is static. The HTML provides keyboard navigation, fade transitions and click-to-zoom figures.</div>''','content','conclusion',title='Next steps')
add('''<div class="chapter-inner"><div class="eyebrow">LDS1071 · FINAL PROJECT</div><h1>Thank you.</h1><div class="chapter-sub">Research artifacts: notebook, 44 supplied figures, figure manifest, Marp Markdown, HTML and PDF.</div><div class="chip-row"><div class="chip"><strong>44 / 44</strong>figures included</div><div class="chip"><strong>5-fold</strong>stratified CV framework</div><div class="chip"><strong>ROC AUC</strong>primary Kaggle metric</div></div></div>''','closing','closing',title='End')

manifest={'title':'Credit Card Fraud — LDS1071','date':'2026-11-22','source_figures_archive':'figures.zip','source_project_archive':'LDS1071_credit_fraud_conda_gpu_gridsearch_v5.zip','n_figures':len(rows),'n_slides':len(slides),'figures':fig_manifest,'sections':[{'number':i+1,'name':r[1]} for i,r in enumerate(chapters)],'notes':'Image-only source. Treat generated charts as supplied; do not infer numerical results or execution provenance not encoded in images.'}
(PRE/'figure_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(PRE/'slides_metadata.json').write_text(json.dumps(slides,indent=2,ensure_ascii=False),encoding='utf-8')

# Marp-compatible source (no figure data embedded; linked to included ../outputs/figures).
front='''---
marp: true
theme: fraud-minimal
size: 16:9
html: true
paginate: true
transition: fade
title: "Predicting Credit Card Fraud — Visual Report"
description: "LDS1071 final project: 44 figures with explanatory narrative and cross-validation diagnostics"
---
'''
md=[front]
for j,s in enumerate(slides):
 md.append(f'<!-- _class: {s["cls"]} -->\n'+s['body']+'\n')
 if j<len(slides)-1:md.append('---\n')
(PRE/'deck.md').write_text('\n'.join(md),encoding='utf-8')

# Self-contained HTML export, with all images embedded and slide transitions.
# Does not require Marp at viewing time. Marp source is separately editable and can be re-exported via Marp CLI.
embedded={}
for r in rows:
 f=r[0]
 embedded[f]='data:image/png;base64,'+base64.b64encode((FIG/f).read_bytes()).decode('ascii')

html_slides=[]
for i,s in enumerate(slides,1):
 body=s['body']
 for key,uri in embedded.items():
  body=body.replace('../outputs/figures/'+key,uri)
 html_slides.append(f'<section class="{s["cls"]}{" active" if i==1 else ""}" data-index="{i}" data-title="{esc(s["title"] or "")}">{body}<div class="slide-counter">LDS1071 · {i:02d}/{len(slides):02d}</div></section>')
js=r'''
const slides=[...document.querySelectorAll('.deck-shell > section')];
let index=0;
function resize(){ const scale=Math.min(innerWidth/1280,innerHeight/720)*0.985;document.querySelector('.deck-shell').style.transform=`scale(${scale})`; }
function show(next, animate=true){
 next=Math.max(0,Math.min(slides.length-1,next)); if(next===index)return;
 const update=()=>{slides[index].classList.remove('active');slides[next].classList.add('active');index=next;document.getElementById('slideStatus').textContent=`${index+1} / ${slides.length}`;history.replaceState(null,'',`#slide-${index+1}`);};
 if(animate && document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches){document.startViewTransition(update);}else update();
}
addEventListener('resize',resize);resize();
const start=Number((location.hash.match(/^#slide-(\d+)$/)||[])[1]||1); if(start>1)show(start-1,false);
document.getElementById('slideStatus').textContent=`${index+1} / ${slides.length}`;
document.getElementById('previous').onclick=()=>show(index-1);
document.getElementById('next').onclick=()=>show(index+1);
const zoomLayer=document.getElementById('zoomLayer');const zoomImg=document.getElementById('zoomImg');
document.querySelectorAll('.figure-wrap img').forEach(el=>el.addEventListener('click',()=>{zoomImg.src=el.src;zoomImg.alt=el.alt;zoomLayer.classList.add('open');}));
const closeZoom=()=>zoomLayer.classList.remove('open');
document.getElementById('closeZoom').onclick=closeZoom;zoomLayer.onclick=e=>{if(e.target===zoomLayer)closeZoom();};
addEventListener('keydown',e=>{
 if(zoomLayer.classList.contains('open')){if(e.key==='Escape')closeZoom();return;}
 if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();show(index+1);}
 if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();show(index-1);}
 if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);
});
'''
html_doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Predicting Credit Card Fraud | LDS1071</title><meta name="description" content="Visual presentation of 44 credit-fraud modeling figures" />
<style>'''+css+'''</style></head><body class="deck-viewer"><div class="deck-stage"><main class="deck-shell">'''+''.join(html_slides)+'''</main></div>
<nav class="deck-nav" aria-label="Slides"><button id="previous" aria-label="Previous slide">&#8249;</button><span id="slideStatus"></span><button id="next" aria-label="Next slide">&#8250;</button></nav>
<div class="zoom-indicator">Click figure to zoom · ← / → to navigate</div><div id="zoomLayer"><button id="closeZoom" aria-label="Close image">&#10005;</button><img id="zoomImg" alt="Zoomed figure" /></div><script>'''+js+'''</script></body></html>'''
(PRE/'slides.html').write_text(html_doc,encoding='utf-8')
print('slides',len(slides),'figures',len(fig_manifest),'html_MB',round(len(html_doc)/1e6,2),'marp_kB',round(len(''.join(md))/1e3,1))
