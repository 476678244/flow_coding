# bayes-lessons v2 · 设计思考

日期：2026-11-22。范围：`skills/bayes-lessons/`、`skills/bayes-lessons-setup/`、两个仓库根 `.bayes_lessons/`、`new_bug_fix` / `self-reflect-after-bug-fix` 的挂点。

## 0. 第一性原理

> 最终最终的目标：第一性原理：nicole(zonghan/laolao) 与 AI Agent 共同成长，成长的路上谁都不落下。

下面所有决定都从这一句推出来：
- 库里只放两人一起经历过的。
- 每块石头写明是谁在长。
- 只有一边在长的时候，系统要说出来。

## 1. 要解决的问题

本轮 Nicole 给了六句话，设计按顺序被它们推着走：

1. 「希望 agent 能建立自己的贝叶斯思维……时间越长，积累的事实越多，这个 agent 的大脑越有价值。」
2. 「注意这是方法论，与元数据相关。我们要用 bayes lessons skill 捕捉的是具体的事件数据。」
3. 「我希望的是每个 repo 有自己的库……粒度是一个人（Nicole）+ 一个 repo 级别的。一个人在不同的 repo 允许不同的认知。」
4. 「要特别分清楚什么是贝叶斯思维的元数据，什么是贝叶斯思维的数据……开发 skills 的 repo，每一次 bug fix 就是建立贝叶斯事实、事件、认知、纠错的好时机。」以及「template 是非常重要的 guide agent on the setup 元数据框架的方式，需要转正。」
5. 「素材里有很多很多的贝叶斯样本，但是我们不能把每一个样本都加进来……只有 laolao 与 agent 讨论过的贝叶斯事件，或者 laolao 纠正过 agent 的事情，或者 laolao 表达过的自己的认知理解，我们才记录下来。」
6. 「第一性原理：nicole(zonghan/laolao) 与 AI Agent 共同成长，成长的路上谁都不落下。」

一句话目标：**每个仓库一份「Nicole × 仓库」的库，先有元数据框架（template.md），只收两人一起经历过的具体事件，写明谁在长，按类攒起来；要判断时整柜倒出来重算。**

## 2. v1 为什么效果不好

这一节也是 flow_coding 库里的第一批石头。证据在 `features/bayes-lessons/track/bug-2026-11-22-*`。

| 洞 | 证据 | 根因 |
| --- | --- | --- |
| recall 换个说法就取不到 | 少一个问号的「美股指数怎么走」返回 0 条 | 取数钥匙是 `about` 整句，不是类别；keep 把「换说法为空」锁成了正确行为 |
| 出处行号漂移 | 约 15 条指向空行；v1 复现：插入两周后仍报 `weekly.md:1` | 出处存行号不存原文，note 之后从不复查 |
| 71/81 进了未分类 | 导出页统计 | 标签不是必填项，问句 about 过不了形状检查 |
| 库里存的是元数据 | flow_coding 22/22 行在讲技能自己；投资库约 26/81 行是身份、阅读顺序 | 没区分元数据和数据；keep 把「身份要记」锁成了合同 |
| v2 中途放了全局大脑 | Nicole 的纠正 | 把「跨仓库都用得上」当成了「应该共享」（bayesian：改掉了这条设计定性） |
| 投资库把素材当成了共建样本 | 第一次 investigate 从周报总本批量记了 62 块；laolao 的纠正 | 入库门槛只问「是不是事件」，没问「是不是两人一起经历过」 |

flow_coding 库里由这三条「keep 把错的设计锁成了合同」得出的 link：

> 三个洞里 keep 都把当时的设计句锁成了合同（换说法为空、身份必记、Nicole 跟进别的仓库）：测试问的是「实现符不符合我写的规则」，没问「人要的下一步还在不在」。

> 元数据混入、全局大脑、素材当样本这三次，都是 agent 从仓库和系统出发设计（什么都能存、哪里都能用、仓库里有就算），没从「laolao 和 agent 一起经历过什么」出发。

## 3. 原则

0. **共建才入库，谁都不落下**：`admission = co-built`。只收三类：她的原话；共建记录里的行（阅读追问、灵魂拷问、偏差卡、验证追踪、bug 记录、keep 测试、commit）；带她讨论原话（`--discussed`）的素材。每块写 `--grows agent|human|both`。`recall` 报 `growth`，只有一边在长时报 `hint_balance`。
1. **一个人 + 一个仓库一份库**：`meta.json` 写 person 和 repo。同一个人在不同仓库允许不同的认知。没有全局库。
2. **元数据和数据分开**：
   - 元数据 = 怎么想。包括方法（六讲讲稿）、规则（SKILL、三件套、README、entities）、模板（`templates/`、`_template/`），以及库自己的 `template.md` 和 `cabinets.json`。
   - 数据 = 想什么，即已经发生的具体事件。
   - 元数据不能当出处。
3. **template.md 是每个库的元数据框架**，由 setup 生成、agent 填写。它规定这个仓库里什么算数据、从哪来、有哪些柜、什么时候记、认知从哪来。agent 每一轮先读它。
4. **石头是具体事件**：`--when` 必填，原文必贴（文件片段、commit、网页、Nicole 原话）。
5. **格物在前**：柜子先写进 template，再登记；柜名用 Nicole 的词。
6. **整柜重算，不调结论**；link 单独一层，只回看，不当先验。
7. **只追加**：用 `--retracts` 纠错，用 `--supersedes` 换认知。

## 4. 关键决策

| 决策 | 选择 | 谁定 | 放弃的选项 |
| --- | --- | --- | --- |
| 库的粒度 | 一个人 + 一个仓库；去掉全局库 | Nicole（推翻了此前「全局 + 各仓库」） | 全局共享——认知会被混在一起，以后也没法做库与库碰撞 |
| 认知层 | `link`，单列 `links_not_prior` | Nicole | 结论说完即弃——跨会话的 agent 会每次从零开始 |
| 触发 | 只在启用的仓库，靠根上 `AGENTS.md`，以及技能仓里挂在 `new_bug_fix` / `self-reflect` 上 | Nicole | 全局常驻规则；只在点名时触发 |
| 元数据框架 | `template.md`（技能里有空模板，setup 生成，agent 填写；`recall` 有提示） | Nicole（「template 需要转正」） | 只靠 SKILL 文字——各仓库都不一样，通用规则写不出来 |
| 元数据出处 | `meta-source` 只拦方法、规则、模板、`.bayes_lessons*`；代码、测试、bug 记录、commit 可以当出处 | agent，回应「分清元数据和数据」 | 一刀切拦掉 `skills/`、`features/`——技能仓的 bug 记录就进不来了 |
| 新出处类型 | `--commit SHA --quote` | agent，为修洞场景 | 只认文件 |
| 技能仓的柜子 | 洞（事件）/ 根因（事实）/ 修复（纠错）/ Nicole，小类是技能名 | agent，回应「bug fix 是好时机」 | 按根因类型分小类——那是判断，放进 link 更合适 |
| 投资库 | 先把试验库转正；被纠正「素材不等于样本」后按 co-built 重建；最后 Nicole 定「只留一份最终的 `.bayes_lessons`」，试验库和 v1 迁移库移出仓库存档 | Nicole | 逐条撤回 62 块（这份库从头到尾都不是共建的）；仓库里并存多份库 |
| 入库门槛 | `admission = co-built` 写进 meta.json；共建记录用 fnmatch 通配；其它素材要 `--discussed` | Nicole（「只有 laolao 与 agent 讨论过的……才记录」） | 只靠 SKILL 文字——agent 会把素材当样本 |
| 谁在长 | `--grows` 必填；`growth` 计数；最近 5 块只有一边时给 `hint_balance` | Nicole（「谁都不落下」） | 不记方向——两边谁落下都看不见 |
| 取数钥匙 | 柜子 / 小类 + `--q` 兜底 | agent | about 整句；向量检索 |
| 出处定位 | 原文片段；多处匹配时取离旧行最近的那处 | agent | 行号；哈希 |
| bayesian 门槛 | 必须 `--overturns` | agent | 不设门槛 |

## 5. 修洞就是一次贝叶斯更新（技能仓）

| 修洞的段（`/new_bug_fix`） | 贝叶斯里的位置 | 记成 |
| --- | --- | --- |
| 看见现象，define 写 Symptom | 事件：掉下来的那一下，先不解释 | `洞/<技能>`，出处 `02-define.md` |
| build 复现出 red | 事件的确认 | `洞/<技能>`，出处 `04-build.md` |
| 定位根因、Coverage gap | 正在起作用的事实；改掉旧定性的标 bayesian | `根因/<技能>` |
| keep 转绿、commit | 纠错的行为 | `修复/<技能>`，出处是 keep 测试或 `--commit` |
| self-reflect 四问 | 认知：为什么设计没提前挡住 | `link --tag 根因 --based-on …` |
| Nicole 纠正 | 人的行为 | `Nicole/纠正`（她指出的洞同时进 `洞`） |

`recall --tag 根因` 会把所有技能的根因按时间排成一张大表。同类根因第二次出现时，它在这一柜里就是七彩那块，`link --supersedes` 把认知推深一层。

## 6. 南添六讲 → 机制

见 [`skills/bayes-lessons/SKILL.md`](../../../skills/bayes-lessons/SKILL.md)「南添六讲 → 机制」一节，每一行都带讲稿行号。讲稿是元数据，只用来指导做法。

## 7. 实施结果（2026-11-22）

| 库 | 门槛与共建记录 | 柜子 | 数据 | growth |
| --- | --- | --- | --- | --- |
| 投资库 `.bayes_lessons`（co-built 重建） | 周报阅读笔记、灵魂拷问、偏差卡、验证追踪、reading-* | Nicole 11 · 世界要闻 1 · 美元秩序 2 · 美股 5 · A股 0 | 15 块 + 1 条 link。来源：laolao_asked 4、偏差卡 2、阅读笔记 26w28/26w30 5、对话原话 4；15 条出处全部能定位 | agent 2 · human 2 · both 11 |
| flow_coding `.bayes_lessons`（co-built） | bug 记录、keep 测试、技能脚本、commit | Nicole 6 · 洞 7 · 根因 9 · 修复 6 | 6 个 bug 子夹 → 28 块 + 2 条 link；0 lost | agent 4 · human 0 · both 2（其余是加门槛前的旧行） |
| 仓库外存档 `/Users/nicole/workspace/github/a476678244/_backup/investment_bayes_archives_2026-11-22/` | — | — | `.bayes_lessons_material_trial`（素材 62 块 + 另一会话的 2 块素材）、`.bayes_lessons_v1migrated`（v1 原 `facts.v1.jsonl` 81 行 + 迁移 46 条）。投资库根上只剩一份 `.bayes_lessons` | — |

验证：门槛生效——在投资库直接拿总本一行去 note，被拒为 `not-co-built`。

两个读数要说出来：
- flow_coding 里 `human` 是 0。修洞时 laolao 自己看见了什么，还没被记下来。
- 投资库的 A股 柜是空的：共建记录里还没有和 A 股一起讨论过的事件。

## 8. 刻意不做的

- 不做库与库碰撞的实现（Nicole 说「未来」）。数据模型已经为它准备好：每个库有 person、repo，每条有 when、出处、kind。
- 不做向量检索，不加权重字段，不从总本或 bug 记录自动批量抽取——拣不拣、进哪一柜，本身就是格物。
- 不写进 git，不改 git 配置。
