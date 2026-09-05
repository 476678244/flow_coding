---
stage: QA_Check
seq: 7
status: not_started
started_at:
ended_at:
---

# track · QA_Check · __feature_id__

门闩只认 **keep** 的这一次命令输出。浏览器手走若未入库，记 once，不得单独勾 ✅。

## Gate in

- [ ] [06-review.md](06-review.md) `status=done`

## keep · 质量回归（门闩）

```bash
.venv/bin/python -m pytest features/__feature_id__ -v --tb=short
.venv/bin/python -m pytest tests features -q --tb=short
```

| 套件 | 命令 | 结果（贴摘要，全文进 `test-report.md`） |
| --- | --- | --- |
| 本夹 unit + regression | | |
| 全库 | | |
| 入库 e2e | 无则 N/A | |

测试绿而产品未做（fail-fast）：`acceptance-report.md` 写 **未通过**，本段不得把 Index 标 ✅。

## once · 过程探测（不勾验收）

| 探测 | 做了 / 未做 | 证据 |
| --- | --- | --- |
| 浏览器主路径（精选 → 一条 → 来源 → 被降噪 → mute，只走碰到的步） | | |
| 一次性截图 / curl | | |

没有浏览器：写明未做。不得假装做过。once 做了也不代替 keep。

## 勾选（仅 keep 因对的原因绿）

- [ ] `acceptance.md` 对应 keep 条
- [ ] 夹内 Index 已落地
- [ ] [features/Index.md](../../../features/Index.md) 📝/⬜ → ✅

## Gate out

- [ ] `test-report.md` · `acceptance-report.md` 对照本跑次
- [ ] 未用 once 换 ✅
- [ ] 未放宽断言

## Blockers
