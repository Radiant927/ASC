#!/usr/bin/env python3
"""生成 HPCG 输入文件 hpcg.dat（三维网格尺寸 + 运行时间）。"""
import argparse
from pathlib import Path

BYTES_PER_POINT = 216  # HPCG 每网格点约 27 个 double


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None, help="三维网格边长，默认按内存估算")
    ap.add_argument("--runtime", type=int, default=1800, help="运行时间（秒），赛题要求 >= 1800")
    ap.add_argument("--memory-gb", type=float, default=503.0)
    ap.add_argument("--memory-fraction", type=float, default=0.4)
    ap.add_argument("--output", default="hpcg.dat")
    args = ap.parse_args()

    if args.runtime < 1800:
        raise SystemExit("赛题要求 HPCG 运行时间不少于 1800 秒")

    n = args.n
    if n is None:
        points = args.memory_gb * 1e9 * args.memory_fraction / BYTES_PER_POINT
        n = max(104, int(points ** (1 / 3) // 2 * 2))

    est_gb = n ** 3 * BYTES_PER_POINT / 1e9
    text = (
        "HPCG benchmark input file\n"
        "Sandia National Laboratories; University of Tennessee, Knoxville\n"
        f"{n} {n} {n}\n"
        f"{args.runtime}\n"
    )
    Path(args.output).write_text(text, encoding="ascii")
    print(f"已写入 {args.output}: grid={n}x{n}x{n}, runtime={args.runtime}s, 估计内存约 {est_gb:.1f} GB")


if __name__ == "__main__":
    main()
