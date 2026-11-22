# track · bayes-lessons

`/flow-coding-software-engineering` 八段看板。开跑时把本目录拷到 `features/<id>/track/`（建夹从 `_template` 复制已带）。上一段 `status=done`（或规则允许的 `skipped`）才能开下一段。

`status`：`not_started` · `in_progress` · `blocked` · `done` · `skipped`

`skipped` 只许用在技能写明的 N/A（无 DOM 的 demo、`type=docs` 的 build）。**classify / deliver 不许 skip。** keep 测试不许 skip。

测试分类见 [tests.md](tests.md)。once 不能勾验收；keep 才能当门闩。

| # | 段 | 文件 | status | 出门闩 |
| --- | --- | --- | --- | --- |
| 1 | classify | [01-classify.md](01-classify.md) | done | 表已填，ROI 成立，下一跳 define |
| 2 | define | [02-define.md](02-define.md) | done | 合同句已钉，acceptance 未勾 |
| 3 | plan | [03-plan.md](03-plan.md) | done | 里程碑与 keep 已在 plan.md |
| 4 | build | [04-build.md](04-build.md) | done | 先红 15，后绿 15 |
| 5 | verify | [05-verify.md](05-verify.md) | done | 本夹 keep 15 passed |
| 6 | review | [06-review.md](06-review.md) | done | 三面过 |
| 7 | QA_Check | [07-qa-check.md](07-qa-check.md) | done | 验收已勾 |
| 8 | deliver | [08-deliver.md](08-deliver.md) | done | 交人三步 |

合同：看得见的一条带出处的观察 → 跨过进程退出再启动 → 仍能按同一个问题调出这条还成立的观察
