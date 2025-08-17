@echo off
setlocal enabledelayedexpansion

set APP_NAME=VidHarvester
set ENTRY=run.py

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
  echo Installing PyInstaller...
  python -m pip install -r requirements-dev.txt || goto :error
)

if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

pyinstaller -p src --noconsole --name "%APP_NAME%" --hidden-import vidharvester --collect-submodules vidharvester --collect-all vidharvester --collect-all requests --collect-all urllib3 --collect-all idna --collect-all charset_normalizer --collect-all certifi "%ENTRY%"
if %errorlevel% neq 0 goto :error

echo Build complete. EXE in dist\%APP_NAME%\
exit /b 0

:error
echo Build failed.
exit /b 1
