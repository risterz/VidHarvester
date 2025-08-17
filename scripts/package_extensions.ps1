# Package browser extensions and proxy addon for distribution

$DistDir = "dist/extensions"

if (Test-Path $DistDir) {
    Remove-Item -Recurse -Force $DistDir
}

New-Item -ItemType Directory -Force -Path $DistDir

# Copy extensions
Copy-Item -Recurse "extensions/chrome" "$DistDir/"
Copy-Item -Recurse "extensions/firefox" "$DistDir/"

# Copy proxy addon
New-Item -ItemType Directory -Force -Path "$DistDir/proxy"
Copy-Item "proxy/mitm_addon.py" "$DistDir/proxy/"

Write-Host "Extensions packaged in $DistDir" -ForegroundColor Green
