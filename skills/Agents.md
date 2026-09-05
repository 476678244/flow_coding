# Agents · skills

在 `skills/` 里工作前，先读本目录 [Soul.md](Soul.md)。目录与阅读顺序见 [Index.md](Index.md)。

产品仓若另有根 `Soul.md` / `Agents.md` / `features/Agents.md`，先读那些再改产品；**选技能、嵌套、once/keep、自愈预算**以本目录为准。冲突时：点名的 `SKILL.md` > 本文件 > 记忆。

## 你在做什么

把 Flow Coding 收成可点名执行的技能，让人不必离开对话窗口。

动手之前问自己：这个改动是让今天该读的更少、更准，还是只是把管子加粗？

## 读序

```
Soul.md → 本文件 → Index.md → 被点名的 SKILL.md
          （需要时再读该技能的 templates / scripts / references）
```

禁止：跳过 Soul 直接开写；只扫 Index 标题就开干；把 `templates/` 底稿当已完成。

`disable-model-invocation: true` 的技能（总管、三条嵌套、圆桌、反省）**必须被点名或被总管按表转交**，禁止因「看起来像开发」就自动套上。

## 选哪条路

用户点了命令 / 路径 / 中文别名（`开发流程`、`举一反三`、`UI 圆桌`…）→ 打开那份 `SKILL.md`，一步不跳。

没点名 → 用下表，**只选一把**，多把就问人。不要发明第十条管道。

| 情况 | 走 |
| --- | --- |
| 要从分类做到交付 | [`/flow-coding-software-engineering`](flow-coding-software-engineering/SKILL.md)（总管；内部会调下面三条） |
| 只要合同、不要实现 | [`/new_feature_req`](new_feature_req/SKILL.md)（classify + define 后停） |
| 夹已有（或先建夹）再落地 | [`/new_feature_pick_and_implement`](new_feature_pick_and_implement/SKILL.md) |
| 已有产品的洞（看见了但下一步断了） | [`/new_bug_fix`](new_bug_fix/SKILL.md)，不开新主题夹 |
| 洞已交付，问设计为何没防住 | [`/self-reflect-after-bug-fix`](self-reflect-after-bug-fix/SKILL.md) |
| 页面美不美 → 要定版 demo | [`/ui-design-roundtable`](ui-design-roundtable/SKILL.md)，build 前停 |
| 跑 Playwright / 截图 / 5 阶段 | [`flow_coding_testing`](flow_coding_testing/SKILL.md) |
| 三路日志、三角定位 | [`flow_coding_logging`](flow_coding_logging/SKILL.md) |
| 真实 Chrome + 登录态 CDP | [`flow_coding_chrome_cdp`](flow_coding_chrome_cdp/SKILL.md) |

缺「人看见什么 / 下一步 / 有无可见面」→ 先问人，不要猜着建夹或开桌。

## 嵌套（同一条管道）

总管按序：

```
classify → define → plan → build → verify → review → QA_Check → deliver
```

| 命令 | 管道上的段 | 交还 |
| --- | --- | --- |
| `new_feature_req` | classify + define | 被总管 / pick 嵌套：交人表后**不要停**；被反省嵌套：交人后**交回学习层**，不写 `src/`；单独跑：交人后停 |
| `new_feature_pick_and_implement` | plan（若薄）+ build → deliver | 夹不齐：同一轮先整份跑完 req，再 Phase 0 |
| `new_bug_fix` | `type=bug` 八段都走，记在已有夹 `track/bug-<date>-<slug>/` | deliver 后默认立刻上学习层（用户说「只要修洞」才停） |
| `self-reflect-after-bug-fix` | **不在管道上** | 反省出新能力可嵌套 req（只建合同） |

进度只认工作区 `features/<id>/track/` 的 `status`。上一段 `done`（或技能写明的 `skipped`）才能开下一段。`classify` / `deliver` 不许 skip。

合同句（有可见面时必须能填）：

```
看得见的 X → 跨过 <边界> → 仍能做 Y
```

边界指进程重启、uvicorn reload、新 sqlite 连接、新 `create_app`、刷新页。同进程内存断言不算门闩。

## 验证闭环

对不上号时同时看三路，禁止猜：

1. 行为：页 / API / Playwright（[`flow_coding_testing`](flow_coding_testing/SKILL.md)）
2. 前端：`logs/frontend/` 或项目约定的 `logs/ui.log`
3. 后端：`logs/backend/` 或 `logs/server.log` + `logs/access.log`

本目录技能若写了分轨，禁止混写。需要登录态 / 扩展时走 [`flow_coding_chrome_cdp`](flow_coding_chrome_cdp/SKILL.md)：默认 `--restart` + profile 同步，禁止把 `--no-sync` 写成默认。

自愈受 3 × 3 约束；触顶汇总证据交人。

## once / keep

细则：[templates/tests.md](flow-coding-software-engineering/templates/tests.md)。混报禁止。

| 类 | 面向 | 能勾验收 |
| --- | --- | --- |
| **once** | 开发过程的一次性探测：Phase 0 现网、手点、探路 PW、读日志 | **不能** |
| **keep** | 产品质量回归：入库。夹内 unit / regression / 可见面 e2e | **可以** |

禁止：用 once 关账；放宽断言换绿；「从未创建」冒充 persist；只 mock 流式接口。

## 交人

全程结束只留一张表（总管有栏位；子命令按其 `SKILL.md`）。必须能指到：走了哪把技能、哪一段、哪条 keep 命令与结果、人怎么验三步、once 写明「未当门闩」、未做的浏览器步。

用户没要求不要 git commit / 开 PR / 改 git config。临时文件写仓库外，不要 `/tmp`、不要进 git。

## 改本目录

| 变的是 | 改 |
| --- | --- |
| 多了一把技能 | 新夹 + `SKILL.md`，并在 [Index.md](Index.md) 占行 |
| 选技能 / 嵌套 / 交还变了 | 本文件 |
| 「我们是谁 / 不妥协」变了 | [Soul.md](Soul.md) |
| 只加厚某一把的步骤 | 只改那份 `SKILL.md`（及 templates），不要把管子抄进三件套 |

## 不要做

- 不要跳过 Soul 或只扫标题就开写。
- 不要发明第十条管道，或把学习层画进八段当第九格。
- 不要在没有夹、没有合同的时候先改产品代码。
- 不要用探测、假门闩、放宽断言换绿。
- 不要在用户未要求时提交 git、开 PR、改 git config。
