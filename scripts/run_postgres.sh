#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$PROJECT_DIR/.pgdata"
CONTAINER_NAME="bdf-demo-postgres"
IMAGE="docker.io/library/postgres:16"

mkdir -p "$DATA_DIR"

podman rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

podman run \
  --name "$CONTAINER_NAME" \
  --detach \
  --rm \
  --env POSTGRES_USER=postgres \
  --env POSTGRES_PASSWORD=postgres \
  --env POSTGRES_DB=bdf_demo \
  --publish 5432:5432 \
  --volume "$DATA_DIR:/var/lib/postgresql/data:z" \
  "$IMAGE"
