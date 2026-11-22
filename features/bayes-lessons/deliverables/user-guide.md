# bayes-lessons v2 · 使用指南

技能正文：[`skills/bayes-lessons/SKILL.md`](../../../skills/bayes-lessons/SKILL.md)。启用：[`skills/bayes-lessons-setup/SKILL.md`](../../../skills/bayes-lessons-setup/SKILL.md)。

```bash
B=/Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py
S=/Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons-setup/scripts/setup.py
```

## 0. 第一性原理

**Nicole（zonghan / laolao）与 AI Agent 共同成长，成长的路上谁都不落下。**

库里只放两人一起经历过的：
- 一起讨论过的事件
- 她纠正 agent 的事
- 她表达的认知
- agent 帮她看见的自己
- 一起修过的洞

每块写明谁在长。

## 1. 三个概念

| | 是什么 | 在哪 |
| --- | --- | --- |
| **库** | Nicole × 一个仓库。一个仓库一份，互不混 | 仓库根 `.bayes_lessons/` |
| **元数据** | 怎么想：本库的元数据框架、柜子定义、方法、规则、模板 | `template.md`、`cabinets.json`；SKILL、三件套、讲稿 |
| **数据** | 想什么：具体事件（石头）和认知（link） | `brain.jsonl` |

## 2. 给一个仓库启用

1. 先跑 `python3 $S --dry-run`，再跑 `python3 $S --admission co-built --cobuilt "共建记录通配" … --alias laolao --alias zonghan`（例子见 setup SKILL）。脚本会生成 `.bayes_lessons/`，里面有：
   - `meta.json`（person、repo）
   - `cabinets.json`（预置 `Nicole` 柜）
   - `template.md`
   - `index.html`

   如果输出 `needs_migration: true`，先跑 `migrate_v1.py`。
2. **填 `template.md`**：把 `<填>` 换成真内容，共六节——
   1. 要认识什么
   2. 数据从哪来（每行配一条真实原文）
   3. 本仓什么是元数据
   4. 柜子
   5. 什么时候记
   6. 认知从哪来

   参考已经填好的两份：
   - `flow_coding/.bayes_lessons/template.md`（技能仓，修洞）
   - `obsidian_wiki_investment/.bayes_lessons/template.md`（投资库，周报）
3. 按 template 第 4 节登记柜子：`python3 $B cabinets --name 柜 --desc "比什么"`。
4. 第一次 investigate：按第 2 节的出处、第 4 节的柜子，一件事件记一块石头。
5. `python3 $B doctor` 应当是 0 lost；再跑 `python3 $B export`，然后打开 `.bayes_lessons/index.html`。

想先试、不动原来那份库：所有命令前加 `BAYES_REPO_DIR=.bayes_lessons_template`。

## 3. 每一轮

| 时机 | 做什么 | 命令 |
| --- | --- | --- |
| 开工 | 先读 template；倒出相关柜和 Nicole 柜 | `recall`；`recall --tag 洞 --tag 根因 --tag Nicole` |
| 读材料、看现象 | 按 template 的柜子一块块拣 | — |
| 判断 | 只用 `facts` 重算；看 `colorful`、`to_verify`、`sample_size` | — |
| 记 | 只记一起经历过的；带 `--when`、原文、`--grows`；先看 `look_back` | `note … --grows agent\|human\|both` |
| 素材里的一行被一起讨论了 | 那一行 + 她的原话 | `note --file 总本 --quote … --discussed "她的原话" --grows both` |
| Nicole 做了决定或纠正 | 原话 | `note --tag Nicole/纠正 --claim "…" --human --quote "原话"` |
| 收工 | 比旧 link 更深的一句 | `link --tag 柜 --text "…" --based-on f-…` |
| 温故 | 读完送回来的几条；修 lost 和 lonely 小类 | `review --n 3`；`doctor` |

## 4. 技能仓：修洞时怎么记（flow_coding）

挂在 `/new_bug_fix` 的段上，不另开一段：

```bash
# define 写完 Symptom
python3 $B note --tag 洞/bayes-lessons --when 2026-11-22 --claim "recall 换个说法返回 0 条" \
  --file features/bayes-lessons/track/bug-2026-11-22-recall-exact-about/02-define.md --quote "少一个问号）返回 0 条"
# 根因定位
python3 $B note --tag 根因/bayes-lessons --when 2026-11-22 --claim "v1 recall 用 about 整句相等过滤" \
  --file features/bayes-lessons/track/bug-2026-11-22-recall-exact-about/02-define.md --quote "取数钥匙是整句，不是类别"
# keep 转绿
python3 $B note --tag 修复/bayes-lessons --when 2026-11-22 --claim "按柜子取的 keep 转绿" \
  --file features/bayes-lessons/test_bayes_lessons_unit.py --quote "def test_recall_q_finds_paraphrase_by_words"
#   或者用提交作出处：--commit <sha> --quote "提交信息里的一句"
# self-reflect 之后
python3 $B link --tag 根因 --text "为什么设计没提前挡住的那一句" --based-on f-…,f-…
```

## 5. 投资库：每周怎么记

每周校准总本之后，在同一次工作里，把新周二、三、五、六章的事件一柜一柜记下来：

```bash
python3 $B note --tag 美股/流动性 --when 26w47 --claim "ICI 截至 11/11 Domestic Equity 净流入 370.58 亿美元" \
  --file wiki/laolao/weekly_full_monitor_bayes_facts/weekly-full-all_weeks_all_years.md --quote "Domestic 370.58 亿，上一列仍是 308.68 亿"
```

一、四、七章（模式识别、西方共识、laolao 推演）是判断，不进库；能落到几块石头上的那一句，写成 link。

## 6. 命令速查

| 命令 | 关键输出 |
| --- | --- |
| `recall` | `library`（person / repo / admission / cobuilt / aliases）、`template`、`hint_template`、`growth`、`hint_balance`、`cabinets` |
| `recall --tag X [--tag Y]` / `--q "词 词"` | `facts`、`colorful`、`to_verify`、`sample_size`、`hint`、`hint_colorful`、`links_not_prior`、`retracted_count` |
| `note` | `id`、`line`、`look_back` |
| `link` | `id`、`other_links_same_cabinet` |
| `cabinets --name --desc` | — |
| `review [--n] [--tag]` | `review[]` |
| `doctor` | `moved`、`lost`、`stale_links`、`lonely_subtags` |
| `export` | `paths` |

出处四选一：`--file F --quote`、`--commit SHA --quote`、`--url U --quote`、`--human --quote`。

可选项：
- `--kind difference`
- `--kind bayesian --overturns "…"`
- `--uncertain`
- `--retracts f-…`（只能撤回同一柜里的；同一句原文可以用它降级）

## 7. 被拒绝时

| reason | 怎么办 |
| --- | --- |
| `not-co-built` | 这是素材，不是两人一起经历过的 | 不记；如果对话里讨论过，加 `--discussed "她的原话"` |
| `no-grows` / `bad-grows` | 没写或写错了谁在长 | `--grows agent`、`--grows human`（她的名字和别名也算）、`--grows both` |
| `unknown-cabinet` | 先找旧柜；真没有，先写进 template 第 4 节，再 `cabinets --name` |
| `no-when` / `bad-when` | 写成 `26w40` / `2026w40` / `2026-11-22` |
| `meta-source` | 出处是方法、规则或模板。换成 bug 记录、测试、代码、commit、原始材料 |
| `quote-not-found` | 原样复制原文；`**`、空白、`[[x\|y]]`、反引号会自动忽略 |
| `bad-commit` | 用 `git log` 里真实存在的 sha |
| `inference` | 去掉解释，只留发生了什么（「应该」也会被拦，引号里的也一样） |
| `bayesian-needs-overturns` | 写明改掉了哪句定性；说不清就用 fact |
| `duplicate` / `bad-retract` | 不重复记；只能撤回同一柜里的 |
| `bad-based-on` / `bad-supersedes` / `forced-weight` | link 只能挂在本库活着的事实上；不写概率 |
| `repo-not-enabled` / `per-repo-only` | 先跑 setup；不存在全局库 |

## 8. 当前状态（2026-11-22）

| 库 | 柜子（条数） | growth | 备注 |
| --- | --- | --- | --- |
| flow_coding `.bayes_lessons`（co-built） | Nicole 6 · 洞 7 · 根因 9 · 修复 6；link 2 | agent 4 · human 0 · both 2 | 6 个 bug 子夹：`features/bayes-lessons/track/bug-2026-11-22-*` |
| 投资库 `.bayes_lessons`（co-built） | Nicole 11 · 世界要闻 1 · 美元秩序 2 · 美股 5 · A股 0；link 1 | agent 2 · human 2 · both 11 | 出处：阅读笔记、灵魂拷问、偏差卡、对话原话 |
| 仓库外 `/Users/nicole/workspace/github/a476678244/_backup/investment_bayes_archives_2026-11-22/` | 素材试验库 64 块；v1 迁移库 46 条 + v1 原件 81 行 | — | 只存档，投资库根上只剩一份 `.bayes_lessons` |
| `~/.config/devin/bayes_brain.retired-2026-11-22` | — | — | 原全局库，数据已移回各仓库 |

## 9. 验证

```bash
cd /Users/nicole/workspace/github/a476678244/flow_coding
source /opt/miniconda3/etc/profile.d/conda.sh && conda activate safe_claw
python -m pytest features/bayes-lessons -q      # 59 passed
```
