---
stage: define
seq: 2
status: done
started_at: 2026-11-09T20:50:00+08:00
ended_at: 2026-11-09T21:00:00+08:00
---

# track · define · bayes-lessons

禁止写 `src/` / `frontend/src`。

## Gate in

- [x] [01-classify.md](01-classify.md) `status=done`
- [x] 三句可见即可续已有答案（或已写无 DOM）

## 产物

| 产物 | 路径 | 有 / 无 |
| --- | --- | --- |
| goal + spec | `spec.md` | 有 |
| api resp | `spec.md` §API 响应 | 有（无 HTTP；合同在 CLI） |
| acceptance | `acceptance.md`（全未勾） | 有 |
| demo html | 无 DOM，不建 `demo.html` | 无 |
| references | `references/Index.md` | 有 |
| 夹已占行 | [features/Index.md](../../Index.md) 📝/⬜ | 📝 |

## 测试（只点名，不写断言）

define **不跑**测试。`acceptance.md` 里每条必须标 `keep`。once 探测排到 build，不要写进验收当勾选项。

| 类 | 将锁什么 | 将落在哪 | 标好了？ |
| --- | --- | --- | --- |
| keep · unit | 技能正文含日常路径和初始 investigate 顺序，且不把 `investigate` 写成命令；打开即有 `.bayes_lessons/meta.json`；无出处拒绝且 `facts.jsonl` 不变；推论词拒绝；第三动词拒绝；`recall` 空结果是空数组 | `test_bayes_lessons_unit.py` | 已点名，占位 skip |
| keep · regression | 写盘 → 新进程 → 同一问题仍能调出；撤回后再开进程，旧观察不在、新观察在 | `test_bayes_lessons_regression.py` | 已点名，占位 skip |
| keep · e2e | 无 DOM | N/A | N/A |
| once | 本段不做 | — | N/A |

## Gate out

- [x] 合同句同一句出现在 Index / spec / acceptance
- [x] acceptance 条目标了 `keep`，且至少一条跨边界
- [x] 未把愿望标 ✅

## Blockers
