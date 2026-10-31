#!/bin/bash
# Task1: 一键运行 CPU + GPU GEMM 测速
echo "========== CPU GEMM Benchmark =========="
python cpu_gemm.py
echo ""
echo "========== GPU GEMM Benchmark =========="
CUDA_VISIBLE_DEVICES=0 python gpu_gemm.py
