# 结果目录说明

每个 `results/{scenario}/{caseN}/` 需要包含：

| 文件 | 说明 |
|------|------|
| `0_full_fs6.mp4` | 优化后生成的完整视频 |
| `output.log` | 优化后运行的完整终端输出，必须包含 `real time` |
| `baseline.log` | 优化前运行的终端输出，包含 `real time` |
| `psnr.json` | `psnr_eval.py` 输出，至少包含 `psnr` 字段 |

根目录 `summary.json` 由 `gen_summary.py` 生成，每条形如：

```json
{"scenario": "unitree_z1_dual_arm_stackbox", "case_id": 1,
 "time_before_optim": 606.984, "time_after_optim": 397.532, "psnr": 28.3627}
```

当前 `summary.json` 中数值为 `null` 表示尚未实测，**不能作为最终提交版本**。真实跑完后重新执行 `gen_summary.py` 覆盖即可。

注意：赛题原文要求 `summary.json` 覆盖 5 个场景共 20 条；本队只复现 2 个场景，提交前请按当届通知确认是提交 8 条还是补齐其余场景。
