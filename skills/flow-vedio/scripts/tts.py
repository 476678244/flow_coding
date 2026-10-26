"""Synthesize narration lines with edge-tts and write timeline.json.

Usage:
    PYTHONPATH=<project>/pylib python3 tts.py --project <project_dir>

Reads <project>/script.json:
    {
      "voice": "zh-CN-YunjianNeural",
      "rate": "+20%",
      "gap": 0.2,
      "lead": 0.4,
      "tail": 0.6,
      "target_seconds": 20,
      "look": ["深色底", "金色衬线标题"],
      "source": "代码渲染",
      "lines": [{"key": "intro", "text": "...", "must": ["画面上必须看见的东西"], "source": "代码渲染"}]
    }

`look` is the whole-film director card; each line's `must` is what its still is judged against.
`source` on a line overrides the top-level default and is shown as the on-screen provenance tag.

Writes <project>/audio/line_<i>.mp3 and <project>/timeline.json.
"""
import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

MIN_LINE_SECONDS = 0.3
REQUIRED_KEYS = ("voice", "rate", "gap", "lead", "tail", "output", "look", "lines")
DEFAULT_SOURCE = "代码渲染"

try:
    import edge_tts
except ImportError as e:
    raise SystemExit(
        "[flow-vedio/tts] edge-tts not importable\n"
        "  Install outside the repo: python3 -m pip install --target <project>/pylib edge-tts\n"
        "  Then run with: PYTHONPATH=<project>/pylib python3 tts.py --project <project>\n"
        f"  Error: {e}"
    )


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return float(out.strip())


def is_text_list(v) -> bool:
    return isinstance(v, list) and bool(v) and all(isinstance(x, str) and x.strip() for x in v)


def load_script(project: Path) -> dict:
    path = project / "script.json"
    if not path.is_file():
        raise SystemExit(f"[flow-vedio/tts] script.json not found\n  Path: {path}")
    script = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED_KEYS if k not in script]
    if missing:
        raise SystemExit(
            f"[flow-vedio/tts] script.json missing keys\n  Path: {path}\n  Missing: {missing}\n  Expected: {list(REQUIRED_KEYS)}"
        )
    keys = [l.get("key") for l in script["lines"]]
    if not script["lines"] or None in keys or len(set(keys)) != len(keys):
        raise SystemExit(
            f"[flow-vedio/tts] lines must be non-empty with unique 'key'\n  Path: {path}\n  Keys: {keys}"
        )
    blank = [l.get("key") for l in script["lines"] if not str(l.get("text", "")).strip()]
    if blank:
        raise SystemExit(f"[flow-vedio/tts] lines with empty text\n  Path: {path}\n  Keys: {blank}")
    if not is_text_list(script["look"]):
        raise SystemExit(
            f"[flow-vedio/tts] look must be a non-empty list of strings (whole-film director card)\n"
            f"  Path: {path}\n  Actual: {script['look']!r}\n  Example: [\"深色星空背景\", \"金色衬线标题\"]"
        )
    no_must = [l["key"] for l in script["lines"] if not is_text_list(l.get("must"))]
    if no_must:
        raise SystemExit(
            f"[flow-vedio/tts] lines missing 'must' (what the still for this line is judged against)\n"
            f"  Path: {path}\n  Keys: {no_must}\n  Example: \"must\": [\"数字停在 33%\", \"其余元素变暗\"]"
        )
    if not str(script["output"]).strip().endswith(".mp4"):
        raise SystemExit(
            f"[flow-vedio/tts] output must be a .mp4 file name\n  Path: {path}\n  Actual: {script['output']!r}"
        )
    return script


async def main(project: Path) -> None:
    script = load_script(project)
    audio_dir = project / "audio"
    audio_dir.mkdir(exist_ok=True)

    lines = []
    t = float(script["lead"])
    for i, line in enumerate(script["lines"]):
        mp3 = audio_dir / f"line_{i}.mp3"
        await edge_tts.Communicate(line["text"], script["voice"], rate=script["rate"]).save(str(mp3))
        d = duration(mp3)
        if d < MIN_LINE_SECONDS:
            raise SystemExit(
                f"[flow-vedio/tts] synthesized audio is empty\n"
                f"  Voice: {script['voice']}\n  Line {i} ({line['key']}): {line['text']}\n"
                f"  Duration: {d:.3f}s (min {MIN_LINE_SECONDS}s)\n  File: {mp3}"
            )
        lines.append({
            "key": line["key"],
            "text": line["text"],
            "start": round(t, 3),
            "end": round(t + d, 3),
            "file": f"audio/{mp3.name}",
            "must": line["must"],
            "source": line.get("source") or script.get("source") or DEFAULT_SOURCE,
        })
        print(f"[flow-vedio/tts] {line['key']}: {d:.2f}s  {line['text']}")
        t += d + float(script["gap"])

    total = round(t - float(script["gap"]) + float(script["tail"]), 3)
    timeline = {"total": total, "look": script["look"], "lines": lines}
    (project / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    target = script.get("target_seconds")
    note = f" (target {target}s, diff {total - target:+.1f}s)" if target else ""
    print(f"[flow-vedio/tts] total {total}s{note} -> {project / 'timeline.json'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, type=Path)
    args = ap.parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        sys.exit(f"[flow-vedio/tts] project dir not found\n  Path: {project}")
    asyncio.run(main(project))
