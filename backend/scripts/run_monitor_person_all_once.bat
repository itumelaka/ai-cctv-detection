@echo off
setlocal

set "PROJECT_ROOT=C:\Users\burnk\OneDrive\Documents-assets\ai-cctv-detection"
set "BACKEND_DIR=%PROJECT_ROOT%\backend"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "LOG_DIR=%BACKEND_DIR%\data\task-logs"
set "LOG_FILE=%LOG_DIR%\monitor_person_all.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo ================================================== >> "%LOG_FILE%"
echo Run started: %date% %time% >> "%LOG_FILE%"

cd /d "%PROJECT_ROOT%"
"%PYTHON_EXE%" "%BACKEND_DIR%\scripts\monitor_person_all_once.py" >> "%LOG_FILE%" 2>&1

echo Exit code: %ERRORLEVEL% >> "%LOG_FILE%"
echo Run ended: %date% %time% >> "%LOG_FILE%"

endlocal
exit /b 0
