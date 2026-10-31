# 结果目录

每个 `results/{scenario}/{caseN}/` 需要：

| 文件 | 说明 |
|------|------|
| `0_full_fs6.mp4` | 优化后的完整视频 |
| `output.log` | 优化后运行的终端输出，必须含 `real time` |
| `baseline.log` | 优化前运行的终端输出，含 `real time` |
| `psnr.json` | `psnr_eval.py` 输出，含 `psnr` 字段 |

`summary.json` 由 `gen_summary.py` 生成：

```json
{"scenario": "unitree_z1_dual_arm_stackbox", "case_id": 1,
 "time_before_optim": 606.984, "time_after_optim": 397.532, "psnr": 28.3627}
```

当前 `summary.json` 里的 `null` 表示还没实测，不能直接提交。跑完后重新执行 `gen_summary.py` 覆盖。

赛题要求 20 条记录；本队只做 2 个场景，提交前确认是交 8 条还是补齐其余场景。
