# Index · skills

Flow Coding 技能目录。先读 [Soul.md](Soul.md) 与 [Agents.md](Agents.md)，范式正文见根 [README_zh.md](../README_zh.md)。

## 先读

1. [Soul.md](Soul.md) — 这是什么、为什么做、什么算成功
2. [Agents.md](Agents.md) — 怎么选技能、怎么嵌套、什么禁止
3. 本文件 — 地图与现状

原则如果和实现细节冲突，听 Soul。约定如果和临时代码冲突，改代码，不改原则。

## 现在有什么

技能分三层。不要把学习层画进交付八段。

```
学习层    self-reflect-after-bug-fix
                ↑ deliver 关账后上来（默认）
交付层    classify → define → plan → build → verify → review → QA_Check → deliver
            │         │         └────────── new_feature_pick_and_implement ──────────┘
            └─ new_feature_req ─┘
            type=bug → new_bug_fix（已有夹 track/bug-…/，八段都走）
            type=ui 且只要设计 → ui-design-roundtable（build 前停）

验证层    flow_coding_testing  +  flow_coding_logging  +  flow_coding_chrome_cdp
```

图例：✅ 可跑（有 `SKILL.md`）。愿望不要标 ✅。

### 三件套

| 文件 | 作用 |
| --- | --- |
| [Soul.md](Soul.md) | 本目录为何存在 |
| [Agents.md](Agents.md) | 选技能、嵌套、once/keep、交人 |
| [Index.md](Index.md) | 本图 |

### 交付层

| 夹 | 作用 | 状态 |
| --- | --- | --- |
| [flow-coding-software-engineering/](flow-coding-software-engineering/SKILL.md) | 总管八段；一次一件。模板在 [templates/](flow-coding-software-engineering/templates/Index.md) | ✅ |
| [new_feature_req/](new_feature_req/SKILL.md) | classify + define；从模板建合同夹。不改产品 | ✅ |
| [new_feature_pick_and_implement/](new_feature_pick_and_implement/SKILL.md) | plan（若薄）+ build → deliver | ✅ |
| [new_bug_fix/](new_bug_fix/SKILL.md) | `type=bug` 八段；先红 keep 再修。不开新主题夹 | ✅ |

once / keep：[templates/tests.md](flow-coding-software-engineering/templates/tests.md)。

### 学习层

| 夹 | 作用 | 状态 |
| --- | --- | --- |
| [self-reflect-after-bug-fix/](self-reflect-after-bug-fix/SKILL.md) | 洞关账后：测试 / 系统 / log / 架构为何没预防；可嵌套 req | ✅ |

正文落在出洞夹 `track/bug-…/reflection.md` 与 `self-reflect.md`。

### 设计（交付前停）

| 夹 | 作用 | 状态 |
| --- | --- | --- |
| [ui-design-roundtable/](ui-design-roundtable/SKILL.md) | 真实 DOM 底板 + 功能合同 + 定版 demo。不代替 build | ✅ |

请人先读 [assets/masters.md](ui-design-roundtable/assets/masters.md)。骨架存档 [references/](ui-design-roundtable/references/)。

### 验证层

| 夹 | 作用 | 状态 |
| --- | --- | --- |
| [flow_coding_testing/](flow_coding_testing/SKILL.md) | 5 阶段算法；Playwright 截图与比对 | ✅ |
| [flow_coding_logging/](flow_coding_logging/SKILL.md) | 三路落盘与三角定位 | ✅ |
| [flow_coding_chrome_cdp/](flow_coding_chrome_cdp/SKILL.md) | 真实 Chrome CDP；默认 sync profile | ✅ |

可见面约定：Playwright TS、viewport **1920×1080**。CDP：默认 rsync 日常 profile → `Chrome-CDP`，禁止把 `--no-sync` 写成默认。

## 尚未做

- 根目录尚未写仓库级 Soul / Agents / Index——产品宪章暂以 README 为准
- 不要擅自加「智能选技能」或第十条管道

新技能：新夹 + `SKILL.md` + 本表占行。路由变了改 [Agents.md](Agents.md)。身份变了改 [Soul.md](Soul.md)。
