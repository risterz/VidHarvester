# PowerShell build script for VidHarvester

$AppName = "VidHarvester"
$Entry = "run.py"

# Check if PyInstaller is available
if (!(Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    python -m pip install -r requirements-dev.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller"
        exit 1
    }
}

# Clean previous builds
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

# Build with PyInstaller
Write-Host "Building $AppName..." -ForegroundColor Green
pyinstaller -p src --noconsole --name $AppName --hidden-import vidharvester --collect-submodules vidharvester --collect-all vidharvester --collect-all requests --collect-all urllib3 --collect-all idna --collect-all charset_normalizer --collect-all certifi $Entry

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build complete. EXE in dist\$AppName\" -ForegroundColor Green
} else {
    Write-Error "Build failed"
    exit 1
}
