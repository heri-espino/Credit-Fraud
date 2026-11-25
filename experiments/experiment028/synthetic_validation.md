# Synthetic validation — experiment028

Local Python environment: NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, scikit-learn 1.8.0, Matplotlib 3.10.8, Seaborn 0.13.2.

Executed checks on copied core formulas and plotting code (not the full committed notebook): ten synthetic classifiers, 12 positive and 19 negative observations, deliberate score ties and identical classifiers. DeLong positive/negative placements and covariance matched direct pairwise kernel computation. Observed AUCs matched scikit-learn. All ten exact weighted AUCs matched scikit-learn sample_weight on 50 independent paired stratified resamples, including ties; identical score columns gave identical bootstrap values. The three continuous Seaborn panels rendered with a common [0,1] normalization; each displayed the original 45 lower-triangular numerical values with no binarization. Assertions passed.

The local environment could not resolve github.com and did not have private experiment024 checkpoints or original training data. The full repository smoke test (including cache integration), complete notebook run, and actual AUC/recall p-values remain pending on the owner's machine. No empirical results are claimed.
