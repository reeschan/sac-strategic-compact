#!/usr/bin/env python3
"""Append one Kiln compact event (JSONL). For harness joins later."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log", required=True, help="Path to compact-events.jsonl")
    p.add_argument("--run-id", required=True)
    p.add_argument("--regime", required=True, choices=["FHA", "EoCC", "SAC"])
    p.add_argument(
        "--boundary",
        required=True,
        choices=["phase", "wave", "soft", "forced", "failed_approach", "topic_shift", "manual"],
    )
    p.add_argument("--role", required=True, choices=["designer", "implementer"])
    p.add_argument("--action", required=True, choices=["noop", "suggest", "compact", "handoff", "aux_on", "fork"])
    p.add_argument("--tokens-before", required=True, type=int)
    p.add_argument("--tokens-after", type=int, default=None)
    p.add_argument("--peak-budget", type=int, default=None)
    p.add_argument("--soft-budget", type=int, default=None)
    p.add_argument("--phase", default=None)
    p.add_argument("--host", default=None)
    p.add_argument("--state-path", default=None)
    p.add_argument("--task-id", default=None)
    p.add_argument("--notes", default=None)
    args = p.parse_args()

    event = {
        "v": 1,
        "event": "compact",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": args.run_id,
        "host": args.host,
        "regime": args.regime,
        "boundary": args.boundary,
        "role": args.role,
        "phase": args.phase,
        "tokens_before": args.tokens_before,
        "tokens_after": args.tokens_after,
        "peak_budget": args.peak_budget,
        "soft_budget": args.soft_budget,
        "action": args.action,
        "state_path": args.state_path,
        "notes": args.notes,
        "task_id": args.task_id,
        "outcome": None,
    }

    path = Path(args.log)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
