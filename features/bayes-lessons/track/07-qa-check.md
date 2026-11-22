---
stage: QA_Check
seq: 7
status: done
started_at: 2026-11-10T08:27:00+08:00
ended_at: 2026-11-10T08:28:00+08:00
---

# track · QA_Check · bayes-lessons

门闩只认 **keep** 的这一次命令输出。浏览器手走若未入库，记 once，不得单独勾 ✅。

## Gate in

- [x] [06-review.md](06-review.md) `status=done`

## keep · 质量回归（门闩）

```bash
.venv/bin/python -m pytest features/bayes-lessons -v --tb=short
.venv/bin/python -m pytest tests features -q --tb=short
```

| 套件 | 命令 | 结果（贴摘要，全文进 `test-report.md`） |
| --- | --- | --- |
| 本夹 unit + regression | `.venv/bin/python -m pytest features/bayes-lessons -v --tb=short` | 15 passed in 0.46s |
| 全库 | 仓库没有 `tests/`。`.venv/bin/python -m pytest features -q --tb=line` | 15 passed in 0.45s |
| 入库 e2e | 无 DOM | N/A |

## once · 过程探测（不勾验收）

| 探测 | 做了 / 未做 | 证据 |
| --- | --- | --- |
| 浏览器主路径 | 未做。无页面 | 未当门闩 |
| Phase 0 命令不存在 | 做了 | `04-build.md`。未当门闩 |

## Gate out

- [x] 本夹 keep 绿
- [x] acceptance 已勾
- [x] `features/Index.md` 与夹内 Index 已标落地

## Blockers
