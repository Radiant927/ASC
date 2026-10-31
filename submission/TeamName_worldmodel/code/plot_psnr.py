#!/usr/bin/env python3
"""绘制各样本 PSNR 柱状图，并标注 25 分阈值线。"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--threshold", type=float, default=25.0)
    args = ap.parse_args()

    data = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    labels = [
        f'{item["scenario"].replace("unitree_", "")}\ncase{item["case_id"]}'
        for item in data
    ]
    values = [item["psnr"] if item["psnr"] is not None else 0 for item in data]

    fig, ax = plt.subplots(figsize=(12, 4.5), dpi=150)
    ax.bar(range(len(data)), values, color="#4C78A8")
    for index, item in enumerate(data):
        if item["psnr"] is None:
            ax.text(index, 0.5, "NA", ha="center", va="bottom", fontsize=8)
        else:
            ax.text(index, item["psnr"] + 0.2, f'{item["psnr"]:.2f}', ha="center", va="bottom", fontsize=8)

    ax.axhline(args.threshold, color="#E45756", linestyle="--", label=f"PSNR threshold {args.threshold:g}")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("PSNR (dB)")
    ax.set_title("Per-sample PSNR")
    ax.legend()
    fig.tight_layout()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"图表已保存: {args.output}")


if __name__ == "__main__":
    main()
