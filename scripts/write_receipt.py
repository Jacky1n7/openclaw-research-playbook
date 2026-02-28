#!/usr/bin/env python3
"""Write a small JSON receipt for auditability.

This is deliberately tiny and dependency-free.

Usage:
  python3 scripts/write_receipt.py --out artifacts/receipts/<run_id>.json \
    --tool "tavily_search" --params '{"q":"..."}' --output artifacts/results/x.json \
    --reason "ok"

You can call this from cron/heartbeat loops.
"""

import argparse
import json
import os
import time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--params", default="{}")
    ap.add_argument("--output", action="append", default=[])
    ap.add_argument("--reason", default="ok")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        params = {"raw": args.params}

    obj = {
        "ts": int(time.time()),
        "tool": args.tool,
        "params": params,
        "outputs": args.output,
        "reason": args.reason,
        "cwd": os.getcwd(),
    }

    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
