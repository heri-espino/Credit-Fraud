"""Pairwise recall inference from experiment024 checkpoints. No model fitting."""
from pathlib import Path
import json, zipfile
import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, brier_score_loss

SEED_FOLDS = 42
N_FOLDS = 5
METRICS = ('roc_auc','average_precision','log_loss','brier')

def read_labels(root):
    root=Path(root)
    for path in (root/'data/train.csv',root/'train.csv',Path('/kaggle/input/playground-series-s6e11/train.csv')):
        if path.is_file():
            df=pd.read_csv(path,usecols=['id','is_fraud'])
            break
    else:
        for path in (root/'playground-series-s6e11.zip',root/'data/playground-series-s6e11.zip',root.parent/'playground-series-s6e11.zip'):
            if path.is_file():
                with zipfile.ZipFile(path) as z, z.open('train.csv') as f:
                    df=pd.read_csv(f,usecols=['id','is_fraud'])
                break
        else:
            raise FileNotFoundError('Falta train.csv original o playground-series-s6e11.zip. No reordenar las filas.')
    if not df.id.is_unique or df.id.isna().any() or set(df.is_fraud.unique())!={0,1}:
        raise ValueError('Identificadores o etiquetas inválidos.')
    return df.is_fraud.to_numpy(dtype=np.int8)

def read_oof(checkpoints, ranking, manifest, y):
    """Verify signed-run identifier, original outer splits, coverage and all published metrics."""
    checkpoints=Path(checkpoints)
    if manifest['protocolo']!='experiment024' or manifest['n_particiones']!=N_FOLDS:
        raise ValueError('Se requiere la corrida experiment024 de cinco folds.')
    if len(y)!=manifest['observaciones_entrenamiento']:
        raise ValueError('Número de filas incompatible con el manifiesto.')
    names=ranking.familia.tolist()
    if len(names)!=10 or len(set(names))!=10 or ranking.puesto.tolist()!=list(range(1,11)):
        raise ValueError('Se requieren diez finalistas únicos, en orden original.')
    if not ranking.roc_auc.is_monotonic_decreasing or names[0]!=manifest['seleccion_nominal']:
        raise ValueError('Ranking incompatible con el manifiesto.')
    if not np.isclose(ranking.roc_auc.iloc[0],manifest['auc_seleccionado'],rtol=0,atol=5e-10):
        raise ValueError('AUC del ganador incompatible.')
    family_ensemble={'Promedio de familias','Bagging XGBoost','Stacking XGBoost','Logística + XGBoost'}
    files={}
    for j,name in enumerate(names):
        family,scenario=name.rsplit(' | ',1)
        prefix=f'ensemble_{scenario}' if family in family_ensemble else 'individual'
        files.setdefault(prefix,[]).append((j,name))
    folds=list(StratifiedKFold(n_splits=N_FOLDS,shuffle=True,random_state=SEED_FOLDS).split(np.zeros(len(y)),y))
    P=np.full((len(y),len(names)),np.nan,dtype=np.float64)
    coverage=np.zeros(len(y),dtype=np.int8)
    for k,(_,va) in enumerate(folds,1):
        coverage[va]+=1
        for prefix,entries in files.items():
            path=checkpoints/f'{prefix}_fold{k}_PRIVATE.npz'
            if not path.is_file():
                raise FileNotFoundError(f'Falta {path}. Recuperar los checkpoints privados de la corrida original; no hace falta reentrenar si existen.')
            with np.load(path,allow_pickle=False) as z:
                if str(z['firma'])!=manifest['firma'] or not np.array_equal(z['va'],va):
                    raise ValueError(f'Firma o índices del fold incompatibles: {path}')
                for j,name in entries:
                    values=z[name+'__oof']
                    if values.shape!=(len(va),) or not np.isfinite(values).all() or not ((values>=0)&(values<=1)).all():
                        raise ValueError(f'Predicciones inválidas: {path}, {name}')
                    P[va,j]=values
    if not (coverage==1).all() or not np.isfinite(P).all():
        raise ValueError('Cobertura OOF incompleta o duplicada.')
    rows=[]
    for j,name in enumerate(names):
        p=P[:,j]
        rows.append(dict(familia=name,roc_auc=roc_auc_score(y,p),average_precision=average_precision_score(y,p),
                         log_loss=log_loss(y,p),brier=brier_score_loss(y,p)))
    audit=pd.DataFrame(rows)
    if not np.allclose(audit[list(METRICS)],ranking[list(METRICS)],atol=5e-10,rtol=0):
        raise ValueError('Las métricas reconstruidas no coinciden con el ranking publicado. Revisar etiquetas, orden y archivos.')
    return P,folds,audit

def decisions(y,P,folds,target=.98,fixed_threshold=None):
    """Replicate original alert policy; no threshold selected on its evaluation fold."""
    if not 0<target<=1 or (fixed_threshold is not None and not 0<=fixed_threshold<=1):
        raise ValueError('Umbral u objetivo inválidos.')
    Z=np.empty(P.shape,dtype=bool)
    thresholds=[]
    for k,(tr,va) in enumerate(folds,1):
        for j in range(P.shape[1]):
            if fixed_threshold is None:
                pos=np.sort(P[tr[y[tr]==1],j])
                if not len(pos): raise ValueError('Fold sin positivos de calibración.')
                t=float(pos[max(0,int(np.floor((1-target)*len(pos))))])
            else:
                t=float(fixed_threshold)
            Z[va,j]=P[va,j]>=t
            thresholds.append(dict(fold=k,modelo=f'M{j+1:02}',umbral=t))
    return Z,pd.DataFrame(thresholds)

def adjust_p(p):
    """Bonferroni and step-down Holm; stable handling of ties and original order."""
    p=np.asarray(p,dtype=float)
    if p.ndim!=1 or not len(p) or not np.isfinite(p).all() or not ((p>=0)&(p<=1)).all():
        raise ValueError('p-values inválidos.')
    m=len(p)
    order=np.argsort(p,kind='stable')
    holm=np.empty_like(p)
    holm[order]=np.minimum(1,np.maximum.accumulate((m-np.arange(m))*p[order]))
    return np.minimum(1,m*p),holm

def bootstrap_counts(Z,B=100000,seed=20261125,batch=512):
    """Exact distributional shortcut: sample joint binary patterns, not individual row indices."""
    Z=np.asarray(Z)
    if Z.ndim!=2 or not len(Z) or not np.isin(Z,[0,1]).all() or B<1 or batch<1:
        raise ValueError('Matriz binaria o parámetros bootstrap inválidos.')
    patterns,counts=np.unique(Z.astype(np.int64),axis=0,return_counts=True)
    rng=np.random.default_rng(seed)
    draws=np.empty((B,Z.shape[1]),dtype=np.int64)
    for start in range(0,B,batch):
        end=min(start+batch,B)
        weights=rng.multinomial(len(Z),counts/counts.sum(),size=end-start)
        draws[start:end]=weights@patterns
    return draws,len(patterns)

def pairwise_recall(y,Z,names,B=100000,seed=20261125,alpha=.05):
    """All unordered pairs; differences are row minus column in heatmaps."""
    y=np.asarray(y)
    Z=np.asarray(Z)
    if y.ndim!=1 or Z.shape!=(len(y),len(names)) or len(names)<2 or len(set(names))!=len(names):
        raise ValueError('Dimensiones o nombres inválidos.')
    if set(np.unique(y))!={0,1} or not np.isin(Z,[0,1]).all() or not 0<alpha<1:
        raise ValueError('Datos binarios/alpha inválidos.')
    pos=Z[y==1].astype(bool); neg=Z[y==0].astype(bool)
    n=len(pos)
    draws,n_patterns=bootstrap_counts(pos,B,seed)
    totals=pos.sum(axis=0)
    q=np.quantile(draws/n,[alpha/2,1-alpha/2],axis=0)
    models=pd.DataFrame(dict(modelo=names,VP=totals,FN=n-totals,FP=neg.sum(0),
        VN=len(neg)-neg.sum(0),recall=totals/n,recall_ci_low=q[0],recall_ci_high=q[1],
        tasa_falsas_alarmas=neg.mean(0)))
    rows=[]
    for i in range(1,len(names)):
        for j in range(i):
            b=int(np.sum(pos[:,i]&~pos[:,j]))
            c=int(np.sum(~pos[:,i]&pos[:,j]))
            obs=b-c
            delta=draws[:,i]-draws[:,j]
            lo,hi=np.quantile(delta/n,[alpha/2,1-alpha/2])
            # Center at the observed difference to approximate the null distribution.
            # Integer count scale avoids floating-point discrepancies at the boundary.
            p_boot=(1+np.count_nonzero(np.abs(delta-obs)>=abs(obs)))/(B+1)
            p_exact=binomtest(b,b+c,p=.5,alternative='two-sided').pvalue if b+c else 1.
            rows.append(dict(fila=names[i],columna=names[j],n_positivos=n,
                solo_fila=b,solo_columna=c,ambos_detectan=int(np.sum(pos[:,i]&pos[:,j])),
                ninguno_detecta=int(np.sum(~pos[:,i]&~pos[:,j])),
                delta_recall=obs/n,delta_pp=100*obs/n,
                ci_low=lo,ci_high=hi,p_mcnemar=p_exact,p_bootstrap=p_boot))
    pairs=pd.DataFrame(rows)
    for method in ('mcnemar','bootstrap'):
        b,h=adjust_p(pairs['p_'+method])
        pairs['p_'+method+'_bonferroni']=b
        pairs['p_'+method+'_holm']=h
        pairs['rechazo_'+method+'_holm']=h<=alpha
    return models,pairs,n_patterns

def p_matrix(pairs,names,column):
    matrix=pd.DataFrame(np.nan,index=names,columns=names)
    for row in pairs.itertuples(index=False):
        matrix.loc[row.fila,row.columna]=getattr(row,column)
    return matrix
