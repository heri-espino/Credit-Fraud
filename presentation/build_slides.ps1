# Requires Node.js/npm and a browser supported by @marp-team/marp-cli.
# Run from repository root:
#   pwsh -File .\presentation\build_slides.ps1 -FiguresDirectory 'D:\research\Credit-Fraud\outputs'
param([string]$FiguresDirectory = "")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

$figureOut = Join-Path $root "outputs\figures"
New-Item -ItemType Directory -Force -Path $figureOut | Out-Null
# Use versioned EDA / smoke images only if current full-run versions are absent.
$archives = @(
  "experiments\experiment002\figures",
  "experiments\experiment003\figures",
  "experiments\experiment004\figures_full_train_eda",
  "experiments\experiment004\figures_smoke_models",
  "experiments\experiment005\smoke_figures"
)
foreach ($relative in $archives) {
  $src = Join-Path $root $relative
  if (Test-Path $src) {
    Get-ChildItem -LiteralPath $src -Filter "*.png" -File | ForEach-Object {
      $dst = Join-Path $figureOut $_.Name
      if (-not (Test-Path $dst)) { Copy-Item -LiteralPath $_.FullName -Destination $dst }
    }
  }
}
if ($FiguresDirectory) {
  if (-not (Test-Path -LiteralPath $FiguresDirectory)) {
    throw "Runner cannot access figures directory: $FiguresDirectory"
  }
  $source = (Resolve-Path -LiteralPath $FiguresDirectory).Path
  if ((Split-Path $source -Leaf) -eq 'figures') {
    $source = Split-Path $source -Parent
  }
  $sets = @(
    @{ Rel = "figures"; Dst = "outputs\figures" },
    @{ Rel = "ensemble_extension\figures"; Dst = "outputs\ensemble_extension\figures" },
    @{ Rel = "bootstrap_comparison"; Dst = "outputs\bootstrap_comparison" }
  )
  foreach ($set in $sets) {
    $src = Join-Path $source $set.Rel
    $dst = Join-Path $root $set.Dst
    if (Test-Path -LiteralPath $src) {
      New-Item -ItemType Directory -Force -Path $dst | Out-Null
      Get-ChildItem -LiteralPath $src -Filter "*.png" -File | Copy-Item -Destination $dst -Force
    }
  }
}
# Fail early on missing figures rather than silently exporting broken slides.
$decks = @("presentacion_corta", "presentacion_completa")
$missing = New-Object System.Collections.Generic.List[string]
foreach ($name in $decks) {
  $deck = Join-Path $root "presentation\$name\deck.md"
  $source = Get-Content -Raw -Encoding utf8 -LiteralPath $deck
  foreach ($m in [regex]::Matches($source, 'src=["' + "'" + ']([^"' + "'" + ']+)["' + "'" + ']')) {
    $asset = $m.Groups[1].Value
    if ($asset -match '^(https?:|data:)') { continue }
    $assetPath = [System.IO.Path]::GetFullPath((Join-Path (Split-Path $deck -Parent) $asset))
    if (-not (Test-Path -LiteralPath $assetPath)) {
      $missing.Add("$name -> $asset")
    }
  }
}
if ($missing.Count -gt 0) {
  $missing | ForEach-Object { Write-Warning $_ }
  throw "Missing $($missing.Count) figure assets. Supply the original local outputs/ path using FiguresDirectory."
}
$css = Join-Path $root "presentation\themes\fraud-whitegrid.css"
foreach ($name in $decks) {
  $source = Join-Path $root "presentation\$name\deck.md"
  $out = Join-Path $root "presentation\dist\$name"
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  & npx --yes '@marp-team/marp-cli@4.5.1' $source --theme-set $css --allow-local-files --html --template bespoke -o (Join-Path $out 'slides.html')
  if ($LASTEXITCODE -ne 0) { throw "Marp HTML build failed: $name" }
  & npx --yes '@marp-team/marp-cli@4.5.1' $source --theme-set $css --allow-local-files --html --pdf -o (Join-Path $out 'slides.pdf')
  if ($LASTEXITCODE -ne 0) { throw "Marp PDF build failed: $name" }
}
Write-Host "Done. See presentation\dist for compiled artifacts."
