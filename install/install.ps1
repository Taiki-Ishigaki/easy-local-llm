$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    winget install Ollama.Ollama
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
}

Set-Location $ProjectRoot

uv sync
ollama pull phi3
docker compose build

Write-Host "Installation complete"
