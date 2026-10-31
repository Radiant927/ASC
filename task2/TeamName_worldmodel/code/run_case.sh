#!/bin/bash
# 运行 UnifoLM-WMA 官方推理脚本，并归档 output.log 与 mp4
# 用法: bash run_case.sh <repo_dir> <scenario> <case_id> <baseline|optimized> <out_dir>
set -euo pipefail

REPO_DIR=${1:?repo_dir}
SCENARIO=${2:?scenario}
CASE_ID=${3:?case_id}
MODE=${4:?baseline|optimized}
OUT_DIR=${5:?out_dir}

ENTRY="$REPO_DIR/$SCENARIO/$CASE_ID/run_world_model_interaction.sh"
CONFIG=${WORLD_MODEL_CONFIG:-$REPO_DIR/configs/inference/world_model_interaction.yaml}
CONFIG_OPT="${CONFIG%.yaml}_opt.yaml"

if [ ! -f "$ENTRY" ]; then
  echo "error: entry script not found: $ENTRY" >&2
  exit 1
fi
mkdir -p "$OUT_DIR"

BACKUP=""
restore_config() {
  if [ -n "$BACKUP" ] && [ -f "$BACKUP" ]; then
    cp "$BACKUP" "$CONFIG"
    rm -f "$BACKUP"
  fi
}
trap restore_config EXIT

if [ "$MODE" = "optimized" ]; then
  if [ ! -f "$CONFIG_OPT" ]; then
    echo "error: optimized config not found: $CONFIG_OPT" >&2
    echo "run: python prepare_opt_config.py --repo-dir $REPO_DIR" >&2
    exit 1
  fi
  BACKUP=$(mktemp)
  cp "$CONFIG" "$BACKUP"
  cp "$CONFIG_OPT" "$CONFIG"
fi

if [ "$MODE" = "baseline" ]; then
  LOG="$OUT_DIR/baseline.log"
else
  LOG="$OUT_DIR/output.log"
fi

cd "$REPO_DIR"
bash "$ENTRY" 2>&1 | tee "$LOG"

LATEST_VIDEO=$(find "$REPO_DIR/$SCENARIO" -type f -name "*.mp4" -newer "$LOG" 2>/dev/null | sort | tail -n 1)
if [ -z "$LATEST_VIDEO" ]; then
  LATEST_VIDEO=$(find "$REPO_DIR/$SCENARIO" -type f -name "*.mp4" 2>/dev/null | xargs -r ls -t 2>/dev/null | head -n 1)
fi
if [ -n "$LATEST_VIDEO" ]; then
  cp "$LATEST_VIDEO" "$OUT_DIR/0_full_fs6.mp4"
  echo "saved video: $OUT_DIR/0_full_fs6.mp4"
else
  echo "warning: no mp4 produced under $REPO_DIR/$SCENARIO" >&2
fi

echo "saved log: $LOG"
