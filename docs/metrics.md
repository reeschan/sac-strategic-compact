# Measuring compaction lift

Goal: compare **FHA** (full history) vs **EoCC** (or **SAC**) on the same tasks.

## Required logs

1. One line per decision in `.kiln/compact-events.jsonl` (see schema).
2. One harness run record per task with at least: `run_id`, `task_id`, `regime`, `passed` / score, total input+output tokens, wall time.

Join on `run_id` (+ `task_id` when present).

## Suggested metrics

| Metric | Definition |
|---|---|
| Accuracy Δ | `score(EoCC) - score(FHA)` (or pass-rate Δ) |
| Peak context | max `tokens_before` / measured peak live context |
| Token spend | sum input+output over the run |
| Cost proxy | token spend × host price, or GPU-hour if self-hosted |
| Compact count | number of `action` in {compact, handoff} |
| Recovery turns | user/agent clarifications in the first N turns after compact (optional) |

Report medians and max peak context the way the paper does (median / max).

## Harness checklist (later)

- [ ] Fixed task set and seeds
- [ ] Same model and tool policy across regimes
- [ ] `run_id` shared between compact log and outcome log
- [ ] Write `outcome` back onto compact events or keep a separate `runs.jsonl`
- [ ] At least one A/B cell: FHA vs EoCC at kiln soft/peak defaults
