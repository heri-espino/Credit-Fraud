param(
    [ValidateSet('offline','marp')]
    [string]$Renderer = 'offline'
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if ($Renderer -eq 'marp') {
    npx --yes '@marp-team/marp-cli@4.5.1' '.\deck.md' --theme-set '.\themes\fraud-minimal.css' --allow-local-files --template bespoke --output '.\slides-marp.html'
    npx --yes '@marp-team/marp-cli@4.5.1' '.\deck.md' --theme-set '.\themes\fraud-minimal.css' --allow-local-files --pdf --output '.\slides-marp.pdf'
} else {
    python -m pip install -r '.\requirements-export.txt'
    python '.\build_deck.py'
    python '.\build_pdf.py'
}
