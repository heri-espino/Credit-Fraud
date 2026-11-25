"""Synthetic F1 and pairing checks; no real predictions needed."""
from pathlib import Path
import sys
import numpy as np
import nbformat
from sklearn.metrics import f1_score
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/experiment027'))
sys.path.insert(0,str(Path(__file__).parent))
from f1_inference import pairwise_f1, f1_from_counts
from recall_inference import bootstrap_counts, p_matrix
nb=nbformat.read(ROOT/'notebook_inferencia_final_es.ipynb',as_version=4)
nbformat.validate(nb)
for i,c in enumerate(nb.cells):
    if c.cell_type=='code': compile(c.source,f'cell {i}','exec')
rng=np.random.default_rng(42)
y=np.r_[np.ones(30,dtype=int),np.zeros(80,dtype=int)]
Z=rng.integers(0,2,(len(y),10)).astype(bool)
Z[:,1]=Z[:,0]
names=['Logística + XGBoost | standardized_kmeans_dbscan']+[f'Synthetic {j}' for j in range(1,10)]
m,p,k=pairwise_f1(y,Z,names,B=5000,seed=42)
np.testing.assert_allclose(m.f1,[f1_score(y,Z[:,j]) for j in range(10)])
assert len(p)==45 and p_matrix(p,names,'p_holm').notna().sum().sum()==45
q=p[(p.fila==names[1])&(p.columna==names[0])].iloc[0]
assert q.delta_f1==q.ci_low==q.ci_high==0
assert q.p_bootstrap==q.p_holm==1
assert (p.p_holm>=p.p_bootstrap-1e-15).all()
streams=np.random.SeedSequence(42).spawn(2)
tp,_=bootstrap_counts(Z[y==1],B=5000,seed=streams[0])
fp,_=bootstrap_counts(Z[y==0],B=5000,seed=streams[1])
d=f1_from_counts(tp,fp,30)
np.testing.assert_array_equal(d[:,0],d[:,1])
q=p[(p.fila==names[2])&(p.columna==names[0])].iloc[0]
delta=d[:,2]-d[:,0]
np.testing.assert_allclose([q.ci_low,q.ci_high],np.quantile(delta,[.025,.975]))
assert np.isclose(q.delta_f1,m.f1.iloc[2]-m.f1.iloc[0])
assert q.p_bootstrap==(1+np.count_nonzero(np.abs(delta-q.delta_f1)>=abs(q.delta_f1)-1e-15))/5001
print('PASS: notebook syntax, original names, F1, paired bootstrap, 45 pairs, Holm, CI')
