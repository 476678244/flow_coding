# 贝叶斯思维的元数据 · @@PERSON@@ × @@REPO@@

> 🧭 **先照技能做（任何 agent 读到这里都一样）**：这一份库是 agent 技能建立的。具体工作怎么进行，以 flow_coding 仓库里的两份 agent 技能为准：
> - 每一轮工作（recall / note / link / review / doctor），照 [`/bayes-lessons`](file://@@BAYES_SKILL@@) 做，路径 `@@BAYES_SKILL@@`；
> - 启用、重建、补框架、迁移，照 [`/bayes-lessons-setup`](file://@@SETUP_SKILL@@) 做，路径 `@@SETUP_SKILL@@`。
> - 脚本：`python3 @@BAYES_PY@@`。
>
> 本文件由 setup 按骨架 [`templates/template.md`](file://@@SKELETON@@) 生成，生成记录在 `meta.json` 的 `template_from`；同目录的 `Agents.md` 是给 agent 的入口说明。

> 🔒 **本文件不可改。** 它是本库的元数据框架，规定什么算数据、放哪个柜、什么时候记；它不是记事本。
> - 工作中学到的新东西——包括关于 @@PERSON@@ 的称呼、偏好、纠正、决定——一律**记成数据**：`note --human --quote "她的原话"` 或 `note --file … --quote …`。不要写进本文件。
> - 只有 @@PERSON@@ 明确说「改 template / 改框架」时才改。改完跑 `bayes.py template --approve --quote "她的原话"`，脚本会记一块 `@@PERSON@@/决定`、更新 `meta.json` 的 `template_sha256`，并把本文件设为只读。
> - 没经批准的改动，`recall` 会报 `hint_template_changed`，`doctor` 会报 `template.changed`。遇到时先恢复本文件，再把那条新内容记成数据。

> 本文件是**元数据**：告诉 agent 在这个仓库里什么算数据、放进哪个柜、什么时候记。它本身不是石头，不能当出处。
> 数据只在同目录 `brain.jsonl`。柜子的机器清单在 `cabinets.json`，和第 4 节保持一致。
> 粒度是「@@PERSON@@ + @@REPO@@」：这里的事实和认知只属于这一份库，别的仓库可以不同。
> 带 `<填>` 的地方没填完之前，`recall` 会提醒先填本文件。

## 0. 第一性原理与入库门槛

**@@PERSON@@ 与 AI Agent 共同成长，成长的路上谁都不落下。**

库里只放两人一起经历过的：
- 一起讨论过的事件
- @@PERSON@@ 纠正过 agent 的事
- @@PERSON@@ 表达过的自己的认知
- agent 帮 @@PERSON@@ 看见的东西

素材再多，没被一起讨论过，就不进库。

- 门槛（`meta.json` 的 `admission`）：<填：co-built 或 open>
- 共建记录（`meta.json` 的 `cobuilt`，fnmatch 通配）：<填：哪些文件是两人一起写下的，例如阅读追问、灵魂拷问、偏差卡、bug 记录>
- 其它素材要进库，`note` 时加 `--discussed "@@PERSON@@ 讨论时的原话"`
- 每块写 `--grows`：
  - `agent`：agent 被纠正 / 学到
  - `human`：@@PERSON@@ 看见 / 改变了什么
  - `both`：一起讨论后两边都更新
- `recall` 会报 `growth`；最近几块只有一边在长时，给出 `hint_balance`

## 1. 这个仓库要认识什么

<填：一句话。投资库例：市场里正在起作用的事件；技能仓例：每次修洞里暴露出来的事件、根因和纠错>

## 2. 数据从哪来（出处）

| 出处 | 例子 | 通常进哪个柜 |
| --- | --- | --- |
| <填：文件或目录> | <填：一条真实的原文片段> | <填> |
| 对话里 @@PERSON@@ 的原话（`--human`） | 她的决定、纠正、否掉、坚持 | `@@PERSON@@` |

## 3. 什么是元数据（不进库，脚本会以 `meta-source` 拒绝）

- 方法：南添六讲讲稿（`business_analysis_bayes`）
- 规则：`SKILL.md`、`AGENTS.md` / `Soul.md` / `Index.md`、`README`、`entities.json`
- 模板：`templates/`、`_template/`、本文件，以及整个 `.bayes_lessons*`
- <填：本仓特有的、看起来像数据其实是元数据的东西，没有就删掉这一行>

## 4. 柜子（格物：按事物自己的类）

| 柜 | 比什么 | 小类（用自己的词） | 一块石头的样子（`--when` + claim） |
| --- | --- | --- | --- |
| @@PERSON@@ | @@PERSON@@ 在 @@REPO@@ 里做过、说过的事 | 决定 / 纠正 / 否掉 / 目标 | `2026-11-22` 她把库的粒度定为一个人加一个仓库 |
| <填> | <填> | <填> | <填> |

新柜先写进这张表，再 `bayes.py cabinets --name 柜 --desc "比什么"`。新概念优先并进旧柜。

## 5. 什么时候记（触发时机）

| 时机 | 记什么 | 命令要点 |
| --- | --- | --- |
| 每一轮开工 | 不记；先 `recall`，倒出相关柜和 `@@PERSON@@` 柜 | `recall --tag …` |
| <填：本仓最自然的那一刻，例如每周校准总本后、修洞 deliver 时> | <填> | `note --when … --quote …` |
| @@PERSON@@ 做了决定或纠正 | 她的原话 | `note --tag @@PERSON@@/… --human --quote` |
| 收工 | 比旧 link 更深的一句 | `link --based-on …` |

## 6. 认知（link）从哪来

<填：在这个仓库里，哪种工作会产出「比过去更深的一句」。例：周报第七章推演之后；修洞后的反省>

link 只回看，不当先验；依据被撤回时会标 `stale_because`。
