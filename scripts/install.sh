#!/bin/bash
set +x
cd ../
if command -v python3 > /dev/null 2>&1; then
    NODE=python3
else
    NODE=python
fi
echo "init venv..."
$NODE -m venv sclat-venv
source sclat-venv/bin/activate
echo "install modules..."
pip install -r requirements.txt
deactivate