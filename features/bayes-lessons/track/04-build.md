---
stage: build
seq: 4
status: done
started_at: 2026-11-10T08:17:00+08:00
ended_at: 2026-11-10T08:25:00+08:00
---

# track · build · bayes-lessons

Phase 0 再按 milestone：once 探测 → 红 keep → 实现 → 绿 keep。禁止用 once 绿代替 keep。

## Gate in

- [x] [03-plan.md](03-plan.md) `status=done`
- [x] 夹齐（`Index` · `spec` · `acceptance` · `references/`）

## once · 过程探测（本轮）

| # | 何时 | 做了什么 | 证据（命令/截图/日志路径） | 不入库 |
| --- | --- | --- | --- | --- |
| 0 | Phase 0 未改代码 | 跑 `python3 skills/bayes-lessons/scripts/bayes.py recall --about 基线` | `can't open file ... bayes.py: [Errno 2] No such file or directory` | 是 |
| 1 | 无 DOM | 不跑浏览器，不跑 CDP。`flow_coding_logging` 的页面/服务三路在此无对象 | 本段写明未做 | 是 |

TDD 跑次：先 `.venv/bin/python -m pytest features/bayes-lessons -q` → **15 failed**（脚本与 SKILL.md 都不在）。实现后再跑 → **15 passed**。失败跑次是 once，未当门闩。

## keep · 质量回归（入库文件）

| # | 文件::用例 | 先红（命令+结果） | 实现触点 | 后绿（命令+结果） | 跨边界 |
| --- | --- | --- | --- | --- | --- |
| 1 | `test_bayes_lessons_unit.py` | 15 failed 中的 13 条 unit | `skills/bayes-lessons/scripts/bayes.py` · `SKILL.md` | 13 passed | 否 |
| 2 | `test_bayes_lessons_regression.py` | 2 failed | 同上，追加日志 | 2 passed | 写盘 → 新 Python 进程 |

## 自检

| 项 | 结论 |
| --- | --- |
| 简化（能删的层 / 多余依赖） | 一个脚本，标准库。pytest 只在 `.venv`，不进产品依赖 |
| fail fast（空头诚实、单源不拖垮） | 坏日志 `corrupt-log` 退出 2，不跳过坏行。空 recall 是 `[]` |
| 性能（默认不做） | 只读这一份 jsonl |

## Gate out

- [x] 计划内 keep 已落成真文件，能红能绿
- [x] once 未冒充门闩
- [x] 未 skip-forever

## Blockers
