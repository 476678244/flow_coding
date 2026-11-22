---
stage: verify
seq: 5
status: done
started_at: 2026-11-10T08:25:00+08:00
ended_at: 2026-11-10T08:26:00+08:00
---

# track · verify · bayes-lessons

先跑 keep，对不上号再用 once 三角定位。acceptance **先记后勾**。

## Gate in

- [x] [04-build.md](04-build.md) `status=done`

## keep · 质量回归（必须跑）

```bash
.venv/bin/python -m pytest features/bayes-lessons -v --tb=short
```

| 项 | 结论 | 证据 |
| --- | --- | --- |
| unit | 13 passed | 2026-11-10 本次输出，见 `test-report.md` |
| regression | 2 passed。写盘的进程退出后，另一个 `python` 进程 `recall` | 同上 |
| acceptance 对照 | 九条 keep 都有对应用例。写入 `acceptance-report.md` 后再勾 | |

## once · 过程探测（仅当 keep 不够定位）

| 现象 | 手段（页/API · frontend 日志 · backend 日志） | 结论 | 会不会改成 keep？ |
| --- | --- | --- | --- |
| 无失败需要定位 | 无页、无 `logs/ui.log`、无 `logs/server.log`。行为信号就是 pytest 看到的 stdout JSON | 不猜。三路日志技能在此没有服务可看 | 否 |

## 其它

| 项 | 结论 |
| --- | --- |
| anti fragile | 创建过的 `facts.jsonl` 在新进程里还在。拒绝写入不改已有字节。不是「文件从未出现所以失败」冒充持久 |
| dependency | 无新增产品依赖 |

## Gate out

- [x] keep 绿，且 regression 真跨进程
- [x] acceptance-report 已写，勾选在 QA

## Blockers
