#!/bin/bash
# 对 2 个场景 × 4 个 case 依次执行 baseline 与 optimized 推理
# 用法: REPO_DIR=/path/to/unifolm-world-model-action RESULTS_DIR=/path/to/results bash run_all.sh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_DIR=${REPO_DIR:?set REPO_DIR to the unifolm-world-model-action clone}
RESULTS_DIR=${RESULTS_DIR:?set RESULTS_DIR to submission results directory}
SCENARIOS=${SCENARIOS:-"unitree_z1_dual_arm_cleanup_pencils,unitree_z1_dual_arm_stackbox"}
CASES=${CASES:-"case1,case2,case3,case4"}

IFS=',' read -ra SCENARIO_LIST <<< "$SCENARIOS"
IFS=',' read -ra CASE_LIST <<< "$CASES"

for scenario in "${SCENARIO_LIST[@]}"; do
  for case_id in "${CASE_LIST[@]}"; do
    out="$RESULTS_DIR/$scenario/$case_id"
    echo "===== $scenario / $case_id : baseline ====="
    bash "$SCRIPT_DIR/run_case.sh" "$REPO_DIR" "$scenario" "$case_id" baseline "$out"
    echo "===== $scenario / $case_id : optimized ====="
    bash "$SCRIPT_DIR/run_case.sh" "$REPO_DIR" "$scenario" "$case_id" optimized "$out"
  done
done

echo "全部推理完成，结果目录：$RESULTS_DIR"
