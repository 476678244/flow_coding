# 证据 — `<FEATURE_TITLE>`

对照：[acceptance.md](./acceptance.md) · [guide.md](./guide.md) · [e2e.md](./e2e.md)

## 结论

`<一句话：过了什么，冻了什么。>`

## 命令与结果（YYYY-MM-DD）

```bash
cd test/e2e
npx playwright test <feature-id>.spec.ts --retries=0
HEADED=1 npx playwright test <feature-id>.spec.ts --retries=0
```

| 轮次 | 模式 | 结果 |
|------|------|------|
| | headless | |
| | headed | |

| ID | 锁什么 | 结果 |
|----|--------|------|
| S1 | 进行中可见面 | |
| S2 | 完成后 + 跨边界 | |
| S3 | 父合同回归 | |

## Phase 0 现网基线

```text
~/Downloads/safe_claw_worksapce/workspace/<probe>-during.png
~/Downloads/safe_claw_worksapce/workspace/<probe>-after.png
```

冻结 class / 文案（若适用）：

```text
```

## 实现触点

| 文件 | 作用 |
|------|------|
| | |

**未改**：`<冻结组件>`
