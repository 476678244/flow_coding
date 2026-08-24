# 使用指南 — `<FEATURE_TITLE>`

`<一句话：人打开 UI 后怎么用。>`  
定版：[demo-`<feature-id>`.html](./demo-`<feature-id>`.html) · 行为：[methodology.md](./methodology.md)

## 使用前

1. API `http://localhost:8000` 与 UI `http://localhost:3000` 已起。  
2. `<进入功能的路径：New Chat / /ppt / …>`  
3. 改过代码后**重启对应 server** 并硬刷新，不要依赖旧 HMR。

## 你会看见什么

| 时候 | 人看见 | 下一步 |
|------|--------|--------|
| 进行中 | `<可见物>` | `<等 / 确认 / 停止>` |
| 完成后 | `<终态>` | `<继续聊 / 改 / 贴>` |
| 跨边界（刷新 / 换会话） | `<仍能看见的>` | `<仍能做的 Y>` |

## 操作

| ID | 操作 | 期望 | 证据 |
|----|------|------|------|
| G1 | | | E2E S1 |

## 不要指望

- `<本期明确不做>`  

## 自己复验

```bash
cd test/e2e
FRONTEND_URL=http://localhost:3000 npx playwright test <feature-id>.spec.ts --retries=0
HEADED=1 npx playwright test <feature-id>.spec.ts --retries=0
```
