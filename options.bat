@echo off
setlocal

REM
set nogui_found=false
for %%a in (%*) do (
    if "%%a"=="--nogui" (
        set nogui_found=true
    )
)

REM
if "%nogui_found%"=="true" (
    python ./nogui.py
) else (
    python ./gui.py
)
endlocal