# 贝叶斯思维的元数据 · Nicole × flow_coding

> 本文件是**元数据**：告诉 agent 在这个仓库里什么算数据、放进哪个柜、什么时候记。它本身不是石头，不能当出处。
> 数据只在同目录 `brain.jsonl`。柜子的机器清单在 `cabinets.json`，和第 4 节保持一致。
> 粒度是「Nicole + flow_coding」：这里的事实和认知只属于这一份库，别的仓库可以不同。

## 0. 第一性原理与入库门槛

**laolao（Nicole / zonghan）与 AI Agent 共同成长，成长的路上谁都不落下。**

这个仓库里的「一起」就是一起修洞：她看见洞、纠正设计，agent 定位根因、写 keep、改对，最后一起反省。只记这些。技能说明、合同、总结不算。

- 门槛：`admission = co-built`。
- 共建记录（`cobuilt`）：
  - `features/*/track/bug-*/*.md`
  - `features/*/test_*.py`
  - `skills/*/scripts/*.py`
  - `commit`
  - 以及 `--human` 原话
- `--grows`：
  - `agent`：agent 被纠正、学到了。多数洞是这一类。
  - `human`：laolao 在修洞里看见、改变了什么。
  - `both`：一起定下的修法或原则。
- 现状：`growth` 里 `human` 还是 0。修洞时要问一句：laolao 这次看见了什么？

## 1. 这个仓库要认识什么

这是开发技能的仓库。要认识的是**每一次修洞里暴露出来的事件、根因和纠错**：哪个技能、什么时候、人看见了什么、断在哪、为什么、怎么改对的；以及 Nicole 在过程中的决定和纠正。

修洞就是一次贝叶斯更新：洞是事件（多数是噪音，先记现象），根因是正在起作用的事实，修复是纠错的行为，反省得出的那一句是认知。

## 2. 数据从哪来（出处）

| 出处 | 例子 | 通常进哪个柜 |
| --- | --- | --- |
| bug 记录 `features/<id>/track/bug-<日期>-<slug>/02-define.md` 的 Symptom / Root cause | `recall --about "美股指数怎么走"`（少一个问号）返回 0 条 | 洞、根因 |
| 同一子夹 `04-build.md` 的 red 复现与 green keep | `{"about": "美股指数怎么走", "observations": []}` | 洞（red）、修复（green） |
| keep 测试文件 `features/<id>/test_*_regression.py`、`test_*_unit.py` | `def test_each_repo_keeps_its_own_nicole_and_its_own_cognition` | 修复 |
| 技能脚本 `skills/<name>/scripts/*.py`（代码是状态，配合洞或修复用） | `if meta_source(rel):` | 根因、修复 |
| git commit（`--commit SHA --quote`） | 修复落地的那一次提交信息 | 修复 |
| 运行输出、日志（`real-run.txt`、`logs/`） | 真实跑出来的那一行 | 洞 |
| 对话里 Nicole 的原话（`--human`） | 她的决定、纠正、否掉、坚持 | Nicole；她指出的洞也进 洞 |

## 3. 什么是元数据（不进库，脚本会以 `meta-source` 拒绝）

- 方法：南添六讲讲稿（`business_analysis_bayes`）
- 规则：`SKILL.md`、`AGENTS.md` / `Soul.md` / `Index.md`、`README`、`entities.json`
- 模板：`templates/`、`_template/`、本文件，以及整个 `.bayes_lessons*`
- 本仓特有：`spec.md`、`acceptance.md`、`plan.md`、`deliverables/` 是合同和总结，不是事件——脚本拦不住，靠 agent 自己分。技能说明里「应该怎么做」永远是元数据；只有「某天跑起来实际发生了什么」才是数据。

## 4. 柜子（格物：按事物自己的类）

小类一律用技能名（例 `bayes-lessons`、`flow-vedio`）。同一个根因在不同技能里重复出现，整柜倒出来就看得见。

| 柜 | 比什么 | 小类（用自己的词） | 一块石头的样子（`--when` + claim） |
| --- | --- | --- | --- |
| Nicole | Nicole 在 flow_coding 里做过、说过的事 | 决定 / 纠正 / 否掉 / 目标 | `2026-11-22` 她把库的粒度定为一个人加一个仓库 |
| 洞 | 看得见的现象：人看见了什么、下一步断在哪 | 技能名 | `2026-11-22` bayes-lessons：recall 换个说法返回 0 条 |
| 根因 | 正在起作用的原因：哪行代码、哪条合同、哪条测试把错锁成了对 | 技能名 | `2026-11-22` bayes-lessons：v1 recall 用 about 整句相等过滤 |
| 修复 | 纠错落地：keep 红转绿、commit、数据迁移 | 技能名 | `2026-11-22` bayes-lessons：test_recall_q_finds_paraphrase_by_words 转绿 |

新柜先写进这张表，再 `bayes.py cabinets --name 柜 --desc "比什么"`。新概念优先并进旧柜。

## 5. 什么时候记（触发时机）

挂在 [`/new_bug_fix`](../skills/new_bug_fix/SKILL.md) 的段上，不另开一段管道。

| 时机 | 记什么 | 命令要点 |
| --- | --- | --- |
| 每一轮开工 | 不记；先 `recall --tag 洞 --tag 根因`，看同类洞以前怎么来的；再倒 `Nicole` 柜；看 `growth` | `recall --tag …` |
| define 写完 Symptom | 洞：现象 | `note --tag 洞/<技能> --when <日期> --file …/02-define.md --quote …` |
| build 跑出 red | 洞补一块：复现输出（`--uncertain` 直到 keep 能锁住） | `--file …/04-build.md` |
| 根因定位 | 根因 | `note --tag 根因/<技能> …`；改掉了旧认识用 `--kind bayesian --overturns` |
| keep 转绿 / deliver | 修复 | `note --tag 修复/<技能> --file test_*.py` 或 `--commit` |
| Nicole 做了决定或纠正 | 她的原话；她指出的洞同时记进 洞 | `--human --quote` |
| self-reflect 之后 | 「设计为什么没提前挡住」那一句 | `link --tag 根因 --based-on 洞…,根因…` |

## 6. 认知（link）从哪来

[`/self-reflect-after-bug-fix`](../skills/self-reflect-after-bug-fix/SKILL.md) 的结论：为什么现有测试 / 系统 / 日志 / 架构设计没提前挡住这个洞。只写比上一句更深的；同一类根因第二次出现时，用 `--supersedes` 把旧 link 换成更深的那句。

link 只回看，不当先验；依据被撤回时会标 `stale_because`。
