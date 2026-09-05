# `<FEATURE_TITLE>`

`<一句话：进行中看见什么，完成后必须怎样>`

| 项 | 值 |
|----|-----|
| Feature ID | `<feature-id>` |
| 定版 demo | [demo-`<feature-id>`.html](./demo-`<feature-id>`.html) |
| SoT（行为） | [methodology.md](./methodology.md) |
| 验收标准 | [acceptance.md](./acceptance.md) |
| 使用语境 | 个人自用；Fail Fast；浅色 |
| 状态 | Phase 0 进行中 |

## 一句话合同

> `<进行中改什么。完成后禁止什么。>`

## 可见即可续

```text
看得见的 X  →  跨过 <边界>  →  仍能做 Y
```

## 文档索引

1. [problem.md](./problem.md)  
2. [methodology.md](./methodology.md)  
3. [plan.md](./plan.md)  
4. [milestones.md](./milestones.md)  
5. [acceptance.md](./acceptance.md)  
6. [e2e.md](./e2e.md)  
7. [scripts.md](./scripts.md)  
8. [guide.md](./guide.md) — 产品怎么用  
9. [evidence.md](./evidence.md) — 验收证据  
10. [demo-`<feature-id>`.html](./demo-`<feature-id>`.html)  

## 相关代码

| 区域 | 路径 |
|------|------|
| 进行中可见面 | `<tsx>` |
| 完成后可见面（若冻结则禁止改） | `<tsx>` |
| SSE / API | `<path>` |
| 测试 | `test/e2e/<feature-id>.spec.ts` |
