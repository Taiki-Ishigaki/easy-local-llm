$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    winget install Ollama.Ollama
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is required for this project. Install Docker Desktop and start it first."
    exit 1
}

docker compose version *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker Compose v2 is required. Install Docker Desktop or enable the Docker Compose plugin."
    exit 1
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker is installed, but the Docker daemon is not reachable. Start Docker Desktop and run this installer again."
    exit 1
}

Set-Location $ProjectRoot

uv sync
ollama pull phi3
docker compose build

Write-Host "Installation complete"
