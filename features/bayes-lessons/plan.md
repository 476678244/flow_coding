# plan · bayes-lessons

入口 [Index.md](Index.md)。这是 define 里的里程碑草稿。`track/03-plan.md` 仍是 `not_started`，人审过合同再把 plan 段标 done。仍不改产品。

## arch design pattern

- 业务进一个可单测的 Python 模块：折叠日志、拒绝规则、追加一行。命令行只解析参数并打印 JSON。
- 技能 `skills/bayes-lessons/SKILL.md` 写日常路径和初始 investigate 的顺序，再写两个动词和拒绝清单，不写存储格式。`investigate` 不是命令。
- 配置：不新增配置。工作目录固定为当前仓库 `.bayes_lessons/`。观察只追加在其中的 `facts.jsonl`。

## dependency

无新依赖。Python 标准库。

默认禁止 Postgres / Redis / Docker / 后端 Node。这里都不引入。

## solution

不走抓取、聚类、打分那条管道。本仓没有那条管道。本功能是目标仓库上的一本追加日志，加上一个只含两个动词的技能。

## steps_milestones

| # | 切片 | once（过程探测，不入库） | keep（先红哪条，入库） | 绿了人看见什么 |
| --- | --- | --- | --- | --- |
| 1 | 技能里的日常路径、初始 investigate，以及 `note` 的拒绝与追加 | 对一个临时目录手跑一次无证据的 note，看退出码 | `test_bayes_lessons_unit.py`：两段顺序、`investigate` 不是命令、无证据、推论词、第三动词、成功追加 | 拒绝时日志不动；成功时终端有 id |
| 2 | 跨进程 `recall` | 记一条，关掉解释器，再开一次 recall | `test_bayes_lessons_regression.py`：新进程仍返回该观察；空问题返回 `[]` | 新进程打出同一条 claim |
| 3 | 撤回仍是 `note` | 手跑 `--retracts` 看旧行还在文件里 | 同一 regression：新进程的 recall 不含旧 id，含新观察 | 终端只剩还成立的那条 |

## keep · UT

`features/bayes-lessons/test_bayes_lessons_unit.py` 锁：技能正文里的日常路径和初始 investigate；`investigate` 不是命令；拒绝三条（无证据、推论词、未知动词）；一次成功追加。允许用临时目录，不要求新进程。

## keep · playwright e2e

无 DOM：`N/A`。
