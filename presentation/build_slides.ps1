# Build current Marp sources. Optional -FiguresDirectory: report ZIP or extracted folder.
param([string]$FiguresDirectory = "")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
if ($FiguresDirectory) {
  & python presentation/import_experiment024.py $FiguresDirectory
  if ($LASTEXITCODE -ne 0) { throw "No se pudo importar el informe experiment024." }
}
$css = Join-Path $root "presentation\themes\fraud-final-es.css"
foreach ($name in @("presentacion_corta", "presentacion_completa")) {
  $source = Join-Path $root "presentation\$name\deck.md"
  $content = Get-Content -LiteralPath $source -Raw -Encoding utf8
  foreach ($m in [regex]::Matches($content, 'src="([^"]+)"')) {
    $asset = [System.IO.Path]::GetFullPath((Join-Path (Split-Path $source -Parent) $m.Groups[1].Value))
    if (-not (Test-Path -LiteralPath $asset)) { throw "Falta $asset. Use -FiguresDirectory con el ZIP de experiment024." }
  }
  $out = Join-Path $root "presentation\dist\$name"
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  & npx --yes '@marp-team/marp-cli@4.5.1' $source --theme-set $css --allow-local-files --html --template bespoke -o (Join-Path $out 'slides.html')
  if ($LASTEXITCODE -ne 0) { throw "Marp HTML build failed: $name" }
  & npx --yes '@marp-team/marp-cli@4.5.1' $source --theme-set $css --allow-local-files --html --pdf -o (Join-Path $out 'slides.pdf')
  if ($LASTEXITCODE -ne 0) { throw "Marp PDF build failed: $name" }
}
Write-Host "Listo: presentation\dist"
