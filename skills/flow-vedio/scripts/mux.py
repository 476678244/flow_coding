"""Mix narration lines at their timeline offsets and mux with video_silent.mp4.

Usage:
    python3 mux.py --project <project_dir>

Reads <project>/timeline.json, <project>/script.json ("output" file name), <project>/video_silent.mp4.
Writes <project>/narration.wav and <project>/<output>.mp4, then prints duration and loudness.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def fail(msg: str) -> None:
    sys.exit(f"[flow-vedio/mux] {msg}")


def main(project: Path) -> None:
    tl_path, script_path, video = project / "timeline.json", project / "script.json", project / "video_silent.mp4"
    for p in (tl_path, script_path, video):
        if not p.is_file():
            fail(f"required file missing\n  Path: {p}\n  Expected order: tts.py -> render.js -> mux.py")
    tl = json.loads(tl_path.read_text(encoding="utf-8"))
    script = json.loads(script_path.read_text(encoding="utf-8"))
    if "output" not in script:
        fail(f"script.json missing 'output' (final mp4 name)\n  Path: {script_path}")

    inputs, filters = [], []
    for i, line in enumerate(tl["lines"]):
        audio = project / line["file"]
        if not audio.is_file():
            fail(f"narration file missing\n  Line: {line['key']}\n  Path: {audio}")
        inputs += ["-i", str(audio)]
        ms = int(line["start"] * 1000)
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    n = len(tl["lines"])
    filters.append(
        "".join(f"[a{i}]" for i in range(n))
        + f"amix=inputs={n}:normalize=0,apad,atrim=0:{tl['total']},loudnorm=I=-16:TP=-1.5[out]"
    )
    narration = project / "narration.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
         "-map", "[out]", "-ar", "48000", str(narration)],
        check=True,
    )

    out = project / script["output"]
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(narration),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
        check=True,
    )

    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]
    ).strip())
    vd = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(out), "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    mean = re.search(r"mean_volume: (-?[\d.]+) dB", vd)
    if not mean:
        fail(f"no audio stream detected in output\n  Path: {out}")
    mean_db = float(mean.group(1))
    if abs(dur - float(tl["total"])) > 0.1:
        fail(
            f"duration differs from timeline\n  Output: {dur:.3f}s\n  timeline.total: {tl['total']}s\n  Tolerance: 0.1s\n  Path: {out}"
        )
    if not -20 <= mean_db <= -14:
        fail(f"mean volume outside -20 to -14 dB\n  Actual: {mean_db} dB\n  Path: {out}")
    print(f"[flow-vedio/mux] {out}  duration {dur:.2f}s  mean_volume {mean_db} dB  size {out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, type=Path)
    project = ap.parse_args().project.expanduser().resolve()
    if not project.is_dir():
        fail(f"project dir not found\n  Path: {project}")
    main(project)
