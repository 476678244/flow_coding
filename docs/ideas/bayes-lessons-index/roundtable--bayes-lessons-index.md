# 圆桌：贝叶斯样本库这一页

底板：`obsidian_wiki_investment/.bayes_lessons/index.html`  
写出它的函数：`flow_coding/skills/bayes-lessons/scripts/bayes.py` 的 `render_html`。

用户在定义轮之后要求每人出一版 HTML。五版用同一份库：31 个问题，60 条还成立的事实。文末三节是导出器还会写出的状态（整库为空、空问、撤回），不是库里的事实。

## 功能合同

F1 页名。F2 导语，判断不上这一页。F3 整库为空写「还没有事实。」F4 每个 about 原句原序。F5 空问写「还没有事实。」F6 claim 原文并转义。F7 kind、id、出处同时在，且是文字。F8 出处链接文字是完整 evidence，href 为 `../` 加路径。F9 撤回有删除线，并写「已撤回」或「已撤回，由 {id} 代替」。F10 组内先开放后撤回。F11 `lang="zh"`，句子不改写。F12 五版本身无脚本。对照台的切换条有一段脚本。

## 五版

| 文件 | 人 | 这一版动的是 |
| --- | --- | --- |
| `01-monet.html` | 莫奈 | kind 做成三种光，铺在句子背后。句子仍是句子。 |
| `02-zhang.html` | 张大千 | 一条的问留白，两条到三条用细线，四条及以上收成通栏墨块。 |
| `03-norman.html` | Norman | 问题目录，条数写在目录上。类别、编号、出处分成带名字的字段，链接看得出来。 |
| `04-tufte.html` | Tufte | 问题并成小倍数。kind 与 id 在左列，句子与出处在右列，题后有条数。 |
| `05-rams.html` | Rams | 白底，一种无衬线，没有配色。kind、id、出处三列对齐。 |

对照台：`index.html`。

## 第二轮：标签如何落进 Tufte

用户选定 `04-tufte.html` 的呈现。标签按已有含义谈：口播里先点标签，只留下那一袋；命令没有 tags 字段。`about` 是袋名，`kind` 是轻重。

分岔：点开一个 about 之后，其余小倍数留下（Tufte、Rams）还是离场（张大千、Norman）。莫奈：标签不上色。一条事实再挂多个跨袋词，是新字段，这一轮不展开。

## 标签五版

对照台：`index-tags.html`。底都是 Tufte 的小倍数。标签是 about 原句，kind 仍在左列。

| 文件 | 点开一袋之后 |
| --- | --- |
| `06-tufte.html` | 其余袋子留下。这一袋只加一条黑边。再点一次取消。 |
| `07-norman.html` | 其余袋子离场。左侧「全部」回到整面墙。 |
| `08-rams.html` | 题不是控件。没有点开这一步。 |
| `09-zhang.html` | 先只看见袋名。点开后其余离场，这一袋铺开。`各袋` 回到名单。 |
| `10-monet.html` | 袋子都留下。光只在 fact / difference / bayesian 上，题不上色。点题只把这一袋滚到眼前。 |

## 合稿

用户留下莫奈和 Norman。`11-merge.html`：整面墙用莫奈的三种光；点开一袋按 Norman，其余离场，左侧「全部」回来。题不上色。格子仍是 Tufte 的左列坐标、右列句子和出处。点开优先于只滚动。

定稿写入 `skills/bayes-lessons/templates/export.html`。`export` 读这份模板。点开用页内链接，不放脚本。
