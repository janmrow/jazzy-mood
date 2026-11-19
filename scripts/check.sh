#!/usr/bin/env bash
# Project check for the M1 first slice (P01, P02, P05, P07).
# Runs pytest, frontend type checking, the production build and the
# essential browser journey against the single-origin backend.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PORT="${PORT:-8000}"
BASE_URL="http://localhost:${PORT}"
SERVER_PID=""

cleanup() {
  if [ -n "${SERVER_PID}" ]; then
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "== pytest =="
python3 -m pytest -q

echo "== frontend typecheck =="
(cd frontend && npm run typecheck)

echo "== frontend build =="
(cd frontend && npm run build)

echo "== browser journey (single origin on ${BASE_URL}) =="
python3 -m uvicorn backend.app.main:app --port "${PORT}" >/tmp/jazzy-mood-check.log 2>&1 &
SERVER_PID=$!

for attempt in $(seq 1 60); do
  if curl -fsS "${BASE_URL}/healthz" >/dev/null 2>&1; then
    break
  fi
  if [ "${attempt}" -eq 60 ]; then
    echo "Backend did not become ready on ${BASE_URL}/healthz"
    cat /tmp/jazzy-mood-check.log || true
    exit 1
  fi
  sleep 0.5
done

(cd frontend && E2E_BASE_URL="${BASE_URL}" npx playwright test)

echo "All checks passed."
