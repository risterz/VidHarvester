# VidHarvester (MVP)

A Qt6 desktop app with yt-dlp download engine, a local capture server, simple Chrome/Firefox extensions that forward media URLs, and an optional mitmproxy addon.

## Quick start

1) Create venv and install deps

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run the app

```bash
python run.py
```

Alternative:

```bash
# If you prefer -m, add src to PYTHONPATH
$env:PYTHONPATH = "$(Get-Location)\src"  # PowerShell
python -m vidharvester.app
```

3) Load the browser extension

- Chrome/Edge: load `extensions/chrome` as an unpacked extension.
- Firefox: load `extensions/firefox` as a temporary add-on.

4) Verify capture

- Visit a page with media. The extension will POST to `http://127.0.0.1:8089/capture` and the link will appear in the app's Captured list.

5) Download

- Double-click a captured link or paste a URL. Click "Get Info / Formats" or "Download".
  - Optional: browse a `cookies.txt` (Netscape format) for logged-in downloads.

## Proxy capture (optional)

Install mitmproxy and run:

```bash
mitmproxy -s proxy/mitm_addon.py
```

Configure your browser/system to use the proxy, accept the mitmproxy cert, then browse. Detected media URLs will be forwarded to the app.

In the app (tray icon), you can toggle Capture ON/OFF, which starts/stops mitmproxy (requires `mitmdump` on PATH). When a video is detected, a tray notification appears.

## Notes

- This MVP focuses on core flows; UI polish, database, queue/history, and auto-updates can be added next.
- Only capture/download content you have rights to.
- Pause stops the current job; click Download again to resume (yt-dlp continues partial files).
- Theme: use the menu Theme → Dark/Light to switch; preference is saved.

## Build a Windows EXE

1) Install dev dep:

```powershell
python -m pip install -r requirements-dev.txt
```

2) Run the build script (PowerShell):

```powershell
scripts\build_windows.ps1
```

Or (cmd):

```bat
scripts\build_windows.bat
```

Output: `dist/VidHarvester/VidHarvester.exe`
Optional one-file: `dist/VidHarvester-OneFile.exe`

To include the proxy addon with your release, zip `proxy/mitm_addon.py` alongside the EXE. In a future release, this will be toggled in-app with start/stop.

If you see "No module named 'vidharvester'" when running the EXE, rebuild with the provided scripts (they add `-p src`), or ensure the build command includes `-p src` so the packaged app can import from `src/`.