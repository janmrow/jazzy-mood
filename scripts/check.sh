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
LOG_FILE="$(mktemp "${TMPDIR:-/tmp}/jazzy-mood-check.XXXXXX")"

cleanup() {
  status=$?
  if [ -n "${SERVER_PID}" ]; then
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  if [ "${status}" -ne 0 ] && [ -s "${LOG_FILE}" ]; then
    echo "--- server log (${LOG_FILE}) ---"
    cat "${LOG_FILE}" || true
  else
    rm -f "${LOG_FILE}"
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
# Refuse a port that already answers: otherwise the readiness poll below
# could succeed against a stale occupant while our own server fails to
# bind, giving a false-green run against the wrong backend.
if curl -fsS -m 5 "${BASE_URL}/healthz" >/dev/null 2>&1; then
  echo "Port ${PORT} already answers ${BASE_URL}/healthz."
  echo "Stop that server or set PORT to a free one."
  exit 1
fi
# The default uvicorn access format logs the full request line including
# any query string, outside the audited app logger. The app middleware is
# the audited log (route path only, never visitor text), so the access
# log stays off here; production logging lands with the M1-02 image.
python3 -m uvicorn backend.app.main:app --port "${PORT}" --no-access-log >"${LOG_FILE}" 2>&1 &
SERVER_PID=$!

for attempt in $(seq 1 60); do
  if curl -fsS -m 5 "${BASE_URL}/healthz" >/dev/null 2>&1; then
    break
  fi
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "Backend died before becoming ready (port ${PORT})."
    exit 1
  fi
  if [ "${attempt}" -eq 60 ]; then
    echo "Backend did not become ready on ${BASE_URL}/healthz"
    exit 1
  fi
  sleep 0.5
done

# Confirm the ready server is the one we started, not a stale occupant
# that appeared after the pre-flight check. Retry briefly: startup output
# can lag behind the first successful health probe.
if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
  echo "Backend is not running after the readiness check."
  exit 1
fi
confirmed=""
for _ in $(seq 1 20); do
  if grep -q "Uvicorn running on .*:${PORT}" "${LOG_FILE}" 2>/dev/null; then
    confirmed="yes"
    break
  fi
  sleep 0.5
done
if [ -z "${confirmed}" ]; then
  echo "Backend log does not confirm port ${PORT}; refusing a stale server."
  exit 1
fi

(cd frontend && E2E_BASE_URL="${BASE_URL}" npx playwright test)

echo "All checks passed."
