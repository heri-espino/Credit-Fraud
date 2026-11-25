# Presentation sources (current)

- `presentacion_corta/deck.md`: **Spanish v11** — 36 slides, approximately 18.1 minutes, 21 figure placements. EDA, PCA, probability prediction, 19 candidate models and four ensemble strategies, paired bootstrap.
- `presentacion_completa/deck.md`: **Spanish v10** — 93 slides, 51 figures, including detailed model assumptions and OOF evaluation.
- `themes/fraud-whitegrid.css`: minimal Seaborn `whitegrid` look with formulas sized near body text.

## Build on Windows

```powershell
# Run from repo root on a machine with Node.js and Chrome/Chromium installed.
.\presentation\build_slides.ps1 -FiguresDirectory 'C:\path\to\Credit-Fraud\outputs'
```

The source may reference original generated images in `outputs/figures/`, `outputs/ensemble_extension/figures/` and `outputs/bootstrap_comparison/`. These folders are ignored and normally exist only on your workstation. The script first tries the versioned PNGs in `experiments/`, then copies PNGs from the supplied local directory, checks every image reference, and runs the **official Marp CLI** to build HTML/PDF in `presentation/dist/`. It never retrains any model.

Alternatively use GitHub **Actions → Verify project / build slides → Run workflow**, enable `build_presentations`, and provide the local absolute `outputs/` path visible to the self-hosted runner. The workflow generates a downloadable artifact and does not commit PDFs or touch the previous model outputs.

Earlier HTML/PDF in `presentation/archive/` are historical, not exports of the current sources. The v11 short and v10 long decks were previously exported with an offline renderer; the new workflow uses Marp CLI and may render typography differently. Existing figure labels inside PNGs remain in English by design.
