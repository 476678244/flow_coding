# 里程碑 — `<FEATURE_TITLE>`

| 里程碑 | 准入 | 准出 | 证据 |
|--------|------|------|------|
| M0 合同 | headed 现网探测 | 文档 + demo 齐套 | 本目录 |
| M1 数据 | M0 | 合同字段到达可见面 | dump / 断言 |
| M2 UI | M1 | 对照 demo 建议态 | headed |
| M3 边界 | M2 | 空态诚实；父合同不回归 | spec |
| M4 E2E | M3 | S1–S3 绿 | `test/e2e/<id>.spec.ts` |
| M5 验收 | M4 | acceptance 勾选 | 本文件 |

## 测试分层

| 层 | 覆盖 |
|----|------|
| Playwright mock | 进行中字段、完成后 DOM |
| Playwright 跨边界 | reload / persist 后再做 Y |
| 有头人工 | 对照 demo |
| 禁止当门闩 | 只 mock stream、不断言完成后 / 刷新 |
