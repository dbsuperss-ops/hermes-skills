---
name: activity-monitor
description: "Setup and run ActivityMonitor — foreground window tracking tray app for Windows"
version: 1.0.0
author: go-seonsaeng
---

# ActivityMonitor

Windows 트레이 상주 앱 — 10초마다 활성 창을 추적하여 JSON 로그 저장.

## 셋업 명령 (최초 1회)

WSL 터미널에서 실행:

```bash
# 1. Windows .NET SDK로 빌드
cd /mnt/c/Users/dbsup/source/repos/ActivityMonitor
/mnt/c/Program\ Files/dotnet/dotnet build -c Release

# 2. 실행 (백그라운드)
powershell.exe -Command "Start-Process -WindowStyle Hidden -FilePath 'C:\Users\dbsup\source\repos\ActivityMonitor\bin\Release\net10.0\ActivityMonitor.exe'"
```

## 확인

```bash
# 로그 폴더 확인
ls -la /mnt/c/Users/dbsup/activity-logs/

# 프로세스 확인
powershell.exe -Command "Get-Process ActivityMonitor -ErrorAction SilentlyContinue | Format-Table Id, ProcessName"
```

## 중지

```bash
powershell.exe -Command "Stop-Process -Name ActivityMonitor -Force"
```

## 자동 시작 등록 (선택)

```bash
powershell.exe -Command @'
$wshell = New-Object -ComObject WScript.Shell
$shortcut = $wshell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\ActivityMonitor.lnk")
$shortcut.TargetPath = "C:\Users\dbsup\source\repos\ActivityMonitor\bin\Release\net10.0\ActivityMonitor.exe"
$shortcut.Save()
'@
```