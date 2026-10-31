#!/bin/bash
# 周期采集功耗，写入 CSV
# 用法: bash power_sample.sh <输出csv>；间隔由 INTERVAL 控制（默认 5 秒）
# 优先级：ACPI 功率计（sensors） > IPMI > nvidia-smi GPU 总功耗
set -uo pipefail

OUT=${1:?usage: power_sample.sh out.csv}
INTERVAL=${INTERVAL:-5}

read_power() {
  local line val unit w
  line=$(sensors 2>/dev/null | grep -m1 '^power1:' || true)
  if [ -n "$line" ]; then
    val=$(printf '%s\n' "$line" | sed -E 's/^power1:[[:space:]]*([0-9.]+).*/\1/')
    unit=$(printf '%s\n' "$line" | sed -E 's/^power1:[[:space:]]*[0-9.]+[[:space:]]*([kM]?W).*/\1/')
    if [ "$unit" = "kW" ]; then
      val=$(awk -v v="$val" 'BEGIN{printf "%.1f", v*1000}')
    fi
    echo "$val,acpi-power-meter"
    return 0
  fi

  if command -v ipmitool >/dev/null 2>&1; then
    w=$(ipmitool dcmi power reading 2>/dev/null | awk -F: '/Instantaneous power reading/ {gsub(/[^0-9.]/, "", $2); print $2}' | head -n 1)
    if [ -n "$w" ]; then
      echo "$w,ipmi"
      return 0
    fi
  fi

  if command -v nvidia-smi >/dev/null 2>&1; then
    w=$(nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits 2>/dev/null | awk '{s+=$1} END {print s}')
    if [ -n "$w" ] && [ "$w" != "0" ]; then
      echo "$w,nvidia-smi-gpu-total"
      return 0
    fi
  fi

  return 1
}

echo "timestamp,source,watts" > "$OUT"
while true; do
  ts=$(date +%s)
  reading=$(read_power || true)
  if [ -n "$reading" ]; then
    echo "$ts,${reading#*,},${reading%,*}" >> "$OUT"
  fi
  sleep "$INTERVAL"
done
