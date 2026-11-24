import nbformat, os
from pathlib import Path
nb=nbformat.read(str(Path(__file__).resolve().parents[2] / 'credit_card_fraud.ipynb'),as_version=4)
ns={'__name__':'__main__'}
def run_match(contains):
 for i,c in enumerate(nb.cells):
  if c.cell_type=='code' and contains in c.source:
   print('EXEC CELL',i,contains,flush=True)
   exec(compile(c.source,f'cell_{i}','exec'),ns)
   return
 raise RuntimeError(contains)
run_match('RANDOM_STATE = 42')
ns['OUTPUT_DIR']=Path(str(Path(__file__).resolve().parent / 'rerun_outputs')); ns['OUTPUT_DIR'].mkdir(exist_ok=True)
ns['FIGURE_DIR']=ns['OUTPUT_DIR']/'figures'; ns['FIGURE_DIR'].mkdir(exist_ok=True)
ns['FAST_DEV_RUN']=True
ns['DEV_SAMPLE_SIZE']=6000
ns['N_JOBS']=2
ns['SAVE_FOLD_MODELS']=False
os.chdir(str(Path(__file__).resolve().parents[2]))
run_match('train_full = read_competition_csv')
run_match('class LogisticOffsetXGBClassifier')
print('available model candidates:',[(s['name'],s['params']) for s in ns['specs'] if 'offset_xgb' in s['name']],flush=True)
ns['specs']=[s for s in ns['specs'] if s['name'] in ['logit_C1','offset_xgb_depth2_lr05','offset_xgb_depth3_lr05','xgb_depth3_lr08']]
run_match('def evaluate_candidate')
for s in ns['specs']:
 r=ns['evaluate_candidate'](s)
 print('SCORES',s['name'], {k:round(r[k],5) for k in ['roc_auc','average_precision','log_loss','brier']},flush=True)
ns['leaderboard']=ns['pd'].DataFrame(ns['candidate_records']).sort_values('roc_auc',ascending=False)
ns['fold_scores']=ns['pd'].DataFrame(ns['fold_records'])
run_match('fixed_comparison = [name for name in')
for name in ['offset_xgb_depth2_lr05','offset_xgb_depth3_lr05']:
 d=ns['np'].load(ns['OUTPUT_DIR']/f'{name}_components_oof.npz')
 assert {'baseline_prob','correction_logit','corrected_prob'}<=set(d.files)
 assert (d['baseline_prob']>=0).all() and (d['baseline_prob']<=1).all()
 assert ns['np'].abs(d['correction_logit']).mean() > 0
 assert ns['np'].isfinite(d['correction_logit']).all()
 print('CORRECTION',name, 'mean absolute logit correction',float(ns['np'].abs(d['correction_logit']).mean()))
print('TEST_PASSED',flush=True)
