# flow-vedio · reference

## 踩过的坑

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `say -v Eddy` 等中文男声输出 0.016 秒音频 | macOS 语音包未下载，只有 Tingting（女声）能出声 | 用 edge-tts；`tts.py` 会对空音频报错 |
| `browserType.launch: Executable doesn't exist ... chromium_headless_shell-xxxx` | Playwright 包版本和缓存里的浏览器版本对不上 | `chromium.launch({ channel: 'chrome' })` 用系统 Chrome |
| 中文标题回退成默认字体 | 截第一帧时字体还没加载 | `window.SCENE_FONTS` 预加载 |
| 首版旁白 26 秒，目标 20 秒 | 每句太长 | 先删字；语速只到 `+20%` |
| 盯人阶段球员挤成一团 | 跑位终点和区域站位太近 | 终点拉开 ≥ 2 个球员半径 |
| 外压后两人叠在一起 | 只改了 y，没分配 x | 外压时每人给目标 x |
| 箭头和人错位 | 箭头位置写死，人在动 | 箭头跟着当前位置画 |
| 图例文字压到下一个色点 | 间距按色点算，没按文字宽度 | 间距 ≥ 文字宽度 + 色点 |
| edge-tts 报 `WSServerHandshakeError: 403` | `pylib` 里的 edge-tts 太旧，服务端换了签名 | `pip install --target $P/pylib --upgrade edge-tts`（7.3.1 可用） |
| 冻帧检测把「下划线慢慢变长」也判成静止 | 按整帧平均差算，细线的变化被摊薄 | 改成数「明显变了的像素」：单像素 RGB 差和 > 30，超过 40 个就算在动 |
| 一句 4 秒，画面 3 秒不动 | 元素只在句首进一次场，之后什么都不变 | 用 `drift` 做慢推 / 生长；`--motion` 会报 |

## edge-tts 中文声音

| voice | 性别 | 适合 |
| --- | --- | --- |
| `zh-CN-YunjianNeural` | 男 | 体育、激情、解说 |
| `zh-CN-YunyangNeural` | 男 | 新闻、稳重 |
| `zh-CN-YunxiNeural` | 男 | 年轻、轻快 |
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖、叙述 |

列出全部：`PYTHONPATH=$P/pylib python3 -m edge_tts --list-voices | rg zh-CN`

## 资源实测（Apple M4 Max，14 核，36 GB）

21.8 秒、1920×1080、30fps 的 2D Canvas 战术板：

| 指标 | 值 |
| --- | --- |
| 渲染 654 帧 | 10.35 秒墙钟（约 63 帧/秒） |
| 峰值内存（Chrome + Node + ffmpeg） | 约 2.0 GB |
| 峰值 CPU | 约 2.2 核 |
| 成片 | 1.86 MB |
| 场景代码 | 456 行（`examples/corner_defense/scene.html`） |

用 skill 脚本重跑同一条片子：648 帧、8.9 秒、成片 21.60 秒、平均音量 -17.5 dB、1.86 MB。上面 10.35 秒 / 2 GB 是第一次手写渲染时测的。

`--motion` 冻帧检测（2026-10-25）：21.6 秒片子采 217 帧、全分辨率比对，约 3.3 秒。模板和 `examples/corner_defense/` 都通过；把模板的 `drift` 去掉后，5 句全部报冻帧。

长片估算（未实测）：10 分钟 2D 约 5 分钟渲完；带 WebGL 地形或视频素材降到 5–10 帧/秒，即 30–60 分钟。中间帧若存 PNG，1080p 每帧 2–4 MB，所以本 skill 走管道不落盘。

## 规模化

- 渲染慢：开多个 page，按帧区间分段渲，再用 ffmpeg concat；或先半分辨率出草稿。
- 编码慢：`-c:v h264_videotoolbox -b:v 12M` 改用 Mac 硬件编码。
- 系列内容：把地图、球场、字幕、卡片抽成共享 JS，下一期复用。
- 地图类：真实地形用高程晕渲和 GeoJSON（MapLibre / MapTiler），相机移动时用「固定大图 + CSS 变换」避免底图抖动。

## 合规边界

- **口吻**：可以仿公众人物的说话风格做演示，画面上必须标「仿 X 口吻 · AI 合成配音，非本人」。
- **声音**：不克隆他人声音，除非有本人授权；克隆自己的可以。
- **素材**：搜来的影视片段多数不能商用，由人确认授权后再放进项目。
- **事实**：知识类每个日期、数字、地名都要能对上资料；自检表里的「事实」一项不能跳。
- **出处**：每个镜头标来源。代码渲染、AI 生成（写工具名）、引用的网页或论文（写标题和日期），生成镜头不能冒充代码渲染。

## 代码和视频模型怎么分

| 交给代码（要准） | 交给视频模型或素材（要真） |
| --- | --- |
| 字、数字、公式、图表、地图、示意图、战术板 | 真人、表情、皮肤、光影、实拍质感 |
| 改一个数重渲，其余不变 | 改一处要整条重抽，每次都不一样 |

同一句提示词让几家视频模型生成「每多一个假设，可信度 × 0.8 → 33%」，公式和数字都会走样；代码渲染不会。混剪时代码镜头和生成镜头各自标出处。

## 来源

这条流程在 2026-10-01 跑通（`examples/corner_defense/`）。同类公开实测：

- 竹二木：[我让 Opus 5.5 做了 5 支视频](https://zhuermu.com/blog/opus-5-5-five-videos/)——写 `renderFrame(t)` → 无头 Chrome 并行截图 → ffmpeg → 抽帧拼图自检
- 余弦：[用 Opus 5.5 做视频：制作流程与提示词资源记录](https://blog.cosine.ren/post/opus-5-5-motion-video-resources/)——先静帧确认再动起来，渲染后让模型自己验收
- 详细分析：`~/Downloads/safe_claw_worksapce/workspace/reports/opus55-video-analysis.md`
- 黄叔 vibe 知识大赏解说（录屏 `~/Downloads/iShot_2026-10-25_14.26.11.mp4`，11 分 23 秒，2026-10-25 拆帧对照）。本 skill 从中借了：
  - 错峰进场和冻帧检查：「以前是会动的 PPT，停三秒弹下一张；这一代同一秒十几样东西各走各的」，以及 HeyGen Code2Video 测评里的线性缓动、元素拥挤、同时蹦出
  - `cue` 早一帧：三个新的 Opus 5.5 会话都会把切点放在鼓点前 1 帧（30fps 约 33 毫秒）
  - 导演卡和评委：先写清「深色星空、金色衬线、数字停在 33%」，再按卡判，38% 就打回
  - 交付写明人耳要听的秒数：模型听不见声音
  - 镜头出处角标、代码和视频模型分工（雕版 vs 活字）
