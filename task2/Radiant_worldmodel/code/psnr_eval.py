#!/usr/bin/env python3
"""逐帧计算生成视频与参考视频的 PSNR，输出 JSON。"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def read_video(path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {path}")
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    if not frames:
        raise RuntimeError(f"视频无可用帧: {path}")
    return frames


def frame_psnr(gt, pred):
    mse = np.mean((gt.astype(np.float64) - pred.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0
    return 10.0 * np.log10(255.0 ** 2 / mse)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    gt_frames = read_video(args.gt)
    pred_frames = read_video(args.pred)
    if len(gt_frames) != len(pred_frames):
        raise SystemExit(f"帧数不一致: gt={len(gt_frames)}, pred={len(pred_frames)}")

    scores = []
    for index, (gt, pred) in enumerate(zip(gt_frames, pred_frames)):
        if gt.shape != pred.shape:
            raise SystemExit(f"第 {index} 帧尺寸不一致: {gt.shape} vs {pred.shape}")
        scores.append(frame_psnr(gt, pred))

    result = {
        "psnr": round(float(np.mean(scores)), 4),
        "psnr_min": round(float(np.min(scores)), 4),
        "frames": len(scores),
    }
    print(json.dumps(result, ensure_ascii=False))
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
