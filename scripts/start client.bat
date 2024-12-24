@echo off
cd ../
where python3 >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    set NODE=python3
) ELSE (
    set NODE=python
)
if exist "sclat-venv" (
    call ..\sclat-venv\Scripts\activate
)
%NODE% sclat/sclat.py --with-play-client %*
deactivate