"""Synthetic smoke: no original data or model fitting."""
from pathlib import Path
import sys, tempfile
import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score,average_precision_score,log_loss,brier_score_loss
import nbformat
sys.path.insert(0,str(Path(__file__).parent))
from recall_inference import adjust_p,bootstrap_counts,pairwise_recall,p_matrix,decisions,read_oof
ROOT=Path(__file__).resolve().parents[2]
nb=nbformat.read(ROOT/'notebook_inferencia_final_es.ipynb',as_version=4)
nbformat.validate(nb)
for i,c in enumerate(nb.cells):
    if c.cell_type=='code': compile(c.source,f'cell {i}','exec')
b,h=adjust_p([.04,.001,.02,.8])
np.testing.assert_allclose(b,[.16,.004,.08,1])
np.testing.assert_allclose(h,[.08,.004,.06,.8])
y=np.r_[np.ones(100,dtype=int),np.zeros(100,dtype=int)]
Z=np.zeros((200,10),dtype=bool)
Z[:80,0]=True; Z[:90,1]=True; Z[:,2]=Z[:,0]
names=[f'M{i:02}' for i in range(1,11)]
m,p,k=pairwise_recall(y,Z,names,B=20000,seed=8)
assert len(p)==45 and k==3
q=p.query("fila=='M02' and columna=='M01'").iloc[0]
assert q.solo_fila==10 and q.solo_columna==0 and q.delta_pp==10
assert q.p_mcnemar==binomtest(10,10,.5).pvalue
assert q.ci_low<=.1<=q.ci_high
q=p.query("fila=='M03' and columna=='M01'").iloc[0]
assert q.p_mcnemar==q.p_bootstrap==1 and q.ci_low==q.ci_high==0
assert p_matrix(p,names,'p_mcnemar').notna().sum().sum()==45
assert (p.p_mcnemar_holm<=p.p_mcnemar_bonferroni+1e-15).all()
assert (p.p_mcnemar_holm>=p.p_mcnemar-1e-15).all()
draws,_=bootstrap_counts(Z[y==1],1000,seed=8)
assert np.array_equal(draws[:,0],draws[:,2])
# Integration: synthesize checkpoints with the real naming convention and validate all metrics.
rng=np.random.default_rng(7)
P=rng.uniform(.01,.99,size=(len(y),10))
order=np.argsort([-roc_auc_score(y,P[:,j]) for j in range(10)])
P=P[:,order]
families=['Logística | raw','CatBoost | raw','Stacking XGBoost | raw','Logística + XGBoost | raw',
          'Bagging XGBoost | raw','CatBoost | standardized','Logística | standardized',
          'XGBoost | standardized','Bosque aleatorio | raw','Stacking XGBoost | adaptive']
ranking=pd.DataFrame([dict(puesto=j+1,familia=f,roc_auc=roc_auc_score(y,P[:,j]),
    average_precision=average_precision_score(y,P[:,j]),log_loss=log_loss(y,P[:,j]),brier=brier_score_loss(y,P[:,j]))
    for j,f in enumerate(families)])
manifest=dict(protocolo='experiment024',n_particiones=5,observaciones_entrenamiento=len(y),
    seleccion_nominal=families[0],auc_seleccionado=ranking.roc_auc.iloc[0],firma='synthetic')
folds=list(StratifiedKFold(5,shuffle=True,random_state=42).split(np.zeros(len(y)),y))
with tempfile.TemporaryDirectory() as tmp:
    for k,(tr,va) in enumerate(folds,1):
        groups={}
        for j,f in enumerate(families):
            a,s=f.rsplit(' | ',1)
            prefix=f'ensemble_{s}' if a in ('Stacking XGBoost','Logística + XGBoost','Bagging XGBoost') else 'individual'
            groups.setdefault(prefix,{})[f+'__oof']=P[va,j]
        for prefix,items in groups.items():
            np.savez(Path(tmp)/f'{prefix}_fold{k}_PRIVATE.npz',firma='synthetic',va=va,**items)
    recovered,fs,audit=read_oof(tmp,ranking,manifest,y)
    np.testing.assert_array_equal(recovered,P)
    z,t=decisions(y,P,fs,fixed_threshold=.5)
    np.testing.assert_array_equal(z,P>=.5)
    z,t=decisions(y,P,fs,target=.98)
    for k,(tr,va) in enumerate(fs,1):
        for j in range(10):
            pos=np.sort(P[tr[y[tr]==1],j])
            threshold=pos[int(np.floor(.02*len(pos)))]
            np.testing.assert_array_equal(z[va,j],P[va,j]>=threshold)
    bad=dict(manifest,firma='invalid')
    try: read_oof(tmp,ranking,bad,y)
    except ValueError: pass
    else: raise AssertionError('Wrong signature accepted')
print('PASS: notebook syntax, exact McNemar, paired bootstrap, Holm/Bonferroni, 45 pairs, checkpoints, policies')
