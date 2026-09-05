---
name: flow-coding-software-engineering
description: >-
  Runs one change through classify → define → plan → build → verify →
  review → QA_Check → deliver (type, complexity, urgency_priority, ROI,
  demo HTML, acceptance, spec, API resp, TDD, Playwright e2e, anti-fragile).
  Use when the user says /flow-coding-software-engineering, 开发流程, or wants
  classification before coding.
disable-model-invocation: true
---

# /flow-coding-software-engineering

一次只推进**一件**可验证的事。管道按序，禁止跳段。复杂度 S 只许压缩厚度，不许删段。

```
classify → define → plan → build → verify → review → QA_Check → deliver
```

跟踪：进度与出门闩**只认** `features/<id>/track/`（`_template` 已带）。每段只改对应 `0N-*.md` 的 `status`。上一段 `done`（或规则允许的 `skipped`）才能开下一段。`templates/` 里同名底稿是栏位展开，填完必须回写 track，不要两处各写各的。

测试分两类，禁止混报。细则 [templates/tests.md](templates/tests.md)：

| 类 | 面向 | 能勾 ✅ |
| --- | --- | --- |
| **once** | 开发过程的一次性探测（Phase 0、手点、探路 PW、日志） | **不能** |
| **keep** | 产品质量回归（本夹 unit / regression / 可见面 e2e；仅跨 feature 的才进 `tests/`） | **可以**（可见面必须跨边界） |

对照：[Soul.md](../../../Soul.md) · [Agents.md](../../../Agents.md) · [可见即可续](../../rules/visible-then-continuable.mdc) · [features/Agents.md](../../../features/Agents.md)

先读 Soul → Agents → [features/Index.md](../../../features/Index.md)。动手前问：这是让今天该读的**更少、更准**，还是把管子加粗？管子加粗 → 停，问人。

本仓库**没有** SafeClaw 的 `TC-*`、`test.regression.discover`、`docs/features/_template`。路线图就是 `features/<id>/`。不要跑 `bash test/run_regression.sh`，除非用户本轮明确要求。

## 停 / 转

| 情况 | 走 |
| --- | --- |
| 缺「人看见什么 / 下一步 / 有无可见面」 | 先问人，不要猜着建夹 |
| 已有产品洞（看见了，下一步断了） | classify 填完 → `/new_bug_fix`，不要开新主题夹；关账后离开交付层，走 `/self-reflect-after-bug-fix` |
| 只要合同、不要实现 | 做到 define 交人表后停 |
| 只要设计探讨、不改 `frontend/` | classify `ui` → [ui-design-roundtable](../ui-design-roundtable/SKILL.md)，build 前停 |
| 用户只要其中一段 | 仍先填 classify 表，再从缺的那段续，不要假装前面做过 |

嵌套：本技能是总管。三条子命令**都走同一条管道**，只是负责的段不同：

| 命令 | 管道上的段 |
| --- | --- |
| [new_feature_req](../new_feature_req/SKILL.md) | classify + define |
| [new_feature_pick_and_implement](../new_feature_pick_and_implement/SKILL.md) | plan（若薄）+ build → deliver |
| [new_bug_fix](../new_bug_fix/SKILL.md) | `type=bug`：八段都走，记在已有夹的 `track/bug-<date>-<slug>/`，先红 keep 再修 |
| [self-reflect-after-bug-fix](../self-reflect-after-bug-fix/SKILL.md) | **不在管道上**：学习层。反省出新能力可直接嵌套 `/new_feature_req`（只建合同） |

验证闭环对照 [flow_coding_testing](../flow_coding_testing/SKILL.md)；对不上号对照 [flow_coding_logging](../flow_coding_logging/SKILL.md)（本仓库日志分轨：`logs/backend/` · `logs/frontend/`，禁止混写）。

---

## classify

**理解**：`type` / `complexity` / `urgency_priority` / `ROI`。未填下表禁止 define。

| 项 | 取值 | 问什么 |
| --- | --- | --- |
| type | `feature` · `bug` · `refactor` · `ui` · `docs` | 新能力 / 已有洞 / 边界不变的改码 / 只出 demo / 只改给人读的文档 |
| complexity | `S` · `M` · `L` | 单点配置或文案 / 一个 feature 夹 / 多页面、新依赖、或打分·抓取·聚类 |
| urgency_priority | `P0` · `P1` · `P2` | 现网断下一步 / 合同内该做 / 可等 |
| ROI | 一句话 | 今天该读的是否更少更准？可审计性是否增加？只加粗管子则 `ROI=拒绝` |

`ROI=拒绝` → 停，把理由交给人。`type=bug` → 本段结束后转 `/new_bug_fix`。`type=docs` 且不改产品 → define 写清「无 DOM 合同」，plan/build 写 `N/A`，仍走 verify 里「没改代码的自证」+ deliver。

S：表可以短，plan 可写进 `notes.md`。M/L：必须有 `features/<id>/plan.md`。L：review / QA_Check 不许一行打发。

交人（本段）：把上表贴出来，并写将转入哪一段、哪个既有技能。

---

## define

**产物**：`demo html` / `acceptance` / `spec` / `goal` / `api resp`。禁止写 `src/` / `frontend/src`。

有可见面先问三句（可见即可续）。答不上来先问人。

走 [new_feature_req](../new_feature_req/SKILL.md) 建夹（从 `features/_template` 复制，必带 `references/` 与 `track/`）。夹内至少钉：

| 产物 | 写哪 | 必须含 |
| --- | --- | --- |
| goal | `spec.md` §目标 | 哪种噪声变少 / 哪种信号变强 |
| spec | `spec.md` | 行为、边界、与先验、不做 |
| acceptance | `acceptance.md` | 合同句；只列 keep；未实现前全未勾 |
| api resp | `spec.md` §API 响应 | 方法、路径、关键 JSON 字段、空数据与失败长什么样（空头诚实） |
| demo html | 见下 | 人看见的建议态，不是产品代码 |

**demo html**

- 可见 UI：`features/<id>/demo.html`，或指向已有 `ui-design/ideas/<topic>/`。缺 demo 的前端主题：先补再 plan。需要多视角定版 → 先跑 ui-design-roundtable，再把定版 demo 链进夹内 Index。
- 无 DOM：在 `spec.md` 写「无可见面」，不要造假页面。

合同句（有可见面必须同一句出现在 Index / spec / acceptance）：

```
看得见的 X → 跨过 <边界> → 仍能做 Y
```

边界：进程重启 / uvicorn reload / 新 sqlite 连接 / 新 `create_app` / 刷新页。同进程内存断言不算门闩。

[features/Index.md](../../../features/Index.md) 占行 📝 或 ⬜。禁止把愿望标 ✅。

---

## plan

**产物**：`arch design pattern` / `dependency` / `solution` / `steps_milestones` / `playwright ts scripts_e2e` / `UT`。仍不改产品。

本 feature 的 plan / demo / track / 测试都写在 `features/<id>/`，不要拆到 `tests/` 或 `frontend/e2e/`。`plan.md`（S 可并入 `notes.md`）在夹内 Index 挂号。

| 节 | 写清 |
| --- | --- |
| arch design pattern | 改哪些模块（业务进可单测模块，不堆路由 / Vue）；配置只进 `src/config.py` |
| dependency | 新增库/服务必须点名。默认禁止 Postgres / Redis / Docker / 后端 Node。没有 key 时降噪仍可用 |
| solution | 用哪条现有管道（OPML→抓取→聚类→打分→配额→精选 / 落选可审计），不另造平行分类 |
| steps_milestones | 有序切片；每片写清 once 探测 + 将红的 keep |
| UT（keep） | `features/<id>/test_<slug>_unit.py` 要锁的函数/API 合同 |
| playwright ts scripts_e2e | **入库**才算 keep，文件在本夹：`features/<id>/test_<slug>_e2e.spec.ts`。一次性探路 PW 是 once，记入 `track/04-build.md`。无 DOM：写 `N/A`，不要建 `frontend/e2e/` |

每条 milestone 必须能回答：once 看了什么、先红哪条 **keep**、绿了人看见什么。禁止「一大坨实现完再测」。禁止只列 once。

不要改写 `Inoreader.opml`。不要把第三方手册整篇贴进 plan。

---

## build

**做法**：TDD · test status check · milestones implementation · simplification self check · performance tuning · fail fast。

按 [new_feature_pick_and_implement](../new_feature_pick_and_implement/SKILL.md) 的 Phase 0 再 5–9。夹不齐先把 define 补完，不要边设计边写 `src/`。

每个 milestone：

1. **once（可选但推荐）**：curl / 手点 / 探路截图，记入 `track/04-build.md` once 栏。Phase 0 现网是 once。
2. **TDD keep**：先写真测试（要能红）并入库。未实现用 fail-fast 锁「还没有」，禁止 skip-forever。
3. **implementation**：只动合同范围内的 `src/` · `frontend/` · 本夹 **keep** 测试。
4. **test status check**：立刻跑该片 **keep**，看红变绿。禁止凭记忆填绿。once 绿不能代替。
5. **simplification self check**：能不能删一层？新依赖是否仍必要？有没有把逻辑堆进路由/Vue？
6. **performance tuning**：默认不做。仅当 classify 写了性能目标，或实现引入全库两两比较 / 无超时抓取时，收回去。聚类只在看回窗口内做。
7. **fail fast**：单源失败不拖垮整次；无数据空头诚实；错误不要静默吞掉再假装成功。

有可见面：Phase 0 先看**未改代码前**的页或 API（once）；改完用浏览器走主路径。验证闭环见 flow_coding_testing。探路 PW 是 once；写成本夹 `test_<slug>_e2e.spec.ts` 才是 keep。

---

## verify

**检查**：tests check · acceptance check · bug fix · anti fragile · dependency double check。

```bash
.venv/bin/python -m pytest features/<id> -v --tb=short
```

| 项 | 过关标准 |
| --- | --- |
| tests check（keep） | 本夹 unit + regression 绿；regression 必须写盘 → 关连接或新 `create_app` → 下一步仍成立。once 不够格 |
| acceptance check | `acceptance.md` 逐条对照，先记在 `acceptance-report.md`，**先不勾** |
| bug fix | 本轮引入的洞：先补会红的测试，再改代码。新洞走 `/new_bug_fix`，不要假装是「顺手改一下」 |
| anti fragile | 看得见的 X 跨过边界仍能做 Y。禁止「从未创建」Fail Fast 冒充 persist；禁止只 mock 流式接口 |
| dependency double check | plan 里的依赖是否真的引入了、是否能删；有无把密钥写进仓库 |

对不上号：同时看行为（页/API）、`logs/frontend/`、`logs/backend/`，三角定位后再改，不要猜。

---

## review

**审**：security / quality / performance。未过不得 QA_Check 勾 ✅。

| 面 | 本仓库要点 |
| --- | --- |
| security | 展示 HTML 必须消毒；未消毒内容不得 `\|safe`。不写 token/账号。不爬全文绕过 RSS |
| quality | 一次一件；文案中文、编辑语气；纸色墨色、禁紫色渐变卡片。业务逻辑可单测。父合同（停止、刷新可续、轨入口）不改语义 |
| performance | 无新的全库扫描；抓取有超时与并发上限；没要求就不加 LLM 主路径 |

L：把三面各写 3–6 条到 `features/<id>/notes.md`（或 plan 末节）。S/M：表格式结论即可。

---

## QA_Check

**门闩**：只认 **keep**（夹内 regression / unit、全库、入库 e2e）· evidence。必须是**这一次**的命令输出。浏览器手走是 once，单独不能勾 ✅。

```bash
.venv/bin/python -m pytest features/<id> -v --tb=short
.venv/bin/python -m pytest tests features -q --tb=short
```

有本夹 e2e：再跑 `features/<id>/test_<slug>_e2e.spec.ts`（前端 :5173 打同一套 `/api`）。改了阅读 / 打分 / 抓取 / 页面：至少 HTTP 打通 `GET /api/digest` 是精选、规则能写入、刷新有状态。

有浏览器时走：打开精选 → 点开一条 → 看聚类来源 → 打开被降噪 → 加一条 mute（只走本改动碰到的步）。没有浏览器：写明未做的交互验证，验收不得假装做过。

**evidence**（留在本夹，对照本次跑次）：

| 产物 | 必须含 |
| --- | --- |
| `test-report.md` | 命令、解释器、本夹完整 pytest 输出、全库摘要 |
| `acceptance-report.md` | `acceptance.md` 逐条 → 通过/未通过 + 指向哪条测试 |
| 截图或 API 摘录 | 有可见面：人看见的状态；无 DOM：真实响应 JSON |

测试绿而产品未做（fail-fast）：验收报告写 **未通过**，不得勾 `acceptance.md`、不得把 Index 标 ✅。

门闩因**对的原因**绿，才勾验收、夹内 Index 改已落地、[features/Index.md](../../../features/Index.md) 📝/⬜ → ✅。禁止放宽断言换绿。

---

## deliver

**交付**：docs · guide · product design thinking。用户没要求不要 git commit / 开 PR / 改 git config。不要提交 `data/`、`.venv/`、`__pycache__/`、`logs/**/runtime/`。

| 项 | 何时写 | 写哪 |
| --- | --- | --- |
| docs | 行为或决策变了 | [docs/](../../../docs/Index.md) 里**已有**篇（product / architecture / decisions / usage / glossary）。解释 why，不复述 what。没有新 why 就不要新开长文 |
| guide | 人怎么打开、怎么验变了 | `docs/usage.md`；夹内交人三步。后端 `http://127.0.0.1:8000`，前端 `http://127.0.0.1:5173` |
| product design thinking | 每次必写，可短 | 读者看见什么、今天是否更少更准、故意不做的是什么。取舍进本夹 `notes.md`；够格的决策再记 [docs/decisions.md](../../../docs/decisions.md) |

不要实现多用户、OAuth、云同步、未读红点、无限信息流。不要为了「智能」去掉落选列表。

---

## 交人

全程结束只留这一张表：

| 段 | 写什么 |
| --- | --- |
| classify | type · complexity · urgency_priority · ROI |
| 夹 | `features/<id>/`（或 bug 号 / ui-design 路径） |
| define | spec / acceptance / api resp / demo 路径 |
| plan | `plan.md` 或 notes；里程碑数；PW 有/无 |
| 改了 | 作用域内文件 |
| verify / QA | **keep** 命令与结果；哪些验收 ⬜→✅；once 另写「未当门闩」 |
| review | security / quality / performance 结论 |
| 人怎么验 | 三步主路径 |
| 未做 | 没跑的浏览器步、没引入的依赖 |

## 禁止

- 跳 classify 直接写代码
- 没有夹就改产品（`type=feature`）
- 用 mock 流式接口当 persist；「从未创建」当「创建过、内存没了」
- 用 once 探测代替 keep 回归；把探路脚本永久 skip 塞进套件
- 把未跑的行标 ✅；放宽断言换绿
- 把管子加粗包装成降噪
- 临时文件进仓库或 `/tmp`（工作草稿放仓库外）
