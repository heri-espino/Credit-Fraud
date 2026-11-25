"""experiment024: accelerated factorial representation search, fold-local geometry.
No row-level data or predictions may be committed to the public repository.
"""
from pathlib import Path
import hashlib, json, time, os, warnings, threading, importlib.metadata
from joblib import Parallel, delayed, cpu_count
from threadpoolctl import threadpool_limits
import numpy as np
import pandas as pd
from sklearn.model_selection import ParameterGrid, StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, brier_score_loss

SEMILLA=42
N_BAGGING=5
REPRESENTACIONES=('raw','standardized','raw_kmeans_dbscan','standardized_kmeans_dbscan')
ESCENARIOS=REPRESENTACIONES+('adaptive',)
numericas=[]
logicas=[]
categoricas=[]
CPU_THREADS=1
GRID_JOBS=1
XGB_DEVICE="cpu"
CAT_DEVICE="CPU"
_local=threading.local()

def configurar(columnas_numericas, columnas_logicas, columnas_categoricas, n_bagging=5,
               cpu_jobs=-1, grid_jobs=4, xgb_device='auto', cat_device='auto'):
    """Verify actual accelerator support with small fits; no silent fallback mid-run."""
    global numericas, logicas, categoricas, N_BAGGING, CPU_THREADS, GRID_JOBS, XGB_DEVICE, CAT_DEVICE
    numericas=list(columnas_numericas)
    logicas=list(columnas_logicas)
    categoricas=list(columnas_categoricas)
    N_BAGGING=int(n_bagging)
    assert N_BAGGING>=2
    if cpu_jobs == 0 or cpu_jobs < -1 or grid_jobs < 1:
        raise ValueError('cpu_jobs debe ser -1 o positivo; grid_jobs debe ser positivo.')
    CPU_THREADS=cpu_count() if cpu_jobs==-1 else min(int(cpu_jobs),cpu_count())
    GRID_JOBS=min(int(grid_jobs),CPU_THREADS)
    if xgb_device not in ('auto','cuda','cpu') or cat_device not in ('auto','GPU','CPU'):
        raise ValueError('xgb_device: auto/cuda/cpu; cat_device: auto/GPU/CPU')
    XGB_DEVICE=detectar_xgb(xgb_device)
    CAT_DEVICE=detectar_cat(cat_device)
    print('Hardware:',hardware(),flush=True)

def detectar_xgb(requested):
    if requested=='cpu': return 'cpu'
    from xgboost import XGBClassifier
    x=np.arange(128,dtype=np.float32).reshape(64,2); y=np.tile([0,1],32)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m=XGBClassifier(n_estimators=2,max_depth=2,tree_method='hist',device='cuda',n_jobs=2)
            m.fit(x,y,base_margin=np.zeros(len(y),dtype=np.float32))
            device=json.loads(m.get_booster().save_config())['learner']['generic_param']['device']
            if not device.startswith('cuda'):
                raise RuntimeError('XGBoost no activó CUDA: '+device)
            p=m.predict_proba(x,base_margin=np.zeros(len(y),dtype=np.float32))
            if not np.isfinite(p).all(): raise RuntimeError('Predicciones CUDA no finitas')
        return 'cuda'
    except Exception as exc:
        if requested=='cuda': raise RuntimeError('Prueba CUDA de XGBoost falló') from exc
        print('XGBoost: CUDA no disponible; CPU:',str(exc)[:200],flush=True)
        return 'cpu'

def detectar_cat(requested):
    if requested=='CPU': return 'CPU'
    from catboost import CatBoostClassifier
    x=np.arange(128,dtype=np.float32).reshape(64,2); y=np.tile([0,1],32)
    try:
        m=CatBoostClassifier(iterations=2,depth=2,task_type='GPU',devices='0',
                            thread_count=2,verbose=False,allow_writing_files=False)
        m.fit(x,y)
        if not np.isfinite(m.predict_proba(x)).all(): raise RuntimeError('Predicciones GPU no finitas')
        return 'GPU'
    except Exception as exc:
        if requested=='GPU': raise RuntimeError('Prueba GPU de CatBoost falló') from exc
        print('CatBoost: GPU no disponible; CPU:',str(exc)[:200],flush=True)
        return 'CPU'

def hardware():
    return dict(xgb_device=XGB_DEVICE,catboost_device=CAT_DEVICE,cpu_threads=CPU_THREADS,
                grid_jobs=GRID_JOBS,versions={k:importlib.metadata.version(k) for k in
                ('numpy','pandas','scikit-learn','xgboost','catboost','joblib','threadpoolctl')})

def usa_gpu(familia):
    return CAT_DEVICE=='GPU' if familia=='CatBoost' else (
        familia not in ('Logística','Bosque aleatorio') and XGB_DEVICE=='cuda')

def hilos_modelo():
    return getattr(_local,'threads',CPU_THREADS)

def buscar_configuraciones(familia, params, evaluar, path, firma, reanudar=True):
    """CPU configs concurrently, one GPU fit at a time, atomic progress per batch."""
    params=list(params)
    resultados=[]
    if reanudar and path is not None and path.exists():
        saved=json.loads(path.read_text(encoding='utf8'))
        if saved['firma']!=firma or saved['params']!=params:
            raise ValueError(f'Caché de grilla incompatible: {path}')
        resultados=saved['scores']
        if len(resultados)>len(params) or any(len(s)!=3 or not np.isfinite(s).all() for s in resultados):
            raise ValueError(f'Caché de grilla inválida: {path}')
    jobs=1 if usa_gpu(familia) else min(GRID_JOBS,len(params))
    threads=max(1,CPU_THREADS//jobs)
    # Use shared in-memory fold matrices; avoid copies on Windows (spawn).
    def worker(par):
        _local.threads=threads
        try: return [float(v) for v in evaluar(par)]
        finally: del _local.threads
    # Limit native BLAS independently of explicit estimator threads.
    with threadpool_limits(limits=min(threads,4),user_api='blas'):
        for start in range(len(resultados),len(params),jobs):
            batch=params[start:start+jobs]
            scores=Parallel(n_jobs=jobs,prefer='threads',require='sharedmem')(
                delayed(worker)(par) for par in batch) if jobs>1 else [worker(par) for par in batch]
            resultados.extend(scores)
            if path is not None:
                path.parent.mkdir(parents=True,exist_ok=True)
                tmp=path.with_suffix('.tmp')
                tmp.write_text(json.dumps(dict(firma=firma,params=params,scores=resultados)),encoding='utf8')
                tmp.replace(path)
            print(f'  {familia}: {len(resultados)}/{len(params)} configuraciones',flush=True)
    return list(zip(params,resultados))

def matrices_por_split(x_ent, otros):
    with threadpool_limits(limits=min(CPU_THREADS,8)):
        return _matrices_por_split(x_ent,otros)

def _matrices_por_split(x_ent, otros):
    """Same one-hot columns and standardized geometry in all four conditions."""
    pre=ColumnTransformer([
        ('num',SimpleImputer(strategy='median',keep_empty_features=True),numericas),
        ('bool',SimpleImputer(strategy='most_frequent',keep_empty_features=True),logicas),
        ('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent',keep_empty_features=True)),
                         ('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),categoricas)
    ],sparse_threshold=0)
    def convertir_bool(x):
        return x.assign(**{col:x[col].astype(float) for col in logicas})
    raw=[pre.fit_transform(convertir_bool(x_ent)).astype(np.float32)]
    raw.extend(pre.transform(convertir_bool(x)).astype(np.float32) for x in otros)
    n=len(numericas)
    scaler=StandardScaler().fit(raw[0][:,:n])
    std=[]
    for x in raw:
        z=x.copy()
        z[:,:n]=scaler.transform(x[:,:n])
        std.append(z)
    # PCA is a geometry aid only, not a separate supervised representation.
    rng=np.random.default_rng(SEMILLA)
    ref=std[0][rng.choice(len(std[0]),min(15000,len(std[0])),replace=False)]
    pca=PCA(n_components=.90,svd_solver='full').fit(ref)
    zref=pca.transform(ref)
    km=KMeans(n_clusters=5,n_init=10,random_state=SEMILLA).fit(zref)
    refdb=zref[rng.choice(len(zref),min(2300,len(zref)),replace=False)]
    vecinos=NearestNeighbors(n_neighbors=5,n_jobs=CPU_THREADS).fit(refdb)
    eps=max(float(np.quantile(vecinos.kneighbors(refdb)[0][:,-1],.90)),1e-6)
    db=DBSCAN(eps=eps,min_samples=5,n_jobs=CPU_THREADS).fit(refdb)
    nucleos=refdb[db.core_sample_indices_]
    nn=NearestNeighbors(n_neighbors=1,n_jobs=CPU_THREADS).fit(nucleos) if len(nucleos) else None
    derivados=[]
    for x in std:
        zz=pca.transform(x)
        dk=km.transform(zz)
        dd=nn.kneighbors(zz,return_distance=True)[0] if nn is not None else np.full((len(x),1),2*eps)
        derivados.append(np.c_[dk,dk.min(axis=1),dd,(dd[:,0]>eps).astype(float)].astype(np.float32))
    # Continuous distance columns only; leave binary noise indicator unscaled.
    ds=StandardScaler().fit(derivados[0][:,:-1])
    out=[]
    for a,b,d in zip(raw,std,derivados):
        dstd=d.copy()
        dstd[:,:-1]=ds.transform(d[:,:-1])
        out.append(dict(raw=a,standardized=b,raw_kmeans_dbscan=np.c_[a,d],
                        standardized_kmeans_dbscan=np.c_[b,dstd]))
    return out

GRILLAS_COMUNES = {
    'Logística': {'C':[.01,.1,1.,10.], 'class_weight':[None,'balanced']},
    'Bosque aleatorio': {'max_depth':[12,18,None], 'min_samples_leaf':[5,10,15]},
    'XGBoost': {'max_depth':[3,5,7,10,15,30], 'learning_rate':[.04,.08], 'min_child_weight':[5,10,15]},
    'CatBoost': {'depth':[4,6], 'learning_rate':[.04,.08], 'l2_leaf_reg':[3.,7.]},
}
FAMILIAS_INDIVIDUALES = tuple(GRILLAS_COMUNES)
GRILLA_BOOSTER = GRILLAS_COMUNES['XGBoost']
GRILLAS_COMUNES['Stacking XGBoost'] = GRILLA_BOOSTER
GRILLAS_COMUNES['Logística + XGBoost'] = GRILLA_BOOSTER
ENSAMBLES = ('Promedio de familias','Bagging XGBoost','Stacking XGBoost','Logística + XGBoost')
CANDIDATOS = FAMILIAS_INDIVIDUALES + ENSAMBLES
assert len(ParameterGrid(GRILLA_BOOSTER)) == 36

def nuevo_modelo(familia,parametros):
    from xgboost import XGBClassifier
    from catboost import CatBoostClassifier
    if familia=='Logística':
        return LogisticRegression(**parametros,max_iter=2000,solver='lbfgs',random_state=SEMILLA)
    if familia=='Bosque aleatorio':
        return RandomForestClassifier(**parametros,n_estimators=240,n_jobs=hilos_modelo(),random_state=SEMILLA)
    if familia=='CatBoost':
        return CatBoostClassifier(**parametros,iterations=240,task_type=CAT_DEVICE,thread_count=hilos_modelo(),verbose=False,
                                  **({'devices':'0'} if CAT_DEVICE=='GPU' else {}),
                                  allow_writing_files=False,random_seed=SEMILLA)
    return XGBClassifier(**parametros,n_estimators=240,subsample=.85,colsample_bytree=.85,
                         objective='binary:logistic',eval_metric='logloss',tree_method='hist',
                         device=XGB_DEVICE,n_jobs=hilos_modelo(),random_state=SEMILLA)

def probabilidades(modelo,x):
    return np.asarray(modelo.predict_proba(x)[:,1],dtype=float)

def splits_externos(X,y):
    return list(StratifiedKFold(n_splits=5,shuffle=True,random_state=SEMILLA).split(X,y))

def muestra_interna(tr,y,fold):
    if len(tr)<=36000:
        return tr
    sub,_=train_test_split(tr,train_size=36000,stratify=y[tr],random_state=SEMILLA+fold)
    return sub

def splits_internos(sub,y,fold):
    return list(StratifiedKFold(n_splits=3,shuffle=True,random_state=SEMILLA+100+fold).split(sub,y[sub]))

def cache_interna(X,y,sub,fold):
    cache=[]
    for it,iv in splits_internos(sub,y,fold):
        a,b=matrices_por_split(X.iloc[sub[it]],[X.iloc[sub[iv]]])
        cache.append((a,b,y[sub[it]],y[sub[iv]]))
    return cache

def registro_grilla(registros,fold,familia,rep,par,scores):
    media=float(np.mean(scores))
    registros.append(dict(fold=fold,familia=familia,representacion=rep,parametros=json.dumps(par,sort_keys=True),
                          auc_interna=media,sd_interna=float(np.std(scores))))
    return media

def registrar_ganador(ganadores,fold,familia,rep,par,auc,yv,pv):
    ganadores.append(dict(fold=fold,familia=familia,representacion=rep,parametros=json.dumps(par,sort_keys=True),
                          auc_interna=auc,auc_externa=roc_auc_score(yv,pv)))

def nuevas_predicciones(nombres,n,m):
    return {f:{'oof':np.full(n,np.nan),'test':np.zeros(m)} for f in nombres}

def agregar_prediccion(resultados,f,va,pv,pt):
    assert np.isfinite(pv).all() and np.isfinite(pt).all()
    assert ((pv>=0)&(pv<=1)).all() and ((pt>=0)&(pt<=1)).all()
    resultados[f]['oof'][va]=pv
    resultados[f]['test']+=pt/5

def resumir_predicciones(resultados,y):
    filas=[]
    for f,d in resultados.items():
        p=d['oof']
        assert p.shape==y.shape and np.isfinite(p).all() and np.isfinite(d['test']).all()
        filas.append(dict(familia=f,roc_auc=roc_auc_score(y,p),average_precision=average_precision_score(y,p),
                          log_loss=log_loss(y,p),brier=brier_score_loss(y,p)))
    return pd.DataFrame(filas).sort_values('roc_auc',ascending=False).reset_index(drop=True)


def predicciones_bases_multi(X,y,train_idx,val_idx,escenarios):
    """Fit each distinct family/representation/config once per split; share geometry."""
    assert not np.intersect1d(train_idx,val_idx).size
    a,b=matrices_por_split(X.iloc[train_idx],[X.iloc[val_idx]])
    memo={}; out={}
    for s,elegidos in escenarios.items():
        columnas=[]
        for familia in FAMILIAS_INDIVIDUALES:
            _,rep,par=elegidos[familia]
            key=(familia,rep,json.dumps(par,sort_keys=True))
            if key not in memo:
                m=nuevo_modelo(familia,par).fit(a[rep],y[train_idx])
                memo[key]=probabilidades(m,b[rep])
                del m
            columnas.append(memo[key])
        out[s]=np.column_stack(columnas)
    return out

def meta_oof_multi(X,y,idx,escenarios,n_splits,seed):
    salida={s:np.full((len(idx),len(FAMILIAS_INDIVIDUALES)),np.nan) for s in escenarios}
    cv=StratifiedKFold(n_splits=n_splits,shuffle=True,random_state=seed)
    for it,iv in cv.split(idx,y[idx]):
        for s,p in predicciones_bases_multi(X,y,idx[it],idx[iv],escenarios).items():
            salida[s][iv]=p
    assert all(np.isfinite(p).all() for p in salida.values())
    return salida

def cache_stacking_multi(X,y,sub,fold,escenarios):
    cache={s:[] for s in escenarios}
    for j,(it,iv) in enumerate(splits_internos(sub,y,fold)):
        ti,vi=sub[it],sub[iv]
        mt=meta_oof_multi(X,y,ti,escenarios,2,SEMILLA+1000+10*fold+j)
        mv=predicciones_bases_multi(X,y,ti,vi,escenarios)
        for s in escenarios: cache[s].append((mt[s],mv[s],y[ti],y[vi]))
    return cache

def cache_offset_desde_matrices(cache,elegidos):
    _,rep,par=elegidos['Logística']
    out=[]
    for a,b,yt,yv in cache:
        lr=nuevo_modelo('Logística',par).fit(a[rep],yt)
        out.append((a[rep],b[rep],yt,yv,lr.decision_function(a[rep]),lr.decision_function(b[rep])))
    return out

def buscar_booster(cache,fold,familia,rep,registros,offset=False,path=None,firma=None,reanudar=True):
    def evaluar(par):
        scores=[]
        for paquete in cache:
            a,b,yt,yv=paquete[:4]
            m=nuevo_modelo(familia,par)
            if offset:
                mt,mv=paquete[4:]
                m.fit(a,yt,base_margin=mt)
                pv=m.predict_proba(b,base_margin=mv)[:,1]
            else:
                m.fit(a,yt)
                pv=probabilidades(m,b)
            scores.append(roc_auc_score(yv,pv))
        return scores
    opciones=[]
    for par,scores in buscar_configuraciones(familia,ParameterGrid(GRILLA_BOOSTER),evaluar,path,firma,reanudar):
        auc=registro_grilla(registros,fold,familia,rep,par,scores)
        opciones.append((auc,rep,par))
    return max(opciones,key=lambda q:q[0])

def bagging_xgb(a,b,c,y_train,par,fold):
    """Bootstrap de filas con reemplazo; preprocesador fijo ajustado en el outer train."""
    rng=np.random.default_rng(SEMILLA+2000+fold)
    pv=np.zeros(len(b)); pt=np.zeros(len(c))
    for k in range(N_BAGGING):
        boot=rng.integers(0,len(y_train),size=len(y_train))
        while np.unique(y_train[boot]).size!=2:
            boot=rng.integers(0,len(y_train),size=len(y_train))
        m=nuevo_modelo('XGBoost',par).set_params(random_state=SEMILLA+100*fold+k)
        m.fit(a[boot],y_train[boot])
        pv+=probabilidades(m,b)/N_BAGGING
        pt+=probabilidades(m,c)/N_BAGGING
    return pv,pt



def nombre(familia, escenario):
    return f'{familia} | {escenario}'

def candidatos(familias):
    return tuple(nombre(f,s) for s in ESCENARIOS for f in familias)

def firma_datos(X,y,X_test,train_id,test_id):
    h=hashlib.sha256()
    for obj in (X,pd.Series(y),X_test,pd.Series(train_id),pd.Series(test_id)):
        h.update(pd.util.hash_pandas_object(obj,index=True).to_numpy().tobytes())
    h.update(repr((list(X.columns),list(map(str,X.dtypes)),numericas,logicas,categoricas,
                   SEMILLA,N_BAGGING,GRILLAS_COMUNES,hardware())).encode())
    h.update(Path(__file__).read_bytes())
    return h.hexdigest()

def guardar_fold(path,firma,pred,grid,selected,va,**extra):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp.npz')
    payload={f'{f}__{k}':v for f,d in pred.items() for k,v in d.items()}
    np.savez_compressed(tmp,firma=firma,va=va,grid=json.dumps(grid),
                        selected=json.dumps(selected),**extra,**payload)
    tmp.replace(path)

def cargar_fold(path,firma,va,n_test,nombres):
    with np.load(path,allow_pickle=False) as z:
        if str(z['firma'])!=firma or not np.array_equal(z['va'],va):
            raise ValueError(f'Caché incompatible: {path}. Use otro directorio o elimine la caché.')
        pred={f:{k:z[f'{f}__{k}'] for k in ('oof','test')} for f in nombres}
        for d in pred.values():
            assert d['oof'].shape==(len(va),) and d['test'].shape==(n_test,)
            assert all(np.isfinite(p).all() and ((p>=0)&(p<=1)).all() for p in d.values())
        return pred,json.loads(str(z['grid'])),json.loads(str(z['selected']))

def combinar_fold(total,local,va):
    for f,d in local.items():
        agregar_prediccion(total,f,va,d['oof'],d['test'])

def estado_desde_fold(fold,tr,va,sub,pred,selected):
    escenarios={}
    for s in ESCENARIOS:
        elegidos={}
        for f in FAMILIAS_INDIVIDUALES:
            row=next(q for q in selected if q['familia']==nombre(f,s))
            elegidos[f]=(row['auc_interna'],row['representacion'],json.loads(row['parametros']))
        escenarios[s]=dict(fold=fold,tr=tr,va=va,sub=sub,elegidos=elegidos,
            meta_val=np.column_stack([pred[nombre(f,s)]['oof'] for f in FAMILIAS_INDIVIDUALES]),
            meta_test=np.column_stack([pred[nombre(f,s)]['test'] for f in FAMILIAS_INDIVIDUALES]))
    return escenarios

def protocolo_individual(X,y,X_test,directorio,firma,reanudar=True):
    nombres=candidatos(FAMILIAS_INDIVIDUALES)
    total=nuevas_predicciones(nombres,len(y),len(X_test))
    registros=[]; ganadores=[]; estados=[]
    for fold,(tr,va) in enumerate(splits_externos(X,y),1):
        sub=muestra_interna(tr,y,fold)
        path=directorio/f'individual_fold{fold}_PRIVATE.npz'
        if reanudar and path.exists():
            pred,grid,sel=cargar_fold(path,firma,va,len(X_test),nombres)
        else:
            grid=[]; sel=[]; pred={}; mejores={}
            cache=cache_interna(X,y,sub,fold)
            for f in FAMILIAS_INDIVIDUALES:
                for rep in REPRESENTACIONES:
                    opciones=[]
                    print(f'Fold {fold} · {f} · {rep}',flush=True)
                    def evaluar(par):
                        scores=[]
                        for a,b,yt,yv in cache:
                            m=nuevo_modelo(f,par).fit(a[rep],yt)
                            scores.append(roc_auc_score(yv,probabilidades(m,b[rep])))
                        return scores
                    gp=directorio/'grids'/f'individual_{fold}_{FAMILIAS_INDIVIDUALES.index(f)}_{rep}.json'
                    for par,scores in buscar_configuraciones(f,ParameterGrid(GRILLAS_COMUNES[f]),evaluar,gp,firma,reanudar):
                        auc=registro_grilla(grid,fold,f,rep,par,scores)
                        opciones.append((auc,rep,par))
                    mejores[f,rep]=max(opciones,key=lambda q:q[0])
                print('Fold',fold,f,'mejor representación',max((mejores[f,r] for r in REPRESENTACIONES),key=lambda q:q[0])[:2],flush=True)
            del cache
            a,b,c=matrices_por_split(X.iloc[tr],[X.iloc[va],X_test])
            for f in FAMILIAS_INDIVIDUALES:
                for rep in REPRESENTACIONES:
                    auc,_,par=mejores[f,rep]
                    m=nuevo_modelo(f,par).fit(a[rep],y[tr])
                    pv,pt=probabilidades(m,b[rep]),probabilidades(m,c[rep])
                    key=nombre(f,rep)
                    pred[key]=dict(oof=pv,test=pt)
                    registrar_ganador(sel,fold,key,rep,par,auc,y[va],pv)
                    del m
                auc,rep,par=max((mejores[f,r] for r in REPRESENTACIONES),key=lambda q:q[0])
                key=nombre(f,'adaptive')
                pred[key]=pred[nombre(f,rep)]
                registrar_ganador(sel,fold,key,rep,par,auc,y[va],pred[key]['oof'])
            del a,b,c
            guardar_fold(path,firma,pred,grid,sel,va)
        combinar_fold(total,pred,va)
        estados.append(estado_desde_fold(fold,tr,va,sub,pred,sel))
        registros.extend(grid); ganadores.extend(sel)
    return total,pd.DataFrame(registros),pd.DataFrame(ganadores),estados

def protocolo_ensambles(X,y,X_test,estados,directorio,firma,reanudar=True):
    nombres=candidatos(ENSAMBLES)
    total=nuevas_predicciones(nombres,len(y),len(X_test))
    registros=[]; ganadores=[]
    stack='Stacking XGBoost'; offset='Logística + XGBoost'
    for escenarios in estados:
        fold=escenarios['adaptive']['fold']
        tr,va,sub=(escenarios['adaptive'][k] for k in ('tr','va','sub'))
        assert not np.intersect1d(tr,va).size and np.isin(sub,tr).all()
        pending={}; completed={}
        for s,estado in escenarios.items():
            keys=tuple(nombre(f,s) for f in ENSAMBLES)
            path=directorio/f'ensemble_{s}_fold{fold}_PRIVATE.npz'
            if reanudar and path.exists():
                completed[s]=cargar_fold(path,firma,va,len(X_test),keys)
            else:
                pending[s]=estado['elegidos']
        if pending:
            print(f'Fold {fold}: cross-fitting compartido de {len(pending)} escenarios',flush=True)
            # Every base model is fitted at most once per distinct split/config.
            # Only probability matrices retained, never all full-fold feature matrices.
            sc=cache_stacking_multi(X,y,sub,fold,pending)
            mt=meta_oof_multi(X,y,tr,pending,3,SEMILLA+3000+fold)
            inner=cache_interna(X,y,sub,fold)
            a,b,c=matrices_por_split(X.iloc[tr],[X.iloc[va],X_test])
            offset_memo={}; bag_memo={}
            # Fixed representations are processed before adaptive. Reuse their
            # exact offset/bagging results if the corresponding configuration agrees.
            for s,(pred,grid,sel) in completed.items():
                e=escenarios[s]['elegidos']
                def key(f):
                    _,rep,par=e[f]; return (rep,json.dumps(par,sort_keys=True))
                offset_memo[key('Logística')]=(pred[nombre(offset,s)], [q for q in grid if q['familia']==offset],
                    next(q for q in sel if q['familia']==nombre(offset,s)))
                bag_memo[key('XGBoost')]=(pred[nombre('Bagging XGBoost',s)],
                    next(q for q in sel if q['familia']==nombre('Bagging XGBoost',s)))
            for s,elegidos in pending.items():
                estado=escenarios[s]; grid=[]; sel=[]; pred={}
                def guardar(f,rep,par,auc,pv,pt):
                    key=nombre(f,s)
                    pred[key]=dict(oof=pv,test=pt)
                    registrar_ganador(sel,fold,key,rep,par,auc,y[va],pv)
                print(f'Fold {fold} · ensamble · {s}',flush=True)
                guardar('Promedio de familias',s,{},float('nan'),estado['meta_val'].mean(axis=1),estado['meta_test'].mean(axis=1))
                gp=directorio/'grids'/f'stack_{fold}_{s}.json'
                auc,_,par=buscar_booster(sc[s],fold,stack,s,grid,path=gp,firma=firma,reanudar=reanudar)
                m=nuevo_modelo(stack,par).fit(mt[s],y[tr])
                guardar(stack,s,par,auc,probabilidades(m,estado['meta_val']),probabilidades(m,estado['meta_test']))
                del m
                _,rep_lr,par_lr=elegidos['Logística']
                lk=(rep_lr,json.dumps(par_lr,sort_keys=True))
                if lk in offset_memo:
                    d,rows,row=offset_memo[lk]
                    grid.extend([dict(q,representacion=s) for q in rows])
                    guardar(offset,rep_lr,json.loads(row['parametros']),row['auc_interna'],d['oof'],d['test'])
                else:
                    cache=cache_offset_desde_matrices(inner,elegidos)
                    gp=directorio/'grids'/f'offset_{fold}_{s}.json'
                    auc,_,par=buscar_booster(cache,fold,offset,s,grid,offset=True,path=gp,firma=firma,reanudar=reanudar)
                    del cache
                    lr=nuevo_modelo('Logística',par_lr).fit(a[rep_lr],y[tr])
                    m=nuevo_modelo(offset,par).fit(a[rep_lr],y[tr],base_margin=lr.decision_function(a[rep_lr]))
                    pv=m.predict_proba(b[rep_lr],base_margin=lr.decision_function(b[rep_lr]))[:,1]
                    pt=m.predict_proba(c[rep_lr],base_margin=lr.decision_function(c[rep_lr]))[:,1]
                    guardar(offset,rep_lr,par,auc,pv,pt)
                    offset_memo[lk]=(pred[nombre(offset,s)],[q for q in grid if q['familia']==offset],sel[-1])
                    del lr,m
                _,rep_x,par_x=elegidos['XGBoost']
                xk=(rep_x,json.dumps(par_x,sort_keys=True))
                if xk in bag_memo:
                    d,row=bag_memo[xk]
                    guardar('Bagging XGBoost',rep_x,json.loads(row['parametros']),float('nan'),d['oof'],d['test'])
                else:
                    pv,pt=bagging_xgb(a[rep_x],b[rep_x],c[rep_x],y[tr],par_x,fold)
                    guardar('Bagging XGBoost',rep_x,{**par_x,'n_bootstrap':N_BAGGING},float('nan'),pv,pt)
                    bag_memo[xk]=(pred[nombre('Bagging XGBoost',s)],sel[-1])
                path=directorio/f'ensemble_{s}_fold{fold}_PRIVATE.npz'
                guardar_fold(path,firma,pred,grid,sel,va)
                completed[s]=(pred,grid,sel)
                print('Fold',fold,'ensambles',s,'terminados',flush=True)
            del a,b,c,sc,mt,inner,offset_memo,bag_memo
        for s in escenarios:
            pred,grid,sel=completed[s]
            combinar_fold(total,pred,va)
            registros.extend(grid); ganadores.extend(sel)
    return total,pd.DataFrame(registros),pd.DataFrame(ganadores)

def guardar_agregados(directorio,grid,selected,resultados,y):
    directorio.mkdir(parents=True,exist_ok=True)
    (directorio/'hardware.json').write_text(json.dumps(hardware(),indent=2),encoding='utf8')
    grid.to_csv(directorio/'grid_results.csv',index=False)
    selected.to_csv(directorio/'selected_params.csv',index=False)
    resumen=resumir_predicciones(resultados,y)
    resumen.to_csv(directorio/'summary.csv',index=False)
    return resumen
