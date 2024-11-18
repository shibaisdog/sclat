#!/bin/bash
if command -v python3 > /dev/null 2>&1; then
    NODE=python3
else
    NODE=python
fi
$NODE -m venv sclat-venv
source sclat-venv/bin/activate
pip install -r requirements.txt
deactivate