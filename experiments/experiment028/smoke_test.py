"""Validate exact tied AUC, DeLong and deterministic paired bootstrap on synthetic data."""
from pathlib import Path
import sys,tempfile
import numpy as np
import pandas as pd
import nbformat
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/experiment027'))
sys.path.insert(0,str(Path(__file__).parent))
from auc_inference import prepare_auc,weighted_auc,bootstrap_auc,pairwise_auc
nb=nbformat.read(ROOT/'notebook_inferencia_final_es.ipynb',as_version=4)
nbformat.validate(nb)
for i,c in enumerate(nb.cells):
    if c.cell_type=='code': compile(c.source,f'cell {i}','exec')
rng=np.random.default_rng(42)
y=np.r_[np.ones(12,dtype=int),np.zeros(19,dtype=int)]
P=rng.integers(0,7,(len(y),10))/6
P[:,1]=P[:,0]
auc,vp,vn,cov,prepared=prepare_auc(y,P)
h=(P[:12,None,:]>P[None,12:,:])+.5*(P[:12,None,:]==P[None,12:,:])
np.testing.assert_allclose(vp,h.mean(1),rtol=0,atol=1e-14)
np.testing.assert_allclose(vn,h.mean(0),rtol=0,atol=1e-14)
np.testing.assert_allclose(auc,[roc_auc_score(y,p) for p in P.T],atol=1e-14)
np.testing.assert_allclose(cov,np.cov(h.mean(1),rowvar=False)/12+np.cov(h.mean(0),rowvar=False)/19,atol=1e-14)
for b in range(50):
    wp=np.bincount(rng.integers(12,size=12),minlength=12)
    wn=np.bincount(rng.integers(19,size=19),minlength=19)
    np.testing.assert_allclose(weighted_auc(prepared,wp,wn),[roc_auc_score(y,p,sample_weight=np.r_[wp,wn]) for p in P.T],atol=1e-14)
names=[f'M{i:02}' for i in range(1,11)]
with tempfile.TemporaryDirectory() as d:
    cp=Path(d)/'boot.npz'
    m,p,c,draw=pairwise_auc(y,P,names,B=101,jobs=1,checkpoint=cp)
    m,p,c,draw2=pairwise_auc(y,P,names,B=151,jobs=2,checkpoint=cp)
    np.testing.assert_array_equal(draw,draw2[:101])
    np.testing.assert_array_equal(draw2,bootstrap_auc(prepared,12,19,B=151,jobs=1))
    assert len(p)==45
    pair=p.query("fila=='M02' and columna=='M01'").iloc[0]
    assert pair.p_delong==pair.p_bootstrap==1 and pair.delta_auc==0
    assert pair.ci_low==pair.ci_high==0
    assert (p.p_delong_holm<=p.p_delong_bonferroni+1e-15).all()
    assert (p.p_bootstrap_holm>=p.p_bootstrap-1e-15).all()
    try: pairwise_auc(y,P,names,B=151,seed=43,checkpoint=cp)
    except ValueError: pass
    else: raise AssertionError('Caché incompatible aceptada')
print('PASS: notebook, placements, covariance, tied weighted AUC, 45 pairs, identical predictions, cache')
