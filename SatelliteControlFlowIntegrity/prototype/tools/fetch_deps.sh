#!/usr/bin/env bash
# Fetch the FreeRTOS kernel used by the flight software.
# Pinned so the measurements in docs/05-evaluation.md stay reproducible.
set -euo pipefail

KERNEL_TAG="V11.1.0"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HERE/firmware/third_party/FreeRTOS-Kernel"

if [ -d "$DEST" ]; then
  echo "FreeRTOS kernel already present at $DEST"
  exit 0
fi

mkdir -p "$(dirname "$DEST")"
git clone --depth 1 --branch "$KERNEL_TAG" \
  https://github.com/FreeRTOS/FreeRTOS-Kernel.git "$DEST"
rm -rf "$DEST/.git"
echo "FreeRTOS kernel $KERNEL_TAG fetched to $DEST"
