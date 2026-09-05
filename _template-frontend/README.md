# 前端功能开发流程 Template

可复用的**完整前端功能**开发流程。新功能会留下「人看得见的东西」时，**先复制本目录，再写代码**。

| 项 | 值 |
|----|-----|
| 路径 | `docs/features/_template-frontend/` |
| 流程 SoT | [PROCESS.md](./PROCESS.md) |
| 对照实例 | [thinking-realtime-display](../thinking-realtime-display/)（诊断 → demo → 合同 → 再实现） |
| 父约定 | [../README.md](../README.md) · [可见即可续](../../../.cursor/rules/visible-then-continuable.mdc) · [Flow Coding](../../flow_coding.md) |

## 何时必须用

改 UI / 布局 / 路由 / 客户端状态 / 流式展示 / 卡片 / 预览 / 确认框。  
不适用于纯后端 pytest、纯脚本、无可见面的重构。

## 开新主题（复制）

```bash
# 在仓库根
FEATURE=my-feature-id   # kebab-case
cp -R docs/features/_template-frontend docs/features/$FEATURE
rm -f docs/features/$FEATURE/PROCESS.md docs/features/$FEATURE/README.md
# 把 stubs 里的 <FEATURE_ID> / <一句话合同> 换成真值
# 把 PROCESS.md 留在 _template-frontend，不要拷进主题当正文
```

然后按 [PROCESS.md](./PROCESS.md) **从 Phase 0 做到 Phase 9**，禁止跳过 headed 现网确认；交付当天重启 server。

复制后主题内应有：

| 文件 | 来源 |
|------|------|
| `README.md` | [stubs/README.md](./stubs/README.md) |
| `problem.md` | [stubs/problem.md](./stubs/problem.md) |
| `methodology.md` | [stubs/methodology.md](./stubs/methodology.md) |
| `plan.md` | [stubs/plan.md](./stubs/plan.md) |
| `milestones.md` | [stubs/milestones.md](./stubs/milestones.md) |
| `acceptance.md` | [stubs/acceptance.md](./stubs/acceptance.md) |
| `e2e.md` | [stubs/e2e.md](./stubs/e2e.md) |
| `scripts.md` | [stubs/scripts.md](./stubs/scripts.md) |
| `guide.md` | [stubs/guide.md](./stubs/guide.md) — **给人用** |
| `evidence.md` | [stubs/evidence.md](./stubs/evidence.md) — 命令 / pass 表 / 基线 |
| `demo-<id>.html` | [stubs/demo.template.html](./stubs/demo.template.html) |

最后在 [features README](../README.md) 表里加一行。

## 不要做的事

- 先写实现再补 problem / demo  
- 用假步骤、假图、假进度填空可见面  
- 把「同进程工具成功」写成验收完  
- 临时文件写进仓库或 `/tmp`（只写 `~/Downloads/safe_claw_worksapce/workspace/`）  
- 改合同外的「完成后原始界面」  
