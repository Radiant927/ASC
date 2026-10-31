# ASC 校内选拔赛

仓库只放两个赛题：

```
ASC/
├── task1/   # HPL / HPCG 与 CPU-GPU 算力对照
└── task2/   # UnifoLM-WMA-0 推理管线 + 官方提交结构
    ├── README.md / report_task2.md
    ├── base_model_inference.py
    ├── run_ablations.sh
    ├── configs/
    └── TeamName_worldmodel/   # code / proposal_file / results
```

## 环境

- 服务器：Snorlax（内网地址已隐去）
- CPU：双路 Xeon Platinum 8352V，72 核
- 内存：503 GB
- GPU：NVIDIA L20（46 GB）
- OS：Ubuntu 22.04
- 编译器：GCC 11.4.0
- MPI：OpenMPI 4.1.2
- BLAS：OpenBLAS

## 入口

- task1：`task1/report_task1.docx`，HPCG 脚本见 `task1/hpcg/`
- task2：`task2/TeamName_worldmodel/`（官方 code / proposal_file / results）
