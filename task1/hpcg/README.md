# HPCG 跑分脚本（3.1，兼容 3.0）

## 当前状态

- 运行段错误已定位并修复：源码中混入的调试代码向不存在的 `../Matrix_information/` 写矩阵，`fopen` 返回 NULL 后被直接传给 `fprintf`；删除该代码后程序正常。
- 64³ 网格 4 进程 / 36 进程均输出 `HPCG result is VALID`，报告版本 3.1。
- 640³、36 进程、1800 秒正式跑分在共享登录节点上因可用内存不足未能完整执行；输入、运行和功耗脚本都已保留，可在独立计算节点补跑。

## 文件

| 文件 | 说明 |
|------|------|
| `build_hpcg.sh` | 拉取并编译 HPCG；可用 `HPCG_VERSION=HPCG-release-3-1-0` 指定 3.1 |
| `gen_hpcg_input.py` | 生成 `hpcg.dat`；默认 256³、1800 秒，`--n 0` 按内存估算 |
| `hpcg.dat` | 默认安全输入：256×256×256，1800 秒 |
| `run_hpcg.sh` | 运行 ≥1800 秒测试，日志写入 `../logs/`，同时启动功耗采样 |
| `power_sample.sh` | 功耗采集：ACPI 功率计 > IPMI > nvidia-smi |

## 补跑步骤

```bash
cd task1/hpcg
bash build_hpcg.sh
python3 gen_hpcg_input.py --n 256 --runtime 1800
NP=16 bash run_hpcg.sh
```

确认日志包含 `VALID`、没有 `Quick Path`、执行时间 ≥1800 秒，再把 `../logs/` 下的日志与功耗 CSV 回填报告。

## 注意事项

- **不要在共享登录节点上跑大网格**。640³ + 36 进程会占用上百 GB 内存，足以拖垮登录节点。测试用 64³ / 128³，正式跑分放在独立计算节点。
- 赛题要求 HPCG 3.0、运行时间 ≥1800 秒，禁止 Quick Path；`hpcg.dat` 第 4 行不能为 0。
- 功耗必须 < 3 kW；优先使用 ACPI 功率计或 PDU/IPMI 的整机读数，`nvidia-smi` 只代表 GPU，不能作为整机功耗。
- 若需更高分数，在独立节点上再增大 `--n`（如 384/512），先用小网格确认内存占用。
