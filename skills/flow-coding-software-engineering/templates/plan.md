# plan · __feature_id__

入口 [Index.md](Index.md)。本文件在 plan 段填写，**仍不改产品**。S 可把各节缩进 `notes.md`。

## arch design pattern

- 改哪些模块（业务进可单测模块，不堆路由 / Vue）：
- 配置（只进 `src/config.py`）：无则写「不新增配置」

## dependency

| 依赖 | 为何必要 | 能否不引入 |
| --- | --- | --- |
| （无则删行） | | |

默认禁止 Postgres / Redis / Docker / 后端 Node。没有 key 时降噪仍可用。

## solution

走现有管道的哪一段（OPML → 抓取 → 聚类 → 打分 → 配额 → 精选 / 落选可审计）。不另造平行分类。

## steps_milestones

| # | 切片 | once（过程探测，不入库） | keep（先红哪条，入库） | 绿了人看见什么 |
| --- | --- | --- | --- | --- |
| 1 | | Phase 0 / curl / 手点 | `test___id___unit.py` · | |
| 2 | | | `test___id___regression.py` · 跨边界 | |

禁止「一大坨实现完再测」。禁止只填 once。

## keep · UT

`features/__feature_id__/test___id___unit.py` 要锁的函数 / API 合同：

## keep · playwright e2e（仅入库才写这里）

- 无 DOM：`N/A`
- 一次性探路 PW → 只记 `track/04-build.md` once 栏
- 入库：本夹 [test___id___e2e.spec.ts](test___id___e2e.spec.ts)（建夹后改名为 `test_<slug>_e2e.spec.ts`）
