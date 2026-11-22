# define · 库里存的是元数据，不是事件

status: done（2026-11-22 补记；修洞与本次 v2 重构同轮完成）

1. Symptom：flow_coding 22/22 行在讲 bayes-lessons 自己（ensure_open 在第几行、Agents.md 第几行）；投资库约 26/81 行是身份、阅读顺序、refactor。
2. Broken next step：recall 倒出来的是规则和自我描述，对认识世界和 Nicole 没有用。
3. Boundary：setup 把「这个仓库是什么」定成第一批必记样本；出处可以是任何仓库文件。
4. Acceptance after fix：看得见的一块石头 → 跨过「setup 后第一次 investigate」 → 只能是带 `--when` 的事件，出处不是方法论或规则文件。
5. Coverage gap：v1 keep 把「仓库自己写明的身份要记」锁成了合同；没有一条测试拒绝元数据出处。

Root cause：没有区分贝叶斯思维的元数据（方法、规则、模板、库自身文件）和数据（事件）；事件时间不是必填。
