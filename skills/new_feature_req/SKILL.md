---
name: new_feature_req
description: >-
  Turns a human feature request into a features/<id>/ contract from
  features/_template (spec, acceptance, references/, track/, test stubs).
  Owns classify+define in /flow-coding-software-engineering. Nested from
  /self-reflect-after-bug-fix when reflection finds a new capability.
  Does not implement product code unless nested under
  /new_feature_pick_and_implement.
disable-model-invocation: true
---

# /new_feature_req

## 开发流程（总管）

本仓库完整管道是 [`/flow-coding-software-engineering`](../flow-coding-software-engineering/SKILL.md)，按序：

```
classify → define → plan → build → verify → review → QA_Check → deliver
```

| 本命令负责 | 不负责 |
| --- | --- |
| **classify**（若未填）+ **define** | 不改 `src/` / `frontend/src` |
| 建夹、合同、`track/01`·`02`、keep 点名 | **build** 起走 [`/new_feature_pick_and_implement`](../new_feature_pick_and_implement/SKILL.md) |
| 洞（看见了下一步断了） | 转 [`/new_bug_fix`](../new_bug_fix/SKILL.md)，不开新主题夹 |

进度只认 `features/<id>/track/` 的 `status`。once（过程探测）不能勾验收；keep 才是门闩。本 feature 的测试与文稿留在该夹。细则：[templates/tests.md](../flow-coding-software-engineering/templates/tests.md)。

被总管或 pick_and_implement **嵌套**时：夹和合同建完、交人表写完之后**不要停**，把控制交回去。  
被 [`/self-reflect-after-bug-fix`](../self-reflect-after-bug-fix/SKILL.md) **嵌套**时：需求输入是出洞夹的 `track/bug-…/reflection.md`（原则 + 那一行反三）。建夹后 `notes.md` 注明来源。交人表写完**交回学习层**，不要接着实现。  
单独跑：交人表之后停。

对照：[features/_template](../../../features/_template/Index.md) · [features/Agents.md](../../../features/Agents.md) · 根 [Agents.md](../../../Agents.md) · [可见即可续](../../rules/visible-then-continuable.mdc)

本仓库规格夹是 `features/<id>/`。没有 SafeClaw 的 `docs/features/_template-frontend`、`TC-*`、`test.regression.discover`。建夹只从 `features/_template/` 复制。

Fail Fast / 已有产品洞 → 改走 `/new_bug_fix`，不要开新主题夹。

## 停止条件

缺下面任一项就先问人，不要猜着建夹：

- 人看见什么（预览 / 卡 / 列表 / 确认框 / 文件）
- 看见之后下一步
- 是否有可见面

不要跑 `bash test/run_regression.sh`，除非用户本轮明确要求。

## 流程

### 1. 定 ID

- `feature-id`：`kebab-case`，未占用 `features/<id>/`。
- 合同句先写死：`看得见的 X → 跨过 <边界> → 仍能做 Y`（Index / spec / acceptance 同一句）。

### 2. 建 feature 夹

从本仓库模板复制，**必须带上 `references/` 与 `track/`**：

```bash
FEATURE=<feature-id>          # kebab-case
SLUG=${FEATURE//-/_}          # pytest / 本夹测试文件名
cp -R features/_template "features/$FEATURE"
```

把夹内所有 `__feature_id__` 换成 `$FEATURE`、所有 `__id__` 换成 `$SLUG`（含文件名：`test___id___unit.py` → `test_<slug>_unit.py`，regression / e2e 同理）。

填真值：`Index.md` / `spec.md`（含 §API 响应）/ `acceptance.md`（只列 keep）/ `notes.md` / `plan.md`。`references/Index.md` 至少留目录表。无可见面：**删除** `demo.html` 与 `test_<slug>_e2e.spec.ts`。

禁止：拷贝不存在的 `docs/features/_template-frontend`；禁止建夹不带 `references/` / `track/`；禁止把第三方手册整篇贴进 `spec.md`。

### 3. 填合同（未实现前）

| 文件 | 必须有 |
|------|--------|
| `Index.md` | 能力、合同句、状态「路线图已占，未实现」、文件表（含 `references/` · `track/`） |
| `spec.md` | 目标 / 行为 / 先验 / 不做 / API 响应；第三方依据用 `references/…` |
| `acceptance.md` | 只列 keep；状态全未勾 |
| `plan.md` | 里程碑；once 与 keep 分栏（S 可并 notes） |
| `notes.md` | 取舍（可短） |
| `references/Index.md` | 本夹第三方目录；无本地副本也要有这张表 |
| `track/` | 八段跟踪；进度只认这里的 `status` |
| 本夹测试 | `test_<slug>_unit.py` · `_regression.py`（**keep**）；有可见面再留 `_e2e.spec.ts` 与 `demo.html`。不要写到 `tests/` / `frontend/e2e/` |

禁止把路线图愿望写成已落地。[features/Index.md](../../../features/Index.md) 新行走 📝 或 ⬜，不要 ✅。

### 4. 占目录

[features/Index.md](../../../features/Index.md) 加一行。不要往默认测试套件丢会红的空测试；占位文件保持 skip，直到实现阶段写真断言。

### 5. 交人

用一张表回报，然后停：

| 段 | 路径 |
|----|------|
| 夹 | `features/<id>/` |
| 规格 | `spec.md` · `acceptance.md` · `plan.md` · `notes.md` |
| 跟踪 | `track/`（classify 可先填） |
| 第三方参考 | `references/Index.md`（及已存副本） |
| 本夹测试 | `test_<slug>_unit.py` · `_regression.py`（可见面另有 `_e2e.spec.ts` · `demo.html`） |
| 验收 | `acceptance.md`（未勾） |
| 目录 | `features/Index.md` 已占行 |

下一步只列：「总管下一段是 plan/build，改产品走 `/new_feature_pick_and_implement`（或继续 `/flow-coding-software-engineering`）。」把 `track/01-classify.md` · `02-define.md` 标 `done`（plan 未写完保持 `not_started`）。

（若被 pick_and_implement 嵌套：交人表仍要写，不要停，立刻继续实现。）  
（若被 self-reflect-after-bug-fix 嵌套：交人表仍要写，不要停，**交回学习层**，不要实现。）

## 禁止

- 先写实现再补夹
- 建夹不带 `references/` 或 `track/`
- 用 mock 流式接口当 persist 验收
- 「从未创建」Fail Fast 当「创建过、内存没了」
- 把未实现行标 ✅
- 把整本受版权文档原文塞进 `references/`
