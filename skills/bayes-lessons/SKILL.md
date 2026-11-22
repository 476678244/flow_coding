---
name: bayes-lessons
description: >-
  第一性原理：Nicole（zonghan / laolao）与 AI Agent 共同成长，成长的路上谁都不落下。
  Agent 的贝叶斯大脑，粒度是「一个人 + 一个仓库」：每个仓库根 .bayes_lessons/ 是 Nicole 在这个仓库里的一份库。
  先读本库的元数据框架 template.md（什么算数据、哪些柜、什么时候记），再在日常工作里捕捉具体事件数据
  （哪一周、谁、做了什么、读数多少、原文在哪），按柜子收（格物），整柜倒出来重算（致知），
  上次的结论不当先验。方法论、规则、模板是元数据，不进库。初次启用走 /bayes-lessons-setup。
  Use when the user says /bayes-lessons、贝叶斯样本、记一条事实、调出事实、先 recall、按贝叶斯更新、格物、七彩的石头。
disable-model-invocation: true
---

# /bayes-lessons

## 第一性原理

**Nicole（zonghan / laolao）与 AI Agent 共同成长，成长的路上谁都不落下。**

库里存的不是「仓库里有什么」，而是**两人一起经历过什么**：
- 一起讨论过的事件
- 她纠正 agent 的事
- 她表达过的认知
- agent 帮她看见的自己
- 修洞时一起暴露出来的根因和纠错

每块石头都要写明是谁在长（`--grows agent|human|both`）。只有一边在长的时候，`recall` 会提醒。时间越长、一起攒下的石头越多，新来的一块就越认得出是什么、不是什么。

```bash
B=/Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py
```

## 一个人 + 一个仓库

- 每个仓库根 `.bayes_lessons/` 是一份库：`meta.json` 写 `person` 和 `repo`，事件、关于 Nicole 的事、认知都只在这一份里。
- 同一个人在不同仓库**允许不同的认知**。库与库之间不自动混；以后的「碰撞」是另一件事（见路线图）。
- 没有全局库。`--scope global` 会被 `per-repo-only` 拒绝。

## 入库门槛：co-built（共建）

`meta.json` 的 `admission = co-built`（由 setup 的 `--admission co-built` 写入）时，脚本只收下面三种出处：

1. `--human --quote "她的原话"`；
2. `cobuilt` 通配匹配到的**共建记录**：
   - 投资库：阅读追问、灵魂拷问、偏差卡、验证追踪
   - 技能仓：bug 记录、keep 测试、技能脚本、commit
3. 其它素材，只有带上 `--discussed "她讨论时的原话"` 才收。

素材再多，没被一起讨论过，就不进库（`not-co-built`）。没写 `--grows` 也不收（`no-grows`）。

| `--grows` | 意思 | 例 |
| --- | --- | --- |
| `agent` | agent 被纠正、学到了 | laolao 纠正：素材不等于样本 |
| `human`（或写她的名字、别名） | 她看见了、改变了 | laolao 主动招认意愿倒灌（B-001） |
| `both` | 一起讨论，两边都更新 | 一起读 W28–30，定下「记分维度再重复一次」的确认阈值 |

`recall` 报 `growth`；最近 5 块只有一边在长，给 `hint_balance`。这是「谁都不落下」的门闩。

## 元数据和数据

| | 贝叶斯思维的**元数据** | 贝叶斯思维的**数据** |
| --- | --- | --- |
| 是什么 | 怎么想：方法、规则、柜子的定义、模板 | 想什么：已经发生的具体事件 |
| 在哪 | 南添六讲讲稿；`SKILL.md`、三件套、`README`、`entities.json`；`templates/`、`_template/`；本库的 `template.md`、`cabinets.json` | `brain.jsonl` 里的每一块石头和 link |
| 能当出处吗 | 不能（`meta-source`） | 出处是代码、测试、bug 记录、运行输出、commit、周报原文、Nicole 的原话 |

**每个库的元数据框架是 `template.md`**（由 `/bayes-lessons-setup` 从模板生成并填写）。它回答：

1. 这个仓库要认识什么
2. 数据从哪来
3. 本仓什么是元数据
4. 有哪些柜子，一块石头长什么样
5. 什么时候记
6. 认知从哪来

`recall` 不带参数时会给出它的路径；没填完会提示 `hint_template`。**开工先读它。**

两个例子：

| 仓库 | 要认识什么 | 柜子 | 最自然的记录时机 |
| --- | --- | --- | --- |
| 投资库（co-built） | laolao 和 agent 一起读市场时两边认识的变化 | 世界要闻 / 美元秩序 / 美股 / A股 / Nicole（追问、认知、纠正、看见自己…） | 周报阅读笔记、灵魂拷问、偏差卡写完；对话里讨论了总本某行 |
| flow_coding（技能仓，co-built） | 每次一起修洞暴露出的事件、根因、纠错 | 洞 / 根因 / 修复 / Nicole，小类是技能名 | `/new_bug_fix` 各段；`/self-reflect-after-bug-fix` 出 link |

## 一块石头

一块石头是**一件已经发生的事**。它要写清楚：
- 什么时候：`--when`
- 谁 / 什么
- 做了什么，或读数多少
- 原文在哪：`--file` + `--quote`、`--commit` + `--quote`、`--url` + `--quote`，或 `--human` + `--quote`

| 收 | 不收 |
| --- | --- |
| `26w40` A 股融资余额跌破 8/3 低点，25797 亿元 | 「两融见底的信号」——解释 |
| `2026-11-22` bayes-lessons：recall 换个说法返回 0 条 | 「SKILL 规定 about 整句相等」——规则 |
| `2026-11-22` 一人一仓一库隔离的 regression 转绿 | 「应该按仓库隔离」——观点 |
| `2026-11-22` Nicole 把库的粒度定为一个人加一个仓库（`--human`） | 「Nicole 偏好隔离」——推出来的性格 |

脚本挡住的情况：

| 拒绝原因 | 什么时候触发 |
| --- | --- |
| `no-when` | 没写事件时间（`--human` 不写时默认今天） |
| `meta-source` | 出处是元数据 |
| `inference` | claim 里有推论词：因此 / 所以 / 相当于 / 共识 / 预计 / 或将 / 应该 / 我认为… |
| `quote-not-found` | 文件或 commit 里找不到这段原文 |
| `unknown-cabinet` | 柜子没有登记 |

## 南添六讲 → 机制

讲稿在投资库 `assets/sources/business_analysis_bayes/`（`bab/`）。讲稿本身是元数据。

| 讲的 | 落地 |
| --- | --- |
| **格物**：按事物自己的类装进柜子，一张大表（`bab/nantian-bayesian-brain-misuse.md:76`、`:90`） | 柜子先写进 `template.md`，再登记；`recall --tag` 把这一柜按 `--when` 排成一张表 |
| **别按金字塔抓亮点**，按图索骥（同篇 `:62`、`:68`） | 沿柜子一柜一柜过材料；调料（解释、情绪）留在原文 |
| **七彩的石头**（`:78`）；四块一样留一块（`bab/nantian-bayesian-thinking-three-difficulties.md:178`） | `--kind difference`；`--kind bayesian --overturns`；`colorful`；七彩超过三分之一给 `hint_colorful`；`duplicate` |
| **小乌龟**（misuse `:132`、`:134`） | `--uncertain` → `to_verify`；`review` 先送问号；对不上就 `--retracts` |
| **致知**：样本够了答案浮出来，不强行给 60%（misuse `:116`、`:118`） | 整柜重算；样本少于 5 条给 `hint`；link 拒绝 概率 / 百分之 / 主要矛盾 |
| **flomo 先点标签**（throughline `:49`；`bab/nantian-flomo-usage-afterword.md:63-67`） | `note` 返回 `look_back`；`link` 返回同柜的其它 link，比旧的深才 `--supersedes` |
| **flomo 推送**（afterword `:53`、`:59`） | `review` |
| **flomo 标签**：用自己嚼过的词，定期清理（afterword `:88-89`） | 柜名用 Nicole 的词；`doctor` 报 `lonely_subtags` |
| **人看行为**（throughline `:69`） | 关于 Nicole 只记她做过、说过的事：`--human` |

`link` 是认知层：在 `recall` 结果里单列为 `links_not_prior`，**只回看，不当先验**；它依据的事实被撤回或原文丢失时，标 `stale_because`。

## 命令

```bash
python3 $B recall                                   # 本库：library（person/repo）、template、柜子
python3 $B recall --tag 洞 --tag 根因               # 整柜：facts / colorful / to_verify / sample_size / links_not_prior
python3 $B recall --q "两融 25797"                  # 换了说法时兜底
python3 $B note --tag 洞/bayes-lessons --when 2026-11-22 --grows agent --claim "recall 换个说法返回 0 条" \
  --file features/bayes-lessons/track/bug-2026-11-22-recall-exact-about/02-define.md --quote "少一个问号）返回 0 条"
python3 $B note --tag 修复/bayes-lessons --when 2026-11-22 --grows both --claim "…" --commit <sha> --quote "提交信息里的原文"
python3 $B note --tag Nicole/纠正 --grows agent --claim "她做了什么" --human --quote "她的原话"
python3 $B note --tag A股/走势 --when 26w40 --grows both --claim "…" --file 总本 --quote "那一行" --discussed "她讨论时的原话"
  # 可选：[--kind difference|bayesian --overturns "…"] [--uncertain] [--retracts f-…]
python3 $B link --tag 根因 --grows both --text "想过的一句" --based-on f-…,f-… [--supersedes l-…]
python3 $B cabinets --name 柜名 --desc "这一柜比什么"
python3 $B review [--n 3] [--tag 柜]
python3 $B doctor                                   # moved / lost / stale_links / lonely_subtags
python3 $B export
```

脚本自己找 git 根。`BAYES_REPO_DIR=.bayes_lessons_xxx` 可另开一份试验库；`BAYES_PERSON` 改库的主人（默认 Nicole）。

## 每一轮（已启用的仓库）

1. **开工**：`recall`，读 `template.md`，看 `growth` 和 `hint_balance`；倒出和任务相关的柜，以及 `Nicole` 柜。
2. **格物**：有新材料或新现象，按 `template.md` 的柜子一块块拣出来。
3. **致知**：只用倒出来的 `facts` 整柜重算。看 `colorful` 和 `to_verify`；样本小就说样本小。
4. **记石头**：只记一起经历过的；带 `--when`、原文、`--grows`；先看 `look_back`，不是差异就不记。Nicole 做了决定或纠正，当场用 `--human` 记下。
5. **收工**：比旧 link 更深的一句才写 `link`。判断正文写进这次的工作产物。
6. **温故**：`review` 送回来的读完；`doctor` 报 lost 就找新原文，`--retracts` 换一条。

一件事说不出哪天发生、贴不出原文、是「应该怎么做」，或者不是两人一起经历过的，就不记。

## 迁移

v1 的 `facts.jsonl` 用 `scripts/migrate_v1.py` 迁移：原文件改名 `facts.v1.jsonl`，没迁的列在 `migration_v1.json`。

## 做不到的

见效慢；给的是区间，不是你会进哪一种未来；改不了命运——别人放进他们袋子里的，是你做过的事。
