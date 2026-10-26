---
name: flow-vedio
description: 用代码做知识解说 / 战术分析 / 数据讲解短视频——脚本与导演卡 → TTS 配音与时间轴 → Canvas 场景程序 → 无头 Chrome 逐帧渲染 → 静帧按卡评审与冻帧检测 → ffmpeg 混音成 MP4。适用于用户要「做一个 X 秒的讲解视频」「用某人口吻讲某战术 / 历史 / 知识点」「像黄叔那样让模型自己做视频」的场景。不生成真人表演或电影级画面。
---

# Flow Vedio

## 核心理念

模型不画像素，只写程序。画面是 `render(t)` 这个纯函数，本机 Chrome 逐帧执行，ffmpeg 编码。

所以这条路：

- **可控**：日期、地名、站位写在代码里，错了改一行重渲。
- **可续**：项目目录自包含。换会话、隔天、进程重启以后，改 `script.json` 或 `scene.html` 重跑三条命令，照样出新版本。
- **上限明确**：信息图、地图、战术板、数据动画可以做；真人表演、电影镜头做不了，要素材或生成模型补。

**看帧自检是这条路的门闩。** 代码跑通不等于画面对。每轮渲染后必须看静帧再交付。

**画面对了还要动得像片子。** 模型默认的样子是「会动的 PPT」：匀速直切、元素一起蹦出来、一张卡片停三秒。所以动作要错峰进场、缓动收尾，长句里焦点不能冻住，画面比该句起点早一帧。`render.js --motion` 用机器卡住「冻住」这一项。

**先当导演，再当评委。** 动手前把每句要看见什么写进 `script.json`（`must`），抽帧后逐条对照判对错，不凭印象说「挺好」。

---

## 0. 合同（动手前，缺项就问人）

| 项 | 要定什么 |
| --- | --- |
| 主题与受众 | 讲什么、给谁看 |
| 时长 | 目标秒数。`+20%` 语速下说话约 4.8 字/秒（含标点）；总时长还要加上 `lead`、句间 `gap`、`tail` |
| 口吻 | 仿谁的措辞；**只仿措辞，不克隆真人声音**（除非本人授权） |
| 配音 | 默认 edge-tts；有授权的克隆音 / 商用 TTS 由人提供 key |
| 素材 | 字、数字、图表、示意图走代码；真人、表情、光影走素材或视频生成模型，由人提供并确认授权。每个镜头的出处写进 `source` |
| 导演卡 | 整片样子（`look`：底色、字体、主色）和每句必须看见的东西（`must`），写死数字和位置 |
| 输出目录 | 遵守当前仓库约定的工作区（仓库外），例如 `~/Downloads/safe_claw_worksapce/workspace/<slug>/` |

仿真人口吻或用合成音时，画面必须带免责声明（模板的 `DISCLAIMER`）。

---

## 流程

```
Task Progress:
- [ ] 1. 建项目目录，写 script.json（含导演卡 look / must / source）
- [ ] 2. tts.py 配音 → timeline.json，时长对上目标
- [ ] 3. 从模板写 scene.html（cue / enter / drift / sourceTag）
- [ ] 4. 抽静帧 → 按 checklist.md 逐条判 → --motion 查冻帧 → 修（≤3 轮）
- [ ] 5. 整片渲染 + mux，校验时长与音量
- [ ] 6. 交人（含需人耳确认的秒数）
```

下面 `$SKILL` = 本目录，`$P` = 项目目录。

### 1. 建项目

```bash
mkdir -p "$P" && cp "$SKILL/templates/scene.template.html" "$P/scene.html"
python3 -m pip install -q --target "$P/pylib" edge-tts
```

`script.json` 字段：`voice`、`rate`、`gap`、`lead`、`tail`、`target_seconds`、`output`、`look`、`source`（默认出处，可省）、`lines[{key,text,must,source?}]`。完整样例：[examples/corner_defense/script.json](examples/corner_defense/script.json)。

写导演卡：

- `look`：整片 2–4 条，例如「深色星空背景」「金色衬线标题」。不写就会收敛到模型的默认样子。
- `must`：每句 1–3 条，写成能在一张静帧上判对错的句子，例如「数字停在 33%」「其余球员变暗」「标签不压人」。
- `source`：这句画面的出处，例如「示意画面 · 代码渲染」「AI 生成（Renoise）」「来源：某某论文 图 3」。

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

照 [templates/scene.template.html](templates/scene.template.html) 的约定。模板中间是占位文字，球场、球员、传球弧线在样例 [examples/corner_defense/scene.html](examples/corner_defense/scene.html)，做战术板时从样例改，不要用模板覆盖它。

- `window.setup(timeline)`、`window.render(t)`、`<canvas id="c" width="1920" height="1080">`。
- **`render(t)` 只依赖 t**：禁止 `setTimeout`、`requestAnimationFrame`、`Date.now()`、未设种子的 `Math.random()`。
- 每个动画用模板的时间函数驱动，**不要写死秒数或帧号**。改旁白后画面会自动跟上：
  - `cue(key)`：这句的切点，比配音早一帧。画面先到、声音紧跟，人才觉得切在拍上。
  - `enter(t, key, i)`：这句的第 i 个元素，从切点起每个晚 0.12 秒，缓出。同一刻不要让所有东西一起进场。
  - `drift(t, key)`：整句从 0 走到 1，用来做慢推、下划线生长、发光。长句里焦点不要冻住。
  - `focus(t, key)`：这句在说时为 1，用来高亮主体、压暗其余。
- 节奏按「钩子 → 这句要点 → 收住」排：先进主体，再进标注，最后进辅助信息。
- 分层画：背景 → 主体 → 当前焦点高亮（其余变暗）→ 标签卡 → 字幕 → 出处角标（`sourceTag`）→ 免责声明。
- 字体写进 `window.SCENE_FONTS`，渲染前会预加载。

完整示例（俯视球场、球员站位、弧线传中、整体外压）：[examples/corner_defense/scene.html](examples/corner_defense/scene.html)。

### 4. 静帧自检（门闩）

先从 `timeline.json` 算出每句中点，再按需要补关键动作的时刻（传球落点、外压结束）。不要抄别的片子的秒数，配音时长每次会有零点几秒的差别。

```bash
MIDS=$(python3 -c "import json;t=json.load(open('$P/timeline.json'));print(','.join(f'{(l[\"start\"]+l[\"end\"])/2:.1f}' for l in t['lines']))")
PLAYWRIGHT_MODULE=<node_modules/playwright> node "$SKILL/scripts/render.js" --project "$P" --stills "$MIDS"
```

同时写出 `$P/stills/checklist.md`：每张静帧对应哪句旁白、出处，以及这句的 `must` 清单。用 Read 逐张看 `$P/stills/*.jpg`，**先按 checklist 逐条打勾**（这是当评委：导演卡写「停在 33%」，画面停在 38% 就判错），再对照下表：

| 查 | 典型毛病 |
| --- | --- |
| 导演卡 | `must` 有一条没看见；`look` 走样（字体、底色回到默认） |
| 重叠 | 人和人、卡片和标注、标签压线、文字压到边缘 |
| 对位 | 旁白说的东西此刻在画面上被高亮了吗 |
| 文字 | 截断、溢出、字叠字、图例文字压色点 |
| 运动终点 | 动画结束后的位置是否又撞到一起 |
| 事实 | 日期、地名、番号、数字和资料一致 |
| 出处 | 角标和这句的画面来源一致；生成镜头没有冒充代码渲染 |

再查动作（静帧看不出来，要补抽「切点前后」两帧，或者用机器查）：

```bash
PLAYWRIGHT_MODULE=<node_modules/playwright> node "$SKILL/scripts/render.js" --project "$P" --motion
```

整条时间轴每 0.1 秒采一帧。画面连续超过 2 秒没有明显变化就报错，并给出是哪句。修法：用 `enter` 把元素错开进场，或者给焦点加 `drift`。

| 查 | 典型毛病 |
| --- | --- |
| 缓动 | 匀速直线移动、硬切出现，没有 `easeOut` / `ease` |
| 错峰 | 一句的所有元素同一帧出现 |
| 冻帧 | 一张卡片停三秒才弹下一张（`--motion` 会报） |
| 卡点 | 画面在配音之后才到（用 `cue`，不要用 `line(key).start + x`） |

发现问题 → 改 `scene.html` → 只重抽那几帧。**最多 3 轮**；第 3 轮还有问题，带静帧交人，不要硬交付。质感类画面（水墨、3D）可能要更多轮，这时候先带静帧问人，不要自己放宽。

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
- 需要人耳确认的地方：模型听不见声音，配乐落点、重音和切点对不对要人听；写明秒数（例如「请听 10.7 秒那一下」）
- 哪些不是真的：合成音不是本人、画面是示意不是实拍、哪些镜头是生成的
- 改法：改了 `script.json` 从第 2 步重跑，并且第 4 步静帧必须再看一遍（时间点变了）；只改了 `scene.html` 从第 4 步重跑

---

## Fail Fast

- `script.json` 缺字段、`key` 重复、某句没有 `text`、没有 `output`、没有 `look`、某句没有 `must` → `tts.py` 报错
- 某句音频短于 0.3 秒 → 报错，换 voice，禁止静默跳过
- 场景缺 `setup` / `render` / `canvas`，或渲染中抛异常 → `render.js` 报错并带页面错误
- 画面连续冻住超过 2 秒 → `render.js --motion` 报错，列出时间段和对应的句子
- 找不到 playwright → 报错，提示设 `PLAYWRIGHT_MODULE`
- 输出没有音轨 → `mux.py` 报错

## 依赖

- Node 18+、Google Chrome（`channel: 'chrome'`，不用 Playwright 自带浏览器）、Playwright npm 包
- Python 3.9+、ffmpeg / ffprobe
- edge-tts（装在 `$P/pylib`，不进项目环境）、联网

## 更多

- 踩坑、资源实测、合规边界、规模化：[reference.md](reference.md)
