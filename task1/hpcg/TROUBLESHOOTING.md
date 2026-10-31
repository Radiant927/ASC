# HPCG 段错误排查

## 0. 已定位的根因（本次）

`ComputeSYMGS_ref.cpp` 中混入了一段非官方调试代码：向 `../Matrix_information/A_Matrix_*.txt` 写矩阵。

- 运行目录下没有 `Matrix_information/`，`fopen` 返回 NULL；
- 代码未检查返回值，直接 `fprintf(NULL, "%lf", ...)`，触发 SIGSEGV；
- 与 `sprintf` 缓冲区警告、`_FORTIFY_SOURCE`、栈大小均无关。

处理：备份后删除该调试块（保留 `ComputeSYMGS_ref.cpp.bak`），重新编译即可正常运行。排查时先用 gdb 回栈确认崩溃函数，比猜测编译警告更可靠。

## 1. 先跑一键诊断

```bash
cd task1/hpcg
bash collect_diagnostics.sh /path/to/xhpcg
```

脚本会输出系统信息、`ldd` 链接情况、构建配置、环境变量、资源限制，并依次尝试：1 进程 64³ 小网格、gdb 回栈、4 进程小网格。日志在 `task1/logs/hpcg_diag_*.txt`。

## 2. 最常见原因：OpenMP 线程未限制

36 个 MPI 进程如果各自默认开 72 个 OpenMP 线程，会严重超订并可能直接崩溃。正式跑分务必按核数分配：

```bash
NP=36 OMP_NUM_THREADS=2 bash run_hpcg.sh
# 或者 72 进程
NP=72 OMP_NUM_THREADS=1 bash run_hpcg.sh
```

`run_hpcg.sh` 现在会默认按 `nproc / NP` 自动设置，但显式指定更稳妥。

## 3. 网格过大导致内存分配失败

HPCG 3.0 不检查分配失败，内存不够时会直接段错误。640³ 约需 56 GB；若节点可用内存不足或已有其他进程占用，先缩小网格验证：

```bash
python3 gen_hpcg_input.py --n 320 --runtime 1800 --output hpcg.dat
```

能跑通后再逐步加大。正式跑分要求运行 ≥1800 秒，与网格大小无关。

## 4. 链接了错误的 MPI/BLAS

`ldd xhpcg` 应能看到 OpenMPI 和 OpenBLAS。如果只有 `libmpi` 但编译器不是 `mpicxx`，或混用了 Intel MPI 与 OpenMPI，重新用 `build_hpcg.sh` 构建：

```bash
rm -rf src/hpcg/build
bash build_hpcg.sh
```

## 5. 栈空间不足

```bash
ulimit -s unlimited
```

再运行一次。

## 6. 仍然崩溃

把 `task1/logs/hpcg_diag_*.txt` 完整发回，重点看 gdb 回栈中的函数名（例如 `OptimizeProblem`、`SetupHalo`、`MPI_Init`）。回栈能区分是 MPI 初始化问题、网格分配问题还是计算阶段问题。

## 7. 跑通后回填

确认日志包含 `VALID`、未出现 `Quick Path`、运行时间 ≥1800 秒，再把 `task1/logs/` 下的日志和功耗 CSV 写入报告。
