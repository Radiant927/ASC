# Task2：UnifoLM-WMA-0 世界模型推理优化实验

## 实验目标
基于 UnifoLM-WMA-0 世界模型动作框架，以 Unitree Z1 双臂堆叠方块任务为场景，探究 DDIM 采样步数对视频生成推理时延与 GPU 显存占用的影响，在保证生成质量前提下降低推理耗时、节约显存。

## 环境
- 服务器：Snorlax
- GPU：NVIDIA L20（46 GB，通过 `CUDA_VISIBLE_DEVICES=3` 使用 3 号卡）
- Conda 环境：`unifolm-wma`（Python 3.10, PyTorch + CUDA）
- 测试数据集：`unitree_z1_dual_arm_stackbox`

## 环境约束
UnifoLM-WMA-0 主干权重（约 22 GB）托管于 HuggingFace，hf-mirror 镜像存在 Xet 存储鉴权限制无法下载；本地磁盘不足无法中转上传。因此本实验采用 **Mock 推理方案**，验证整套推理脚本、参数配置、指标采集链路的正确性。

## 文件说明
| 文件 | 说明 |
|------|------|
| `report_task2.md` | 完整实验报告 |
| `base_model_inference.py` | Mock 推理主脚本（参数解析 + 计时 + 显存统计 + 输出 metrics.json） |
| `run_ablations.sh` | 一键运行三组 DDIM 消融实验 |
| `configs/inference/base_model_inference.yaml` | 占位配置文件 |

## 运行方式
```bash
# 一键跑三组消融
bash run_ablations.sh

# 或单独跑某一组
python base_model_inference.py \
  --savedir ./out_baseline \
  --config configs/inference/base_model_inference.yaml \
  --prompt_dir examples/prompts/unitree_z1_dual_arm_stackbox \
  --ddim_steps -1 --ddim_eta 0.0 --bs 1 \
  --height 256 --width 416 \
  --unconditional_guidance_scale 7.5 --seed 42 \
  --video_length 16 --perframe_ae
```

## 实验结果
| 组别 | ddim_steps | 总耗时(s) | 单步(ms) | 峰值显存(GB) |
|------|-----------|----------|---------|-------------|
| Baseline | -1 | 0.065 | 0.06 | 0.02 |
| Opt-50 | 50 | 0.133 | 2.67 | 0.01 |
| Opt-20 | 20 | 0.143 | 7.16 | 0.01 |

详见 `report_task2.md`。

> 正式提交版本（官方目录结构、Colab notebook、PSNR 评估与 proposal）见 `../submission/TeamName_worldmodel/`。
