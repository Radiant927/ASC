#!/bin/bash
# HPCG 3.0 正式跑分：>=1800 秒，同时采集功耗
# 用法: NP=36 bash run_hpcg.sh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
NP=${NP:-36}
HPCG_BIN=${HPCG_BIN:-}
DAT=${HPCG_DAT:-$SCRIPT_DIR/hpcg.dat}
LOG_DIR=${LOG_DIR:-$SCRIPT_DIR/../logs}
TS=$(date +%Y%m%d_%H%M%S)
LOG="$LOG_DIR/hpcg_NP${NP}_${TS}.log"
POWER_LOG="$LOG_DIR/power_NP${NP}_${TS}.csv"

if [ -z "$HPCG_BIN" ]; then
  HPCG_BIN=$(find "$SCRIPT_DIR/src" -type f -name xhpcg 2>/dev/null | head -n 1 || true)
fi
if [ -z "$HPCG_BIN" ] || [ ! -x "$HPCG_BIN" ]; then
  echo "error: 未找到 xhpcg，请先运行 build_hpcg.sh 或设置 HPCG_BIN" >&2
  exit 1
fi
if [ ! -f "$DAT" ]; then
  echo "error: 未找到输入文件 $DAT，请先运行 gen_hpcg_input.py" >&2
  exit 1
fi

mkdir -p "$LOG_DIR"
WORK=$(mktemp -d)
SAMPLER=""
cleanup() {
  [ -n "$SAMPLER" ] && kill "$SAMPLER" 2>/dev/null || true
  rm -rf "$WORK"
}
trap cleanup EXIT
cp "$DAT" "$WORK/hpcg.dat"

bash "$SCRIPT_DIR/power_sample.sh" "$POWER_LOG" &
SAMPLER=$!

cd "$WORK"
set +e
mpirun -np "$NP" --bind-to core "$HPCG_BIN" 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS[0]}
set -e

kill "$SAMPLER" 2>/dev/null || true
wait "$SAMPLER" 2>/dev/null || true
SAMPLER=""

echo "---- 校验 ----"
if grep -qi "quick path" "$LOG"; then
  echo "FAIL: 日志出现 Quick Path，赛题不允许" >&2
fi
if grep -q "VALID" "$LOG"; then
  echo "PASS: 结果 VALID"
else
  echo "WARN: 日志中未找到 VALID，请检查 $LOG" >&2
fi
echo "日志: $LOG"
echo "功耗采样: $POWER_LOG（GPU 功耗不等于整机功耗，整机请以 IPMI/PDU 为准）"
exit "$STATUS"
