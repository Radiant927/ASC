# Task2：UnifoLM-WMA-0 推理管线验证

没有模型权重，只验证了推理管线；结果是 Mock，不代表真实性能。

## 文件
| 文件 | 说明 |
|------|------|
| `base_model_inference.py` | Mock 推理脚本 |
| `run_ablations.sh` | 一键跑三组消融 |
| `configs/inference/base_model_inference.yaml` | 占位配置 |
| `report_task2.md` | 实验报告 |

## 运行
```bash
bash run_ablations.sh
```

## 结果
| 组别 | ddim_steps | 总耗时(s) | 单步(ms) | 峰值显存(GB) |
|------|-----------|----------|---------|-------------|
| Baseline | -1 | 0.065 | 0.06 | 0.02 |
| Opt-50 | 50 | 0.133 | 2.67 | 0.01 |
| Opt-20 | 20 | 0.143 | 7.16 | 0.01 |

Mock 模式没有加载模型，数字无参考价值，详见 `report_task2.md`。

官方提交结构见 `TeamName_worldmodel/`。
