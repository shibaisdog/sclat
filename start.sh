#!/bin/bash
if command -v python3 > /dev/null 2>&1; then
    NODE=python3
else
    NODE=python
fi
source sclat-venv/bin/activate
$NODE ./main.py "$@"
deactivate