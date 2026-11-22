# acceptance · bayes-lessons v2

合同见 [Index.md](Index.md)。只列 keep，2026-11-22 `pytest features/bayes-lessons` 59 passed 后勾选。

- [x] keep · 未知动词 `unknown-verb`；非 git 目录 `recall` 不建任何目录
- [x] keep · `note` 的标签必须属于已登记的柜子，否则 `unknown-cabinet`；柜子在哪一处登记，石头就进哪一处
- [x] keep · `--file --quote`：原文片段必须在文件里（忽略空白、`**`、wikilink），行号由脚本算；绝对路径、`..` 拒绝
- [x] keep · claim 含 因此/相当于/共识/预计/我认为 等 `inference` 拒绝，日志不变
- [x] keep · `bayesian` 必须 `--overturns`；同柜同原文 `duplicate` 拒绝
- [x] keep · `--human --quote` 留在本仓库；meta.json 写 person 与 repo；`--scope global` 被 `per-repo-only` 拒绝
- [x] keep · `recall --tag` 大类含小类、按事件时间排，返回 kind / uncertain / source.line_now
- [x] keep · `recall --q` 词都出现才命中
- [x] keep · `--retracts` 必须同柜；撤回后 recall 不返回，计入 retracted_count
- [x] keep · `link` 必须基于活着的事实；`--supersedes` 后只剩新的一句；依据被撤回时 `stale_because`
- [x] keep · `doctor` 报出处移动与丢失；`review` 轮流送回最久没看的
- [x] keep · 子目录运行写到 git 根；未启用仓库不能建仓库柜
- [x] keep · 导出页有柜子导航、link 标「不作先验」、丢失出处标红
- [x] keep · 跨进程：总本插入新周后 `line_now` 跟到新行（regression）
- [x] keep · 跨仓库隔离：a 仓库记的 Nicole 原话与 link，换到 b 仓库看不到；b 对同一件事可以有不同的 link（regression）
- [x] keep · 跨进程：被 supersede 的 link 不再出现（regression）
- [x] keep · 格物：`--when` 记事件时间，`recall` 同柜按事件时间排成一张表；`note` 返回 `look_back`（flomo 先点标签）
- [x] keep · 七彩：`recall` 返回 `colorful`，七彩超过三分之一给 `hint_colorful`；同一原文 `--retracts` 可把 bayesian 降成 fact
- [x] keep · 小乌龟：`recall` 返回 `to_verify`；样本小于 5 给「不要强行给权重」；`link` 里写 概率/百分之/主要矛盾 拒绝
- [x] keep · flomo：`link` 返回同柜其它 link 供比较深浅；`doctor` 报 `lonely_subtags`；页面有「七彩」「问号」两个镜头
- [x] keep · 元数据 / 数据分界：SKILL、templates、_template、三件套、讲稿、`.bayes_lessons*` 被 `meta-source` 拒绝；bug 记录、脚本、keep 测试可作出处
- [x] keep · `--commit SHA --quote`：原文须在提交信息里，坏 sha `bad-commit`
- [x] keep · `recall` 给出本库 `template.md` 路径；缺或有 `<填>` 时给 `hint_template`
- [x] keep · 第一性原理（共同成长，谁都不落下）：`admission = co-built` 的库拒绝普通素材（`not-co-built`），收 `--human`、`cobuilt` 共建记录、带 `--discussed` 的素材；必须 `--grows`（`no-grows` / `bad-grows`）；别名算 human
- [x] keep · `recall` 报 `growth`；最近 5 块只有一边在长时给 `hint_balance`，另一边补上后消失
- [x] keep · setup `--admission co-built --cobuilt … --alias …` 写进 meta.json；template.md 有「谁都不落下」
- [x] keep · setup 拒绝别人的仓库；自己的仓库写 cabinets.json、页面、启用说明，生成填好 person/repo 的 template.md、预置 Nicole 柜，报告 needs_migration；再跑 dry-run 无可写
