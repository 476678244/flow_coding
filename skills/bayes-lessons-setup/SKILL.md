---
name: bayes-lessons-setup
description: >-
  在 Nicole 自己的一个 git 仓库上启用 /bayes-lessons，建立「Nicole + 这个仓库」的一份库：
  发现仓库根，拒绝别人的仓库，打开 .bayes_lessons/，生成并填写本库的元数据框架 template.md
  （什么算数据、哪些柜、什么时候记），定柜子，再做第一次 investigate 捕捉具体事件数据。
  Use when the user says /bayes-lessons-setup、打开 bayes lessons、建立样本库、给这个仓库启用贝叶斯。
disable-model-invocation: true
---

# /bayes-lessons-setup

启用意味着三件事都要有：
- 仓库根有 `.bayes_lessons/`，里面有 `meta.json`（person、repo）、填完的 `template.md`、至少两个柜子、第一批石头；
- 根上的页面目录写了启用说明；
- 之后每一轮按 [`/bayes-lessons`](../bayes-lessons/SKILL.md) 做。

第一性原理：Nicole（zonghan / laolao）与 AI Agent 共同成长，成长的路上谁都不落下。粒度是一个人 + 一个仓库，没有全局库。库里只放两人一起经历过的，所以默认用 `--admission co-built`。

## 1. 跑脚本

```bash
S=/Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons-setup/scripts/setup.py
python3 $S --dry-run        # 打印 root、would_write、needs_migration
python3 $S --admission co-built --cobuilt "共建记录通配" [--cobuilt …] --alias laolao --alias zonghan
#   投资库：--cobuilt "wiki/laolao/weekly_readings/weekly-reading-*.md" --cobuilt "wiki/laolao/laolao_asked/laolao_asked.md" \
#           --cobuilt "wiki/laolao/laolao_seen/b-*.md" --cobuilt "wiki/laolao/*-verification-tracker.md"
#   技能仓：--cobuilt "features/*/track/bug-*/*.md" --cobuilt "features/*/test_*.py" --cobuilt "skills/*/scripts/*.py" --cobuilt commit
```

- 只接受 origin 指向 GitHub `476678244`，或者没有 origin 且在 `/Users/nicole/workspace/github/a476678244/` 下的仓库。其它一律拒绝，不建目录。
- 脚本会写这些：
  - `.bayes_lessons/meta.json`、`cabinets.json`（空时预置 `Nicole` 柜）、`index.html`；
  - **`template.md`**：从本技能 `templates/template.md` 生成，填好 person 和 repo；开头写上 🧬 出处，链回本技能、骨架、`/bayes-lessons` 和 `bayes.py`。`meta.json` 里记 `template_from`（技能、骨架路径、骨架 sha256、生成日期）；
  - **`.bayes_lessons/Agents.md`**：给任何 agent 的入口。它写明：先照 `/bayes-lessons` 和 `/bayes-lessons-setup` 这两份技能做（给出 flow_coding 里的绝对路径）；目录里每个文件是什么；哪些不能手改。
  - `meta.json` 的 `skills`：写入技能和脚本的路径，每次 setup 都会刷新。
  - 已有的页面目录、`Soul.md`、`Agents.md` 里补启用说明（带 `bayes-lessons v2` 标记）。
- 回链：每次跑完都把这份库登记进本技能的 [`instances.md`](instances.md)（机器清单 `instances.json`），技能这一侧就能链回每一份 template。
- 脚本不写 `brain.jsonl`。
- 想先试、不动原来那份库：加 `BAYES_REPO_DIR=.bayes_lessons_template`。

`needs_migration: true` 时，先 `python3 …/bayes-lessons/scripts/migrate_v1.py --dry-run`，再正式跑。

## 2. 填元数据框架 `template.md`（最重要的一步）

`template.md` 是**本库的元数据框架**：它告诉以后每一轮的 agent，在这个仓库里什么算数据、放进哪个柜、什么时候记。它本身不是石头。读仓库自己的 `Soul.md` / `README` / 页面目录，以及真实的工作产物，把所有 `<填>` 换成真内容：

0. **第一性原理与入库门槛**：哪些文件是两人一起写下的（与 `--cobuilt` 一致）；其它素材要 `--discussed` 才进；`--grows` 怎么判。
1. **要认识什么**：一句话。
2. **数据从哪来**：真实的文件或目录，每行配一条真实的原文片段。
3. **本仓什么是元数据**：看起来像数据、其实是规则、合同或总结的东西。脚本只拦通用的那几类，本仓特有的要写清楚，靠 agent 自己分。
4. **柜子**（格物，`bab/nantian-bayesian-brain-misuse.md:90`）：先定两三个（同篇 `:125`「从两个、三个开始」），用 Nicole 的词，每柜写一块石头的样子。
5. **什么时候记**：本仓最自然的那一刻。例如投资库是「每周校准总本之后」，技能仓是「`/new_bug_fix` 的 define、根因、keep 转绿」。
6. **认知从哪来**：哪种工作会产出比过去更深的一句。

填完给 Nicole 看，她点头后上锁：`python3 /Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py template --approve --quote "她的原话"`。上锁之后 template 是不可改的元数据，以后学到的东西一律记成数据。拿不准就问 Nicole，不要编。

## 3. 登记柜子

```bash
B=/Users/nicole/workspace/github/a476678244/flow_coding/skills/bayes-lessons/scripts/bayes.py
python3 $B cabinets --name 洞 --desc "看得见的现象：哪个技能、什么时候、人看见了什么、下一步断在哪"
```

和 `template.md` 第 4 节保持一致。

## 4. 第一次 investigate：捕捉具体事件数据

1. 写下问题：**在这个仓库里，Nicole 和 agent 一起经历过哪些事？**素材再多，没一起讨论过的不记。
2. 在对话里说出动手前的旧信念。这句不 `note`。
3. 按 `template.md` 第 2 节的出处、第 4 节的柜子，一柜一柜地过原文。每件事件单独记：`note --tag 柜/小类 --when … --claim 冷的事实 --file … --quote …`。
   - 技能仓：bug 记录（`features/<id>/track/bug-*/02-define.md`、`04-build.md`）、keep 测试、commit。
   - 投资库：周报阅读笔记、灵魂拷问、偏差卡、验证追踪，以及对话里她的原话。**不是**周报总本本身。
   - 每块写 `--grows`。记完看 `growth`：哪一边是 0，就说出来。
4. 每个柜 `recall --tag` 一遍，看 `colorful` 和 `to_verify`。说完判断即弃。
5. `doctor` 应当 0 lost；`export` 之后打开页面看一眼。

## 5. 收尾

`recall` 列得出 library、template（没有 `hint_template`）、柜子，各柜都有石头，就交回 `/bayes-lessons`。没有石头时，页面写「还没有事实」，不要编一条。
