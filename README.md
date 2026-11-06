# sac-strategic-compact

**日本語** | [English](README.en.md)

エージェントの作業文脈に、鍛冶場の**窯（Kiln）**という全体制約を置き、論理的な区切りだけで戦略的に冷ます（EoCC / 任意で SAC）ための汎用スキルと、改善率を測るためのログです。

Claude Code の `/compact`、セッションの clear＋resume、会話を捨てて状態ファイルだけ持ち越すホストなら使えます。Atelier 向けの対応表は一例であり、このリポジトリ自体は Atelier に依存しません。

着想: [You don’t need long context](https://arxiv.org/abs/2611.05306)（NVIDIA, 2026）、strategic-compact / PreCompact の実践。

## 何のためのものか

長い会話ほど後のトークンは高く、遅い。一方で「全部の履歴を毎回プロンプトに載せなくても、状態を保てば長い仕事は終わる」ことが論文側でも示されています。

このリポジトリは次を揃えます。

1. **Kiln** … 文脈の容量そのものを概念化する（soft / peak / handoff / aux、設計者室と実装者室）
2. **スキル** `skills/sac-strategic-compact` … いつ冷ますか、何を状態タブレットに残すか
3. **ログ** … ハーネスが FHA（履歴全部）と EoCC を同じタスクで比べられる JSONL

## 概念

| 用語 | 意味 |
|---|---|
| **Kiln（窯）** | 作業文脈の全体制約。どれだけ熱く（大きく）してよいか、どこで冷ますか |
| **Designer（設計者）** | 計画・判定する役割（オーケストレータ） |
| **Implementer（実装者）** | 1回の実装試行（ワーカー）。できれば試行ごとに新規 |
| **EoCC** | 会話末圧縮。状態ファイルに要約し、タスク＋状態だけで新会話 |
| **SAC** | 1アクションごとに会話を捨てる極端な形。既定ではない |
| **FHA** | 履歴を全部残す従来どおり（A/B の対照） |

詳細は [docs/kiln.md](docs/kiln.md)。

## 入れ方

```bash
git clone https://github.com/reeschan/sac-strategic-compact.git
cp -R sac-strategic-compact/skills/sac-strategic-compact ~/.claude/skills/
# または ~/.agents/skills/
```

任意の窯設定:

```bash
cp examples/kiln.example.json .kiln.json
# Atelier ランなら: docs/pbi/kiln.json
```

スキルを開いたら、ホストの文脈トークンを測り、境界で冷ますか判断し、**必ず** compact イベントを1行ログします。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `skills/sac-strategic-compact/SKILL.md` | エージェントが読む手順 |
| `examples/kiln.example.json` | 窯とログの設定例 |
| `schemas/compact-event.schema.json` | 境界判定1件の JSON スキーマ |
| `schemas/run-outcome.schema.json` | タスク完了1件（ハーネス） |
| `scripts/log_compact_event.py` | JSONL 追記 CLI |
| `docs/kiln.md` | 窯の説明 |
| `docs/harness-ab.md` | A/B セル定義 |
| `docs/task-set-v0.md` | タスク一覧 v0 |
| `docs/metrics.md` | 改善率の見方 |
| `docs/atelier-mapping.md` | Atelier への載せ方（任意） |

## いつ冷ますか（要約）

| 境界 | 冷ます？ |
|---|---|
| 調査 → 計画 | する |
| 計画 → 実装 | する（計画は先にファイルへ） |
| 実装の途中 | **しない** |
| 失敗した方針のあと | する（dead ends を書いてから） |
| wave / マイルストーン後 | 測ってから soft / peak / handoff |
| 題材が変わった | する、またはセッションを分ける |

冷ます前に `CONTEXT_STATE.md` のような状態タブレット（Objective〜Remaining plan）を書く。`/compact` には「捨てるもの」ではなく「残すもの」を渡す。

## 計測ログ（ハーネス用）

境界のたびに1行:

```bash
python scripts/log_compact_event.py \
  --log .kiln/compact-events.jsonl \
  --run-id "$RUN_ID" \
  --host claude-code \
  --regime EoCC \
  --boundary phase \
  --role designer \
  --tokens-before 52000 \
  --action handoff \
  --state-path CONTEXT_STATE.md \
  --task-id "$TASK_ID"
```

タスク完了は `.kiln/runs.jsonl`（スキーマは `run-outcome.schema.json`）。`run_id` で結んで、精度差・ピーク文脈・トークン消費を見ます。手順は [docs/harness-ab.md](docs/harness-ab.md)、タスクは [docs/task-set-v0.md](docs/task-set-v0.md)。

## Atelier と使う場合（任意）

Atelier 側に Kiln 概念と `appendix/kiln.md` があります。テンプレは既定で `kiln.enabled: false`、`prompt_install: true`。有効にするときは `docs/pbi/kiln.json` を置き、このスキルを skills に入れます。対応表は [docs/atelier-mapping.md](docs/atelier-mapping.md)。

## ライセンス

MIT
