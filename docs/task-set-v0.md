# Task set v0 (Kiln A/B)

Paired cells from [harness-ab.md](harness-ab.md). Each `task_id` runs under `FHA-control` and `EoCC-kiln-default` (optional: tight / SAC later).

Acceptance is binary `passed` unless `score` is noted. Prefer fixtures you already own; swap paths without changing ids.

## SE — long-horizon (5+)

| task_id | Kind | Setup | Done when | Notes |
|---|---|---|---|---|
| `se-01-typo-fix` | 1–2 file fix | Tiny TS/JS fixture with a deliberate bug + failing unit test | Test green; only intended files changed | Warm-up; should pass both cells |
| `se-02-api-rename` | Multi-file rename | Small package: symbol used in 3+ files + test | All call sites updated; tests green | Forces search + edit loop |
| `se-03-verify-script` | Scripted verify | Repo with `verify.sh` (or Atelier-style verify cmds) that fails until fix | Verify exit 0; report path logged | Mirrors Atelier verify |
| `se-04-rework-loop` | Fail then fix | First acceptance wrong on purpose; rework note required | Second attempt passes; dead end in state tablet on EoCC | Stresses compact-after-failure |
| `se-05-wave-two-pbi` | Two dependent units | PBI-A then PBI-B (B needs A’s API); wave boundary between them | Both units pass; EoCC must hand off or compact at wave | Primary Kiln boundary task |
| `se-06-optional` | Larger SE | Optional: one real mini-SWE or past Atelier PBI (anonymized) | Project’s own verify | Add when smoke gate is green |

## LI — long-input (3+)

Do **not** paste the corpus into the prompt. Place files on disk; agent may `sed`/`rg`/read slices only.

| task_id | Kind | Corpus | Question / task | Done when |
|---|---|---|---|---|
| `li-01-needle` | Needle in haystack | ≥50K tokens of filler + one unique key line | Return the exact key string | Exact match |
| `li-02-cross-ref` | Two-doc join | Two markdown/specs; answer needs both | Short answer citing both paths | Correct + both paths named |
| `li-03-exclude-rule` | Read then apply rule | Long policy/doc; answer needs an exclusion clause | Correct under the exclusion | Wrong if whole-doc skim bias |
| `li-04-optional` | Multi-file tree | Small docs tree (≥10 files) | Count or list matching items | Exact list/count |

## Trap tasks (hold out until cells 1–2 are green)

| task_id | Why held out |
|---|---|
| `trap-history-index` | Needs ith prior tool result verbatim → unfair to lossy compact without external history store |
| `trap-topic-shift` | Mid-run unrelated task; measures fork, not kiln defaults |

## Smoke order

1. `se-01`, `se-02`, `li-01` × (`FHA-control`, `EoCC-kiln-default`)  
2. If smoke gate holds → `se-03`–`se-05`, `li-02`–`li-03`  
3. Then optional / traps

## Fixture layout (suggested)

```text
fixtures/
  se-01-typo-fix/
  se-02-api-rename/
  ...
  li-01-needle/
  ...
```

Each fixture: `README.md` (task prompt), `verify` or test command, and input files. Harness sets cwd to the fixture and passes `task_id` + `RUN_ID`.

## Mapping to Atelier (optional host)

| task_id | Atelier shape |
|---|---|
| `se-03`–`se-05` | One or two PBIs under `docs/pbi/` with `verify.py` |
| `se-05` | Two-PBI wave + existing handoff measure |
| LI tasks | Not Atelier-native; run in mini-agent / generic harness |

Ids stay stable even if the host changes.
