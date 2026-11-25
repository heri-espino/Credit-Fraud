# Synthetic validation — experiment027

A local Python 3.11-compatible environment (NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0) exercised a copied implementation of the statistical core, without network access or original transaction data. Checks passed:

- Known four-p-value Holm and Bonferroni example; monotonic adjustment bounds.
- Ten synthetic classifiers, 45 unordered comparisons, known discordant counts, and exact binomial McNemar agreement.
- Identical decision vectors: p=1 for both tests, zero-width zero-difference interval, identical bootstrap draws.
- Strict lower-triangle matrix contains 45 entries.
- Joint multinomial bootstrap covariance agrees with theoretical row-bootstrap covariance on 400 synthetic observations and 100,000 draws (absolute tolerance 1e-5, relative tolerance .05).

These were core-routine checks, not execution of the complete committed notebook or its integration smoke test. The repository checkout and private experiment024 checkpoints were unavailable in the local environment. The full smoke test and original-data inference remain to be run by the owner. No empirical p-values are claimed.
