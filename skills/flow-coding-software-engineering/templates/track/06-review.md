---
stage: review
seq: 6
status: not_started
started_at:
ended_at:
---

# track · review · __feature_id__

未过不得 QA_Check 勾 ✅。不在这里用 once 截图代替审 keep。

## Gate in

- [ ] [05-verify.md](05-verify.md) `status=done`

## 三面

| 面 | 结论 | 备注 |
| --- | --- | --- |
| security | 过 / 未过 | HTML 消毒；无 `\|safe` 喂脏数据；无 token；不爬全文 |
| quality | 过 / 未过 | 一次一件；中文编辑语气；纸色墨色；逻辑可单测 |
| performance | 过 / 未过 | 无新全库扫描；抓取有超时与并发上限 |

## keep 抽查

| 问 | 答 |
| --- | --- |
| `test_*_regression.py` 是否真跨边界？ | |
| 有无 once 脚本混进默认套件？ | |
| 有无 skip-forever / 放宽断言？ | |

L：每面另写 3–6 条到 `notes.md`。

## Gate out

- [ ] 三面过
- [ ] keep 抽查无「假回归」

## Blockers
