# bayes-lessons

状态：v2 已落地（2026-11-22）。keep 见 [acceptance.md](acceptance.md)，`pytest features/bayes-lessons`。无 DOM，无 e2e。v1 原样备份在 `/Users/nicole/workspace/github/a476678244/_backup/bayes_v1_2026-11-22/`。

目标：Nicole 在每个仓库里和 agent 一起工作，把具体事件数据攒成这个仓库的大脑，时间越长越值钱。bug 记录在 [track/](track/Index.md) 的 `bug-2026-11-22-*` 子夹。

合同：
- 看得见的一条带原文片段的事实 → 跨过进程退出、出处文件被改（最新在上插入新周） → 仍能按柜子调出，并定位到新行或标出丢失
- 看得见的一条 Nicole 原话或 link → 跨过进程退出、换到另一个仓库 → 那个仓库看不到（一个人 + 一个仓库一份库）

| 文件 | 作用 |
| --- | --- |
| [deliverables/](deliverables/Index.md) | 设计思考、使用指南、路线图 |
| [acceptance.md](acceptance.md) | v2 keep |
| [spec.md](spec.md) | v1 规格（已被 v2 取代，留作历史） |
| [notes.md](notes.md) | v1 取舍 |
| [test_bayes_lessons_unit.py](test_bayes_lessons_unit.py) | 命令合同、setup |
| [test_bayes_lessons_regression.py](test_bayes_lessons_regression.py) | 跨进程、跨文件改动、跨仓库 |
