"""Paired stratified F1 bootstrap of fixed out-of-fold decisions."""
import numpy as np
import pandas as pd
from recall_inference import adjust_p, bootstrap_counts

def f1_from_counts(tp,fp,n_pos):
    """Binary F1 = 2 TP / (2 TP + FP + FN), with FN = n_pos - TP."""
    return 2.0*np.asarray(tp)/(n_pos+np.asarray(tp)+np.asarray(fp))

def pairwise_f1(y,Z,names,B=100_000,seed=42,alpha=.05):
    y=np.asarray(y); Z=np.asarray(Z); names=list(names)
    if y.ndim!=1 or Z.shape!=(len(y),len(names)) or len(names)<2 or len(set(names))!=len(names):
        raise ValueError('Dimensiones o nombres incompatibles.')
    if set(np.unique(y))!={0,1} or not np.isin(Z,[0,1]).all() or B<1 or not 0<alpha<1:
        raise ValueError('Etiquetas, decisiones o parámetros inválidos.')
    pos=Z[y==1]; neg=Z[y==0]; n_pos=len(pos)
    # Independent class resamples, shared across all ten classifiers within each class.
    streams=np.random.SeedSequence(seed).spawn(2)
    tp,kp=bootstrap_counts(pos,B=B,seed=streams[0])
    fp,kn=bootstrap_counts(neg,B=B,seed=streams[1])
    observed=f1_from_counts(pos.sum(axis=0),neg.sum(axis=0),n_pos)
    draws=f1_from_counts(tp,fp,n_pos)
    models=pd.DataFrame({'modelo':names,'f1':observed})
    rows=[]
    for i in range(1,len(names)):
        for j in range(i):
            d=float(observed[i]-observed[j])
            delta=draws[:,i]-draws[:,j]
            low,high=np.quantile(delta,[alpha/2,1-alpha/2])
            p=(1+np.count_nonzero(np.abs(delta-d)>=abs(d)-1e-15))/(B+1)
            rows.append(dict(fila=names[i],columna=names[j],delta_f1=d,
                ci_low=low,ci_high=high,p_bootstrap=p))
    pairs=pd.DataFrame(rows)
    _,pairs['p_holm']=adjust_p(pairs.p_bootstrap)
    return models,pairs,dict(patrones_positivos=kp,patrones_negativos=kn)
