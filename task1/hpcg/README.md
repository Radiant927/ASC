# HPCG 3.0 正式跑分脚本

当前状态：HPCG 3.0 编译成功，启动运行时出现段错误，暂未完成 ≥1800 秒正式跑分。脚本保持完整可用，问题修复后可直接补跑。

## 文件

| 文件 | 说明 |
|------|------|
| `build_hpcg.sh` | 拉取 `HPCG-release-3-0-0`，基于 `setup/Make.*` 模板生成 `Make.Linux_MPI` 并编译 |
| `gen_hpcg_input.py` | 生成 `hpcg.dat`（网格尺寸 + 运行时间，默认 1800 秒） |
| `hpcg.dat` | 默认输入：640×640×640，运行 1800 秒 |
| `run_hpcg.sh` | 运行 ≥1800 秒正式测试，日志写入 `../logs/`，同时启动功耗采样 |
| `power_sample.sh` | 周期采集功耗（优先 IPMI，其次 nvidia-smi GPU 总功耗） |

## 补跑步骤

```bash
cd task1/hpcg
bash build_hpcg.sh
python3 gen_hpcg_input.py --n 640 --runtime 1800
NP=36 bash run_hpcg.sh
```

## 注意事项

- 赛题要求 HPCG 3.0、运行时间 ≥1800 秒，且禁止 Quick Path；`hpcg.dat` 第 4 行不能设为 0。
- 功耗必须 < 3 kW。`power_sample.sh` 优先使用 `ipmitool dcmi` 读取整机功耗（可能需要 root 权限）；只有 `nvidia-smi` 时采集的是 GPU 总功耗，不能代表整机功耗，报告中需注明。
- 运行结束后检查日志包含 `VALID`，并将 `../logs/` 下的日志与功耗 CSV 回填到报告。
