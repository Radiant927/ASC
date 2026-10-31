#!/bin/bash
# 构建 HPCG 3.0（GCC + OpenMPI + OpenMP）
# 用法: bash build_hpcg.sh [源码目录]
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC_DIR=${1:-$SCRIPT_DIR/src/hpcg}
VERSION=${HPCG_VERSION:-HPCG-release-3-0-0}

if [ ! -d "$SRC_DIR/.git" ]; then
  mkdir -p "$(dirname "$SRC_DIR")"
  git clone --depth 1 --branch "$VERSION" https://github.com/hpcg-benchmark/hpcg.git "$SRC_DIR"
fi

cd "$SRC_DIR"

TEMPLATE=""
for t in Make.MPI_GCC_OMP Make.MPI_GCC Make.Linux_OpenMPI Make.Linux_MPI; do
  if [ -f "setup/$t" ]; then
    TEMPLATE="setup/$t"
    break
  fi
done
if [ -z "$TEMPLATE" ]; then
  echo "error: 未找到可用的 setup/Make.* 模板，请手动选择" >&2
  ls setup >&2
  exit 1
fi

cp "$TEMPLATE" setup/Make.Linux_MPI
if command -v mpicxx >/dev/null 2>&1; then
  MPI_PREFIX=${MPI_PREFIX:-$(dirname "$(dirname "$(command -v mpicxx)")")}
  sed -i.bak -E \
    -e "s|^MPdir[[:space:]]*=.*|MPdir = ${MPI_PREFIX}|" \
    -e "s|^CXX[[:space:]]*=.*|CXX = mpicxx|" \
    -e "s|^LINKER[[:space:]]*=.*|LINKER = mpicxx|" \
    setup/Make.Linux_MPI
  echo "使用模板 $TEMPLATE，MPI 前缀 $MPI_PREFIX"
fi

mkdir -p build
cd build
../configure Linux_MPI
make -j"$(nproc)"

BIN=$(find "$SRC_DIR" -type f -name xhpcg -perm -u+x | head -n 1)
if [ -z "$BIN" ]; then
  echo "error: 构建结束但未找到 xhpcg" >&2
  exit 1
fi
echo "构建完成：$BIN"
