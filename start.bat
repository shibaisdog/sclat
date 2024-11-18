where python3 >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    set NODE=python3
) ELSE (
    set NODE=python
)
call sclat-venv\Scripts\activate
%NODE% ./main.py %*
deactivate