# 两类测试

计划、实现、验收时必须先标类，禁止混成「测过了」。

| | **once · 过程探测** | **keep · 质量回归** |
| --- | --- | --- |
| 面向 | 这一轮开发有没有走偏 | 产品以后改别处还会不会坏 |
| 寿命 | 本轮；记在 `track/`，默认不进套件 | 入库；`pytest` 默认会跑 |
| 典型 | Phase 0 现网 curl/截图、手点浏览器、一次性 PW 探路、`tail` 日志、REPL | 本夹 `test_<id>_unit.py` · `_regression.py` · `_e2e.spec.ts`；仅跨 feature 才进 `tests/` |
| 勾 `acceptance.md` ✅ | **不能** | **可以**（有可见面必须跨边界） |
| 报告 | `track/04-build.md` / `05-verify.md` 的 once 栏 | `test-report.md` + `acceptance-report.md` |

## once（开发过程 · 一次性）

用来回答「现在这一步做对了吗」。做完记证据，**不要**把脚本留成永久 skip、不要当门闩。

- 未改代码前的页 / API 基线（Phase 0）
- milestone 之间的手测、一次性截图、探路 PW
- 三角定位时读的 `logs/frontend/` · `logs/backend/`
- 某次 TDD 的红/绿**命令输出**（跑次是 once；写成文件的断言若入库则算 keep）

## keep（产品质量 · 回归）

用来回答「人看见之后，跨过边界，还能不能做下一步」。要能红能绿，禁止 skip-forever。

| 文件 | 锁什么 |
| --- | --- |
| 本夹 `test_<id>_unit.py` | 模块内行为、函数/API 合同（可内存库） |
| 本夹 `test_<id>_regression.py` | **跨边界**：写盘 → 关连接或新 `create_app` → 下一步仍成立 |
| 本夹 `test_<id>_e2e.spec.ts` | 可见面：打开、点、刷新后续做。无 DOM 则不建 |
| `tests/test_*.py` | **仅**跨多个 feature 的冒烟，不代替夹内文件 |

没跨过边界的断言不是质量回归。禁止：「从未创建」Fail Fast 冒充 persist；只 mock 流式接口；用 once 的截图代替 keep。

## 各段谁写谁跑

| 段 | once | keep |
| --- | --- | --- |
| classify | 无 | 无（只分类） |
| define | 无 | 在 `acceptance.md` **点名**将要锁的 keep，先不写断言 |
| plan | 列出本轮会做的探测 | 列出将入库的文件与每条锁什么 |
| build | 每片里程碑先做探测，再红 keep | 把 keep 写成真文件 |
| verify | 对不上号时再探测 | 跑本夹 unit + regression |
| review | 无测试门闩 | 抽查 keep 是否真跨边界 |
| QA_Check | 浏览器主路径若未入库，记「做了/未做」 | 本夹 + 全库；有入库 e2e 再跑 |
| deliver | 不把 once 写进产品文档当验收 | 交人只报 keep 命令与哪些 ⬜→✅ |
