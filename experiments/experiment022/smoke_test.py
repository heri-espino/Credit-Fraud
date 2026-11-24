"""Run from the repository root: python experiments/experiment022/smoke_test.py.
Synthetic data only. Reduces trees and grids AFTER checking the production grid.
"""
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
nb = json.loads((ROOT / "notebook_final_es.ipynb").read_text(encoding="utf-8"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
for i, source in enumerate(cells):
    compile(source, f"notebook-code-{i}", "exec")

def find(prefix):
    return next(s for s in cells if s.startswith(prefix))

ns = {"__name__": "__main__"}
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        exec(find("from __future__"), ns)
        ns["EJECUTAR_PROTOCOLO_COMUN"] = False
        ns["CARGAR_PROTOCOLO_COMUN"] = False
        ns["REUTILIZAR_INDIVIDUALES"] = False
        ns["numericas"] = ["amount_usd", "velocity_score", "merchant_risk_score"]
        ns["logicas"] = ["flag"]
        ns["categoricas"] = ["category"]
        exec(find("from sklearn.model_selection import ParameterGrid"), ns)
        exec(find("def matrices_por_split"), ns)
        exec(find("# Ensambles: cada predicción externa"), ns)
        np, pd = ns["np"], ns["pd"]
        grid = ns["GRILLAS_COMUNES"]
        assert len(ns["ParameterGrid"](grid["XGBoost"])) == 36
        assert grid["Stacking XGBoost"] is grid["XGBoost"]
        assert grid["Logística + XGBoost"] is grid["XGBoost"]
        assert len(ns["CANDIDATOS"]) == 8
        # Smoke: one setting per representation; fit actual model families.
        for g in grid.values():
            for key, values in g.items():
                g[key] = values[:1]
        ns["N_BAGGING"] = 2
        original = ns["nuevo_modelo"]
        def small_model(family, params):
            model = original(family, params)
            if family == "CatBoost":
                model.set_params(iterations=3, thread_count=1)
            elif family != "Logística":
                model.set_params(n_estimators=3, n_jobs=1)
            return model
        ns["nuevo_modelo"] = small_model
        rng = np.random.default_rng(42)
        def data(n):
            x = pd.DataFrame(rng.normal(size=(n, 3)), columns=ns["numericas"])
            x["flag"] = rng.integers(0, 2, n).astype(bool)
            x["category"] = rng.choice(["a", "b", "c"], n)
            return x
        X, Xt = data(240), data(50)
        y = (X.amount_usd + .5 * X.velocity_score + rng.normal(size=len(X)) > 0).astype(int).to_numpy()
        ns["entrenamiento"] = X.assign(id=np.arange(len(X)), is_fraud=y)
        ns["prueba"] = Xt.assign(id=np.arange(len(Xt))+len(X))
        ns["IDENTIFICADOR"] = "id"
        ns["variables"] = X.columns.tolist()
        ns["y"] = y
        base, gr, sel, states = ns["protocolo_individual"](X,y,Xt)
        assert len(gr) == 90 and len(sel) == 20
        directory = Path(tmp) / "checkpoint"
        ns["guardar_individuales"](base,gr,sel,states,directory)
        restored, _, _, restored_states = ns["cargar_individuales"](directory)
        for family in base:
            assert np.array_equal(restored[family]["oof"],base[family]["oof"])
        ens, ge, se = ns["protocolo_ensambles"](X,y,Xt,restored_states)
        assert len(ge) == 10 and len(se) == 20
        assert set(ens) == set(ns["ENSAMBLES"])
        assert np.allclose(ens["Promedio de familias"]["oof"],np.mean([d["oof"] for d in base.values()],axis=0))
        assert np.allclose(ens["Promedio de familias"]["test"],np.mean([d["test"] for d in base.values()],axis=0))
        for d in {**base,**ens}.values():
            assert d["oof"].shape == (len(y),) and d["test"].shape == (len(Xt),)
            for p in d.values():
                assert np.isfinite(p).all() and ((p>=0)&(p<=1)).all()
        assert len(ns["resumir_predicciones"]({**base,**ens},y)) == 8
        exec(find("# Extensión experiment022"), ns)
        variants, vs = ns["protocolo_variantes"](X,y,Xt,gr)
        offsets, gs, osel = ns["protocolo_offset_kmeans"](X,y,Xt,gr)
        assert len(variants)==18 and len(vs)==90
        assert len(offsets)==1 and len(gs)==5 and len(osel)==5
        assert set(osel.representacion)=={"kmeans"}
        extension={**variants,**offsets}
        extdir=Path(tmp)/"extension"
        ns["guardar_extension"](extdir,extension,pd.concat([vs,osel]),gs)
        restored_ext,_,_=ns["cargar_extension"](extdir)
        for family in extension:
            assert np.array_equal(extension[family]["oof"],restored_ext[family]["oof"])
        all_results={**base,**ens,**extension}
        assert len(all_results)==27
        exec(find("def ordenar_top10"), ns)
        ranking=ns["ordenar_top10"](ns["resumir_predicciones"](all_results,y),all_results)
        assert len(ranking)==10 and ranking.roc_auc.is_monotonic_decreasing
        print("PASS: syntax, 36-grid identity, checkpoint, fixed K-means offset, 27 candidates and top 10.")
    finally:
        os.chdir(ROOT)
