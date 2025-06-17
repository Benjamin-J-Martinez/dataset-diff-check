@echo off
cd /d "%~dp0"

where streamlit >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Streamlit not found. Checking for pip...
    where pip >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo.
        echo ERROR: pip is not installed. Please install Python and pip first.
        pause
        exit /b 1
    )
    echo Installing requirements...
    pip install -r requirements.txt
)

echo Launching the Dataset Comparison App...
REM Start Streamlit in a new PowerShell process and capture its PID
powershell -Command ^
    "$p = Start-Process streamlit -ArgumentList 'run dataset_comparison_app.py' -PassThru; ^
    Write-Host 'Type exit and press Enter to close the app.'; ^
    while ($true) { ^
        $input = Read-Host; ^
        if ($input -eq 'exit') { ^
            Write-Host 'Shutting down Streamlit...'; ^
            Stop-Process -Id $p.Id; ^
            break ^
        } ^
    }"
