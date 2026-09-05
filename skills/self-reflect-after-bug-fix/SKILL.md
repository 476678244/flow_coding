---
name: self-reflect-after-bug-fix
description: >-
  Meta skill above /flow-coding-software-engineering: after a bug is
  delivered, self-learn, self-reflect, and upgrade test/system/log/architecture
  so the same hole cannot be designed again. May trigger /new_feature_req.
  Use when /new_bug_fix deliver is done, or the user says 举一反三, 自我反省,
  self-reflect-after-bug-fix.
disable-model-invocation: true
---

# /self-reflect-after-bug-fix

**目的是 为了 反思 为什么 现有的 测试设计 / 系统设计 / log设计/ 架构设计 没有提前预防 这个bug的产生。**

这不是开发管道的第九段。

[`/flow-coding-software-engineering`](../flow-coding-software-engineering/SKILL.md) 是**交付层**：把一号洞或一条能力从 classify 送到 deliver。本技能在它**之上**，是指导性的学习层——用这一号已经修好的洞，做 **自我学习 / 自我反省 / 自我升级强化**。交付完成只证明「这次补上了」；本技能问的是「我们当初怎么会设计成防不住」。

```
学习层   self-reflect-after-bug-fix     认知升级（设计为何没预防，下次如何不再这样设计）
              ↑ 交付关账之后上来，不是管道内下一步
交付层   classify → define → plan → build → verify → review → QA_Check → deliver
```

场合：[`/new_bug_fix`](../new_bug_fix/SKILL.md) 的 deliver 已完成。同一轮默认上来（用户说「只要修洞」才留在交付层）。没有修好的洞，没有学习——先把交付层走完。

一次只反这一号。禁止「以后注意」。每一面落到可复查的设计缺陷，并写出**以后 classify / define / plan 会因此改口的那句话**。

## 文件落哪

修洞的交付层记录在 `features/<id>/track/bug-<YYYY-MM-DD>-<slug>/`（见 new_bug_fix）。学习层就写在**同一个 bug 子夹**：

| 文件 | 作用 | 模板 |
| --- | --- | --- |
| `track/bug-…/reflection.md` | 正文：原则 + 四问 + 反三 + 升级 | [templates/reflection.md](templates/reflection.md) |
| `track/bug-…/self-reflect.md` | 学习层 gate（不是第 9 段） | [templates/self-reflect.md](templates/self-reflect.md) |

不要写进根 `docs/` 当流水账。够格的 why 才进 [docs/decisions.md](../../../docs/decisions.md)。

---

## 三层高度（必须都写）

| 层 | 问 | 过关长什么样 |
| --- | --- | --- |
| **自我学习** | 从这一号抽出一条可复用的原则 | 一句话，能用在下一个 feature 的 plan，不是复述症状 |
| **自我反省** | 四种设计为何没提前预防 | 当时怎样 · 为何拦不住 · 当初怎样设计才算预防 |
| **自我升级强化** | 哪份**设计约定**要升一级 | 点名文件：夹内 keep / 流程模板 / 分轨日志约定 / Agents 或 ADR / 新夹合同。只改产品一行不算升级 |

升级优先顺序（从高到低想，从低到高改）：

1. **认知与约定** — 可见即可续、`templates/tests.md` 的 once/keep、log 分轨、`features/Agents.md`、有新 why 才动 ADR
2. **同类设计** — 最多 3 条 sibling 路径（举一反三）
3. **本夹门闩** — 今天补的 keep 若当初在必须会红；不会红则学习层未开始

用户说「只反省不改码」：写完正文停。未说：四问写完后对每一条做**路由**（下表），可以**直接触发** `/new_feature_req`。本轮默认只落地 **一条**；其余进出洞夹 `notes.md` 标「待 req」。管子加粗 → 不触发。

---

## Gate in（离开交付层）

- [ ] 交付层已关账：keep 因对的原因绿，`track/bug-…/08-deliver.md` 已 `done`
- [ ] 读齐入账（`02-define.md`）、新 keep、`acceptance-report.md`
- [ ] 拷 [templates/self-reflect.md](templates/self-reflect.md) 与 [templates/reflection.md](templates/reflection.md) 到 `track/bug-…/`

## 自我反省：四问

对照 [可见即可续](../../rules/visible-then-continuable.mdc)。禁止空答「没有问题」。

### 1. 测试设计

- 哪条 **keep** 该在出事之前就存在？
- 为何没有：没写 / 只 once / 同进程内存 / 「从未创建」冒充 persist / 断言太弱 / ✅ 勾早了
- 今天补的 keep 若当初在，会红吗？不会 → 还停在交付层补门闩
- 原则：下次 plan 写 keep 时，哪句必须写上？

### 2. 系统设计

- 状态活在哪？人看见之后，哪条边界丢掉下一步？
- 空 / 失败 / 单源挂了，是空头诚实还是假装成功？
- 原则：下次 define 的合同句会怎样写，才不会再漏这条边界？

### 3. log 设计

分轨：`logs/backend/` · `logs/frontend/`。对照 [flow_coding_logging](../flow_coding_logging/SKILL.md)。

- 出事时行为 / 前端 / 后端是否都能交叉验证？缺哪路才只能猜？
- 该有而没有的字段？
- 原则：下次同类操作，三角定位还要靠猜吗？要升哪条落盘约定？

### 4. 架构设计

- 业务是否堆在路由 / Vue，导致 keep 锁不住？
- 配置是否没进 `src/config.py`？有没有静默 fallback 把失败做成绿路径？
- 原则：下次 arch 节会拒绝哪一种分层？

## 举一反三（具体）

最多 **3** 条 sibling，必须有路径。问的是「同一设计错误还会在哪发生」，不是「再扫一遍仓库」。

| # | 同类设计错在哪 | 该升的预防 | 路由 | 本轮 |
| --- | --- | --- | --- | --- |
| 1 | | | 见下表 | 已落地 / 待 req / 否 |

### 反省 → 路由（写完四问立刻判，不要等用户再点命令）

| 反省出来的是 | 走 |
| --- | --- |
| 已有夹缺 keep / 假门闩 | 该夹补 **keep**（仍先红后绿） |
| 已有产品洞（看见了下一步断） | [`/new_bug_fix`](../new_bug_fix/SKILL.md)，不开新夹 |
| **新能力**（今天没有这道闸、合同也不在任何夹） | **立刻** [`/new_feature_req`](../new_feature_req/SKILL.md)：把 `reflection.md` 的原则 + 这一行当需求输入。只建合同，不写 `src/` |
| 只升约定（once/keep、分轨、可见即可续） | 改点名的 Agents / 模板 / ADR |
| 管子加粗 | 不触发，写进 notes |

触发 req 时：

1. 新夹 `notes.md` 第一行写：来自 `features/<出洞id>/track/bug-…/reflection.md`。
2. 完整跑完 req 的 classify + define（新夹 `track/01`·`02`、Index 占行 📝）。
3. 交人表写完**回到本技能**收学习层交人，**不要**接着 pick_and_implement，除非用户本轮要落地产品。
4. 缺「人看见什么 / 下一步 / 有无可见面」仍先问人，再建夹。

## 自我升级强化（交人必须点名）

| 升了什么 | 路径 | 以后流水线哪里会不同 |
| --- | --- | --- |
| 原则（自我学习那一句） | `reflection.md` | classify / define / plan 的口 |
| 约定 / keep / 新夹合同 | | 下一次不会用同一种假门闩；新能力已有 `features/<id>/` |

没有「以后流水线哪里会不同」= 还停在交付层，学习层没做。

## 交人

| 项 | 写什么 |
| --- | --- |
| 高度 | 已离开交付层；本技能在 flow 之上 |
| 原则 | 自我学习的那一句 |
| 四问 | 各一句「设计为何没防住」 |
| 升级 | 约定 / sibling keep / **已触发的** `features/<新id>/`（req） |
| 未升 | notes 里待 req 的路径 |

## 禁止

- 把本技能画进 `classify → … → deliver` 当第九格
- 用「门闩已经绿了」代替反省（那是交付层的句号）
- 用 once 当「已预防」
- 空泛「加强测试 / 加日志」不点文件、不改口
- 新能力只写在 notes 里却不触发 req（用户说只要反省除外）
- 触发 req 后偷偷写 `src/`；或把管子加粗包装成新能力
