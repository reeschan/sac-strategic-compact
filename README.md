# sac-strategic-compact

**Kiln** — a forge-wide capacity limit for agent context — plus strategic compaction (EoCC / SAC-style handoffs) with harness-ready logs.

Generic skill. Works with Claude Code `/compact`, session handoff, or any host that can reset a conversation and reinject a state file. An Atelier mapping is only an example.

## Concepts

| Term | Meaning |
|---|---|
| **Kiln** | Global constraint: how hot (how large) the working context may run before you must cool it (compact / handoff). |
| **Designer** | The role that plans and decides (orchestrator, lead agent). |
| **Implementer** | The role that takes one build attempt (worker, coding subagent). Fresh per attempt when possible. |
| **EoCC** | End-of-conversation compaction: summarize into a state file, start a fresh conversation with task + state. |
| **SAC** | Single-action compaction: at most one environment action per conversation; carry only semantic state. Optional extreme; not the default. |

Inspired by [You don’t need long context](https://arxiv.org/abs/2611.05306) and strategic-compact / PreCompact practice.

## Install

Copy or submodule `skills/sac-strategic-compact` into your agent skills directory (Claude Code: `.claude/skills/` or a shared skills repo).

```bash
# example
cp -R skills/sac-strategic-compact ~/.claude/skills/
```

Optional kiln config at the project root or run dir:

```bash
cp examples/kiln.example.json .kiln.json
# or: docs/pbi/kiln.json for Atelier runs
```

## Logging (for harness A/B)

Every compact / handoff / soft-threshold decision should append one JSON line. The harness later joins these with task outcomes to measure accuracy and token cost vs a full-history baseline.

```bash
python scripts/log_compact_event.py \
  --log .kiln/compact-events.jsonl \
  --run-id "$RUN_ID" \
  --regime EoCC \
  --boundary wave \
  --role designer \
  --tokens-before 52000 \
  --action handoff \
  --state-path CONTEXT_STATE.md
```

Schema: `schemas/compact-event.schema.json`. See `docs/metrics.md`.

## License

MIT
