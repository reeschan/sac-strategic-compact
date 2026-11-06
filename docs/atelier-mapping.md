# Example: Atelier

Only a mapping. The skill itself does not depend on Atelier.

| Kiln / skill | Atelier |
|---|---|
| Designer | Orchestrator (`SKILL.md`) |
| Implementer | Worker (`worker.md`), one attempt per PBI try |
| Phase | understand, design, plan, route, build, verify, review, fix, finish |
| Wave boundary | After a build wave; measure with `agent_stats.py --ctx` |
| Handoff artifact | `docs/pbi/HANDOFF.md` (+ optional `CONTEXT_STATE.md`) |
| Kiln file | `docs/pbi/kiln.json` |
| Compact log | `docs/pbi/.kiln/compact-events.jsonl` |
| aux_compress_at | Existing rtk threshold (~150k) |
| handoff_at | Existing handoff threshold (~250k) |

Prefer Atelier’s own handoff procedure when `handoff_at` is crossed. Use `/compact` + state file only below that line.
