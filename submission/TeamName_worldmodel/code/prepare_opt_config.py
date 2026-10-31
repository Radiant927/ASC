#!/usr/bin/env python3
"""从官方推理配置生成减少采样步数的优化配置。"""
import argparse
import sys
from pathlib import Path

import yaml

STEP_KEYS = {"ddim_steps", "num_sampling_steps", "sampling_steps", "num_steps", "ddim_num_steps"}
ETA_KEYS = {"ddim_eta"}


def walk(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield path + (key,), node, key
            yield from walk(value, path + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, path + (str(index),))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", required=True)
    ap.add_argument("--source", default=None)
    ap.add_argument("--output", default=None)
    ap.add_argument("--steps", type=int, default=25)
    args = ap.parse_args()

    repo = Path(args.repo_dir)
    source = Path(args.source) if args.source else repo / "configs/inference/world_model_interaction.yaml"
    output = Path(args.output) if args.output else source.with_name(source.stem + "_opt.yaml")

    config = yaml.safe_load(source.read_text(encoding="utf-8"))
    changed = []
    for path, parent, key in list(walk(config)):
        lowered = str(key).lower()
        if lowered in STEP_KEYS:
            parent[key] = args.steps
            changed.append(".".join(map(str, path)))
        elif lowered in ETA_KEYS and isinstance(parent[key], (int, float)):
            parent[key] = 0.0
            changed.append(".".join(map(str, path)))

    if not changed:
        print(f"未在 {source} 中找到采样步数字段，请手动指定 --source 或修改配置", file=sys.stderr)
        sys.exit(2)

    output.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"已写入 {output}")
    for item in changed:
        print(f"  {item}")


if __name__ == "__main__":
    main()
