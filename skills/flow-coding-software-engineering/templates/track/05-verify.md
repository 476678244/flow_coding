---
stage: verify
seq: 5
status: not_started
started_at:
ended_at:
---

# track · verify · __feature_id__

先跑 keep，对不上号再用 once 三角定位。acceptance **先记后勾**。

## Gate in

- [ ] [04-build.md](04-build.md) `status=done` 或规则允许的 skipped

## keep · 质量回归（必须跑）

```bash
.venv/bin/python -m pytest features/__feature_id__ -v --tb=short
```

| 项 | 结论 | 证据 |
| --- | --- | --- |
| unit | | 完整输出，禁止凭记忆 |
| regression | | 必须是写盘 → 新连接 / 新 `create_app` → 下一步仍成立 |
| acceptance 对照 | 写入 `acceptance-report.md`，**先不勾** | |

## once · 过程探测（仅当 keep 不够定位）

| 现象 | 手段（页/API · frontend 日志 · backend 日志） | 结论 | 会不会改成 keep？ |
| --- | --- | --- | --- |
| | | | 本轮新洞 → 先补 keep 再修，或转 `/new_bug_fix` |

## 其它

| 项 | 结论 |
| --- | --- |
| anti fragile | 可见即可续成立；无「从未创建」冒充 persist |
| dependency | plan 依赖属实、无能删未删、无密钥入库 |

## Gate out

- [ ] keep 绿，且绿的原因对
- [ ] once 若做过，未当作验收证据
- [ ] 本轮洞已补 keep 或已转 bug

## Blockers
