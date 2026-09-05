---
name: new_bug_fix
description: >-
  Fixes one live product hole through /flow-coding-software-engineering
  with type=bug: classify, write the broken next-step contract, add a keep
  regression that is red today, then fix. Use when the user runs /new_bug_fix
  or a visible next step broke across a boundary.
disable-model-invocation: true
---

# /new_bug_fix

## 开发流程（总管）

本仓库完整管道是 [`/flow-coding-software-engineering`](../flow-coding-software-engineering/SKILL.md)，按序：

```
classify → define → plan → build → verify → review → QA_Check → deliver
```

本命令是 **`type=bug`** 的走法：**不要开新主题夹**。define 写的是「洞的合同」，不是新能力。

| 本命令负责 | 不负责 |
| --- | --- |
| 八段都走，但压在**已有** `features/<id>/` | 新能力 → [`/new_feature_req`](../new_feature_req/SKILL.md) |
| 先补会红的 **keep**，再改产品 | 用 once 截图 / 手点关账 |
| 进度写 `features/<id>/track/bug-<YYYY-MM-DD>-<slug>/`（见下） | 覆写该夹原有 `track/01–08`（那是 feature 自己的交付记录） |
| | SafeClaw 的 `TC-*`、`test.regression.discover`、`logs/bugs/`、`safe_claw/`（本仓库没有） |

**bug 子夹**：`cp -R features/_template/track features/<id>/track/bug-<YYYY-MM-DD>-<slug>`，八段 status 只改这里。旧夹没有 `track/` 也一样建这个子夹即可。学习层的 `reflection.md` / `self-reflect.md` 之后也落在同一子夹。

once vs keep：[templates/tests.md](../flow-coding-software-engineering/templates/tests.md)。可见即可续：[规则](../../rules/visible-then-continuable.mdc)。

一次只处理**一个**洞。用户说「先入账」：做到 define 停。给了症状并调用本命令：keep 先红，再修。**deliver 写完不要停**（除非用户只要修洞）：同一轮立刻跑 [`/self-reflect-after-bug-fix`](../self-reflect-after-bug-fix/SKILL.md)。

不要跑 `bash test/run_regression.sh`，除非用户本轮明确要求。临时文件写仓库外，不要 `/tmp`、不要进 git。

---

## classify

填 `track/bug-…/01-classify.md`：`type=bug` · complexity · urgency_priority · ROI。管子加粗当修洞 → 停，问人。

| 可见即可续 | 必须答 |
| --- | --- |
| 人看见什么 | |
| 看见之后哪步断了 | |
| 跨了哪条边界 | 重启 / uvicorn reload / 新 sqlite / 新 `create_app` / 刷新页 |

对不上号：页/API + `logs/frontend/` + `logs/backend/`，不要猜。

## define（入账，不新建 feature 夹）

写进 `track/bug-…/02-define.md`；出洞夹 `notes.md` 加一行指向它。

必须有：

1. Symptom  
2. Broken next step  
3. Boundary  
4. Acceptance after fix：`看得见的 X → 跨过 <边界> → 仍能做 Y`  
5. Coverage gap：哪条本夹 `test_*_regression.py`（或缺失的 keep）该拦？为何没拦（从未创建冒充 persist / 只 mock / 断言太弱 / ✅ 勾早了）？

禁止看见症状就改 `src/` / `frontend/`。

## plan

`track/bug-…/03-plan.md`：当天补哪条 **keep**（优先 `test_<slug>_regression.py`：写盘 → 新连接 / 新 `create_app` → 下一步仍成立）。once 探测可列，不能当门闩。

## build

1. 先把 keep 写成**现在会红**的测试并入库。  
2. 跑红。  
3. 只改修这个洞所必需的文件。  
4. 再跑，必须因对的原因绿。  

禁止：静默 fallback；用 once 代替 keep；「从未创建」Fail Fast 冒充 persist；mock 流式接口当续得上。有可见面：改完走主路径（once），记 `track/bug-…/04-build.md`。

## verify · review · QA_Check

```bash
.venv/bin/python -m pytest features/<id> -v --tb=short
.venv/bin/python -m pytest tests features -q --tb=short
```

| 段 | 过关 |
| --- | --- |
| verify | 本夹 keep 绿；acceptance-report 先记后勾；`bug-…/05` |
| review | security / quality / performance 短表；`bug-…/06` |
| QA_Check | 本夹 + 全库；有本夹 e2e 再跑；`bug-…/07`。once 手走不勾 ✅ |

自问：若今天这条 keep 当初存在，这次洞会红吗？不会 → 门闩仍假，不要关账。

## deliver

`track/bug-…/08-deliver.md`。交人只报 **keep** 命令与结果。用户没要求不要 git commit。

| 洞 | classify → deliver 到哪 | keep | 命令 |
| --- | --- | --- | --- |
| 一句话 | 段 | `features/<id>/test_*_regression.py` | 这一次的 pytest |

交人表写完**立刻**打开并完整遵循 [self-reflect-after-bug-fix/SKILL.md](../self-reflect-after-bug-fix/SKILL.md)。目的：反思为什么现有的测试设计 / 系统设计 / log设计 / 架构设计没有提前预防这个 bug。不要等用户再发一次。用户本轮明确说「只要修洞」才停。

## 禁止

- 开新主题夹修已有洞；或覆写该夹原有 `track/01–08`  
- 先改产品再补测试  
- 走 `TC-*` / `discover` / `logs/bugs/`  
- 用 once 关账；放宽断言换绿  
