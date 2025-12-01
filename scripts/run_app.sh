#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
APP_MODULE="app.main:app"
HOST="0.0.0.0"
PORT="8000"

if [[ ! -d "$VENV_DIR" ]]; then
  python -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if ! python -c "import fastapi" >/dev/null 2>&1; then
  pip install -e .[dev]
fi

exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --reload

