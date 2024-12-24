#!/bin/bash
set +x
cd ../
if command -v python3 > /dev/null 2>&1; then
    NODE=python3
else
    NODE=python
fi
if [ -d "sclat-venv" ]; then
    source sclat-venv/bin/activate
fi
$NODE sclat/sclat.py --with-play-client "$@"
deactivate