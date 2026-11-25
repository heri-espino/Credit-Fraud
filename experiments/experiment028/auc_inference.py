"""Paired full-sample AUC inference: DeLong and exact stratified bootstrap."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
from scipy.stats import norm
from joblib import Parallel, delayed, cpu_count
from threadpoolctl import threadpool_limits
from recall_inference import adjust_p

def prepare_auc(y,P):
    """Compute DeLong placements and sorted indices for exact weighted bootstrap.
    All scores are original float64 values; ties receive one-half credit.
    """
    y=np.asarray(y); P=np.asarray(P,dtype=np.float64)
    if y.ndim!=1 or P.ndim!=2 or P.shape[0]!=len(y) or P.shape[1]<2:
        raise ValueError('Dimensiones de predicciones inválidas.')
    if set(np.unique(y))!={0,1} or not np.isfinite(P).all() or not ((P>=0)&(P<=1)).all():
        raise ValueError('Etiquetas o probabilidades inválidas.')
    pos=P[y==1]; neg=P[y==0]
    m,k=pos.shape; q=len(neg)
    if min(m,q)<2: raise ValueError('Se necesitan al menos dos observaciones por clase.')
    vpos=np.empty((m,k)); vneg=np.empty((q,k)); prepared=[]
    for j in range(k):
        a,b=pos[:,j],neg[:,j]
        order=np.argsort(b,kind='stable')
        bs=b[order]
        left=np.searchsorted(bs,a,side='left')
        right=np.searchsorted(bs,a,side='right')
        vpos[:,j]=(left+right)/(2*q)
        aps=np.sort(a)
        al=np.searchsorted(aps,b,side='left')
        ar=np.searchsorted(aps,b,side='right')
        vneg[:,j]=1-(al+ar)/(2*m)
        prepared.append((order,left,right))
    auc=vpos.mean(axis=0)
    np.testing.assert_allclose(auc,vneg.mean(axis=0),rtol=0,atol=1e-12)
    cov=np.cov(vpos,rowvar=False,ddof=1)/m+np.cov(vneg,rowvar=False,ddof=1)/q
    return auc,vpos,vneg,cov,prepared

def weighted_auc(prepared,wp,wn):
    """One exact AUC vector for shared positive/negative resample multiplicities."""
    out=np.empty(len(prepared))
    den=2.*wp.sum()*wn.sum()
    if den<=0: raise ValueError('Muestra sin una clase.')
    for j,(order,left,right) in enumerate(prepared):
        cum=np.empty(len(wn)+1,dtype=np.int64); cum[0]=0
        np.cumsum(wn[order],dtype=np.int64,out=cum[1:])
        # Strictly lower negatives plus half of ties.
        out[j]=np.sum(wp*(cum[left]+cum[right]),dtype=np.int64)/den
    return out

def bootstrap_auc(prepared,m,q,B=2000,seed=42,jobs=4,checkpoint=None,signature=None,progress=None):
    """Exact stratified paired bootstrap of AUC, resumable by batches.
    Each replicate has an independent deterministic RNG stream; scheduling does not affect draws.
    """
    if B<1 or jobs<1 or min(m,q)<2: raise ValueError('Parámetros inválidos.')
    jobs=min(jobs,cpu_count())
    checkpoint=Path(checkpoint) if checkpoint is not None else None
    if checkpoint is not None and not signature: raise ValueError('Se requiere firma de caché.')
    draws=np.empty((B,len(prepared)),dtype=np.float64); start=0
    if checkpoint is not None and checkpoint.is_file():
        with np.load(checkpoint,allow_pickle=False) as z:
            if str(z['signature'])!=signature: raise ValueError('Caché AUC incompatible; cambiar ruta o desactivar REANUDAR.')
            saved=z['draws']
            if saved.ndim!=2 or saved.shape[1]!=len(prepared) or len(saved)>B or not np.isfinite(saved).all() or not ((saved>=0)&(saved<=1)).all():
                raise ValueError('Caché AUC inválida.')
            start=len(saved); draws[:start]=saved
    def one(b):
        rng=np.random.default_rng(np.random.SeedSequence([seed,b]))
        wp=np.bincount(rng.integers(m,size=m),minlength=m)
        wn=np.bincount(rng.integers(q,size=q),minlength=q)
        return weighted_auc(prepared,wp,wn)
    with threadpool_limits(limits=1), Parallel(n_jobs=jobs,prefer='threads',require='sharedmem') as pool:
        for lo in range(start,B,50):
            hi=min(lo+50,B)
            draws[lo:hi]=pool(delayed(one)(b) for b in range(lo,hi))
            if checkpoint is not None:
                checkpoint.parent.mkdir(parents=True,exist_ok=True)
                tmp=checkpoint.with_suffix('.tmp.npz')
                np.savez_compressed(tmp,signature=signature,draws=draws[:hi])
                tmp.replace(checkpoint)
            if progress: progress(hi,B)
    return draws

def auc_cache_signature(y,P,seed,source_signature):
    h=hashlib.sha256()
    for a in (np.asarray(y),np.asarray(P,dtype=np.float64)):
        h.update(str((a.shape,a.dtype)).encode())
        h.update(np.ascontiguousarray(a).tobytes())
    h.update(str((seed,source_signature,np.__version__)).encode())
    h.update(Path(__file__).read_bytes())
    return h.hexdigest()

def pairwise_auc(y,P,names,B=2000,seed=42,jobs=4,alpha=.05,checkpoint=None,source_signature='',progress=None):
    if len(names)!=np.shape(P)[1] or len(set(names))!=len(names) or not 0<alpha<1:
        raise ValueError('Nombres o alpha inválidos.')
    auc,vp,vn,cov,prepared=prepare_auc(y,P)
    sig=auc_cache_signature(y,P,seed,source_signature)
    draws=bootstrap_auc(prepared,len(vp),len(vn),B,seed,jobs,checkpoint,sig,progress)
    limits=np.quantile(draws,[alpha/2,1-alpha/2],axis=0)
    models=pd.DataFrame(dict(modelo=names,roc_auc=auc,auc_ci_low=limits[0],auc_ci_high=limits[1],
        se_delong=np.sqrt(np.maximum(0,np.diag(cov)))))
    rows=[]
    for i in range(1,len(names)):
        for j in range(i):
            d=float(auc[i]-auc[j])
            # Direct variance of paired placement differences avoids covariance cancellation.
            se=float(np.sqrt(np.var(vp[:,i]-vp[:,j],ddof=1)/len(vp)+np.var(vn[:,i]-vn[:,j],ddof=1)/len(vn)))
            if se==0:
                p=1. if abs(d)<=1e-15 else 0.  # limiting normal test; explicitly flagged
            else:
                p=float(2*norm.sf(abs(d/se)))
            delta=draws[:,i]-draws[:,j]
            low,high=np.quantile(delta,[alpha/2,1-alpha/2])
            # A small roundoff tolerance only for comparison at the exact null boundary.
            pb=(1+np.count_nonzero(np.abs(delta-d)>=abs(d)-1e-15))/(B+1)
            z=norm.isf(alpha/2)
            rows.append(dict(fila=names[i],columna=names[j],delta_auc=d,delta_pp=100*d,
                ci_low=low,ci_high=high,se_delong=se,delong_ci_low=d-z*se,delong_ci_high=d+z*se,
                delong_degenerate=se==0,p_delong=p,p_bootstrap=pb))
    pairs=pd.DataFrame(rows)
    for method in ('delong','bootstrap'):
        bonf,holm=adjust_p(pairs['p_'+method])
        pairs['p_'+method+'_bonferroni']=bonf
        pairs['p_'+method+'_holm']=holm
        pairs['rechazo_'+method+'_holm']=holm<=alpha
    return models,pairs,pd.DataFrame(cov,index=names,columns=names),draws
