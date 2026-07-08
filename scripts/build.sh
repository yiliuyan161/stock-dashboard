#!/bin/bash
# Build verification for stock-dashboard
cd "$(dirname "$0")/.."
python3 -c "import ast; ast.parse(open('backend/main.py').read()); print('build OK')"
