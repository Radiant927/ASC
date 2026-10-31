# ASC 校内选拔赛 赛题一：HPL / HPCG 性能优化

本仓库提交赛题一的实验代码、配置与实验报告。

## 仓库结构

```
ASC/
└── task1/
    ├── report_task1.md / report_task1.docx   # 实验报告
    ├── HPL.dat                                # HPL 运行参数
    ├── cpu_gemm.py / gpu_gemm.py / run_gemm.sh# CPU-GPU 算力对照实验
    ├── README.md
    └── hpcg/                                  # HPCG 编译、输入、运行、功耗脚本
```

## 实验环境

- 服务器：Snorlax 集群（内网地址已隐去）
- CPU：双路 Intel Xeon Platinum 8352V，共 72 核
- 内存：503 GB
- GPU：NVIDIA L20（46 GB 显存）
- 操作系统：Ubuntu 22.04
- 编译器：GCC 11.4.0
- MPI：OpenMPI 4.1.2
- BLAS：OpenBLAS

## 入口

- 报告：`task1/report_task1.docx`
- HPL：`task1/HPL.dat` + 报告第 2 节
- HPCG：`task1/hpcg/README.md`
- CPU/GPU 对照：`task1/run_gemm.sh`
