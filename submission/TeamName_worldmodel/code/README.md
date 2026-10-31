# 提交代码

官方仓库：`https://github.com/unitreerobotics/unifolm-world-model-action`
权重：`https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Dual`
数据：`https://github.com/ASC-Competition/ASC26-Embodied-World-Model-Optimizations`

场景：`unitree_z1_dual_arm_cleanup_pencils`、`unitree_z1_dual_arm_stackbox`，各 4 个 case。

## 前提
- 官方仓库已克隆，依赖已安装，权重和场景数据已就位；
- `configs/inference/world_model_interaction.yaml` 的 `data_dir` 已指向数据目录；
- 入口脚本存在：`$REPO_DIR/{scenario}/{case_id}/run_world_model_interaction.sh`。

## 步骤
```bash
# 1. 生成 25 步优化配置
python prepare_opt_config.py --repo-dir /path/to/unifolm-world-model-action --steps 25

# 2. 跑 baseline 和 optimized
REPO_DIR=/path/to/unifolm-world-model-action \
RESULTS_DIR=../results \
bash run_all.sh

# 3. 计算 PSNR
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

# 5. PSNR 图
python plot_psnr.py --summary ../results/summary.json --output ../results/psnr_chart.png

# 6. DOCX 提案
python make_proposal.py --summary ../results/summary.json --chart ../results/psnr_chart.png
```

## 注意
- `baseline.log` 和 `output.log` 必须包含官方输出的 `real time`。
- 视频统一存为 `0_full_fs6.mp4`。
- optimized 模式会临时替换官方配置，结束后自动恢复；不要并行跑 case。
- case 目录名不是 `case1`~`case4` 时，用 `CASES=...` 覆盖。
