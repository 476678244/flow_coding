---
name: markdown-preview-obsidian
description: >-
  给 VS Code 系编辑器（Devin Desktop / Cursor / Windsurf / VS Code）装同一套
  Obsidian 风格 markdown 预览：双击 .md 默认开预览、预览内双击跳源码、
  [[wikilink]] 可点跳转 + Backlinks 面板 + 共享主题 CSS，多端 UX 一致。
  Use when 用户说「配置 markdown 预览」「markdown preview plugin」
  「Obsidian 双向链接」「两个编辑器要同样的预览体验」「设置默认 preview」。
---

# Markdown Preview Obsidian（多端同一套预览）

## 验收合同（可见即可续）

```
看得见的预览（wikilink 高亮可点 / 双击跳源码 / 主题生效）
  → 跨过 Reload Window · 重启 App（配置全在盘上：扩展目录 + settings.json + CSS）
  → 仍能：双击 .md 开预览、预览内双击跳源码、[[链接]] 跳转、主题仍在
```

装完立刻能看不算数；必须重启后复验。CLI 列表 / JSON 校验是 once 级，不能当门闩关账。

## 选型（不要换）

| 需求 | 机制 |
| --- | --- |
| 默认 preview | 内置 Markdown 预览 + `workbench.editorAssociations: {"*.md": "vscode.markdown.preview.editor"}` |
| 双击看源码 | 内置预览原生行为：预览里双击元素 → 打开源码并滚动到该行 |
| `[[Obsidian 双向链接]]` | `svsool.markdown-memo`（Open VSX，经 `markdown.markdownItPlugins` 注入内置预览；含 Backlinks 面板、`[[a|别名]]`、`![[嵌入]]`、悬停预览） |
| 主题 | `markdown.styles` 指向共享 CSS（本仓 `assets/obsidian-wiki.css`） |

为什么不用 Markdown Preview Enhanced：它是另一套预览，顶掉默认、丢「双击跳源码」。禁止。

## 执行（macOS，每个 App 一遍）

### 0. 定位 App 三件套

| App | CLI | 扩展目录 | settings.json |
| --- | --- | --- | --- |
| Devin Desktop | `/Applications/Devin.app/Contents/Resources/app/bin/devin-desktop` | `~/.devin/extensions` | `~/Library/Application Support/Devin/User/settings.json` |
| Cursor | `cursor` | `~/.cursor/extensions` | `~/Library/Application Support/Cursor/User/settings.json` |
| Windsurf | `windsurf` | `~/.windsurf/extensions` | `~/Library/Application Support/Windsurf/User/settings.json` |
| VS Code | `code` | `~/.vscode/extensions` | `~/Library/Application Support/Code/User/settings.json` |

### 1. 装扩展（每端同版本）

```bash
<CLI> --install-extension svsool.markdown-memo
```

- CLI 卡几分钟不算失败：直接查 `<扩展目录>/svsool.markdown-memo-*` 目录和 `extensions.json` 里有没有注册。
- 市场装不上：从 Open VSX 下 VSIX 再本地装（`downloads.universal` 字段）：
  `https://open-vsx.org/api/svsool/markdown-memo/latest`
  ```bash
  <CLI> --install-extension /path/to/svsool.markdown-memo-<ver>.vsix
  ```

### 2. 放共享主题 CSS

```bash
mkdir -p ~/.config/markdown-preview
cp <本技能夹>/assets/obsidian-wiki.css ~/.config/markdown-preview/
```

### 3. 合并 settings（幂等脚本，禁止手抄）

把 `<settings.json 路径>` 换成上表路径，每端跑一次：

```bash
python3 - <<'EOF'
import json, os
p = os.path.expanduser("<settings.json 路径>")
s = json.load(open(p))
s.update({
  "workbench.editorAssociations": {"*.md": "vscode.markdown.preview.editor"},
  "markdown.preview.openMarkdownLinks": "inPreview",
  "markdown.preview.breaks": True,
  "markdown.preview.linkify": True,
  "markdown.preview.typographer": True,
  "markdown.preview.fontFamily": "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Segoe UI', sans-serif",
  "markdown.preview.fontSize": 15,
  "markdown.preview.lineHeight": 1.75,
  "markdown.styles": ["file://" + os.path.expanduser("~/.config/markdown-preview/obsidian-wiki.css")],
  "memo.markdownPreview.enabled": True,
  "memo.links.format": "short",
  "memo.backlinksPanel.enabled": True,
})
json.dump(s, open(p, "w"), ensure_ascii=False, indent=2)
EOF
```

要点：

- `openMarkdownLinks: "inPreview"`：预览里点 `.md` 链接不跳出预览（Obsidian 阅读流）。
- `memo.links.format: "short"`：`[[名字]]` 按文件名在 workspace 内解析，最接近 Obsidian 语义。

### 4. 自动验证（once 级）

```bash
<CLI> --list-extensions --show-versions | grep memo
python3 -m json.tool <settings.json> > /dev/null && echo valid
ls ~/.config/markdown-preview/obsidian-wiki.css
```

### 5. 人验三步（真门闩，Reload Window 之后）

1. 双击任一 `.md` → 直接开预览（不是源码，也不是别的编辑器）
2. 预览里**双击**某段文字 → 跳到源码对应行
3. 点 `[[wikilink]]` → 跳到目标卡；Explorer 出现 Backlinks 面板；断链是红色虚线

## 坑（写死）

- fabriqa / ognile 等自定义编辑器以 `priority: "default"` 抢 `*.md`——显式 `editorAssociations` 是唯一压制手段；**不要**为了「统一」去卸载用户装的其他插件，报告即可。
- Memo 的渲染 class：wikilink = `a[data-href]`，断链 = `.memo-invalid-link`，`![[嵌入]]` = `.memo-markdown-embed*`。主题选择器写 `.wiki-link` 是错的（那是 kortina 系的 class，不通用）。
- 「多端同样体验」= 同扩展版本 + 同一份 CSS 文件 + 同一 settings 块，缺一即不成立。
- Memo v0.3.19 是 2022 年的版本：老但稳，`markdown.markdownItPlugins` 这条注入路径依赖内置预览 API，升级前先在单端试。

## 交人表

| 栏 | 值 |
| --- | --- |
| 走了哪把 | `markdown-preview-obsidian` |
| 改了什么 | 每端：装 `svsool.markdown-memo`、合并 settings 块、放共享 CSS（列出具体路径与版本） |
| 自动验证 | `--list-extensions` / `json.tool` 结果（once，未当门闩） |
| 人验三步 | Reload Window 后：默认预览 / 双击跳源码 / wikilink 跳转 |
| 未做的 | 未在真实窗口手点的端，写明「未验」，不许默认通过 |
