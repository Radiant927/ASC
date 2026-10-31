#!/bin/bash
# 采集 HPCG 3.0 段错误诊断信息
# 用法: bash collect_diagnostics.sh [xhpcg路径]
set -uo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HPCG_BIN=${1:-${HPCG_BIN:-}}
LOG_DIR=${LOG_DIR:-$SCRIPT_DIR/../logs}
mkdir -p "$LOG_DIR"
OUT=${OUT:-$LOG_DIR/hpcg_diag_$(date +%Y%m%d_%H%M%S).txt}
exec > >(tee "$OUT") 2>&1

if [ -z "$HPCG_BIN" ]; then
  HPCG_BIN=$(find "$SCRIPT_DIR/src" -type f -name xhpcg -perm -u+x 2>/dev/null | head -n 1)
fi

echo "诊断输出: $OUT"
echo "===== 系统 ====="
uname -a
lscpu | sed -n '1,20p'
free -g

echo "===== 工具链 ====="
gcc --version | head -n 1
mpirun --version | head -n 3
mpicxx -show 2>&1

echo "===== 二进制 ====="
if [ -n "$HPCG_BIN" ] && [ -x "$HPCG_BIN" ]; then
  ls -l "$HPCG_BIN"
  file "$HPCG_BIN"
  ldd "$HPCG_BIN" | grep -Ei "mpi|blas|lapack|gomp|omp" || echo "未链接到 MPI/BLAS 库"
else
  echo "未找到 xhpcg，请传入路径"
fi

echo "===== 构建配置 ====="
if [ -f "$SCRIPT_DIR/src/hpcg/setup/Make.Linux_MPI" ]; then
  grep -E "^(CXX|LINKER|CXXFLAGS|CFLAGS|MPdir|MPinc|MPlib|OPENMP)" "$SCRIPT_DIR/src/hpcg/setup/Make.Linux_MPI"
fi

echo "===== 环境变量 ====="
env | grep -Ei "OMP|MPI|MKL|OPENBLAS|CUDA" || true

echo "===== 输入文件 ====="
cat "${HPCG_DAT:-$SCRIPT_DIR/hpcg.dat}"

echo "===== 资源限制 ====="
ulimit -a

if [ -z "$HPCG_BIN" ] || [ ! -x "$HPCG_BIN" ]; then
  echo "缺少 xhpcg，跳过运行测试"
  exit 0
fi

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
printf 'HPCG benchmark input file\nSandia National Laboratories; University of Tennessee, Knoxville\n64 64 64\n60\n' > hpcg.dat

echo "===== 测试 1：1 进程，OMP_NUM_THREADS=1 ====="
OMP_NUM_THREADS=1 timeout 120 mpirun -np 1 "$HPCG_BIN"
echo "退出码: $?"

echo "===== 测试 2：gdb 回栈（如有 gdb） ====="
if command -v gdb >/dev/null 2>&1; then
  OMP_NUM_THREADS=1 timeout 120 gdb -batch -ex run -ex bt --args "$HPCG_BIN"
  echo "退出码: $?"
else
  echo "未安装 gdb"
fi

echo "===== 测试 3：多进程，OMP_NUM_THREADS=1 ====="
NP=${NP:-4}
OMP_NUM_THREADS=1 timeout 120 mpirun -np "$NP" "$HPCG_BIN"
echo "退出码: $?"

echo "===== 完成 ====="
echo "请把 $OUT 的内容发回分析。"
