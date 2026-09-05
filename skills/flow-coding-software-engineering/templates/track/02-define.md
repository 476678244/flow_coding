---
stage: define
seq: 2
status: not_started
started_at:
ended_at:
---

# track · define · __feature_id__

禁止写 `src/` / `frontend/src`。

## Gate in

- [ ] [01-classify.md](01-classify.md) `status=done`
- [ ] 三句可见即可续已有答案（或已写无 DOM）

## 产物

| 产物 | 路径 | 有 / 无 |
| --- | --- | --- |
| goal + spec | `spec.md` | |
| api resp | `spec.md` §API 响应 | |
| acceptance | `acceptance.md`（全未勾） | |
| demo html | `demo.html` 或 `ui-design/ideas/…`（无 DOM 则 skipped） | |
| references | `references/Index.md` | |
| 夹已占行 | [features/Index.md](../../../features/Index.md) 📝/⬜ | |

## 测试（只点名，不写断言）

define **不跑**测试。`acceptance.md` 里每条必须标 `keep`。once 探测排到 build，不要写进验收当勾选项。

| 类 | 将锁什么 | 将落在哪 | 标好了？ |
| --- | --- | --- | --- |
| keep · unit | | `test___id___unit.py` | |
| keep · regression | 写盘 → 新连接 / 新 `create_app` → 仍能做 Y | `test___id___regression.py` | |
| keep · e2e | 无 DOM 则 N/A | 本夹 `test___id___e2e.spec.ts` | |
| once | 本段不做 | — | N/A |

## Gate out

- [ ] 合同句同一句出现在 Index / spec / acceptance
- [ ] acceptance 条目标了 `keep`，且至少一条跨边界
- [ ] 未把愿望标 ✅

## Blockers
