---
marp: true
theme: fraud-minimal
size: 16:9
html: true
paginate: true
transition: fade
title: "Predicting Credit Card Fraud — Visual Report"
description: "LDS1071 final project: 44 figures with explanatory narrative and cross-validation diagnostics"
---

<!-- _class: cover -->
<div class="cover-inner"><div class="eyebrow">LDS1071 · MACHINE LEARNING · FINAL PROJECT</div>
<h1>Predicting<br>Credit Card Fraud</h1>
<div class="cover-sub">A visual investigation of rare-event classification, model selection, calibration and cross-validated risk ranking.</div>
<div class="chip-row"><div class="chip"><strong>699,960</strong>labeled transactions</div><div class="chip"><strong>1.67%</strong>fraud prevalence</div><div class="chip"><strong>44</strong>supplied analytical figures</div><div class="chip"><strong>ROC AUC</strong>competition objective</div></div>
</div>

---

<!-- _class: content -->
<div class="eyebrow">RESEARCH QUESTION</div><h1>What must a useful fraud model do?</h1>
<div class="content-grid">
<div class="content-box"><b>01 · Rank</b><p>Assign higher scores to fraudulent transactions than to legitimate ones.</p></div>
<div class="content-box"><b>02 · Detect</b><p>Capture rare fraud cases within a constrained review budget.</p></div>
<div class="content-box"><b>03 · Quantify</b><p>Produce interpretable risk estimates, not only class predictions.</p></div>
<div class="content-box"><b>04 · Generalize</b><p>Retain performance across folds, customer contexts and transaction subgroups.</p></div>
</div><div class="strip">Kaggle scores probabilistic predictions using ROC AUC. Operational review needs more than that single metric.</div>

---

<!-- _class: content -->
<div class="eyebrow">ANALYSIS MAP</div><h1>From descriptive patterns to evidence</h1>
<div class="content-grid">
<div class="content-box"><b>Part I · Data</b><p>Prevalence, distributions, correlations and category effects.</p></div>
<div class="content-box"><b>Part II · Nonlinearity</b><p>Curvature, temporal behavior and extreme observations.</p></div>
<div class="content-box"><b>Part III · Models</b><p>Logistic regression, PCA, random forests, XGBoost, CatBoost and ensembles.</p></div>
<div class="content-box"><b>Part IV · Decisions</b><p>Calibration, review budgets, subgroup checks and hyperparameter searches.</p></div>
</div><p class="small">Every figure in the supplied outputs/figures archive is presented on its own slide, in numbered order.</p>

---

<!-- _class: content -->
<div class="eyebrow">DESIGN & VALIDATION</div><h1>A five-fold experimental protocol</h1>
<div class="content-grid">
<div class="content-box"><b>Outer folds</b><p>Stratified 5-fold out-of-fold predictions supply a common comparison set.</p></div>
<div class="content-box"><b>Within-fold preprocessing</b><p>Encoding, scaling, imputation and PCA must be fitted only to training partitions.</p></div>
<div class="content-box"><b>Nested tuning</b><p>GridSearchCV selects boosting parameters within outer training data, then evaluates on untouched outer folds.</p></div>
<div class="content-box"><b>Primary and supporting scores</b><p>ROC AUC; average precision, log loss, Brier score, calibration and review-budget metrics.</p></div>
</div><div class="strip">The supplied figure images are the evidence for this presentation; raw fold data were not included in the uploaded figures archive.</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 01 / 06</div><h1>DATA FOUNDATIONS</h1><div class="chapter-sub">Understand the class balance, feature types, distributions and measured associations.</div><div class="chapter-points"><span>Prevalence and missingness</span><span>Marginal distributions</span><span>Correlation and subgroup structure</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 01 / 44 · SOURCE 01</span></div>
<h1 class="fig-title">Fraud prevalence and completeness</h1><div class="figure-wrap"><img src="../outputs/figures/01_target_and_missingness.png" alt="Fraud prevalence and completeness" data-figure="01_target_and_missingness.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Quantify the rare positive class and inspect missing-value counts before modeling.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Accuracy alone is inadequate under strong imbalance; use ranking and precision-recall metrics. Verify the competition target and input schema; missingness is data quality, not model quality.</div></div><div class="fig-meta">Source: supplied outputs/figures/01_target_and_missingness.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 02 / 44 · SOURCE 02</span></div>
<h1 class="fig-title">Numerical feature distributions</h1><div class="figure-wrap"><img src="../outputs/figures/02_numeric_distributions.png" alt="Numerical feature distributions" data-figure="02_numeric_distributions.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare scales, tails, discreteness and potential heavy skew across numerical variables.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Long-tailed variables motivate robust plots, transformations or nonlinear modeling. Distributional shape does not itself prove fraud discrimination.</div></div><div class="fig-meta">Source: supplied outputs/figures/02_numeric_distributions.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 03 / 44 · SOURCE 03</span></div>
<h1 class="fig-title">Distributions conditioned on fraud status</h1><div class="figure-wrap"><img src="../outputs/figures/03_class_conditional_densities.png" alt="Distributions conditioned on fraud status" data-figure="03_class_conditional_densities.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare selected numerical densities between legitimate and fraudulent transactions.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Separation indicates candidate signal, while overlap suggests the need for joint models. Class-normalized densities conceal the underlying prevalence difference.</div></div><div class="fig-meta">Source: supplied outputs/figures/03_class_conditional_densities.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 04 / 44 · SOURCE 04</span></div>
<h1 class="fig-title">Pearson versus Spearman correlation</h1><div class="figure-wrap"><img src="../outputs/figures/04_pearson_spearman_correlations.png" alt="Pearson versus Spearman correlation" data-figure="04_pearson_spearman_correlations.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare linear correlation with rank/monotonic association among features.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Different matrices indicate relationships that may not be captured by linear correlation alone. Correlation is not causation; feature dependence can destabilize interpretation.</div></div><div class="fig-meta">Source: supplied outputs/figures/04_pearson_spearman_correlations.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 05 / 44 · SOURCE 05</span></div>
<h1 class="fig-title">Fraud prevalence across categories</h1><div class="figure-wrap"><img src="../outputs/figures/05_categorical_risks.png" alt="Fraud prevalence across categories" data-figure="05_categorical_risks.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare base rates by categorical groups while checking category frequencies.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>High-rate categories may be informative, especially when supported by many observations. Tiny groups can show unstable rates; inspect support and confidence intervals.</div></div><div class="fig-meta">Source: supplied outputs/figures/05_categorical_risks.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">01 · DATA FOUNDATIONS</span><span class="fig-number">FIGURE 06 / 44 · SOURCE 06</span></div>
<h1 class="fig-title">Boolean flags: frequency versus risk</h1><div class="figure-wrap"><img src="../outputs/figures/06_flag_prevalence_vs_fraud.png" alt="Boolean flags: frequency versus risk" data-figure="06_flag_prevalence_vs_fraud.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Contrast how common each Boolean flag is with its conditional fraud rate.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>A rare flag can be highly discriminative; prevalence and risk answer different questions. A high marginal fraud rate need not persist after adjusting for other variables.</div></div><div class="fig-meta">Source: supplied outputs/figures/06_flag_prevalence_vs_fraud.png</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 02 / 06</div><h1>NONLINEARITY &amp; ANOMALIES</h1><div class="chapter-sub">Look beyond linear assumptions without confusing atypical behavior with fraudulent behavior.</div><div class="chapter-points"><span>Binned risk curves</span><span>Temporal and feature interactions</span><span>Extreme values versus actual fraud</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">02 · NONLINEARITY &amp; ANOMALIES</span><span class="fig-number">FIGURE 07 / 44 · SOURCE 07</span></div>
<h1 class="fig-title">Quantile-binned fraud-rate curves</h1><div class="figure-wrap"><img src="../outputs/figures/07_nonlinear_binned_fraud_rates.png" alt="Quantile-binned fraud-rate curves" data-figure="07_nonlinear_binned_fraud_rates.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Estimate observed fraud probabilities across ordered feature bins.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Curved or nonmonotone rates motivate splines and boosted trees beyond a linear logit. Binning and sparse tails introduce uncertainty; curves are descriptive.</div></div><div class="fig-meta">Source: supplied outputs/figures/07_nonlinear_binned_fraud_rates.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">02 · NONLINEARITY &amp; ANOMALIES</span><span class="fig-number">FIGURE 08 / 44 · SOURCE 08</span></div>
<h1 class="fig-title">Transaction timing and fraud</h1><div class="figure-wrap"><img src="../outputs/figures/08_time_patterns.png" alt="Transaction timing and fraud" data-figure="08_time_patterns.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare fraud rates by hour and day, with uncertainty information where available.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Temporal changes can improve features or motivate periodic transformations. These are aggregated clock patterns, not temporal leakage tests.</div></div><div class="fig-meta">Source: supplied outputs/figures/08_time_patterns.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">02 · NONLINEARITY &amp; ANOMALIES</span><span class="fig-number">FIGURE 09 / 44 · SOURCE 09</span></div>
<h1 class="fig-title">Joint numerical risk surfaces</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/09_bivariate_interaction_heatmaps.png" alt="Joint numerical risk surfaces" data-figure="09_bivariate_interaction_heatmaps.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Study the joint variation in fraud rates for pairs of numeric predictors.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>A strong high-high cell can signal interactions that additive linear models miss. Cells with low support can exaggerate apparent contrasts.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/09_bivariate_interaction_heatmaps.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">02 · NONLINEARITY &amp; ANOMALIES</span><span class="fig-number">FIGURE 10 / 44 · SOURCE 10</span></div>
<h1 class="fig-title">Univariate outlier fences</h1><div class="figure-wrap"><img src="../outputs/figures/10_univariate_outliers.png" alt="Univariate outlier fences" data-figure="10_univariate_outliers.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Count extreme observations using robust, IQR-based thresholds.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Unusual values deserve inspection but are not automatically recording errors. Unsupervised fences do not identify fraud labels or causality.</div></div><div class="fig-meta">Source: supplied outputs/figures/10_univariate_outliers.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">02 · NONLINEARITY &amp; ANOMALIES</span><span class="fig-number">FIGURE 11 / 44 · SOURCE 11</span></div>
<h1 class="fig-title">Isolation Forest anomaly scores</h1><div class="figure-wrap"><img src="../outputs/figures/11_isolation_forest_anomaly_diagnostics.png" alt="Isolation Forest anomaly scores" data-figure="11_isolation_forest_anomaly_diagnostics.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare anomaly scores with empirical fraud prevalence on the diagnostic sample.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Anomaly enrichment can reveal useful risk prioritization signals. In-sample associations do not establish independent fraud-detection performance.</div></div><div class="fig-meta">Source: supplied outputs/figures/11_isolation_forest_anomaly_diagnostics.png</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 03 / 06</div><h1>MODEL DEVELOPMENT</h1><div class="chapter-sub">Compare linear baselines, dimensionality reduction, boosted corrections and probability blends.</div><div class="chapter-points"><span>Five-fold out-of-fold evaluation</span><span>PCA and assumptions</span><span>Offset boosting and ensemble diagnostics</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 12 / 44 · SOURCE 12</span></div>
<h1 class="fig-title">Candidate ROC AUC and fold variation</h1><div class="figure-wrap"><img src="../outputs/figures/12_candidate_scores_and_folds.png" alt="Candidate ROC AUC and fold variation" data-figure="12_candidate_scores_and_folds.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Rank modeling specifications by pooled out-of-fold ROC AUC and inspect fold variability.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Read pooled score together with the spread across five validation folds. Selection and reported performance on the same OOF predictions can be optimistic.</div></div><div class="fig-meta">Source: supplied outputs/figures/12_candidate_scores_and_folds.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 13 / 44 · SOURCE 13</span></div>
<h1 class="fig-title">Correlation among model predictions</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/13_oof_prediction_correlations.png" alt="Correlation among model predictions" data-figure="13_oof_prediction_correlations.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Measure redundancy among candidate probability scores.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Highly correlated models contribute less diversity to naive probability averaging. High correlation does not imply identical ranking of the top-risk transactions.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/13_oof_prediction_correlations.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 14 / 44 · SOURCE 14</span></div>
<h1 class="fig-title">Single models versus probability blends</h1><div class="figure-wrap"><img src="../outputs/figures/14_ensemble_comparisons.png" alt="Single models versus probability blends" data-figure="14_ensemble_comparisons.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare best single model, top-k blend, family representatives and all-candidate blend.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>More members do not guarantee higher ROC AUC or average precision. Blend membership selected on OOF results requires fresh evaluation for unbiased claims.</div></div><div class="fig-meta">Source: supplied outputs/figures/14_ensemble_comparisons.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 15 / 44 · SOURCE 15</span></div>
<h1 class="fig-title">ROC and precision–recall curves</h1><div class="figure-wrap"><img src="../outputs/figures/15_oof_roc_pr_curves.png" alt="ROC and precision–recall curves" data-figure="15_oof_roc_pr_curves.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Inspect discrimination over many thresholds instead of one arbitrary cutoff.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>ROC AUC measures ranking; precision–recall is highly sensitive to fraud rarity. Threshold-free metrics do not choose a deployment threshold.</div></div><div class="fig-meta">Source: supplied outputs/figures/15_oof_roc_pr_curves.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 16 / 44 · SOURCE 16</span></div>
<h1 class="fig-title">How many principal components explain 90%?</h1><div class="figure-wrap"><img src="../outputs/figures/16_pca_explained_variance.png" alt="How many principal components explain 90%?" data-figure="16_pca_explained_variance.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Use singular values/eigenvalues to inspect retained feature variance.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>High explained input variance does not necessarily preserve rare-class discrimination. Fit PCA only inside CV training folds to avoid leakage.</div></div><div class="fig-meta">Source: supplied outputs/figures/16_pca_explained_variance.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 17 / 44 · SOURCE 17</span></div>
<h1 class="fig-title">Logistic assumptions and feature shift</h1><div class="figure-wrap"><img src="../outputs/figures/17_assumptions_vif_and_feature_shift.png" alt="Logistic assumptions and feature shift" data-figure="17_assumptions_vif_and_feature_shift.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Inspect multicollinearity diagnostics and exploratory feature-shift measures.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Reference-category encoding limits exact dummy redundancy; regularization improves stability. A low VIF does not verify independence or correct logit specification.</div></div><div class="fig-meta">Source: supplied outputs/figures/17_assumptions_vif_and_feature_shift.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 18 / 44 · SOURCE 18</span></div>
<h1 class="fig-title">OOF logistic diagnostics</h1><div class="figure-wrap"><img src="../outputs/figures/18_oof_logistic_assumption_checks.png" alt="OOF logistic diagnostics" data-figure="18_oof_logistic_assumption_checks.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare logistic residual behavior, calibration and convergence information.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>A nonlinear residual pattern motivates a more flexible conditional probability model. Descriptive out-of-fold checks do not verify all statistical assumptions.</div></div><div class="fig-meta">Source: supplied outputs/figures/18_oof_logistic_assumption_checks.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">03 · MODEL DEVELOPMENT</span><span class="fig-number">FIGURE 19 / 44 · SOURCE 19</span></div>
<h1 class="fig-title">Gradient boosting as a logit correction</h1><div class="figure-wrap"><img src="../outputs/figures/19_logistic_offset_boosting_diagnostics.png" alt="Gradient boosting as a logit correction" data-figure="19_logistic_offset_boosting_diagnostics.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare baseline logistic results with XGBoost that adds nonlinear log-odds corrections.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>The boosted stage models corrections rather than replacing the linear baseline. Only held-out metrics can establish whether the added flexibility helps.</div></div><div class="fig-meta">Source: supplied outputs/figures/19_logistic_offset_boosting_diagnostics.png</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 04 / 06</div><h1>DEEPER DATA EXPLORATION</h1><div class="chapter-sub">Inspect individual-feature discrimination, joint patterns, and possible train-test shift.</div><div class="chapter-points"><span>ECDF and single-feature AUC</span><span>Conditional interactions</span><span>Unlabeled distribution shift</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 20 / 44 · SOURCE 20</span></div>
<h1 class="fig-title">Predictive ability of individual features</h1><div class="figure-wrap"><img src="../outputs/figures/20_univariate_feature_discrimination.png" alt="Predictive ability of individual features" data-figure="20_univariate_feature_discrimination.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Rank single predictors by univariate discrimination and direction of association.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Strong individual signals help explain candidate selection and model interpretation. Univariate AUC ignores interactions and redundant information.</div></div><div class="fig-meta">Source: supplied outputs/figures/20_univariate_feature_discrimination.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 21 / 44 · SOURCE 21</span></div>
<h1 class="fig-title">Empirical CDFs by outcome</h1><div class="figure-wrap"><img src="../outputs/figures/21_class_conditional_ecdfs.png" alt="Empirical CDFs by outcome" data-figure="21_class_conditional_ecdfs.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare cumulative numerical distributions for legitimate and fraud cases.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Widening ECDF gaps highlight thresholds or ranges with class separation. Do not interpret class-normalized curves as population fraud probabilities.</div></div><div class="fig-meta">Source: supplied outputs/figures/21_class_conditional_ecdfs.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 22 / 44 · SOURCE 22</span></div>
<h1 class="fig-title">Categorical × Boolean interactions</h1><div class="figure-wrap"><img src="../outputs/figures/22_categorical_flag_interactions.png" alt="Categorical × Boolean interactions" data-figure="22_categorical_flag_interactions.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare conditional fraud rates and support across joint feature groups.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Interactions can expose differences hidden in one-feature plots. Sparse combinations should be interpreted with support counts in view.</div></div><div class="fig-meta">Source: supplied outputs/figures/22_categorical_flag_interactions.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 23 / 44 · SOURCE 23</span></div>
<h1 class="fig-title">Hour-of-week risk heatmaps</h1><div class="figure-wrap"><img src="../outputs/figures/23_weekly_hourly_fraud_surface.png" alt="Hour-of-week risk heatmaps" data-figure="23_weekly_hourly_fraud_surface.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Visualize fraud rate and observation counts jointly across time coordinates.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Rate patterns are more credible where sample support is substantial. No causal or temporal stability guarantee follows from one observed period.</div></div><div class="fig-meta">Source: supplied outputs/figures/23_weekly_hourly_fraud_surface.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 24 / 44 · SOURCE 24</span></div>
<h1 class="fig-title">Fraud geometry in two dimensions</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/24_pairwise_class_geometry.png" alt="Fraud geometry in two dimensions" data-figure="24_pairwise_class_geometry.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Inspect selected feature pairs for overlap, clusters and unusual regions.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Nonlinear class boundaries may explain why trees compete with additive models. Plotting subsamples can distort apparent density and class composition.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/24_pairwise_class_geometry.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">04 · DEEPER DATA EXPLORATION</span><span class="fig-number">FIGURE 25 / 44 · SOURCE 25</span></div>
<h1 class="fig-title">Train–test distribution comparisons</h1><div class="figure-wrap"><img src="../outputs/figures/25_train_test_ecdf_shift.png" alt="Train–test distribution comparisons" data-figure="25_train_test_ecdf_shift.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare unlabeled feature distributions between training and test splits.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>A visible shift warns that held-out CV may not exactly match test conditions. Without test labels, score deterioration cannot be quantified directly.</div></div><div class="fig-meta">Source: supplied outputs/figures/25_train_test_ecdf_shift.png</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 05 / 06</div><h1>PREDICTIVE PERFORMANCE</h1><div class="chapter-sub">Evaluate ranking, calibration, workload, subgroup behavior, and the cost of training.</div><div class="chapter-points"><span>ROC AUC and average precision</span><span>Calibration versus discrimination</span><span>Review capacity and subgroup robustness</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 26 / 44 · SOURCE 26</span></div>
<h1 class="fig-title">A four-metric model scorecard</h1><div class="figure-wrap"><img src="../outputs/figures/26_four_metric_model_scorecard.png" alt="A four-metric model scorecard" data-figure="26_four_metric_model_scorecard.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare ROC AUC, average precision, log loss and Brier loss.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Ranking quality and probability quality need not order models identically. Choose a primary metric before interpreting many scores.</div></div><div class="fig-meta">Source: supplied outputs/figures/26_four_metric_model_scorecard.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 27 / 44 · SOURCE 27</span></div>
<h1 class="fig-title">Predictive quality versus compute cost</h1><div class="figure-wrap"><img src="../outputs/figures/27_performance_vs_training_time.png" alt="Predictive quality versus compute cost" data-figure="27_performance_vs_training_time.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Plot candidate performance against wall-clock training expense.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Small gains may not justify large computation on a teaching project. Times depend on hardware, device, threading and cache state.</div></div><div class="fig-meta">Source: supplied outputs/figures/27_performance_vs_training_time.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 28 / 44 · SOURCE 28</span></div>
<h1 class="fig-title">Predicted-risk distributions by class</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/28_oof_score_distributions.png" alt="Predicted-risk distributions by class" data-figure="28_oof_score_distributions.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Compare predicted fraud probabilities for legitimate and fraud cases.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Overlap reveals unavoidable false positives and false negatives at any cutoff. These are out-of-fold scores, not deployment calibration guarantees.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/28_oof_score_distributions.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 29 / 44 · SOURCE 29</span></div>
<h1 class="fig-title">Cumulative gains and lift</h1><div class="figure-wrap"><img src="../outputs/figures/29_cumulative_gains_and_lift.png" alt="Cumulative gains and lift" data-figure="29_cumulative_gains_and_lift.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Measure how many fraud cases are captured within the highest-ranked transactions.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Lift compares model-guided review against random screening at the same budget. Operational usefulness depends on review costs and achievable capacity.</div></div><div class="fig-meta">Source: supplied outputs/figures/29_cumulative_gains_and_lift.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 30 / 44 · SOURCE 30</span></div>
<h1 class="fig-title">Precision and recall at limited review budget</h1><div class="figure-wrap"><img src="../outputs/figures/30_precision_recall_at_review_budget.png" alt="Precision and recall at limited review budget" data-figure="30_precision_recall_at_review_budget.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Examine quality as the fraction of investigated transactions increases.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Fraud screening is a ranking-and-capacity problem, not only 0.5 classification. Selecting capacity using the same OOF labels can induce optimism.</div></div><div class="fig-meta">Source: supplied outputs/figures/30_precision_recall_at_review_budget.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 31 / 44 · SOURCE 31</span></div>
<h1 class="fig-title">Confusion matrices under two decision rules</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/31_confusion_matrices_by_policy.png" alt="Confusion matrices under two decision rules" data-figure="31_confusion_matrices_by_policy.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Contrast fixed 0.5 probability threshold with an intervention budget (top 1%).</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Threshold selection materially changes precision, recall and false alarms. Never transfer a threshold across populations without validation.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/31_confusion_matrices_by_policy.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 32 / 44 · SOURCE 32</span></div>
<h1 class="fig-title">Reliability diagrams across models</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/32_model_reliability_comparison.png" alt="Reliability diagrams across models" data-figure="32_model_reliability_comparison.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Compare observed fraud frequency against predicted risk by score bin.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>A model may rank well but still misstate absolute risk. Rare-event bins require caution, especially near extreme predicted risks.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/32_model_reliability_comparison.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 33 / 44 · SOURCE 33</span></div>
<h1 class="fig-title">Calibration uncertainty intervals</h1><div class="figure-wrap"><img src="../outputs/figures/33_calibration_with_wilson_intervals.png" alt="Calibration uncertainty intervals" data-figure="33_calibration_with_wilson_intervals.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Plot uncertainty around observed bin-level fraud rates.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Wide intervals reveal where limited positive counts weaken conclusions. Intervals summarize within-bin sampling variation, not all sources of model uncertainty.</div></div><div class="fig-meta">Source: supplied outputs/figures/33_calibration_with_wilson_intervals.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 34 / 44 · SOURCE 34</span></div>
<h1 class="fig-title">Model quality across channels</h1><div class="figure-wrap"><img src="../outputs/figures/34_subgroups_channel.png" alt="Model quality across channels" data-figure="34_subgroups_channel.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare discrimination by transaction channel for selected candidates.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Subgroup metrics can reveal heterogeneous predictive behavior. Subgroup sample sizes and fraud counts determine precision.</div></div><div class="fig-meta">Source: supplied outputs/figures/34_subgroups_channel.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 35 / 44 · SOURCE 34</span></div>
<h1 class="fig-title">Model quality across merchant categories</h1><div class="figure-wrap"><img src="../outputs/figures/34_subgroups_merchant_category.png" alt="Model quality across merchant categories" data-figure="34_subgroups_merchant_category.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Examine predictive quality across major merchant groups.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>A strong global score can conceal weaker performance in some subgroups. Small subgroup differences may be sampling noise; avoid overinterpretation.</div></div><div class="fig-meta">Source: supplied outputs/figures/34_subgroups_merchant_category.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">05 · PREDICTIVE PERFORMANCE</span><span class="fig-number">FIGURE 36 / 44 · SOURCE 35</span></div>
<h1 class="fig-title">Agreement among the top 1% riskiest cases</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/35_top_risk_set_overlap.png" alt="Agreement among the top 1% riskiest cases" data-figure="35_top_risk_set_overlap.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Use Jaccard overlap to compare models on transactions that actually trigger review.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Highly correlated overall predictions may still disagree at the operational margin. The most useful diversity depends on labeling costs and error consequences.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/35_top_risk_set_overlap.png</div>

---

<!-- _class: chapter -->
<div class="chapter-inner"><div class="chapter-num">SECTION 06 / 06</div><h1>INTERPRETATION &amp; TUNING</h1><div class="chapter-sub">Explain what models learn, whether blending helps, and how to interpret grid-search results.</div><div class="chapter-points"><span>Feature importance and partial dependence</span><span>Hyperparameter and fold stability</span><span>Outer-fold evidence for tuning</span></div></div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 37 / 44 · SOURCE 36</span></div>
<h1 class="fig-title">Logistic coefficients and tree importances</h1><div class="figure-wrap"><img src="../outputs/figures/36_model_feature_importance.png" alt="Logistic coefficients and tree importances" data-figure="36_model_feature_importance.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Contrast coefficient-based linear interpretation with tree feature importance.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Importance notions are model-specific and not on a common causal scale. Correlated features and encoding influence apparent importance.</div></div><div class="fig-meta">Source: supplied outputs/figures/36_model_feature_importance.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 38 / 44 · SOURCE 37</span></div>
<h1 class="fig-title">Partial dependence: learned nonlinear response</h1><div class="figure-wrap"><img src="../outputs/figures/37_partial_dependence_models.png" alt="Partial dependence: learned nonlinear response" data-figure="37_partial_dependence_models.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare average predicted response while varying selected features.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Different shapes help explain disagreements between linear, spline and tree models. Marginal interventions can evaluate unrealistic correlated-feature combinations.</div></div><div class="fig-meta">Source: supplied outputs/figures/37_partial_dependence_models.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 39 / 44 · SOURCE 38</span></div>
<h1 class="fig-title">How blending changes individual scores</h1><div class="figure-wrap"><img src="../outputs/figures/38_blend_vs_single_predictions.png" alt="How blending changes individual scores" data-figure="38_blend_vs_single_predictions.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare selected ensemble predictions against the leading single model.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Blending can alter risk ordering even when overall metrics barely change. A change in predicted probability is not evidence of better calibration.</div></div><div class="fig-meta">Source: supplied outputs/figures/38_blend_vs_single_predictions.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 40 / 44 · SOURCE 39</span></div>
<h1 class="fig-title">Unlabeled Kaggle submission diagnostics</h1><div class="figure-wrap"><img src="../outputs/figures/39_submission_probability_sanity.png" alt="Unlabeled Kaggle submission diagnostics" data-figure="39_submission_probability_sanity.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Inspect distribution, extremes and rank behavior of final test probabilities.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Sanity checks can catch invalid ranges or suspicious collapse of risk scores. Unlabeled test plots cannot estimate true predictive accuracy.</div></div><div class="fig-meta">Source: supplied outputs/figures/39_submission_probability_sanity.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 41 / 44 · SOURCE 40</span></div>
<h1 class="fig-title">Effects of model hyperparameters</h1><div class="figure-wrap"><img src="../outputs/figures/40_hyperparameter_effects.png" alt="Effects of model hyperparameters" data-figure="40_hyperparameter_effects.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare model families, regularization and capacity settings.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Tree depth, leaf size and learning rate trade expressivity against variance. These are tested configurations, not a continuous optimization landscape.</div></div><div class="fig-meta">Source: supplied outputs/figures/40_hyperparameter_effects.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 42 / 44 · SOURCE 41</span></div>
<h1 class="fig-title">Fold-by-fold ROC AUC stability</h1><div class="figure-body"><div class="figure-wrap tall"><img src="../outputs/figures/41_fold_auc_heatmap.png" alt="Fold-by-fold ROC AUC stability" data-figure="41_fold_auc_heatmap.png" /></div>
<div class="fig-sidebar"><div class="note-card"><span class="note-label">How to read</span>Compare candidate scores across common validation folds.</div>
<div class="note-card secondary"><span class="note-label">Interpretation / limit</span>Consistent differences are more persuasive than single pooled-rank changes. Five folds do not fully quantify sampling uncertainty.</div></div></div><div class="fig-meta">Source: supplied outputs/figures/41_fold_auc_heatmap.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 43 / 44 · SOURCE 42</span></div>
<h1 class="fig-title">Inner grid search: every tested configuration</h1><div class="figure-wrap"><img src="../outputs/figures/42_gridsearch_full_parameter_space.png" alt="Inner grid search: every tested configuration" data-figure="42_gridsearch_full_parameter_space.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Visualize scikit-learn GridSearchCV scores across the XGBoost/CatBoost candidate grid.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Grid-search performance selects configurations inside the training data only. Best inner-CV score is not the unbiased estimate of final test performance.</div></div><div class="fig-meta">Source: supplied outputs/figures/42_gridsearch_full_parameter_space.png</div>

---

<!-- _class: figure-slide -->
<div class="fig-head"><span class="eyebrow">06 · INTERPRETATION &amp; TUNING</span><span class="fig-number">FIGURE 44 / 44 · SOURCE 43</span></div>
<h1 class="fig-title">Did tuning help on held-out outer folds?</h1><div class="figure-wrap"><img src="../outputs/figures/43_nested_gridsearch_outer_results.png" alt="Did tuning help on held-out outer folds?" data-figure="43_nested_gridsearch_outer_results.png" /></div>
<div class="bottom-notes"><div class="note-card"><span class="note-label">What this shows</span>Compare fixed and tuned families on untouched outer folds, including search cost.</div>
<div class="note-card secondary"><span class="note-label">Interpretation & caution</span>Use outer-fold results, not the best inner score, to judge tuning benefits. Compute-time comparisons are device-dependent; finite-fold differences remain uncertain.</div></div><div class="fig-meta">Source: supplied outputs/figures/43_nested_gridsearch_outer_results.png</div>

---

<!-- _class: content -->
<div class="eyebrow">SYNTHESIS</div><h1>What the 44 figures establish</h1>
<div class="content-grid">
<div class="content-box"><b>Fraud is rare and structured</b><p>Risk varies across feature values, time periods and feature combinations.</p></div>
<div class="content-box"><b>Linear is a useful benchmark</b><p>Logistic regression offers an interpretable log-odds starting point; splines and trees relax additivity.</p></div>
<div class="content-box"><b>Evaluation is multidimensional</b><p>ROC AUC, precision-recall, calibration and operational review budgets answer different questions.</p></div>
<div class="content-box"><b>Tuning needs honest validation</b><p>The performance of a tuned model must be judged on outer held-out folds, not its best inner score.</p></div>
</div>

---

<!-- _class: content -->
<div class="eyebrow">THESIS · ANTITHESIS · SYNTHESIS</div><h1>Why not just pick the largest ROC AUC?</h1>
<div class="content-grid">
<div class="content-box"><b>Thesis</b><p>A high ROC AUC means useful ranking for Kaggle's objective.</p></div>
<div class="content-box"><b>Antithesis</b><p>The same model can be miscalibrated, expensive to train, unstable across folds, or unhelpful at an actual review budget.</p></div>
<div class="content-box"><b>Synthesis</b><p>Use ROC AUC to rank candidates, then stress-test calibration, rare-event precision, stability, subgroup behavior and cost.</p></div>
<div class="content-box"><b>Selection rule</b><p>Prefer a simpler model if added complexity or tuning brings no convincing held-out improvement.</p></div>
</div>

---

<!-- _class: content -->
<div class="eyebrow">VALIDITY & UNCERTAINTY</div><h1>Limits of what these plots can prove</h1>
<div class="content-grid">
<div class="content-box"><b>Observational, often synthetic</b><p>Descriptive differences do not identify causal drivers of fraud.</p></div>
<div class="content-box"><b>Selection optimism</b><p>Using the same out-of-fold labels to choose a winning candidate or blend can inflate reported success.</p></div>
<div class="content-box"><b>Unknown provenance of image-only results</b><p>Numerical claims require the saved fold CSVs, configurations, hardware logs and sample counts.</p></div>
<div class="content-box"><b>External validity</b><p>Unlabeled Kaggle test results and possible train–test shift limit generalization claims.</p></div>
</div>

---

<!-- _class: content -->
<div class="eyebrow">REPRODUCIBILITY & NEXT STEPS</div><h1>From a visual report to a defensible submission</h1>
<div class="content-grid">
<div class="content-box"><b>Reproduce</b><p>Run final_project/credit_card_fraud.ipynb with the project Conda environment; record versions, seed and device.</p></div>
<div class="content-box"><b>Archive</b><p>Keep OOF predictions, fold metrics, complete hyperparameter searches, figure catalog and model configurations.</p></div>
<div class="content-box"><b>Validate again</b><p>Use a fresh holdout or nested evaluation if choosing the final blend based on many OOF candidates.</p></div>
<div class="content-box"><b>Submit</b><p>Verify probability bounds and id order; submit the selected id,is_fraud CSV and record public leaderboard feedback separately.</p></div>
</div><div class="strip">The PDF is static. The HTML provides keyboard navigation, fade transitions and click-to-zoom figures.</div>

---

<!-- _class: closing -->
<div class="chapter-inner"><div class="eyebrow">LDS1071 · FINAL PROJECT</div><h1>Thank you.</h1><div class="chapter-sub">Research artifacts: notebook, 44 supplied figures, figure manifest, Marp Markdown, HTML and PDF.</div><div class="chip-row"><div class="chip"><strong>44 / 44</strong>figures included</div><div class="chip"><strong>5-fold</strong>stratified CV framework</div><div class="chip"><strong>ROC AUC</strong>primary Kaggle metric</div></div></div>
