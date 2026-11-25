"""experiment023: common factorial representation search, fold-local geometry.
No row-level data or predictions may be committed to the public repository.
"""
from pathlib import Path
import hashlib, json, time
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

def configurar(columnas_numericas, columnas_logicas, columnas_categoricas, n_bagging=5):
    global numericas, logicas, categoricas, N_BAGGING
    numericas=list(columnas_numericas)
    logicas=list(columnas_logicas)
    categoricas=list(columnas_categoricas)
    N_BAGGING=int(n_bagging)
    assert N_BAGGING>=2

def matrices_por_split(x_ent, otros):
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
    vecinos=NearestNeighbors(n_neighbors=5).fit(refdb)
    eps=max(float(np.quantile(vecinos.kneighbors(refdb)[0][:,-1],.90)),1e-6)
    db=DBSCAN(eps=eps,min_samples=5).fit(refdb)
    nucleos=refdb[db.core_sample_indices_]
    nn=NearestNeighbors(n_neighbors=1).fit(nucleos) if len(nucleos) else None
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
        return RandomForestClassifier(**parametros,n_estimators=240,n_jobs=-1,random_state=SEMILLA)
    if familia=='CatBoost':
        return CatBoostClassifier(**parametros,iterations=240,task_type='CPU',thread_count=4,verbose=False,
                                  allow_writing_files=False,random_seed=SEMILLA)
    return XGBClassifier(**parametros,n_estimators=240,subsample=.85,colsample_bytree=.85,
                         objective='binary:logistic',eval_metric='logloss',tree_method='hist',
                         device='cpu',n_jobs=4,random_state=SEMILLA)

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


def predicciones_bases(X,y,train_idx,val_idx,elegidos):
    assert not np.intersect1d(train_idx,val_idx).size
    a,b=matrices_por_split(X.iloc[train_idx],[X.iloc[val_idx]])
    columnas=[]
    for familia in FAMILIAS_INDIVIDUALES:
        _,rep,par=elegidos[familia]
        m=nuevo_modelo(familia,par).fit(a[rep],y[train_idx])
        columnas.append(probabilidades(m,b[rep]))
    return np.column_stack(columnas)

def meta_oof(X,y,idx,elegidos,n_splits,seed):
    """OOF de las cuatro bases, entrenadas exclusivamente en índices permitidos."""
    salida=np.full((len(idx),len(FAMILIAS_INDIVIDUALES)),np.nan)
    cv=StratifiedKFold(n_splits=n_splits,shuffle=True,random_state=seed)
    for it,iv in cv.split(idx,y[idx]):
        salida[iv]=predicciones_bases(X,y,idx[it],idx[iv],elegidos)
    assert np.isfinite(salida).all()
    return salida

def cache_stacking(X,y,sub,fold,elegidos):
    # Para cada validación meta, generar OOF solo en meta-train, sin etiquetas meta-val.
    cache=[]
    for j,(it,iv) in enumerate(splits_internos(sub,y,fold)):
        train_idx,val_idx=sub[it],sub[iv]
        mt=meta_oof(X,y,train_idx,elegidos,2,SEMILLA+1000+10*fold+j)
        mv=predicciones_bases(X,y,train_idx,val_idx,elegidos)
        cache.append((mt,mv,y[train_idx],y[val_idx]))
    return cache

def cache_offset(X,y,sub,fold,elegidos):
    _,rep,par=elegidos['Logística']
    cache=[]
    for a,b,yt,yv in cache_interna(X,y,sub,fold):
        lr=nuevo_modelo('Logística',par).fit(a[rep],yt)
        cache.append((a[rep],b[rep],yt,yv,
                      lr.decision_function(a[rep]),lr.decision_function(b[rep])))
    return cache

def buscar_booster(cache,fold,familia,rep,registros,offset=False):
    opciones=[]
    for par in ParameterGrid(GRILLA_BOOSTER):
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
                   SEMILLA,N_BAGGING,GRILLAS_COMUNES)).encode())
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
                    for par in ParameterGrid(GRILLAS_COMUNES[f]):
                        scores=[]
                        for a,b,yt,yv in cache:
                            m=nuevo_modelo(f,par).fit(a[rep],yt)
                            scores.append(roc_auc_score(yv,probabilidades(m,b[rep])))
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
        # Checkpoint per representation so completed ensembles are resumable.
        for s,estado in escenarios.items():
            keys=tuple(nombre(f,s) for f in ENSAMBLES)
            path=directorio/f'ensemble_{s}_fold{fold}_PRIVATE.npz'
            if reanudar and path.exists():
                pred,grid,sel=cargar_fold(path,firma,va,len(X_test),keys)
            else:
                grid=[]; sel=[]; pred={}
                elegidos=estado['elegidos']
                def guardar(f,rep,par,auc,pv,pt):
                    key=nombre(f,s)
                    pred[key]=dict(oof=pv,test=pt)
                    registrar_ganador(sel,fold,key,rep,par,auc,y[va],pv)
                guardar('Promedio de familias',s,{},float('nan'),estado['meta_val'].mean(axis=1),estado['meta_test'].mean(axis=1))
                cache=cache_stacking(X,y,sub,fold,elegidos)
                auc,_,par=buscar_booster(cache,fold,stack,s,grid)
                del cache
                mt=meta_oof(X,y,tr,elegidos,3,SEMILLA+3000+fold)
                m=nuevo_modelo(stack,par).fit(mt,y[tr])
                guardar(stack,s,par,auc,probabilidades(m,estado['meta_val']),probabilidades(m,estado['meta_test']))
                del m,mt
                _,rep_lr,par_lr=elegidos['Logística']
                cache=cache_offset(X,y,sub,fold,elegidos)
                auc,_,par=buscar_booster(cache,fold,offset,s,grid,offset=True)
                del cache
                a,b,c=matrices_por_split(X.iloc[tr],[X.iloc[va],X_test])
                lr=nuevo_modelo('Logística',par_lr).fit(a[rep_lr],y[tr])
                m=nuevo_modelo(offset,par).fit(a[rep_lr],y[tr],base_margin=lr.decision_function(a[rep_lr]))
                pv=m.predict_proba(b[rep_lr],base_margin=lr.decision_function(b[rep_lr]))[:,1]
                pt=m.predict_proba(c[rep_lr],base_margin=lr.decision_function(c[rep_lr]))[:,1]
                guardar(offset,rep_lr,par,auc,pv,pt)
                del lr,m
                _,rep_x,par_x=elegidos['XGBoost']
                pv,pt=bagging_xgb(a[rep_x],b[rep_x],c[rep_x],y[tr],par_x,fold)
                guardar('Bagging XGBoost',rep_x,{**par_x,'n_bootstrap':N_BAGGING},float('nan'),pv,pt)
                del a,b,c
                guardar_fold(path,firma,pred,grid,sel,va)
            combinar_fold(total,pred,va)
            registros.extend(grid); ganadores.extend(sel)
            print('Fold',fold,'ensambles',s,'terminados',flush=True)
    return total,pd.DataFrame(registros),pd.DataFrame(ganadores)

def guardar_agregados(directorio,grid,selected,resultados,y):
    directorio.mkdir(parents=True,exist_ok=True)
    grid.to_csv(directorio/'grid_results.csv',index=False)
    selected.to_csv(directorio/'selected_params.csv',index=False)
    resumen=resumir_predicciones(resultados,y)
    resumen.to_csv(directorio/'summary.csv',index=False)
    return resumen
