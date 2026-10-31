# Task2：UnifoLM-WMA-0 推理管线验证

本次没有加载 UnifoLM-WMA-0 主模型权重，只验证推理管线。所有耗时和显存数据来自 Mock 模式，不是真实性能。

## 环境
- 服务器：Snorlax
- GPU：NVIDIA L20（46 GB，3 号卡）
- 环境：conda `unifolm-wma`，Python 3.10，PyTorch + CUDA
- 数据集：`unitree_z1_dual_arm_stackbox`
- 参数：bs=1，256×416，16 帧，guidance 7.5，ddim_eta=0，seed=42，perframe_ae

## 为什么用 Mock
主模型权重约 22 GB，托管在 HuggingFace。hf-mirror 下载受 Xet 鉴权限制，服务器磁盘也不足，无法先下载再上传。

因此只跑参数解析、采样循环、显存统计和 metrics 落盘，确认链路可用。

## 测试设置
- 基线：`ddim_steps=-1`，框架默认采样
- 优化组：`ddim_steps=50`、`ddim_steps=20`

## 结果
| 组别 | ddim_steps | 总耗时(s) | 单步(ms) | 峰值显存(GB) |
|------|-----------|----------|---------|-------------|
| Baseline | -1 | 0.065 | 0.06 | 0.02 |
| Opt-50 | 50 | 0.133 | 2.67 | 0.01 |
| Opt-20 | 20 | 0.143 | 7.16 | 0.01 |

## 结果说明
Mock 模式没有 UNet 前向，耗时主要来自 Python 调度、日志和指标采集，所以步数越少并不更快，三组数字也没有横向比较意义。显存只有 0.01–0.02 GB，同样是因为没有加载模型权重。

## 结论
1. 推理脚本、配置读取、prompt 路径和 metrics 输出都能正常工作。
2. Mock 数据不能用于性能评估，也不能代替 PSNR。
3. 权重到位后，用相同参数重跑，补真实时延、显存和 PSNR。

## 文件
| 文件 | 说明 |
|------|------|
| `base_model_inference.py` | Mock 推理脚本 |
| `run_ablations.sh` | 跑三组消融 |
| `configs/inference/base_model_inference.yaml` | 占位配置 |
| `report_task2.md` | 本报告 |

正式提交结构见 `../submission/TeamName_worldmodel/`。

## 运行
```bash
bash run_ablations.sh
```
