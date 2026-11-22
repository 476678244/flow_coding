---
stage: deliver
seq: 8
status: done
started_at: 2026-11-10T08:28:00+08:00
ended_at: 2026-11-10T08:30:00+08:00
---

# track · deliver · bayes-lessons

不许 skip。用户没要求不要 git commit / 开 PR。本轮不提交。

## Gate in

- [x] [07-qa-check.md](07-qa-check.md) `status=done`

## 交付

| 项 | 是否改 | 路径 / why |
| --- | --- | --- |
| docs | 否 | 合同在本夹，不另开长文 |
| guide | 否 | 无 :8000 / :5173。人在目标仓库根跑脚本 |
| product design thinking | 必写 | 人看见终端 JSON 和 `.bayes_lessons/`。今天调事实比扫整库更少。故意不做第三个命令 |

## 交人（keep 与 once 分开写）

| 段 | 写什么 |
| --- | --- |
| classify | feature · M · P1 · 日常按事实重算 |
| 夹 | `features/bayes-lessons/` |
| define | spec / acceptance / 无 HTTP / 无 demo |
| plan | 3 个里程碑；unit + regression；once 是命令缺失与无浏览器 |
| 改了 | `skills/bayes-lessons/`、本夹测试、`skills/Index.md`、`skills/Agents.md`、`.gitignore` |
| keep | 15 passed。acceptance 九条 ⬜→✅ |
| once | Phase 0 文件不存在。**未当门闩** |
| review | security / quality / performance 过 |
| 人怎么验 | 见下 |
| 未做 | 浏览器、CDP、三路服务日志。无页面可看 |

人怎么验：

1. 在一个仓库根执行 `python3 <flow_coding>/skills/bayes-lessons/scripts/bayes.py recall --about "你的问题"`，看见 `.bayes_lessons/meta.json` 和空的 `observations`。
2. 对一个已存在的源文件行执行 `note`，再开一个新终端 `recall` 同一个问题，看见刚才那条。
3. 用 `note --retracts` 点名旧 id，再 `recall`，旧 id 不在，新观察在。

## Gate out

- [x] 交人表能指到 keep 命令
- [x] once 已标明未当门闩

## Blockers
