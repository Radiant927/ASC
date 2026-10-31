# Task1：HPL/HPCG 基准测试与 CPU-GPU 算力对照实验

## 实验目标
在 Snorlax 服务器上完成 HPL 基准跑分；HPCG 的运行段错误已定位并修复（调试代码对空文件指针调用 `fprintf`），64³ 小网格验证输出 VALID；受共享登录节点内存限制，1800 秒正式跑分未完成，完整编译/输入/运行/功耗脚本见 `hpcg/`，需在独立计算节点补跑；同时用稠密矩阵乘法（GEMM）作为代理算例，对比 CPU 与 GPU 浮点算力。

## 环境
- CPU：双路 Intel Xeon Platinum 8352V，共 72 核
- 内存：503 GB
- GPU：NVIDIA L20（46 GB 显存），CUDA 可用
- Python：numpy（CPU, float64）、PyTorch（GPU, float32）

## 文件说明
| 文件 | 说明 |
|------|------|
| `report_task1.md` | 完整实验报告（含 HPL 跑分结果、HPCG 尝试说明、GEMM 对照表） |
| `HPL.dat` | HPL 运行参数文件（N=20000, NB=192, 6×6 进程网格） |
| `hpcg/` | HPCG 编译、输入生成、1800 秒运行与功耗采集脚本（含段错误诊断） |
| `cpu_gemm.py` | CPU 矩阵乘法测速脚本（numpy） |
| `gpu_gemm.py` | GPU 矩阵乘法测速脚本（PyTorch, CUDA） |
| `run_gemm.sh` | 一键运行 CPU+GPU 测速 |

## 运行方式
```bash
# CPU 测速
python cpu_gemm.py

# GPU 测速（指定 0 号卡）
CUDA_VISIBLE_DEVICES=0 python gpu_gemm.py

# 一键跑全部
bash run_gemm.sh
```

## 关键结果
| 设备 | 矩阵规模 | 耗时(s) | GFLOPS |
|------|---------|---------|--------|
| CPU  | 1024×1024 | 0.011 | 198.39 |
| CPU  | 2048×2048 | 0.020 | 863.83 |
| CPU  | 4096×4096 | 0.097 | 1418.70 |
| GPU(L20) | 2048×2048 | 0.002 | 7289.59 |
| GPU(L20) | 4096×4096 | 0.007 | 19151.52 |
| GPU(L20) | 8192×8192 | 0.061 | 17902.23 |

HPL 实测（36 进程，N=20000, NB=192, 6×6 网格）：**883.06 GFLOPS**，残差校验 PASSED。
