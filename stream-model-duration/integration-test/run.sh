#!/usr/bin/env bash
set -euo pipefail

# Ensure we execute relative to script's directory so docker-compose file is found
cd "$(dirname "$0")"

# Load environment variables from .env if present
if [[ -f .env ]]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Ensure EVENT_HUB_CONNECTION_STR is set
if [[ -z "${EVENT_HUB_CONNECTION_STR:-}" ]]; then
  echo "❌ Missing EVENT_HUB_CONNECTION_STR environment variable"
  exit 1
fi

# Optional jitter before start
sleep $(( (RANDOM % 3) + 1 ))

# Bring up model container
echo "🚀 Bringing up model container..."
docker-compose up -d model

# Wait for model readiness
READY_MARKER="Job host started"
MODEL_CONTAINER=$(docker-compose ps -q model)
if [[ -z "$MODEL_CONTAINER" ]]; then
  echo "❌ Failed to find model container" >&2
  exit 1
fi

MAX_WAIT=30
start_time=$(date +%s)
while true; do
  if docker logs "$MODEL_CONTAINER" 2>&1 | grep -q "$READY_MARKER"; then
    echo "✅ Model host is ready."
    break
  fi
  now=$(date +%s)
  if (( now - start_time >= MAX_WAIT )); then
    echo "❌ Timed out waiting for model readiness." >&2
    docker-compose logs model
    exit 1
  fi
  sleep 1
done

# Run docker-based integration tests first
echo "🧪 Running docker-based tests (test_docker.py)..."
if ! python -u test_docker.py 2>&1 | tee test_docker_output.log; then
  echo "❌ test_docker.py failed. See test_docker_output.log" >&2
  exit 1
fi
echo "✅ test_docker.py passed."

# Start listening for predictions BEFORE sending the event
echo "📡 Starting test_kinesis.py listener (waiting for prediction)..."
LOG_FILE="test_kinesis_output.log"
PYTHONUNBUFFERED=1 python -u test_kinesis.py 2>&1 | tee "$LOG_FILE" &
LISTENER_PID=$!

# Wait until listener is actually ready
LISTENING_MARKER="🚀 Waiting for events (exit after first valid one)..."
start_time=$(date +%s)
while true; do
  if grep -q "$LISTENING_MARKER" "$LOG_FILE"; then
    echo "✅ Listener is ready; sending event."
    break
  fi
  now=$(date +%s)
  if (( now - start_time >= 15 )); then
    echo "❌ Timed out waiting for listener readiness." >&2
    kill "$LISTENER_PID" || true
    exit 1
  fi
  sleep 0.5
done

# Send event to ride-input
echo "📤 Sending event to Event Hub: ride-input"
if ! python send_event.py --ride-id 101 --pu 12 --do 45 --distance 8.2; then
  echo "❌ send_event.py failed." >&2
  kill "$LISTENER_PID" || true
  exit 1
fi

# Wait for listener to finish
wait "$LISTENER_PID"
KINESIS_EXIT=$?
if (( KINESIS_EXIT != 0 )); then
  echo "❌ test_kinesis.py exited with code ${KINESIS_EXIT}."
  exit "$KINESIS_EXIT"
fi

# Final confirmation
printf "\n📄 Output captured in %s\n" "$LOG_FILE"
echo "✅ All tests passed successfully!"
echo "🎉 Integration test completed successfully."