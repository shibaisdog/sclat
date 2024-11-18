#!/bin/bash
python -m venv sclat-venv
source sclat-venv/bin/activate
pip install -r requirements.txt
deactivate