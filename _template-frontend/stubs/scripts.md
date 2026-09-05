# 脚本 — `<FEATURE_TITLE>`

临时文件只写 `~/Downloads/safe_claw_worksapce/workspace/`。

## 定版 demo

```text
docs/features/<feature-id>/demo-<feature-id>.html
```

## Phase 0 探测（不进仓库）

```bash
cd test/e2e
# 从 workspace 拷入探测 spec，跑完删除
HEADED=1 npx playwright test <probe>.spec.ts --retries=0
```

## 实现后

```bash
cd test/e2e
npx playwright test <feature-id>.spec.ts --retries=0
HEADED=1 npx playwright test <feature-id>.spec.ts --retries=0
```
