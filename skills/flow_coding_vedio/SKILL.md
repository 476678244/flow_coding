---
name: flow_coding_vedio
description: 用代码做知识解说 / 战术分析 / 数据讲解短视频——脚本 → TTS 配音与时间轴 → Canvas 场景程序 → 无头 Chrome 逐帧渲染 → 抽帧看图自检 → ffmpeg 混音成 MP4。适用于用户要「做一个 X 秒的讲解视频」「用某人口吻讲某战术 / 历史 / 知识点」「像黄叔那样让模型自己做视频」的场景。不生成真人表演或电影级画面。
---

# Flow Coding Vedio

## 核心理念

模型不画像素，只写程序。画面是 `render(t)` 这个纯函数，本机 Chrome 逐帧执行，ffmpeg 编码。

所以这条路：

- **可控**：日期、地名、站位写在代码里，错了改一行重渲。
- **可续**：项目目录自包含。换会话、隔天、进程重启以后，改 `script.json` 或 `scene.html` 重跑三条命令，照样出新版本。
- **上限明确**：信息图、地图、战术板、数据动画可以做；真人表演、电影镜头做不了，要素材或生成模型补。

**看帧自检是这条路的门闩。** 代码跑通不等于画面对。每轮渲染后必须看静帧再交付。

---

## 0. 合同（动手前，缺项就问人）

| 项 | 要定什么 |
| --- | --- |
| 主题与受众 | 讲什么、给谁看 |
| 时长 | 目标秒数。`+20%` 语速下说话约 4.8 字/秒（含标点）；总时长还要加上 `lead`、句间 `gap`、`tail` |
| 口吻 | 仿谁的措辞；**只仿措辞，不克隆真人声音**（除非本人授权） |
| 配音 | 默认 edge-tts；有授权的克隆音 / 商用 TTS 由人提供 key |
| 素材 | 默认纯代码画面；影视空镜、照片由人提供并确认授权 |
| 输出目录 | 遵守当前仓库约定的工作区（仓库外），例如 `~/Downloads/safe_claw_worksapce/workspace/<slug>/` |

仿真人口吻或用合成音时，画面必须带免责声明（模板的 `DISCLAIMER`）。

---

## 流程

```
Task Progress:
- [ ] 1. 建项目目录，写 script.json
- [ ] 2. tts.py 配音 → timeline.json，时长对上目标
- [ ] 3. 从模板写 scene.html
- [ ] 4. 抽静帧 → 看图 → 修（≤3 轮）
- [ ] 5. 整片渲染 + mux，校验时长与音量
- [ ] 6. 交人
```

下面 `$SKILL` = 本目录，`$P` = 项目目录。

### 1. 建项目

```bash
mkdir -p "$P" && cp "$SKILL/templates/scene.template.html" "$P/scene.html"
python3 -m pip install -q --target "$P/pylib" edge-tts
```

`script.json` 字段：`voice`、`rate`、`gap`、`lead`、`tail`、`target_seconds`、`output`、`lines[{key,text}]`。完整样例：[examples/corner_defense/script.json](examples/corner_defense/script.json)。

写旁白：

- 每行 = 一个画面焦点，`key` 用英文短词（场景里按 key 取时间）。
- 每行 10–22 字，口语短句，一句只讲一件事。
- 总长 ≈ 字数 / 4.8 + `lead` + `gap`×(句数−1) + `tail`。超了删字，不要把语速拉过 `+25%`。

### 2. 配音

```bash
PYTHONPATH="$P/pylib" python3 "$SKILL/scripts/tts.py" --project "$P"
```

脚本输出每句时长和总长对目标的偏差。偏差超过 ±10% → 改 `lines` 重跑。音频为空会直接报错（macOS `say` 的多数中文男声就是空音频，见 [reference.md](reference.md)）。

### 3. 写场景

照 [templates/scene.template.html](templates/scene.template.html) 的约定：

- `window.setup(timeline)`、`window.render(t)`、`<canvas id="c" width="1920" height="1080">`。
- **`render(t)` 只依赖 t**：禁止 `setTimeout`、`requestAnimationFrame`、`Date.now()`、未设种子的 `Math.random()`。
- 每个动画用 `line(key).start / .end` 或 `focus(t, key)` 驱动，**不要写死秒数**。改旁白后画面会自动跟上。
- 分层画：背景 → 主体 → 当前焦点高亮（其余变暗）→ 标签卡 → 字幕 → 免责声明。
- 字体写进 `window.SCENE_FONTS`，渲染前会预加载。

完整示例（俯视球场、球员站位、弧线传中、整体外压）：[examples/corner_defense/scene.html](examples/corner_defense/scene.html)。

### 4. 静帧自检（门闩）

先从 `timeline.json` 算出每句中点，再按需要补关键动作的时刻（传球落点、外压结束）。不要抄别的片子的秒数，配音时长每次会有零点几秒的差别。

```bash
MIDS=$(python3 -c "import json;t=json.load(open('$P/timeline.json'));print(','.join(f'{(l[\"start\"]+l[\"end\"])/2:.1f}' for l in t['lines']))")
PLAYWRIGHT_MODULE=<node_modules/playwright> node "$SKILL/scripts/render.js" --project "$P" --stills "$MIDS"
```

用 Read 逐张看 `$P/stills/*.jpg`，对照下表：

| 查 | 典型毛病 |
| --- | --- |
| 重叠 | 人和人、卡片和标注、标签压线 |
| 对位 | 旁白说的东西此刻在画面上被高亮了吗 |
| 文字 | 截断、溢出、字叠字、图例文字压色点 |
| 运动终点 | 动画结束后的位置是否又撞到一起 |
| 事实 | 日期、地名、番号、数字和资料一致 |

发现问题 → 改 `scene.html` → 只重抽那几帧。**最多 3 轮**；第 3 轮还有问题，带静帧交人，不要硬交付。

### 5. 出片

```bash
PLAYWRIGHT_MODULE=<node_modules/playwright> node "$SKILL/scripts/render.js" --project "$P"
python3 "$SKILL/scripts/mux.py" --project "$P"
```

帧直接管道送进 ffmpeg，不落盘。`mux.py` 自己验收，不合格直接报错退出：

- 成片时长与 `timeline.total` 相差超过 0.1 秒
- 平均音量不在 -20 到 -14 dB

通过后再抽最后一帧看收尾。

### 6. 交人

一段话加一张静帧（`![](...)` 内嵌），说清：

- 成片路径、时长、分辨率
- 每句旁白对应的画面
- 修掉了哪些自检问题
- 哪些不是真的：合成音不是本人、画面是示意不是实拍
- 改法：改了 `script.json` 从第 2 步重跑，并且第 4 步静帧必须再看一遍（时间点变了）；只改了 `scene.html` 从第 4 步重跑

---

## Fail Fast

- `script.json` 缺字段、`key` 重复、某句没有 `text`、没有 `output` → `tts.py` 报错
- 某句音频短于 0.3 秒 → 报错，换 voice，禁止静默跳过
- 场景缺 `setup` / `render` / `canvas`，或渲染中抛异常 → `render.js` 报错并带页面错误
- 找不到 playwright → 报错，提示设 `PLAYWRIGHT_MODULE`
- 输出没有音轨 → `mux.py` 报错

## 依赖

- Node 18+、Google Chrome（`channel: 'chrome'`，不用 Playwright 自带浏览器）、Playwright npm 包
- Python 3.9+、ffmpeg / ffprobe
- edge-tts（装在 `$P/pylib`，不进项目环境）、联网

## 更多

- 踩坑、资源实测、合规边界、规模化：[reference.md](reference.md)
