# 提交代码说明

官方仓库：`https://github.com/unitreerobotics/unifolm-world-model-action`
权重：`https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Dual`
输入数据：`https://github.com/ASC-Competition/ASC26-Embodied-World-Model-Optimizations`

复现场景：`unitree_z1_dual_arm_cleanup_pencils`、`unitree_z1_dual_arm_stackbox`，各 4 个 case。

## 前置条件

- 官方仓库已克隆并安装依赖，权重与场景数据已就位；
- 已在 `configs/inference/world_model_interaction.yaml` 中设置正确的 `data_dir`；
- 官方入口脚本存在：`$REPO_DIR/{scenario}/{case_id}/run_world_model_interaction.sh`。

## 运行流程

```bash
# 1. 生成 25 步的优化配置
python prepare_opt_config.py --repo-dir /path/to/unifolm-world-model-action --steps 25

# 2. 跑 baseline + optimized（2 场景 × 4 case）
REPO_DIR=/path/to/unifolm-world-model-action \
RESULTS_DIR=../results \
bash run_all.sh

# 3. 对每个 case 计算 PSNR（参考视频路径按官方数据目录调整）
python psnr_eval.py \
  --gt /path/to/gt/unitree_z1_dual_arm_stackbox/case1.mp4 \
  --pred ../results/unitree_z1_dual_arm_stackbox/case1/0_full_fs6.mp4 \
  --output ../results/unitree_z1_dual_arm_stackbox/case1/psnr.json

# 4. 汇总
python gen_summary.py \
  --results ../results \
  --scenarios unitree_z1_dual_arm_cleanup_pencils,unitree_z1_dual_arm_stackbox \
  --cases case1,case2,case3,case4 \
  --output ../results/summary.json

# 5. PSNR 阈值图
python plot_psnr.py --summary ../results/summary.json --output ../results/psnr_chart.png

# 6. 生成 DOCX 提案
python make_proposal.py --summary ../results/summary.json --chart ../results/psnr_chart.png
```

## 说明

- baseline 日志保存为 `baseline.log`，optimized 日志保存为 `output.log`；两者都必须包含官方输出的 `real time`。
- 生成的视频统一归档为 `0_full_fs6.mp4`。
- `run_case.sh` 在 optimized 模式下会临时替换官方配置文件，结束后自动恢复；不要并行运行多个 case。
- 若官方 case 目录名不是 `case1`~`case4`，通过 `CASES=...` 覆盖。
