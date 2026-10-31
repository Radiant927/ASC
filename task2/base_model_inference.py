import argparse
import json
import time
import torch
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--savedir", type=str, default="./out")
    parser.add_argument("--ckpt_path", type=str, default="mock_ckpt")
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--prompt_dir", type=str, required=True)
    parser.add_argument("--ddim_steps", type=int, default=-1)
    parser.add_argument("--ddim_eta", type=float, default=0.0)
    parser.add_argument("--bs", type=int, default=1)
    parser.add_argument("--height", type=int, default=256)
    parser.add_argument("--width", type=int, default=416)
    parser.add_argument("--unconditional_guidance_scale", type=float, default=7.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--video_length", type=int, default=16)
    parser.add_argument("--text_input", action="store_true")
    parser.add_argument("--perframe_ae", action="store_true")
    args = parser.parse_args()

    save_dir = Path(args.savedir)
    save_dir.mkdir(exist_ok=True, parents=True)

    device = torch.device("cuda:0")
    dev_name = torch.cuda.get_device_name(device) if torch.cuda.is_available() else "CPU"

    torch.manual_seed(args.seed)
    start_total = time.time()

    # mock 模拟推理循环，对齐 ddim 步数逻辑
    if args.ddim_steps == -1:
        step_count = 1
    else:
        step_count = args.ddim_steps

    for _ in range(step_count):
        # mock 空前向，模拟采样步骤
        x = torch.randn(args.bs, 4, args.height // 8, args.width // 8, device=device)
        _ = x * 0.9

    torch.cuda.synchronize()
    total_time = time.time() - start_total
    avg_step_ms = (total_time / step_count) * 1000 if step_count > 0 else 0

    peak_mem_gb = torch.cuda.max_memory_allocated(device) / 1024 / 1024 / 1024
    torch.cuda.reset_peak_memory_stats(device)

    out_metrics = {
        "config": vars(args),
        "total_inference_time_s": round(total_time, 3),
        "avg_step_time_ms": round(avg_step_ms, 2),
        "peak_gpu_memory_GB": round(peak_mem_gb, 2),
        "device_name": dev_name,
    }

    with open(save_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(out_metrics, f, indent=2, ensure_ascii=False)
    print(f"Done, metrics saved to {save_dir / 'metrics.json'}")


if __name__ == "__main__":
    main()
