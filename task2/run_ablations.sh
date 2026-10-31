#!/bin/bash
# Task2: 一键运行三组 DDIM 采样消融实验
# 默认绑定 3 号卡，可通过环境变量覆盖
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-3}"
COMMON_ARGS="--config configs/inference/base_model_inference.yaml \
  --prompt_dir examples/prompts/unitree_z1_dual_arm_stackbox \
  --ddim_eta 0.0 --bs 1 --height 256 --width 416 \
  --unconditional_guidance_scale 7.5 --seed 42 --video_length 16 --perframe_ae"

echo "===== Baseline (ddim_steps=-1) ====="
python base_model_inference.py --savedir ./out_baseline --ddim_steps -1 $COMMON_ARGS

echo "===== Opt-50step (ddim_steps=50) ====="
python base_model_inference.py --savedir ./out_opt_ddim50 --ddim_steps 50 $COMMON_ARGS

echo "===== Opt-20step (ddim_steps=20) ====="
python base_model_inference.py --savedir ./out_opt_ddim20 --ddim_steps 20 $COMMON_ARGS

echo "===== All done. Results: ====="
for d in out_baseline out_opt_ddim50 out_opt_ddim20; do
  echo "--- $d ---"
  cat $d/metrics.json
  echo
done
