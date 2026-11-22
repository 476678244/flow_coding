# define · recall 换个说法就取不到

status: done（2026-11-22 补记；修洞与本次 v2 重构同轮完成）

1. Symptom：投资库里 `recall --about "美股指数怎么走？"` 返回 4 条，`recall --about "美股指数怎么走"`（少一个问号）返回 0 条，`recall --about "纳指还会跌吗？"` 返回 0 条。
2. Broken next step：代理按 AGENTS.md「先 recall 问题原话」开工，原话几乎不会和库里的句子逐字相同，先验每轮都是空的。
3. Boundary：新会话：用户换了一种问法。
4. Acceptance after fix：看得见的一柜事实 → 跨过「换一种问法 / 新会话」 → 仍能按柜子 `recall --tag` 整柜倒出，或用 `--q` 词兜底取到。
5. Coverage gap：v1 keep `test_recall_unknown_about_is_empty_list` 把「换说法为空」锁成了正确行为；没有一条测试问「同一类换个说法还取得到吗」。

Root cause：v1 `recall` 的过滤条件是 `row.get("about") == about`，取数钥匙是整句，不是类别。
