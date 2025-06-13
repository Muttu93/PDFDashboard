[Setup]
AppName=PDF Dashboard
AppVersion=1.0
DefaultDirName={pf}\PDFDashboard
OutputDir=output
OutputBaseFilename=PDFDashboardInstaller
SetupIconFile="dashboard_icon.ico"

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs
Source: "templates\*"; DestDir: "{app}\templates"; Flags: recursesubdirs

[Icons]
Name: "{group}\PDF Dashboard"; Filename: "{app}\app.exe"
