#!/bin/bash

echo "=== Architecture Check ==="
echo "System: $(uname -m)"
echo "Python: $(python3 -c 'import platform; print(platform.machine())')"
echo "=========================="

python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 