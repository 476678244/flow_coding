# QA_Check · __feature_id__

正式跟踪用 [track/07-qa-check.md](track/07-qa-check.md)。门闩只认 **keep**。浏览器手走是 **once**，单独不勾 ✅。

必须是**这一次**的命令输出。测试绿而产品未做：验收报告写未通过，不得勾 ✅。

```bash
.venv/bin/python -m pytest features/__feature_id__ -v --tb=short
.venv/bin/python -m pytest tests features -q --tb=short
```

有本夹 e2e：再跑 `features/__feature_id__/test___id___e2e.spec.ts`（:5173 → `/api`）。

| 门闩 | 命令 | 结果 |
| --- | --- | --- |
| 本夹 | | |
| 全库 | | |
| e2e | 无则 `N/A` | |
| 浏览器主路径 | 精选 → 一条 → 来源 → 被降噪 → mute（只走碰到的步） | 做了 / 未做（写明） |

证据：`test-report.md` · `acceptance-report.md` · 截图或真实 JSON。

门闩因对的原因绿，才勾 `acceptance.md`、夹内 Index 已落地、[features/Index.md](../Index.md) 📝/⬜ → ✅。
