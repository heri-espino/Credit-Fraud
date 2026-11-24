# Agent handoff — Credit Fraud, migration of experiment011 sources

## Verified current state
The dedicated repository `heri-espino/Credit-Fraud` originally contained the main modeling notebook, ensemble notebook, experiments 001–005 and an earlier 20/75-slide Spanish presentation. This migration aligns it with the most recent privately distributed work through **experiment011** while preserving the older artifacts as historic versions.

- Latest clean main notebook: 100 cells; CatBoost, XGBoost CUDA fallback, nested parameter grids, OOF evaluation.
- Ensemble extension: 22 cells; cached fold logistic models/predictions, 4 strategies compared with best standalone.
- Paired bootstrap: 12 cells; requires `experiments/experiment010/bootstrap_core.py`, cached OOF predictions and Kaggle labels on the owner's PC.
- Short deck v11: 36 Spanish slides, 21 figures, EDA/PCA and probabilistic target explanation, planned 18.1 minutes.
- Long deck v10: 93 Spanish slides, 51 figures and extensive statistical methodology.
- Latest OOF AUCs: offset XGB .9462047549947218; XGB standalone .9461201492641279; RF stack .9457469470932846; probability blend .9432801044177533; explicit residual .9402409115631302.
- Paired bootstrap (B=600; seed=20261123): offset-minus-fixed-XGB delta 0.0000846057306, 95% CI [-0.0002625875,0.0004397256].
- The tuned `xgb_nested_grid` OOF vector has **not** been provided in the ensemble ZIP; re-run only the bootstrap notebook when it is available from `outputs/all_candidate_predictions.npz`.

## Machine and workflows
Owner reported an idle self-hosted **Windows X64** runner `PCAG103A-15`. A read-only, manually dispatched workflow is installed to lint notebooks, inspect CUDA/Conda and compile presentation outputs when local figure inputs are supplied. No execution of the 699,960-row modeling run is triggered automatically. The runner's working directory is not equivalent to the previously used local project directory; cached model files must be supplied separately if reused in Actions.

## Reproducibility and caveats
The official competition dataset, trained fold binaries and per-transaction predictions are not committed. Existing older executed notebook binary content remains as a historical archive reference. Presentation PDF/HTML in the historic archive reflect **earlier versions**; the current Marp Markdown sources are canonical, and freshly built outputs are workflow artifacts.

The public GitHub repository previously already held competition modeling source. Verify required corresponding Kaggle public Notebook/Discussion publication before further code distribution. Avoid false claims of independent statistical significance; the bootstrap still uses models selected on OOF data. Do not change old experiments or PRs without review.

## Next actions
1. On the Windows workstation, restore `outputs/` from the previous run without deleting local fitted models.
2. Verify `outputs/all_candidate_predictions.npz`, `outputs/ensemble_extension/five_way_oof_and_test_predictions.npz`, the original labeled CSV/ZIP, and optionally the `xgb_nested_grid` OOF column.
3. Run the `paired_bootstrap_comparison.ipynb` only if updated comparisons are required.
4. Use Actions manual workflow with figure directory to compile latest HTML/PDF. Keep generated files as artifacts or use Git LFS/external storage, not ordinary repeated large Git blobs.
5. Record any new analyses as `experiment012`.
