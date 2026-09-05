# templates · flow-coding-software-engineering

本夹是 **`/flow-coding-software-engineering` 各段的空白稿**。拷进工作目录再填真值，空着不当完成。

**SoT**：进度 / 出门闩只认 `features/<id>/track/`。下面「内容底稿」补栏位，填完回写对应 `track/0N-*.md`，禁止只填底稿不改 status。

- **跟踪（必填）**：[track/](track/Index.md) → 建夹已在 `_template/track/`
- **两类测试**：[tests.md](tests.md)（与 [track/tests.md](track/tests.md) 须同文）
- feature 夹本体从 [features/_template](../../../../features/_template/Index.md) 复制（必带 `references/` + `track/`）

占位符：`__feature_id__`（kebab）· `__id__` / `__slug__`（下划线）。

| 段 | 跟踪 | 内容底稿 → 落到 |
| --- | --- | --- |
| classify | [track/01-classify.md](track/01-classify.md) | [classify.md](classify.md) 对话交人 |
| define | [track/02-define.md](track/02-define.md) | `_template/spec.md` 已含 §API；[demo.html](demo.html) 已在 `_template`（无 DOM 则删） |
| plan | [track/03-plan.md](track/03-plan.md) | [plan.md](plan.md) → 本夹；可见面 e2e → 本夹 [test___id___e2e.spec.ts](test___id___e2e.spec.ts) |
| build | [track/04-build.md](track/04-build.md) | [build.md](build.md) 可并 notes |
| verify | [track/05-verify.md](track/05-verify.md) | [verify.md](verify.md) |
| review | [track/06-review.md](track/06-review.md) | [review.md](review.md) |
| QA_Check | [track/07-qa-check.md](track/07-qa-check.md) | [qa-check.md](qa-check.md) + 夹内两份报告 |
| deliver | [track/08-deliver.md](track/08-deliver.md) | [deliver.md](deliver.md) · [handoff.md](handoff.md) |

不要把底稿整份复制进夹根（`track/` 除外）。不要用示例 JSON 冒充已实现。once 不进 `acceptance.md`。
