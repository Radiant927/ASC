#!/usr/bin/env python3
"""扫描结果目录，从日志与 psnr.json 生成 summary.json。"""
import argparse
import json
import re
from pathlib import Path

TIME_PATTERNS = [
    re.compile(r"real\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.I),
    re.compile(r"inference\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.I),
    re.compile(r"耗时\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)"),
]


def parse_time(log_path):
    if not log_path.exists():
        return None
    text = log_path.read_text(errors="ignore")
    for pattern in TIME_PATTERNS:
        match = pattern.search(text)
        if match:
            return float(match.group(1))
    return None


def parse_psnr(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8")).get("psnr")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--scenarios", required=True, help="逗号分隔")
    ap.add_argument("--cases", default="case1,case2,case3,case4")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    root = Path(args.results)
    entries = []
    for scenario in args.scenarios.split(","):
        for case in args.cases.split(","):
            scenario = scenario.strip()
            case = case.strip()
            case_dir = root / scenario / case
            digits = re.sub(r"\D", "", case)
            entries.append({
                "scenario": scenario,
                "case_id": int(digits) if digits else case,
                "time_before_optim": parse_time(case_dir / "baseline.log"),
                "time_after_optim": parse_time(case_dir / "output.log"),
                "psnr": parse_psnr(case_dir / "psnr.json"),
            })

    output = Path(args.output) if args.output else root / "summary.json"
    output.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"写入 {output}，共 {len(entries)} 条")


if __name__ == "__main__":
    main()
