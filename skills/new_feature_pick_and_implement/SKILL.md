---
name: new_feature_pick_and_implement
description: >-
  Implements one feature folder. Owns build through deliver in
  /flow-coding-software-engineering (TDD keep, verify, review, QA_Check).
  If features/<id>/ is missing, first run /new_feature_req. Product holes
  go to /new_bug_fix.
disable-model-invocation: true
---

# /new_feature_pick_and_implement

## 开发流程（总管）

本仓库完整管道是 [`/flow-coding-software-engineering`](../flow-coding-software-engineering/SKILL.md)，按序：

```
classify → define → plan → build → verify → review → QA_Check → deliver
```

| 本命令负责 | 不负责 |
| --- | --- |
| **plan**（若还薄）+ **build** → **verify** → **review** → **QA_Check** → **deliver** | 没有夹就写代码（先 [`/new_feature_req`](../new_feature_req/SKILL.md)） |
| Phase 0 once + TDD keep；进度写 `track/03`–`08` | 已有产品洞（看见了下一步断了）→ [`/new_bug_fix`](../new_bug_fix/SKILL.md) |

夹不存在或缺少 `Index.md` / `spec.md` / `acceptance.md` / `references/`：同一轮先把 req **整份**跑完，交人表写完**不要停**，再从 Phase 0 续。缺 `track/` 从 `_template/track` 补上。

进度只认 `features/<id>/track/`。once 不能勾 ✅；keep 才是门闩。本夹测试不要写到 `tests/` / `frontend/e2e/`。细则：[templates/tests.md](../flow-coding-software-engineering/templates/tests.md)。

对照：模板 [features/_template](../../../features/_template/Index.md) · 规格夹 [features/](../../../features/) · [可见即可续](../../rules/visible-then-continuable.mdc) · 建夹技能 [new_feature_req](../new_feature_req/SKILL.md)

一次只做一个 `feature-id`。产品洞 → `/new_bug_fix`。

## 选哪条

1. 人点了 id / 路径 / 「做 clustering」→ 用那条。
2. 没点名：列出 [features/Index.md](../../../features/Index.md) 里状态为「路线图已占，未实现」/ 📝、或已登记仍 ⬜ 的项，**一条**就做，多条就问人。
3. **夹不存在**（`features/<id>/` 没有，或没有 `Index.md` + `spec.md` + `acceptance.md` + `references/`）：**不要停、不要边设计边写代码**。先把 `/new_feature_req` 整份跑完把夹建好（从 `features/_template` 复制，必带 `references/` 与 `track/`），再回到下面的 Phase 0 / 5–9。

本仓库规格夹是 `features/<id>/`（`Index.md` · `spec.md` · `acceptance.md` · `notes.md` · `plan.md` · **`references/`** · **`track/`**）。冲突以本夹 `spec.md` + `acceptance.md` 为准。本 feature 的测试只放本夹。

开做前（夹已存在之后）读齐：

`features/<id>/` 的 `spec.md` · `acceptance.md` · `plan.md` · `track/` · `references/Index.md` · 夹内测试与报告（若已有）

本仓库**没有** `test.regression.discover`、`TC-*`、`e2e.md`。不要跑 `bash test/run_regression.sh`，除非用户本轮明确要求。临时文件写仓库外工作目录，不要 `/tmp`、不要进 git。

## 夹不存在：先 /new_feature_req

触发：`features/<id>/` 不存在，或夹不完整（缺 `Index.md` / `spec.md` / `acceptance.md` / `references/`）。

同一轮里按序：

1. **立刻**打开并完整遵循 [new_feature_req/SKILL.md](../new_feature_req/SKILL.md)。一步不跳。
2. 把当前这条 `feature-id` 与 Index 里那行能力说明当作 req 的需求输入。缺「人看见什么 / 下一步 / 是否有可见面」就先问人，不要猜着建夹。
3. req 的「默认不改产品代码」「交人表」必须做到。被本命令嵌套时：**交人表写完不要停**，不要等用户再发一次 pick_and_implement。
4. 确认 `features/<id>/` 已在、Index 已占行、acceptance 仍全未勾。然后才进入 Phase 0。
5. 禁止：先写 `src/` / 测试再补夹；禁止把 req 缩成「mkdir 三个空 md」。

## 流程（按序，禁止跳 Phase 0）

夹已齐之后才进入。禁止跳 Phase 0。下面的编号是本命令的历史步序，对应总管八段如下：

| 本命令步 | 总管段 | track |
| --- | --- | --- |
| 0 headed 现网 | build 的 once 基线 | `04-build.md` once 栏 |
| 5 实现 | build | `04-build.md` |
| 6 再 headed | build 的 once 复核 | `04-build.md` |
| 7 门闩 | verify + **review** | `05-verify.md` · `06-review.md` |
| 8 验收勾选 | QA_Check | `07-qa-check.md` |
| 9 guide + evidence | deliver | `08-deliver.md` |

plan 还薄（`plan.md` 无里程碑 / keep 清单）：先补 `plan.md` 与 `03-plan.md`，再进 Phase 0。

### 0. headed 现网（未改代码之前）

有可见面：未改代码前看现网页或 API（**once**），记入 `track/04-build.md` once 栏。  
无可见面：跳过 headed，仍要写清无 DOM 合同。

demo 已在夹里则对照建议态；缺 demo 的前端主题先补再实现。

### 5. 实现

只动合同范围内的 `src/` · `frontend/` · **本夹** keep 测试。无数据：空头诚实，不编造可见物。  
父合同（停止、刷新可续、轨入口）不改语义。  
本夹 `test_<slug>_unit.py` / `_regression.py` / 可见面 `_e2e.spec.ts` **本阶段落成真文件**，要能红能绿，不要永久 skip。once 探测不入库。

### 6. 再 headed / 浏览器

有可见面：按用户规则走主路径（点、打开、外点、刷新），不是只截一张静态图。对照 demo 建议态与完成后。

### 7. 门闩

按本夹 `acceptance.md` / `plan.md` 跑 **keep**。本仓库默认：

```bash
.venv/bin/python -m pytest features/<id> -v --tb=short
```

本 feature 的测试只跑本夹。有 `test_<slug>_e2e.spec.ts` 再跑该文件（仍在本夹）。跨 feature 冒烟才动 `tests/`。regression 必须真跨边界（reload / 新 db 连接 / 新 `create_app`）。Mock 流式接口不能代替 persist。  
「从未创建」Fail Fast 不能代替「创建过再丢内存」。

绿了之后**同一步做 review**（`06-review.md`）：security（HTML 消毒、无 token、不爬全文）· quality（一次一件、中文编辑语气、逻辑可单测）· performance（无新全库扫描、抓取有超时与并发上限）。任一面未过不进第 8 步。

### 8. 验收勾选

门闩因**对的原因**绿，才：

- 先跑全库 `.venv/bin/python -m pytest tests features -q --tb=short`；`test-report.md` · `acceptance-report.md` 对照本跑次  
- `features/<id>/acceptance.md` 勾 **keep** 项  
- [features/Index.md](../../../features/Index.md) 该行 ⬜/📝→✅  
- 夹内 `Index.md` 状态改成已落地（写清哪几条绿）  
- `track/07-qa-check.md` 出门闩勾完  

未绿保持 ⬜。禁止放宽断言。禁止用 once 换 ✅。

### 9. guide + evidence

证据留在本夹：`test-report.md` · `acceptance-report.md` · `track/08-deliver.md`。  
交付写清人怎么打开：后端 `http://127.0.0.1:8000`，前端 `http://127.0.0.1:5173`。改过前端 / API 后 HMR 不够就重启。

## 交人

| 项 | 写什么 |
|----|--------|
| 选中 | `features/<id>/` |
| 建夹 | 若本轮先跑了 req：写明夹是新建的 |
| 改了 | 文件列表（只列作用域内） |
| 门闩 | **keep** 命令与结果；once 写「未当门闩」；`track/03`–`08` status |
| 用例 | 哪些验收项从 ⬜ 变 ✅，哪些仍 ⬜ |
| 人怎么验 | 三步主路径 |

## 禁止

- 没有夹就直接改产品代码（必须先 `/new_feature_req`）
- 建夹时边设计边写 `src/`
- 跳过 headed 直接「感觉对了」
- 改合同外的冻结面
- 用修代码补洞却不开 `/new_bug_fix`
- 把未跑的行标 ✅
- 临时文件进仓库或 `/tmp`
