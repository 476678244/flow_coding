---
stage: classify
seq: 1
status: done
started_at: 2026-11-09T20:47:00+08:00
ended_at: 2026-11-09T20:50:00+08:00
---

# track · classify · bayes-lessons

## Gate in

- [x] 已读 Soul · Agents · [features/Index.md](../../Index.md)
- [x] 已问：更少更准，还是管子加粗？

## 字段

| 项 | 值 |
| --- | --- |
| type | feature |
| complexity | M |
| urgency_priority | P1 |
| ROI | 日常开发和 工作按同一条路径认识世界：先调事实、当次重算、只记带出处的新事实。跨进程还在。第一版只有 note / recall，柜子、事件、哈希都不做，管子不加粗。 |

| 可见即可续 | 答 |
| --- | --- |
| 人看见什么 | 打开技能后，目标仓库根上出现 `.bayes_lessons/`。终端里一条 `note` 的成功 JSON，以及该目录里 `facts.jsonl` 的一行。之后 `recall` 把还成立的观察打回终端。 |
| 看见之后下一步 | 按这些观察继续当前问题（改代码、下判断）。调出的结果里没有「因此」。 |
| 哪条边界会丢状态 | 进程退出再启动。同进程内存不算。无 DOM。 |

## 测试（本段无）

classify 不写测试。不把「心里有数」当成 once。

## Gate out

- [x] 上表填完
- [x] `ROI=拒绝` 已停并交人，**或** ROI 成立
- [x] 下一跳已写：define / `/new_bug_fix` / ui-design-roundtable / 停

下一跳：define（本夹）。不改 `src/` / `frontend/`。实现留到人审过合同之后。

## Blockers
