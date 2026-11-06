---
name: sac-strategic-compact
description: Use when an agent session approaches context limits, at phase or wave boundaries, or when configuring Kiln budgets for designer vs implementer roles. Strategic compaction (EoCC/SAC-style) with harness-ready compact-event logs.
---

# sac-strategic-compact

Keep the **Kiln** from cracking: hold working context under role budgets, compact only at logical boundaries, and log every decision for later harness measurement.

Generic. Host-agnostic (Claude Code `/compact`, clear+resume handoff, or any reset that reinjects a state file). Product-specific mappings (e.g. Atelier) belong in docs, not in this recipe.

## Kiln

The kiln is the forge-wide capacity constraint for context.

| Line | Meaning |
|---|---|
| Soft | Prefer cool-down at the next phase boundary |
| Peak | Must cool before starting the next phase |
| Handoff | Write state, end session, resume with task + state only |
| Aux | Optional host compressor (e.g. command-output shrinker); not a substitute for state handoff |

Defaults (override with `.kiln.json` or a path the project documents):

```json
{
  "kiln": {
    "designer_peak": 48000,
    "designer_soft": 36000,
    "implementer_peak": 24000,
    "implementer_soft": 18000,
    "handoff_at": 250000,
    "aux_compress_at": 150000
  },
  "log": { "path": ".kiln/compact-events.jsonl", "require_run_id": true }
}
```

Roles:

- **Designer** — plans and decides. Larger chamber.
- **Implementer** — one build attempt. Smaller chamber; prefer a fresh session per attempt.

## When to compact

| Boundary | Compact? |
|---|---|
| Research → plan | Yes |
| Plan → implement | Yes (plan must be on disk first) |
| Mid-implementation | No |
| After a failed approach | Yes (record dead ends first) |
| Topic shift | Yes or fork a new session |
| Wave / milestone done | Measure, then soft/peak/handoff rules |
| Verify / review done before next unit | Yes |

Prefer **EoCC** (bounded state file + fresh conversation). Use **SAC** (one action per conversation) only when the user or experiment template asks for it.

## State tablet (before cool-down)

Write a short state file (e.g. `CONTEXT_STATE.md`), then compact or hand off. Keep it tight (about 40–80 lines):

1. **Objective** — one line
2. **Established facts** — paths, symbols, commands, observed values (separate guesses)
3. **Applied changes** — files touched and whether verified
4. **Verification** — checks, outcomes, obstacles
5. **Dead ends** — do not repeat
6. **Remaining plan** — ordered subgoals, immediate next action, done condition

For `/compact`-style hosts, pass keep-instructions (what to keep), not discard lists. Include exact paths, ids, and error strings that the next stretch needs.

## Logging (required)

Before or right after each decision, append one JSON line with the repo script (or equivalent):

```bash
python <repo>/scripts/log_compact_event.py \
  --log .kiln/compact-events.jsonl \
  --run-id "$RUN_ID" \
  --host claude-code \
  --regime EoCC \
  --boundary phase \
  --role designer \
  --phase plan \
  --tokens-before <n> \
  --peak-budget 48000 \
  --soft-budget 36000 \
  --action handoff \
  --state-path CONTEXT_STATE.md \
  --task-id "$TASK_ID"
```

Schema: `schemas/compact-event.schema.json`. Harness later fills `outcome` (pass/score/tokens/wall) to measure compaction lift vs FHA. See `docs/metrics.md`.

If `run_id` is missing and `require_run_id` is true, create one (UUID or harness id) and keep it for the whole run.

`action` values: `noop` | `suggest` | `compact` | `handoff` | `aux_on` | `fork`.

## Procedure

1. Load kiln config (project file or defaults).
2. Measure current context tokens if the host exposes them.
3. Choose: `noop` | `aux_on` | `suggest`/`compact` (EoCC) | `handoff` | `fork` using soft/peak/handoff lines. Never compact mid-implementer attempt.
4. If cooling: write the state tablet first.
5. Log the event (always, including `noop` when you measured at a boundary and stayed).
6. Execute host cool-down (`/compact …`, clear+resume, or SAC reset).
7. After resume: read task + state tablet only; do not redo finished phases from chat memory.

## Do not

- Compact mid-implementation
- Pass designer chat history into an implementer attempt
- Skip the compact-event log when measuring (harness needs it)
- Treat SAC as the default
