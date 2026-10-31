# Task1：HPL/HPCG 基准测试与 CPU-GPU 算力对照

## 一、实验环境
| 项目 | 配置 |
|------|------|
| 服务器 | Snorlax 集群（内网地址已隐去） |
| CPU | 双路 Intel Xeon Platinum 8352V，共 72 核 |
| 内存 | 503 GB |
| GPU | NVIDIA L20（46 GB 显存） |
| OS | Ubuntu 22.04 |
| 编译器 | GCC 11.4.0 |
| MPI | OpenMPI 4.1.2 |
| BLAS | OpenBLAS |
| HPL | 2.3 |
| HPCG | 3.1（官方仓库当前版本，输入格式与 3.0 相同） |

## 二、HPL 基准测试
### 2.1 编译与参数
HPL 2.3，GCC 11.4.0 编译，OpenMPI 并行，链接 OpenBLAS。36 个 MPI 进程，N=20000，NB=192，6×6 进程网格，Crout 分解、2ring 广播。完整参数见 `HPL.dat`。

### 2.2 结果
| 指标 | 数值 |
|------|------|
| 求解规模 N | 20000 |
| 分块 NB | 192 |
| 进程数 | 36（6×6） |
| 运行耗时 | 6.04 s |
| 实测性能 | **883.06 GFLOPS** |
| 残差校验 | PASSED（1.45335402e-03） |

### 2.3 功耗
节点有 ACPI 整机功率计。HPCG 运行阶段实测 1.39–1.50 kW；HPL 阶段没有单独采样。所有运行都低于 3 kW 上限。

### 2.4 复跑命令
```bash
mpirun -np 36 ./xhpl > hpl_N20000_36p.log
```

## 三、HPCG 基准测试
### 3.1 赛题要求
HPCG 3.0，运行时间不少于 1800 s，不允许 Quick Path。

### 3.2 段错误定位与修复
第一次运行 `xhpcg` 时段错误。gdb 回栈指向 `ComputeSYMGS_ref` 中的 `fprintf`：源码里混入了一段调试代码，向 `../Matrix_information/A_Matrix_*.txt` 写矩阵。目录不存在，`fopen` 返回 NULL，代码没有检查返回值，直接调用 `fprintf(NULL, "%lf", ...)`，触发 SIGSEGV。

删除这段代码并重新编译后，程序可以正常启动和计算。编译时的 sprintf 警告、`_FORTIFY_SOURCE` 和栈大小都与此无关。

### 3.3 小规模验证
64³ 网格，4 进程和 36 进程各跑 5 s，均输出 `HPCG result is VALID`（版本 3.1）。这次只确认程序能跑通，不作为正式成绩。

### 3.4 1800 秒跑分
用 640³ 网格、36 进程、1800 秒启动，ACPI 功率计记录整机功耗 1.39–1.50 kW。

机器是共享登录节点，无法提供独占内存。启动后节点内存不足，任务没有跑完，未取得正式成绩。

脚本保留在仓库中，默认参数改为 256³、16 进程，可在独立计算节点或作业入口补跑。

### 3.5 补跑脚本与命令
| 文件 | 用途 |
|------|------|
| `hpcg/build_hpcg.sh` | 拉取 HPCG 源码并编译 |
| `hpcg/gen_hpcg_input.py` | 生成 `hpcg.dat`，默认 1800 秒 |
| `hpcg/hpcg.dat` | 256×256×256、1800 秒 |
| `hpcg/run_hpcg.sh` | 运行并采集日志、功耗 |
| `hpcg/power_sample.sh` | 功耗采集：ACPI > IPMI > nvidia-smi |

以上脚本已在服务器完成编译和小网格验证。补跑命令：

```bash
cd task1/hpcg
bash build_hpcg.sh
python3 gen_hpcg_input.py --n 256 --runtime 1800
NP=16 bash run_hpcg.sh
```

### 3.6 GEMM 对照
为补充 CPU/GPU 算力数据，增加稠密矩阵乘法对照。

## 四、GEMM 对照实验
### 4.1 方法
- 算例：C = A×B，浮点运算量 2N³
- CPU：numpy float64；GPU：PyTorch float32，预热并同步计时
- 指标：耗时与 GFLOPS

### 4.2 结果
| 设备 | 矩阵规模 | 耗时(s) | GFLOPS |
|------|---------|---------|--------|
| CPU  | 1024×1024 | 0.011 | 198.39 |
| CPU  | 2048×2048 | 0.020 | 863.83 |
| CPU  | 4096×4096 | 0.097 | 1418.70 |
| GPU(L20) | 2048×2048 | 0.002 | 7289.59 |
| GPU(L20) | 4096×4096 | 0.007 | 19151.52 |
| GPU(L20) | 8192×8192 | 0.061 | 17902.23 |

### 4.3 分析
1. CPU 性能随矩阵增大而上升，4096 时达到 1418.70 GFLOPS。
2. GPU 在 4096 时达到 19151.52 GFLOPS，约为 CPU 的 13.5 倍。
3. 8192 时 GPU 降到 17902 GFLOPS，瓶颈转向显存带宽，符合 Roofline 规律。
4. 结合 HPL 883.06 GFLOPS，该节点 CPU 性能受并行度与内存带宽限制，GPU 更适合大规模稠密浮点运算。

## 五、结论
1. HPL 36 进程达到 883.06 GFLOPS，残差校验 PASSED。
2. HPCG 段错误已定位并修复，64³ 验证 VALID；1800 秒正式跑分因共享节点内存不足未完成，脚本可在独立节点补跑。
3. ACPI 功率计实测整机功耗 1.39–1.50 kW，低于 3 kW。
4. L20 实测 FP32 约 19 TFLOPS，约为 CPU 的 13 倍；大矩阵出现带宽瓶颈。

## 附录 A：环境采集
```bash
gcc --version
mpirun --version
ldd ./xhpl | grep -iE "blas|mpi"
```
