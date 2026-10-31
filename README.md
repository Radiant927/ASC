# ASC 国际大学生超算竞赛实验代码与报告仓库

本仓库包含 ASC 竞赛两道赛题的实验代码、配置与实验报告。task2 当前为 Mock 推理管线验证版本，尚未加载真实模型权重。

## 仓库结构
```
ASC/
├── task1/   # 赛题一：HPL / HPCG 基准测试与 CPU-GPU 算力对照实验
├── task2/   # 赛题二：UnifoLM-WMA-0 世界模型推理优化（DDIM 采样消融）
└── submission/TeamName_worldmodel/   # 赛题二官方提交格式（code / proposal_file / results）
```

## 实验环境
- 服务器：Snorlax 集群（内网地址已隐去）
- GPU：NVIDIA L20（46 GB 显存）
- CPU：双路 Xeon Platinum 8352V，共 72 核
- 内存：503 GB
- 操作系统：Linux (Ubuntu 22.04)
- Python 环境：conda env `unifolm-wma`（Python 3.10, PyTorch + CUDA）

## 各任务入口
- **task1**：HPL 跑分与 CPU/GPU GEMM 对照；HPCG 段错误已定位修复、64³ 验证 VALID，1800 秒正式跑分受共享节点内存限制未完成，脚本见 `task1/hpcg/`，详见 `task1/README.md`
- **task2**：UnifoLM-WMA-0 推理管线验证（Mock 模式，未加载真实权重），详见 `task2/README.md`
- **submission**：按赛题二官方格式组织的代码、结果模板与 DOCX proposal，真实推理需在 Colab/服务器上执行后回填
