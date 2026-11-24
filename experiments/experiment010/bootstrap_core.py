"""Exact stratified, paired nonparametric bootstrap of ROC AUC.

Fraud and non-fraud records are resampled separately using the same row indices
for every candidate. Score ties receive one-half credit.
"""
from __future__ import annotations
import numpy as np

def prepare_roc(y, predictions):
    """Precompute score order and tie-group boundaries for all models."""
    y = np.asarray(y, dtype=np.uint8)
    assert y.ndim == 1 and set(np.unique(y)) <= {0, 1}
    models = {}
    for name, score in predictions.items():
        score = np.asarray(score, dtype=np.float64)
        if score.shape != y.shape or not np.isfinite(score).all():
            raise ValueError(f"Invalid shape/values for {name}")
        order = np.argsort(score, kind="mergesort")
        ordered = score[order]
        starts = np.r_[0, np.flatnonzero(ordered[1:] != ordered[:-1]) + 1].astype(np.intp)
        models[name] = (order, starts, y[order].astype(bool))
    return models

def auc_weighted(prepared, counts):
    """Exact tie-aware ROC AUC using weighted sample multiplicities."""
    order, starts, positive = prepared
    sw = counts[order]
    wp = np.where(positive, sw, 0)
    wn = np.where(~positive, sw, 0)
    p = np.add.reduceat(wp, starts).astype(np.float64)
    n = np.add.reduceat(wn, starts).astype(np.float64)
    P, N = p.sum(), n.sum()
    if P == 0 or N == 0:
        raise ValueError("Bootstrap sample must contain both classes")
    return float(np.sum(p * (np.cumsum(n) - n + 0.5*n)) / (P*N))

def paired_stratified_bootstrap(y, scores, reference, n_replicates=1000, seed=2026, progress=None):
    """Return pooled AUC intervals, paired differences, and all bootstrap draws."""
    import pandas as pd
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y, dtype=np.uint8)
    positive_idx, negative_idx = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    if not len(positive_idx) or not len(negative_idx):
        raise ValueError("Both classes are required")
    if reference not in scores:
        raise KeyError(reference)
    pre = prepare_roc(y, scores)
    names = list(scores)
    rng = np.random.default_rng(seed)
    draws = np.empty((n_replicates, len(names)), dtype=np.float64)
    for b in range(n_replicates):
        positive = positive_idx[rng.integers(0, len(positive_idx), len(positive_idx))]
        negative = negative_idx[rng.integers(0, len(negative_idx), len(negative_idx))]
        counts = np.bincount(np.r_[positive, negative], minlength=len(y)).astype(np.float64)
        for j, name in enumerate(names):
            draws[b, j] = auc_weighted(pre[name], counts)
        if progress is not None and (b+1)%50 == 0:
            progress(b+1, n_replicates)
    observed = np.array([roc_auc_score(y, scores[name]) for name in names])
    ref_idx = names.index(reference)
    delta_draws = draws - draws[:, [ref_idx]]
    delta_obs = observed - observed[ref_idx]
    rows = []
    for j, name in enumerate(names):
        low, high = np.quantile(draws[:,j], [.025,.975])
        dlow, dhigh = np.quantile(delta_draws[:,j], [.025,.975])
        rows.append(dict(name=name, roc_auc=observed[j], auc_ci_low=low, auc_ci_high=high,
                         delta_vs_reference=delta_obs[j], delta_ci_low=dlow, delta_ci_high=dhigh,
                         bootstrap_frac_delta_positive=float(np.mean(delta_draws[:,j]>0)),
                         bootstrap_replicates=n_replicates, bootstrap_seed=seed,
                         reference=reference, scope='OOF exploratory, selected on same data'))
    return pd.DataFrame(rows), pd.DataFrame(draws, columns=names), pd.DataFrame(delta_draws, columns=names)
