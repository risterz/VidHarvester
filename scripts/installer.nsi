; NSIS Installer Script for VidHarvester
!define APPNAME "VidHarvester"
!define COMPANYNAME "VidHarvester Team"
!define DESCRIPTION "Video downloading application"
!define VERSIONMAJOR 0
!define VERSIONMINOR 1
!define VERSIONBUILD 0
!define HELPURL "https://github.com/risterz/VidHarvester"
!define UPDATEURL "https://github.com/risterz/VidHarvester/releases"
!define ABOUTURL "https://github.com/risterz/VidHarvester"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"
Name "${APPNAME}"
OutFile "${APPNAME}-Setup-${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.exe"

Page directory
Page instfiles

Section "install"
    SetOutPath $INSTDIR
    File /r "dist\${APPNAME}\*"
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    CreateShortCut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
SectionEnd

Section "uninstall"
    Delete "$SMPROGRAMS\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir /r $INSTDIR
SectionEnd
