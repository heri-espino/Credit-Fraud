"""Synthetic integration test; run from the repository root."""
from pathlib import Path
import json, tempfile, sys
import numpy as np
import pandas as pd
import nbformat
sys.path.insert(0,str(Path(__file__).parent))
import protocolo as p
root=Path(__file__).resolve().parents[2]
nb=nbformat.read(root/'notebook_final_es.ipynb',as_version=4)
nbformat.validate(nb)
for i,c in enumerate(nb.cells):
    if c.cell_type=='code': compile(c.source,f'cell {i}','exec')
assert len(p.ParameterGrid(p.GRILLA_BOOSTER))==36
assert p.GRILLA_BOOSTER is p.GRILLAS_COMUNES['Stacking XGBoost'] is p.GRILLAS_COMUNES['Logística + XGBoost']
p.configurar(['a','b'],['flag'],['cat'],2,cpu_jobs=2,grid_jobs=2,xgb_device='cpu',cat_device='CPU')
rng=np.random.default_rng(42)
def datos(n):
    return pd.DataFrame(dict(a=100*rng.normal(size=n)+300,b=rng.normal(size=n),
        flag=rng.integers(0,2,n).astype(bool),cat=rng.choice(['x','y','z'],n)))
X=datos(150); Xt=datos(20)
Xt.loc[0,'cat']='unknown'
y=(X.a+80*rng.normal(size=len(X))>300).astype(int).to_numpy()
a,b=p.matrices_por_split(X,[Xt])
assert set(a)==set(p.REPRESENTACIONES)
assert np.allclose(a['raw'][:,0],X.a,rtol=1e-6)
assert abs(a['standardized'][:,0].mean())<1e-5
assert a['raw_kmeans_dbscan'].shape[1]==a['raw'].shape[1]+8
assert np.array_equal(a['raw'][:,2:],a['standardized'][:,2:])
assert np.array_equal(a['raw_kmeans_dbscan'][:,:a['raw'].shape[1]],a['raw'])
assert np.isfinite(b['standardized_kmeans_dbscan']).all()
for g in p.GRILLAS_COMUNES.values():
    for k,v in g.items(): g[k]=v[:1]
original=p.nuevo_modelo
def small(f,par):
    m=original(f,par)
    if f=='CatBoost':m.set_params(iterations=2,thread_count=1)
    elif f!='Logística':m.set_params(n_estimators=2,n_jobs=1)
    return m
p.nuevo_modelo=small
with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp); signature=p.firma_datos(X,y,Xt,np.arange(len(X)),np.arange(len(Xt)))
    # Validate the actual parallel scheduling and checkpoint resumption without retraining.
    gp=d/'test_grid.json'; calls=[]
    def eval_test(par):
        calls.append(par['v'])
        return [par['v']/10]*3
    params=[{'v':v} for v in range(1,5)]
    out=p.buscar_configuraciones('Logística',params,eval_test,gp,signature)
    assert len(calls)==4 and len(out)==4
    out2=p.buscar_configuraciones('Logística',params,eval_test,gp,signature)
    assert out==out2 and len(calls)==4
    base,g,s,states=p.protocolo_individual(X,y,Xt,d,signature)
    assert len(base)==20 and len(g)==80 and len(s)==100
    ens,ge,se=p.protocolo_ensambles(X,y,Xt,states,d,signature)
    assert len(ens)==20 and len(ge)==50 and len(se)==100
    allp={**base,**ens}
    assert len(allp)==40
    ranking=p.resumir_predicciones(allp,y)
    assert ranking.roc_auc.is_monotonic_decreasing
    for f in allp:
        assert all(np.isfinite(v).all() and ((v>=0)&(v<=1)).all() for v in allp[f].values())
    base2,_,_,states2=p.protocolo_individual(X,y,Xt,d,signature)
    ens2,_,_=p.protocolo_ensambles(X,y,Xt,states2,d,signature)
    for f,v in {**base2,**ens2}.items():
        for k in v: assert np.array_equal(v[k],allp[f][k])
    try: p.protocolo_individual(X,y,Xt,d,'invalid')
    except ValueError: pass
    else: raise AssertionError('Incompatible cache accepted')
print('PASS: factorial matrix, 36 grid, 40 candidates, parallel grid, checkpoints, syntax')
