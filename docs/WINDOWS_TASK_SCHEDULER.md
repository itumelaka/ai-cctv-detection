
## Multi-Camera Scheduler Update

The original scheduler pilot was created for single-camera monitoring.

The scheduler has now been updated to use the multi-camera hidden VBS launcher:

backend/scripts/run_monitor_person_all_once_hidden.vbs

The VBS launcher runs:

backend/scripts/run_monitor_person_all_once.bat

The BAT launcher runs:

backend/scripts/monitor_person_all_once.py

The Python script checks all enabled cameras from:

backend/config/cameras.json

Runtime log:

backend/data/task-logs/monitor_person_all.log

Exit code meaning:

0 = no person detected
1 = one or more camera checks failed
2 = person detected

The BAT file returns success to Windows Task Scheduler to avoid marking person detection as a task failure.

Current scheduler status:

Disabled intentionally

Enable only when operational testing is ready.

PowerShell commands:

Enable-ScheduledTask -TaskName "ITU AI CCTV Person Monitor"
Disable-ScheduledTask -TaskName "ITU AI CCTV Person Monitor"
Get-ScheduledTask -TaskName "ITU AI CCTV Person Monitor" | Select-Object TaskName, State

## Multi-Camera Scheduler Update

The original scheduler pilot was created for single-camera monitoring.

The scheduler has now been updated to use the multi-camera hidden VBS launcher:

backend/scripts/run_monitor_person_all_once_hidden.vbs

The VBS launcher runs:

backend/scripts/run_monitor_person_all_once.bat

The BAT launcher runs:

backend/scripts/monitor_person_all_once.py

The Python script checks all enabled cameras from:

backend/config/cameras.json

Runtime log:

backend/data/task-logs/monitor_person_all.log

Exit code meaning:

0 = no person detected
1 = one or more camera checks failed
2 = person detected

The BAT file returns success to Windows Task Scheduler to avoid marking person detection as a task failure.

Current scheduler status:

Disabled intentionally

Enable only when operational testing is ready.

PowerShell commands:

Enable-ScheduledTask -TaskName "ITU AI CCTV Person Monitor"
Disable-ScheduledTask -TaskName "ITU AI CCTV Person Monitor"
Get-ScheduledTask -TaskName "ITU AI CCTV Person Monitor" | Select-Object TaskName, State
