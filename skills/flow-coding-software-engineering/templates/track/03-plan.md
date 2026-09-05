---
stage: plan
seq: 3
status: not_started
started_at:
ended_at:
---

# track · plan · __feature_id__

仍不改产品。正文在 `plan.md`（S 可并 `notes.md`）。两类测试见 [tests.md](tests.md)。

## Gate in

- [ ] [02-define.md](02-define.md) `status=done`

## 产物

| 节 | 已写 |
| --- | --- |
| arch design pattern | |
| dependency | |
| solution | |
| steps_milestones | |

## 测试计划（分栏，禁止只写「加测试」）

### once · 过程探测（本轮用完即弃）

| # | 探测什么 | 手段（curl / 手点 / 一次性 PW / 日志） | 记在哪 | 不入库？ |
| --- | --- | --- | --- | --- |
| 0 | Phase 0 未改代码前的页或 API | | `04-build.md` | 是 |
| 1 | | | | 是 |

### keep · 质量回归（入库，能红能绿）

| # | 锁什么 | 文件 | 跨边界？ |
| --- | --- | --- | --- |
| 1 | 模块/API 合同 | `test___id___unit.py` | 否（unit 允许内存） |
| 2 | 看得见的 X → 边界 → 仍能做 Y | `test___id___regression.py` | **必须是** |
| 3 | 可见面 e2e（无 DOM 则删） | 本夹 `test___id___e2e.spec.ts` | 刷新后续做 |

每条 milestone 必须同时有：一次 once 探测（可选但推荐）+ 一条将红的 keep。禁止「一大坨实现完再测」。

## Gate out

- [ ] keep 清单能对应到 acceptance 的 keep 条
- [ ] 可见面：regression 写清哪条边界
- [ ] 无 DOM：e2e 标 N/A，不是漏写

## Blockers
