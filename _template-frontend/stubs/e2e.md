# E2E — `<FEATURE_TITLE>`

前置：UI `http://localhost:3000`。默认 **mock** 不依赖真 LLM。有头：`HEADED=1`。

SoT：[acceptance.md](./acceptance.md) · [methodology.md](./methodology.md)

## 规格文件

| 文件 | 覆盖 |
|------|------|
| `test/e2e/<feature-id>.spec.ts` | S1 / S2 / S3 |

## S1 — 进行中

1. mock 必要 API + 进行中事件（不要过早 `done`）  
2. 操作到可见面出现  
3. **期望**：合同 testid + 字段文本  

## S2 — 完成后 + 跨边界

1. 走到终态  
2. **期望**：临时物卸掉；终态 DOM 符合合同  
3. persist 后 `reload`（或换 session / 清 store）  
4. **期望**：仍能做 Y  

若 persist 被 route 掉，GET 必须仍返回那条可见物。

## S3 — 回归

相邻父合同（停止 / Rerun / mode…）仍绿。

## 命令

```bash
cd test/e2e && FRONTEND_URL=http://localhost:3000 npx playwright test <feature-id>.spec.ts --retries=0
cd test/e2e && HEADED=1 FRONTEND_URL=http://localhost:3000 npx playwright test <feature-id>.spec.ts --retries=0
```
