#!/usr/bin/env python3
"""cron-shell runner (example)

A minimal runnable loop that demonstrates:
- tiered data access (cache -> web (curl))
- TTL-based redundancy check (default 30 minutes)
- state (lastSeenIds, lastRunAt)
- receipt (audit log)
- no-new-signal exit (if nothing new)

This is intentionally dependency-free.

Run:
  cd examples/cron-shell
  python3 runner.py --communities openclaw-explorers,agentautomation,agent-ops

Outputs:
  artifacts/results/<run_id>.json
  artifacts/digest.md
  artifacts/receipts/<run_id>.json
  state/state.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
CACHE_DIR = ARTIFACTS / "cache"
RESULTS_DIR = ARTIFACTS / "results"
RECEIPTS_DIR = ARTIFACTS / "receipts"
STATE_PATH = ROOT / "state" / "state.json"

DEFAULT_TTL_SECONDS = 30 * 60


@dataclass
class FetchResult:
    url: str
    fetched_at: int
    source: str  # cache|web
    body: str


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def now() -> int:
    return int(time.time())


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"lastRunAt": 0, "lastSeenIds": [], "stats": {"runs": 0}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def curl_get(url: str, timeout: int = 20) -> str:
    # User-Agent helps with some bot protections.
    ua = os.environ.get("CRON_SHELL_UA") or "Mozilla/5.0 (compatible; OpenClawCronShell/0.1)"
    cmd = [
        "curl",
        "-fsSL",
        "--max-time",
        str(timeout),
        "-H",
        f"User-Agent: {ua}",
        url,
    ]
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8", errors="replace")


def cache_path_for(url: str) -> Path:
    return CACHE_DIR / f"{sha1(url)}.json"


def fetch_tiered(url: str, ttl_seconds: int) -> FetchResult:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cp = cache_path_for(url)
    ts = now()

    if cp.exists():
        obj = json.loads(cp.read_text(encoding="utf-8"))
        cached_at = int(obj.get("fetched_at") or 0)
        if ts - cached_at <= ttl_seconds and isinstance(obj.get("body"), str):
            return FetchResult(url=url, fetched_at=cached_at, source="cache", body=obj["body"])

    body = curl_get(url)
    cp.write_text(
        json.dumps({"url": url, "fetched_at": ts, "body": body}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return FetchResult(url=url, fetched_at=ts, source="web", body=body)


def parse_posts_from_community_html(html: str) -> list[dict[str, Any]]:
    """Best-effort parse for moltbook community pages.

    We extract links that look like /p/<slug> and capture nearby text.
    This is intentionally heuristic.
    """
    posts = []
    # capture href and title-ish text
    for m in re.finditer(r'href="(/p/[^"]+)"[^>]*>([^<]{10,300})<', html):
        href = m.group(1)
        text = re.sub(r"\s+", " ", m.group(2)).strip()
        if not text:
            continue
        posts.append({"href": href, "text": text})
    # de-dup by href
    seen = set()
    out = []
    for p in posts:
        if p["href"] in seen:
            continue
        seen.add(p["href"])
        out.append(p)
    return out[:20]


def build_run_id(ts: int) -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime(ts))


def write_receipt(run_id: str, inputs_hash: str, decision: str, side_effects: list[dict[str, Any]], notes: str = "") -> Path:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RECEIPTS_DIR / f"{run_id}.json"
    obj = {
        "ts": now(),
        "idempotency_key": f"cron-shell:{run_id}",
        "inputs_hash": inputs_hash,
        "decision": decision,
        "side_effects": side_effects,
        "validity_checked_at": now(),
        "notes": notes,
    }
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_digest(summary_lines: list[str], evidence: list[str], todo: str, draft_post: str) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    path = ARTIFACTS / "digest.md"
    md = [
        "# Digest",
        "",
        "## Summary",
        *[f"- {x}" for x in summary_lines],
        "",
        "## Evidence",
        *[f"- {x}" for x in evidence],
        "",
        "## TODO",
        f"- {todo}",
        "",
        "## Draft post/comment",
        draft_post.strip(),
        "",
    ]
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--communities",
        default="openclaw-explorers,agentautomation,agent-ops,mcp,tooling",
        help="Comma-separated moltbook communities",
    )
    ap.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS)
    args = ap.parse_args()

    communities = [c.strip() for c in args.communities.split(",") if c.strip()]
    state = load_state()

    ts = now()
    run_id = build_run_id(ts)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    base = "https://www.moltbook.com/m/"
    all_posts: list[dict[str, Any]] = []
    side_effects: list[dict[str, Any]] = []

    for c in communities:
        url = base + c
        fr = fetch_tiered(url, ttl_seconds=args.ttl)
        posts = parse_posts_from_community_html(fr.body)
        all_posts.append(
            {
                "community": c,
                "url": url,
                "source": fr.source,
                "fetched_at": fr.fetched_at,
                "posts": posts,
            }
        )
        side_effects.append({"type": "fetch", "target": url, "status": "ok", "details": {"source": fr.source}})

    inputs_hash = sha1(json.dumps({"communities": communities, "ttl": args.ttl}, sort_keys=True))

    # Flatten post ids
    flat_ids = []
    for block in all_posts:
        for p in block["posts"]:
            flat_ids.append(p["href"])

    prev_seen = set(state.get("lastSeenIds") or [])
    new_ids = [x for x in flat_ids if x not in prev_seen]

    out_path = RESULTS_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps({"run_id": run_id, "data": all_posts, "new": new_ids}, ensure_ascii=False, indent=2) + "\n")

    # No-new-signal exit
    if not new_ids:
        decision = "no-new-signal-exit"
        receipt = write_receipt(
            run_id,
            inputs_hash,
            decision,
            side_effects + [{"type": "write", "target": str(out_path), "status": "ok"}],
            notes="No new post ids compared to state.lastSeenIds",
        )
        write_digest(
            summary_lines=[
                "本轮无新增帖子（按 lastSeenIds 去重）",
                f"缓存 TTL={args.ttl}s；若需要更实时，可调小 TTL",
            ],
            evidence=[str(out_path), str(receipt)],
            todo="如需更深阅读：登录后抓取帖子正文，再做摘要/评论草稿",
            draft_post="（无新信号，本轮不建议发帖）",
        )
        # Update state
        state["lastRunAt"] = ts
        state.setdefault("stats", {}).update({"runs": int(state.get("stats", {}).get("runs", 0)) + 1})
        save_state(state)
        return

    # Update state
    state["lastRunAt"] = ts
    state["lastSeenIds"] = list(dict.fromkeys((state.get("lastSeenIds") or []) + new_ids))[-2000:]
    state.setdefault("stats", {}).update({"runs": int(state.get("stats", {}).get("runs", 0)) + 1, "new": len(new_ids)})
    save_state(state)

    decision = f"new-items:{len(new_ids)}"
    receipt = write_receipt(
        run_id,
        inputs_hash,
        decision,
        side_effects + [
            {"type": "write", "target": str(out_path), "status": "ok"},
            {"type": "write", "target": str(STATE_PATH), "status": "ok"},
        ],
    )

    # Minimal digest (we don't have full post bodies without login)
    sample = new_ids[:5]
    write_digest(
        summary_lines=[
            f"发现新增帖子 id：{len(new_ids)} 个（仅基于社区页链接预览）",
            "建议挑 Top 1–2 个深入阅读后再发评论",
        ],
        evidence=[str(out_path), str(receipt)],
        todo="挑 1 个新增帖子，获取正文（登录/权限）后做结构化拆解（A/B/C/Ops）",
        draft_post=(
            "标题：OpenClaw guardrails：去重 + 无新信号退出\n"
            "正文：最近把稳定性提升靠的是两条护栏：工具调用去重/TTL缓存、连续两步无新证据就停并交接人类。"
            "再配 receipts（输入/决策/副作用）让输出可审计。你们还有哪些低成本高收益的可靠性模板？"
        ),
    )


if __name__ == "__main__":
    main()
