---
stage: review
seq: 6
status: done
started_at: 2026-11-10T08:26:00+08:00
ended_at: 2026-11-10T08:27:00+08:00
---

# track · review · bayes-lessons

未过不得 QA_Check 勾 ✅。不在这里用 once 截图代替审 keep。

## Gate in

- [x] [05-verify.md](05-verify.md) `status=done`

## 三面

| 面 | 结论 | 备注 |
| --- | --- | --- |
| security | 过 | 无 HTML。证据路径拒绝 `..` 和绝对路径，只读仓库内已存在的文件，不执行命令，不写 token |
| quality | 过 | 一次一件：两个动词。判断留在技能正文，不进日志。逻辑在一个脚本里，测试直接打进程 |
| performance | 过 | 不扫仓库。只读 `.bayes_lessons/facts.jsonl` 和证据指出的那一个文件 |

## keep 抽查

| 问 | 答 |
| --- | --- |
| `test_*_regression.py` 是否真跨边界？ | 是。`note` 与 `recall` 是两次 `subprocess`，第二次是新解释器 |
| 有无 once 脚本混进默认套件？ | 无 |
| 有无 skip-forever / 放宽断言？ | 无。占位 skip 已换成断言 |

## Gate out

- [x] 三面过
- [x] keep 抽查无「假回归」

## Blockers
