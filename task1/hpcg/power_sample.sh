#!/bin/bash
# 周期采集整机/GPU 功耗，写入 CSV
# 用法: bash power_sample.sh <输出csv>；间隔由 INTERVAL 控制（默认 5 秒）
OUT=${1:?usage: power_sample.sh out.csv}
INTERVAL=${INTERVAL:-5}
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

echo "timestamp,source,watts" > "$OUT"
while true; do
  ts=$(date +%s)
  if command -v ipmitool >/dev/null 2>&1 && ipmitool dcmi power reading >"$TMP" 2>/dev/null; then
    w=$(awk -F: '/Instantaneous power reading/ {gsub(/[^0-9.]/, "", $2); print $2}' "$TMP" | head -n 1)
    [ -n "$w" ] && echo "$ts,ipmi,$w" >> "$OUT"
  elif command -v nvidia-smi >/dev/null 2>&1; then
    w=$(nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits 2>/dev/null | awk '{s+=$1} END {print s}')
    [ -n "$w" ] && [ "$w" != "0" ] && echo "$ts,nvidia-smi-gpu-total,$w" >> "$OUT"
  fi
  sleep "$INTERVAL"
done
