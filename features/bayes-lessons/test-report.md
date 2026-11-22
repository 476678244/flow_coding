# test-report · bayes-lessons

2026-11-10

```bash
.venv/bin/python -m pytest features/bayes-lessons -v --tb=short
```

15 passed in 0.46s。

- unit 13：技能正文、空仓库 recall、无证据、五个推论词、`investigate` 不是动词、成功追加、未知问题、坏日志、路径逃逸
- regression 2：新进程 recall；新进程里撤回后的 recall

仓库没有 `tests/`。`.venv/bin/python -m pytest features -q --tb=line` → 15 passed in 0.45s。

无 e2e。Phase 0「脚本文件不存在」是 once，未当门闩。

## 本仓真跑（once，未代替上面的 keep）

`features/bayes-lessons/real-run.txt`：pytest **17 passed**。跑完时 `.bayes_lessons` 仍 absent。随后第一次 `recall` 写出 `meta.json`，没有 `facts.jsonl`。

然后再 `note` 六条带行号的事实，新进程 `recall` 六条都在。问题是「打开 /bayes-lessons 时，.bayes_lessons 什么时候出现？」。旧信念只在对话里：技能文件落地时目录就已经在。日志里没有这句。
