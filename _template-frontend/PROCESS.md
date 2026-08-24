# 前端功能开发流程（完整 · 可复用）

SoT：本文件。主题合同写在 `docs/features/<id>/`，**不得**把本流程抄进主题当验收代替物。

对照实例：[thinking-realtime-display](../thinking-realtime-display/)（2026-08-24：先 headed 探测，再落盘诊断 / 计划 / demo）。

```text
0 现网 headed 确认
  → 1 诊断落盘 problem.md
  → 2 合同 methodology + 可见即可续
  → 3 计划 plan / milestones
  → 4 定版 demo HTML（绑定真实 testid）
  → 5 实现（只动合同面）
  → 6 再 headed 对照 demo
  → 7 E2E（进行中 + 完成后 + 跨边界）
  → 8 acceptance 勾选 + features README
  → 9 使用指南 guide.md + 证据 evidence.md
```

禁止：跳过 0 直接写代码；跳过 4 直接「感觉上好看了」；用 mock stream 代替「刷新后还能续」。

---

## Phase 0 — 现网 headed 确认（未改代码之前）

**目的**：人看见的现网是什么、完成后是什么。没有这两张图，后面的「加强 / 不改」都是猜。

1. 确认前端 `http://localhost:3000`（或 `FRONTEND_URL`）已起。  
2. 写**探测 spec**（不进仓库，放 workspace）：  
   - **进行中**：mock 或真路径，等到可见面出现，截全页 + dump 根节点 `outerHTML` / `innerText` / class。  
   - **完成后**：同一条路径走到稳定终态，再截 + dump。  
   - 若合同说「完成后不改」，dump 的 class 字符串就是冻结基线。  
3. 跑：

```bash
cd test/e2e
# 探测文件若在 workspace，先 cp 进 test/e2e，跑完删除
HEADED=1 npx playwright test <probe>.spec.ts --retries=0
```

4. 证据只写：

```text
~/Downloads/safe_claw_worksapce/workspace/
```

**退出**：至少一张「进行中」、一张「完成后」截图 + JSON dump。`problem.md` 能引用它们。

**探测 spec 要点**

- 复用现成 harness（见 `test/e2e/stop-during-thinking.spec.ts`：mock `/sessions`、`/settings/model`、`/chat/stream`）。  
- Playwright `testDir` 是 `test/e2e`：workspace 里的 spec 必须拷进去才能发现。  
- `HEADED=1` 时 config 已 `headless: false` + `slowMo: 500`。  
- 进行中若需要停住：SSE **不要**发 `done`。  
- 完成后：步骤 + `content` + `done`。

---

## Phase 1 — 诊断落盘 `problem.md`

对着截图和代码各写一节，禁止只有形容词。

必填：

| 节 | 写什么 |
|----|--------|
| 驱动场景 | 用户做了什么，看见什么，下一步想做什么 |
| 现网事实 | headed 表：进行中 / 完成后的 DOM、testid、class、全文 |
| 根因 | 数据断点（SSE 字段丢了？只 push 了名字？读错组件？） |
| 可见即可续 | `看得见的 X → 跨过 <边界> → 仍能做 Y` |
| 成功差异 | 进行中之前/之后；**完成后之前/之后**（常为「相同」） |
| 非本问题 | 明确不碰的父合同、右栏、另一条死代码路径 |

先定位**真组件**再写根因。本仓库已漏过：旧 `src/components/*` 与 `features/chat/components/*` 并存。以 headed 对上的 `data-testid` 为准。

---

## Phase 2 — 合同 `methodology.md`

把「改哪里 / 冻哪里」写成硬表，而不是愿望。

必填：

1. **一句话合同**（进行中改什么，完成后禁止什么）。  
2. **可见即可续**一行（与 problem / acceptance / e2e 同一句）。  
3. **作用域表**：在范围内 / 不在范围内。  
4. **testid 表**：旧的冻结；新的命名；何时可见。  
5. **数据合同**：每条 SSE / store 字段，可见面上必须怎么用；禁止丢掉的字段点名。  
6. **生命周期**：出现 → 更新 → 卸掉 / persist。  
7. **Fail Fast**：禁止假数据填空、禁止静默 fallback。

若完成后界面冻结：把探测 dump 的 class / 文案结构写进合同。实现 diff **不得**改该组件外观，除非另开主题。

---

## Phase 3 — 计划 `plan.md` + `milestones.md`

分阶段，每段有**交付文件**和**退出证据**。前端主题最低：

| Phase | 内容 |
|-------|------|
| 0 | 本文档齐套 + demo |
| A | 数据接线（字段到达可见面的 store） |
| B | 可见面 UI（只动合同组件） |
| C | 去重 / 真状态 / 边界（刷新、停止、空态） |
| D | Playwright（进行中 + 完成后 + 跨边界） |
| E | acceptance 勾选 |

`milestones.md`：准入 / 准出 / 证据。写明哪一层**不能**当门闩（例如只 mock stream）。

---

## Phase 4 — 定版 demo HTML

路径：`docs/features/<id>/demo-<id>.html`。  
浏览器直接打开，**不依赖** dev server。

硬要求：

- 顶栏 harness：主题名 + 一句话合同 + 真 `data-testid`。  
- **至少两态**：现网进行中 / 建议进行中。若完成后冻结，必须有第三态「完成后」，且与现网终态同构。  
- 每块标注 `data-testid`，与将要实现的 DOM **同名**。  
- HTML 注释写清映射到哪个 tsx。  
- 浅色；禁止用假业务数据冒充现网协议（demo 可用一组**标明是示例**的步骤，但 testid 必须真）。  
- 建议态可「播放一轮」演示实时进入，便于 headed 对照。

对照：[demo-thinking-realtime.html](../thinking-realtime-display/demo-thinking-realtime.html) · [demo-ui-improve.html](../ui-improve/demo-ui-improve.html)

---

## Phase 5 — 实现

1. 只改 methodology 作用域里的文件。  
2. 新控件必须带合同里的 testid。  
3. 无数据时：**空头 + 诚实**，禁止写死假步骤 / 假图 / 假进度。  
4. 父合同（停止、Halt、mode）testid 与语义不改，加回归。  
5. 临时文件、探针、截图不进主题目录（除 demo HTML 与文档）。

---

## Phase 6 — 再 headed 对照 demo

实现后用**同一套**进行中 / 完成后探测（或正式 spec + `HEADED=1`）：

- 进行中：字段、testid、布局对照 demo 建议态。  
- 完成后：对照 demo 第三态 **和** Phase 0 的 after dump（class 未漂）。  
- 走一遍周围路径（停止、再发一条、另一 route 若共享 store）。

单张静态截图 **不算**验证。要操作：发消息 → 等过程 → 结束或停止。

---

## Phase 7 — E2E

`test/e2e/<id>.spec.ts` + 主题 `e2e.md`。

最低三条（按主题裁剪，但「完成后 / 跨边界」不能裁掉）：

| 编号 | 锁什么 |
|------|--------|
| S1 | **进行中**可见面：合同字段 + testid |
| S2 | **完成后**原始界面 + **跨边界**（reload / 新 session / 清内存后仍能做下一步） |
| S3 | 相邻父合同不回归（如停止、Rerun） |

S2 必须真的跨过边界。Playwright 若 mock 掉 persist，reload 后 GET 必须仍能读回那条可见物。  
「从未创建 → Fail Fast」不能代替「创建过、内存没了」。

有头跑法写进 `e2e.md` / `scripts.md`：`HEADED=1 npx playwright test ...`

---

## Phase 8 — 验收

`acceptance.md` 可勾选，且含：

- 可见即可续那一行 + 对应真测试勾选  
- 文档 §0  
- 进行中 §U  
- 完成后冻结 §A（若适用）  
- E2E §E  
- 明确不验收  

勾完后：`docs/features/README.md` 表里更新状态。需要报告则加 `acceptance-report-YYYY-MM-DD.md`。

---

## Phase 9 — 使用指南 + 证据（交付给人）

实现绿了不算交付完。还要让**使用者**知道怎么操作，以及**后来的人**能核对当时为何算过。

**交付**

| 文件 | 写给谁 | 必填 |
|------|--------|------|
| `guide.md` | 打开 UI 的人 | 使用前（含**重启 server**）、看见什么、操作表（ID ↔ 期望 ↔ E2E）、不要指望什么、复验命令 |
| `evidence.md` | 验收 / 回归 | 结论、命令与 pass 表、Phase 0 基线路径、实现触点、**未改**的冻结面 |

对照：[thinking-realtime-display/guide.md](../thinking-realtime-display/guide.md) · [evidence.md](../thinking-realtime-display/evidence.md) · [ppt-keyboard/guide.md](../ppt-keyboard/guide.md)

**重启（交付当天必做）**

改过前端 / API 后，HMR 不够就杀进程重拉，再硬刷新，让人用到新 bundle：

```bash
# UI :3000
cd safeclaw-ui/my-app && npm run dev
# API :8000
conda activate safe_claw && python start_api.py
```

`guide.md` 必须写「改完要重启哪一侧」。交付消息里给出可点的 `http://localhost:3000`。

**退出**：README 索引含 guide / evidence；人按 guide 能独立走完主路径。

---

## 全程硬规则

| 规则 | 含义 |
|------|------|
| Fail Fast | 无数据就暴露，不编造可见物 |
| 可见即可续 | 人看见之后，跨边界仍能做下一步 |
| 完成后冻结 | 合同写了「不改终态」就禁止动该组件 class / 结构 |
| testid 稳定 | 旧 id 不改名；新 id 先写进 methodology |
| 工作目录 | 探针 / 截图 / dump → `~/Downloads/safe_claw_worksapce/workspace/` |
| 先合同后代码 | Phase 0–4 未齐，不准当实现已完成 |
| 有头是一等公民 | 现网确认与终验都要 headed，不只 CI headless |

## 三问（每个可见面必答）

1. **人看见什么？** 预览、文件、卡片、列表行、badge、确认框、思考卡。  
2. **看见之后下一步？** 改、贴、确认、停止、恢复、继续聊。  
3. **哪条边界丢掉看不见的状态？** reload、uvicorn reload、换 `session_id`、`clear_*_store`、只 mock 了 stream。

写成：

```text
看得见的 X  →  跨过 <边界>  →  仍能做 Y
```
