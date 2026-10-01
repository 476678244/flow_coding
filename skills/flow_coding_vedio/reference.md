# flow_coding_vedio · reference

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

## 来源

这条流程在 2026-10-01 跑通（`examples/corner_defense/`）。同类公开实测：

- 竹二木：[我让 Opus 5.5 做了 5 支视频](https://zhuermu.com/blog/opus-5-5-five-videos/)——写 `renderFrame(t)` → 无头 Chrome 并行截图 → ffmpeg → 抽帧拼图自检
- 余弦：[用 Opus 5.5 做视频：制作流程与提示词资源记录](https://blog.cosine.ren/post/opus-5-5-motion-video-resources/)——先静帧确认再动起来，渲染后让模型自己验收
- 详细分析：`~/Downloads/safe_claw_worksapce/workspace/reports/opus55-video-analysis.md`
