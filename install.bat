where python3 >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    set NODE=python3
) ELSE (
    set NODE=python
)
%NODE% -m venv sclat-venv
call sclat-venv\Scripts\activate
pip install -r requirements.txt
deactivate