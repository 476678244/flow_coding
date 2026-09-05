---
stage: build
seq: 4
status: not_started
started_at:
ended_at:
---

# track · build · __feature_id__

Phase 0 再按 milestone：once 探测 → 红 keep → 实现 → 绿 keep。禁止用 once 绿代替 keep。

## Gate in

- [ ] [03-plan.md](03-plan.md) `status=done`（`type=docs` 且无代码可 skipped）
- [ ] 夹齐（`Index` · `spec` · `acceptance` · `references/`）

## once · 过程探测（本轮）

| # | 何时 | 做了什么 | 证据（命令/截图/日志路径） | 不入库 |
| --- | --- | --- | --- | --- |
| 0 | Phase 0 未改代码 | | | 是 |
| 1 | milestone 1 手测 / curl | | | 是 |

TDD **跑次**记上面。不要把探路脚本提交进默认套件。

## keep · 质量回归（入库文件）

| # | 文件::用例 | 先红（命令+结果） | 实现触点 | 后绿（命令+结果） | 跨边界 |
| --- | --- | --- | --- | --- | --- |
| 1 | `test___id___unit.py`:: | | | | |
| 2 | `test___id___regression.py`:: | | | | 写盘→新 app |

## 自检

| 项 | 结论 |
| --- | --- |
| 简化（能删的层 / 多余依赖） | |
| fail fast（空头诚实、单源不拖垮） | |
| 性能（默认不做） | |

## Gate out

- [ ] 计划内 keep 已落成真文件，能红能绿
- [ ] once 未冒充门闩
- [ ] 未 skip-forever

## Blockers
