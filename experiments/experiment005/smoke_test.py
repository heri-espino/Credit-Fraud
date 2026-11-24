from pathlib import Path
import os, sys, nbformat, traceback, time
root=Path(__file__).resolve().parents[2]
work=root/'outputs'/'experiment005_smoke'
work.mkdir(exist_ok=True)
zip_path=work/'playground-series-s6e11.zip'
if not (root/'playground-series-s6e11.zip').exists():
    raise FileNotFoundError('Place playground-series-s6e11.zip beside credit_card_fraud.ipynb first.')
if not zip_path.exists():
    # Use a symlink when permitted; on Windows without Developer Mode use a file copy.
    try:
        zip_path.symlink_to(root/'playground-series-s6e11.zip')
    except (OSError, NotImplementedError):
        import shutil
        shutil.copy2(root/'playground-series-s6e11.zip', zip_path)
os.chdir(work)
nb=nbformat.read(root/'credit_card_fraud.ipynb',as_version=4)
state={'__name__':'__main__'}
def run(name,match,modifier=None):
    cell=next(c for c in nb.cells if c.cell_type=='code' and match in c.source)
    src=cell.source
    if modifier:src=modifier(src)
    print('START',name,flush=True)
    started=time.time()
    exec(compile(src,name,'exec'),state)
    print('DONE',name,round(time.time()-started,2),flush=True)

def conf(src):
    for a,b in [('FAST_DEV_RUN = False','FAST_DEV_RUN = True'),
                ('DEV_SAMPLE_SIZE = 15_000','DEV_SAMPLE_SIZE = 3_000'),
                ('N_JOBS = -1  # Internal','N_JOBS = 3  # Internal'),
                ('SAVE_FOLD_MODELS = True  # Persist','SAVE_FOLD_MODELS = False  # Persist'),
                ('RUN_PDP = True  # One','RUN_PDP = False  # One'),
                ('GRID_SEARCH_DEV_ROWS = 2_000','GRID_SEARCH_DEV_ROWS = 1_200'),
                ('ANOMALY_SAMPLE_SIZE = 30_000','ANOMALY_SAMPLE_SIZE = 800')]:
        assert a in src,a
        src=src.replace(a,b)
    return src
run('setup','from __future__ import annotations',conf)
run('data','DATA_DIRS = [')
# set X_test after model data setup
run('models','class CatBoostNativePreprocessor',lambda src:src+'\nX_test=X_test.iloc[:200].copy()\n')
# for fair evaluation retain 5 outer folds
run('search configuration','XGB_SEARCH_BASE =')
run('CV configuration','def classification_metrics(')
state['specs']=[sp for sp in state['specs'] if sp['name'] in ['logit_C1','xgb_depth3_lr08','catboost_depth5_lr06','xgb_nested_grid','catboost_nested_grid']]
assert len(state['specs'])==5,state['specs']
print('smoke specs:',[sp['name'] for sp in state['specs']],flush=True)
for sp in state['specs']:
    try:
        r=state['evaluate_candidate'](sp)
        print('COMPLETE',sp['name'],round(r['roc_auc'],5),flush=True)
    except Exception as e:
        print('ERROR',sp,e,flush=True);traceback.print_exc();raise
# replicate result globals for core plot and grid plots
state['leaderboard']=state['pd'].DataFrame(state['candidate_records']).sort_values('roc_auc',ascending=False).reset_index(drop=True)
state['fold_scores']=state['pd'].DataFrame(state['fold_records'])
state['best_each_family']=(state['leaderboard'].sort_values('roc_auc',ascending=False).drop_duplicates('family')['candidate'].tolist())
# Running the new grid plots verifies end-to-end plotting with trained objects.
run('grid figures','if GRID_RESULTS:')
print('FINISHED',state['leaderboard'][['candidate','roc_auc','average_precision']].to_string(index=False),flush=True)
