---
stage: plan
seq: 3
status: done
started_at: 2026-11-09T21:10:00+08:00
ended_at: 2026-11-10T08:20:00+08:00
---

# track · plan · bayes-lessons

仍不改产品。正文在 `plan.md`。两类测试见 [tests.md](tests.md)。

## Gate in

- [x] [02-define.md](02-define.md) `status=done`

## 产物

| 节 | 已写 |
| --- | --- |
| arch design pattern | 是。命令解析与折叠分开；技能只写顺序 |
| dependency | 是。无新依赖，pytest 只在本机 `.venv` |
| solution | 是。不走抓取打分管道 |
| steps_milestones | 是。三片，见 plan.md |

## 测试计划（分栏，禁止只写「加测试」）

### once · 过程探测（本轮用完即弃）

| # | 探测什么 | 手段（curl / 手点 / 一次性 PW / 日志） | 记在哪 | 不入库？ |
| --- | --- | --- | --- | --- |
| 0 | Phase 0 命令尚不存在 | 直接跑脚本，文件找不到 | `04-build.md` | 是 |
| 1 | 无 DOM，无页可看 | 不跑 Playwright | `04-build.md` | 是 |

### keep · 质量回归（入库，能红能绿）

| # | 锁什么 | 文件 | 跨边界？ |
| --- | --- | --- | --- |
| 1 | 技能顺序、拒绝、成功追加、空 recall | `test_bayes_lessons_unit.py` | 否 |
| 2 | 写盘后新进程仍能 recall；撤回后旧 id 消失 | `test_bayes_lessons_regression.py` | **是，新进程** |
| 3 | 无 DOM | N/A，不建 e2e | — |

## Gate out

- [x] keep 清单能对应到 acceptance 的 keep 条
- [x] 可见面：regression 写清哪条边界
- [x] 无 DOM：e2e 标 N/A，不是漏写

## Blockers
