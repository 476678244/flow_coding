---
stage: deliver
seq: 8
status: not_started
started_at:
ended_at:
---

# track · deliver · __feature_id__

不许 skip。用户没要求不要 git commit / 开 PR。

## Gate in

- [ ] [07-qa-check.md](07-qa-check.md) `status=done`（未实现停在 define 则 QA 为 skipped，本段仍交人）

## 交付

| 项 | 是否改 | 路径 / why |
| --- | --- | --- |
| docs | 是 / 否 | 只改已有篇；没有新 why 不开长文 |
| guide | 是 / 否 | :8000 / :5173 |
| product design thinking | 必写 | 读者看见什么；是否更少更准；故意不做 → `notes.md` |

## 交人（keep 与 once 分开写）

| 段 | 写什么 |
| --- | --- |
| classify | type · complexity · urgency_priority · ROI |
| 夹 | `features/__feature_id__/` |
| define | spec / acceptance / api / demo |
| plan | 里程碑数；keep 文件；once 探测种类 |
| 改了 | 作用域内文件 |
| keep | 命令与结果；哪些验收 ⬜→✅ |
| once | 做了哪些探测；**明确写「未当门闩」** |
| review | security / quality / performance |
| 人怎么验 | 1.  2.  3. |
| 未做 | 没跑的浏览器步、没引入的依赖 |

不要提交 `data/`、`.venv/`、`__pycache__/`、`logs/**/runtime/`。不要把 once 写进 `docs/` 当产品验收。

## Gate out

- [ ] 交人表填完
- [ ] keep / once 未混报

## Blockers
