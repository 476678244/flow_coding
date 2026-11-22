# Agents

<!-- bayes-lessons v2 --> 本仓已启用 `/bayes-lessons`：根上 `.bayes_lessons/` 是 Nicole 在 flow_coding 里的一份库。本仓是开发技能的仓库，**每次修洞就是一次贝叶斯更新**：洞（事件）→ 根因（事实）→ 修复（纠错）→ 反省（link）。什么算数据、放哪个柜、什么时候记，先读 [`.bayes_lessons/template.md`](.bayes_lessons/template.md)（本库的元数据框架）。

读序： [Soul.md](Soul.md) → 本文件 → [Index.md](Index.md)。选技能、嵌套、once/keep 再读 [skills/Agents.md](skills/Agents.md)。细则在 [skills/bayes-lessons/SKILL.md](skills/bayes-lessons/SKILL.md)。

在本仓工作的每一轮都做（细则以技能为准）：

1. **开工**：`recall` 列出柜子；`recall --tag` 倒出和任务相关的柜，以及本仓的 `Nicole` 柜。
2. **重算**：只用倒出来的 `facts` 在对话里判断。`links_not_prior` 是上次想过的话，只回看，不当先验。
3. **干活中**：只记 Nicole 和 agent 一起经历过的事（门槛见 template.md §0），带 `--file … --quote …` 或 `--human --quote "原话"`，并写 `--grows agent|human|both`。
4. **收工**：想出比旧 link 更深的一句，写 `link --based-on`。判断正文写进这次的工作产物，不写进石头库。

```bash
python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py recall
python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py recall --tag 柜子
python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py note --tag 柜子/小类 --when 26wXX --grows both --claim "发生了什么" --file 相对路径 --quote "原文片段"
python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py note --tag Nicole/决定 --grows agent --claim "她做了什么" --human --quote "她的原话"
python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py link --tag 柜子 --text "想过的一句" --based-on f-xxxxxx
```
