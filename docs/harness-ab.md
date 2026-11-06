# Harness A/B: Kiln compaction lift

Measure whether **EoCC under Kiln** beats **FHA** (full-history) on the same tasks, using compact-event logs.

Do not change product code for this cell. The harness only varies context regime and kiln budgets.

## Cells

| Cell id | Regime | Kiln | Notes |
|---|---|---|---|
| `FHA-control` | FHA | off (no soft/peak cool-down) | Baseline. Still log `noop` at wave boundaries if measured. |
| `EoCC-kiln-default` | EoCC | designer 48k/36k, implementer 24k/18k, handoff 250k | Primary treatment. |
| `EoCC-kiln-tight` | EoCC | designer 32k/24k, implementer 16k/12k, handoff 128k | Stress cell (optional second treatment). |
| `SAC-explore` | SAC | designer state only; one action per conversation | Optional; run only after EoCC cells look stable. |

Pair every treatment run with a control run on the **same task_id**, same model, same tool policy, same seed when the host allows it.

## Fixed factors

- Model and effort / thinking settings
- Tool allowlist and max turns
- Task set and acceptance checks
- `run_id` format: `{experiment}-{yyyyMMdd}-{cell}-{task_id}-{rep}`
- Compact log path: `.kiln/compact-events.jsonl` (or Atelier: `docs/pbi/.kiln/compact-events.jsonl`)
- Outcome log path: `.kiln/runs.jsonl`

## Task set (v0)

Concrete ids and smoke order: [task-set-v0.md](task-set-v0.md).

Start small; expand after the join pipeline works.


## What each run must write

### compact-events.jsonl

One line per boundary decision via `scripts/log_compact_event.py` (schema in `schemas/compact-event.schema.json`).

Required on every boundary measurement, including control:

- `run_id`, `regime`, `boundary`, `role`, `tokens_before`, `action`
- `task_id` when known
- `state_path` when a tablet was written
- `tokens_after` when the host exposes it after cool-down

Control (`FHA-control`) uses `regime: FHA` and usually `action: noop` (or `aux_on` only).

### runs.jsonl

One object per finished task attempt:

```json
{
  "v": 1,
  "run_id": "kiln-ab-20261106-EoCC-kiln-default-se-01-1",
  "experiment": "kiln-ab",
  "cell": "EoCC-kiln-default",
  "task_id": "se-01",
  "rep": 1,
  "regime": "EoCC",
  "model": "<id>",
  "passed": true,
  "score": 1.0,
  "input_tokens": 0,
  "output_tokens": 0,
  "wall_ms": 0,
  "peak_context": 0,
  "compact_actions": 0,
  "notes": null
}
```

`peak_context` = max observed live context (or max `tokens_before` if that is all you have).  
`compact_actions` = count of compact-events with `action` in `compact|handoff`.

Harness may also patch `outcome` onto compact events; keeping `runs.jsonl` separate is enough for v0.

## Metrics (report)

Per cell, over the task set:

| Metric | How |
|---|---|
| Pass rate / mean score | from `runs.jsonl` |
| Accuracy Δ | treatment − `FHA-control` (paired by `task_id`) |
| Median / max peak context | from `peak_context` |
| Median token spend | `input_tokens + output_tokens` |
| Compact count | `compact_actions` |
| Wall time Δ | optional |

Smoke gate before a full sweep: on ≥3 SE tasks, EoCC-kiln-default pass rate ≥ FHA−1 task, and median peak context clearly below FHA.

## Procedure

1. Freeze task list and model.
2. For each `task_id` × cell × rep: start with a fresh session, set `RUN_ID`, enable or disable kiln per cell.
3. On every phase/wave boundary: measure tokens → decide → **log** → cool only if the cell allows.
4. Run verify / acceptance → append `runs.jsonl`.
5. Join and print the metrics table; do not tune kiln mid-experiment (change cells between sweeps).

## Atelier note

When the host is Atelier, map designer/implementer and thresholds as in `docs/atelier-mapping.md`. Prefer existing HANDOFF when `handoff_at` fires; still write compact-events so the join stays uniform.

## Out of scope for v0

- Changing Atelier stage graph
- Training an SSSM
- Claiming cost $ without a priced token table
