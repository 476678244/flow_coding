# .bayes_lessons · Agents（给任何 agent 的第一句话）

> 本文件由 [`/bayes-lessons-setup`](file://@@SETUP_SKILL@@) 生成，属于元数据，不要手改。

**你看到了 `.bayes_lessons/`，说明这个仓库启用了 `/bayes-lessons`。在这里做任何事之前，先打开并照着做下面两份 agent 技能。它们是唯一真本，存放在 flow_coding 仓库，不在本仓库：**

| 什么时候 | 打开哪份技能 |
| --- | --- |
| 每一轮工作：开工 `recall`、记 `note` / `link`、温故 `review` / `doctor` | [`/bayes-lessons`](file://@@BAYES_SKILL@@)（`@@BAYES_SKILL@@`） |
| 第一次启用、重建、补 template、迁移旧数据 | [`/bayes-lessons-setup`](file://@@SETUP_SKILL@@)（`@@SETUP_SKILL@@`） |

脚本只有一份：`python3 @@BAYES_PY@@ <命令>`。在本仓库任意目录里运行即可，脚本会自己找到 git 根。

这一份库是「@@PERSON@@ × @@REPO@@」。第一性原理：@@PERSON@@ 与 AI Agent 共同成长，成长的路上谁都不落下。

本目录里的文件：

| 文件 | 是什么 | 能不能手改 |
| --- | --- | --- |
| `template.md` | 本库的元数据框架：什么算数据、柜子、什么时候记 | 不能。已上锁，只有 @@PERSON@@ 明确要求时才改，改完 `template --approve` |
| `cabinets.json` | 柜子清单 | 不能。用 `bayes.py cabinets` |
| `meta.json` | 人、仓库、入库门槛、template 的锁和出处、技能路径 | 不能。由 setup 和 `bayes.py` 维护 |
| `brain.jsonl` | 数据：只追加的石头和 link | 不能。只用 `bayes.py note` / `link` 追加 |
| `index.html` | 给人看的页面 | 不能。由 `bayes.py export` 生成 |

开工先跑这两条：

```bash
python3 @@BAYES_PY@@ recall          # 会给出 template 路径、growth、各种 hint
python3 @@BAYES_PY@@ template        # 确认 template 没被改过
```
