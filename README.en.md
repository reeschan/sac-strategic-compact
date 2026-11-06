# sac-strategic-compact

[日本語](README.md) | **English**

A generic agent skill that treats working context as a forge-wide **Kiln** capacity limit, cools only at logical boundaries (EoCC, optionally SAC), and writes harness-ready logs so you can measure compaction lift.

Works with Claude Code `/compact`, clear+resume handoff, or any host that can reset a conversation and reinject a state file. The Atelier mapping is an example only; this repo does not depend on Atelier.

Inspired by [You don’t need long context](https://arxiv.org/abs/2611.05306) (NVIDIA, 2026) and strategic-compact / PreCompact practice.

## Why

Later tokens cost more and run slower. Long-horizon and long-input work often do not need the full transcript in every call if you keep a compact semantic state. This repo packages:

1. **Kiln** — name the capacity lines (soft / peak / handoff / aux) and designer vs implementer chambers
2. **Skill** `skills/sac-strategic-compact` — when to cool, what to keep on a state tablet
3. **Logs** — JSONL so a harness can compare FHA (full history) vs EoCC on the same tasks

## Concepts

| Term | Meaning |
|---|---|
| **Kiln** | Global constraint on how large working context may run before cool-down |
| **Designer** | Plans and decides (orchestrator) |
| **Implementer** | One build attempt (worker); prefer fresh per attempt |
| **EoCC** | End-of-conversation compaction into a state file, then a fresh conversation |
| **SAC** | At most one environment action per conversation; optional extreme |
| **FHA** | Full-history accumulation (A/B control) |

See [docs/kiln.md](docs/kiln.md).

## Install

```bash
git clone https://github.com/reeschan/sac-strategic-compact.git
cp -R sac-strategic-compact/skills/sac-strategic-compact ~/.claude/skills/
# or ~/.agents/skills/
```

Optional kiln config:

```bash
cp examples/kiln.example.json .kiln.json
# Atelier runs: docs/pbi/kiln.json
```

## Layout

| Path | Purpose |
|---|---|
| `skills/sac-strategic-compact/SKILL.md` | Agent procedure |
| `examples/kiln.example.json` | Sample kiln + log config |
| `schemas/compact-event.schema.json` | One boundary decision |
| `schemas/run-outcome.schema.json` | One finished task (harness) |
| `scripts/log_compact_event.py` | Append JSONL |
| `docs/harness-ab.md` | A/B cells |
| `docs/task-set-v0.md` | Task ids v0 |
| `docs/metrics.md` | How to report lift |
| `docs/atelier-mapping.md` | Optional Atelier wiring |

## Cool-down rules (short)

Cool after research→plan and plan→implement (plan on disk first). **Never** mid-implementation. Cool after a failed approach (record dead ends). At wave boundaries, measure then apply soft / peak / handoff. Write a state tablet first; pass keep-instructions to `/compact`, not discard lists.

## Logging

```bash
python scripts/log_compact_event.py \
  --log .kiln/compact-events.jsonl \
  --run-id "$RUN_ID" \
  --regime EoCC \
  --boundary phase \
  --role designer \
  --tokens-before 52000 \
  --action handoff \
  --state-path CONTEXT_STATE.md
```

Join with `.kiln/runs.jsonl` on `run_id`. See [docs/harness-ab.md](docs/harness-ab.md).

## License

MIT
