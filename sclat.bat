@echo off
set folderPath=%SCLAT_PATH%
if not defined folderPath (
    echo "Please run the setup.ps1 file."
    exit
)

cd /d "%folderPath%"
python "./options.py" %*