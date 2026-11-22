"""bayes-lessons v2 regression keep. 跨边界：写盘 → 进程退出 → 文件被改 / 换仓库 → 下一步仍成立（或仍隔离）。"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "bayes-lessons" / "scripts" / "bayes.py"


def run(cwd, home, *args):
    args = list(args)
    if args[0] == "note" and "--when" not in args and "--human" not in args:
        args += ["--when", "26w40"]
    proc = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, capture_output=True, text=True,
                          env=dict(os.environ))
    return proc.returncode, json.loads(proc.stdout)


def repo(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    (path / ".bayes_lessons").mkdir()
    return path


def test_fact_survives_restart_and_weekly_rewrite(tmp_path):
    """看得见的一条带原文片段的事实 → 进程退出、总本最新在上插入新周 → 仍能按柜子调出并定位到新行。"""
    home, a = tmp_path / "brain", repo(tmp_path / "a")
    doc = a / "weekly.md"
    doc.write_text("- 26w40：美联储加息 25bp\n", encoding="utf-8")
    run(a, home, "cabinets", "--name", "利率", "--desc", "政策利率动作")
    code, body = run(a, home, "note", "--tag", "利率/美联储", "--claim", "26w38 美联储加息 25bp", "--file", "weekly.md", "--quote", "美联储加息 25bp")
    assert code == 0 and body["line"] == 1
    doc.write_text("- 26w41：新的一周\n- 26w42：又一周\n" + doc.read_text(encoding="utf-8"), encoding="utf-8")
    code, body = run(a, home, "recall", "--tag", "利率")
    fact = body["facts"][0]
    assert fact["source"]["line"] == 1 and fact["source"]["line_now"] == 3 and fact["source"]["moved"] is True


def test_each_repo_keeps_its_own_nicole_and_its_own_cognition(tmp_path):
    """在 a 仓库记下的 Nicole 原话和 link → 进程退出、换到 b 仓库 → b 看不到；b 可以对同一件事有不同的 link。"""
    home = tmp_path / "unused"
    a, b = repo(tmp_path / "a"), repo(tmp_path / "b")
    for r in (a, b):
        run(r, home, "cabinets", "--name", "Nicole", "--desc", "她做过说过的事")
        (r / "x.md").write_text("SOFR 从 3.65% 跳到 3.9%\n", encoding="utf-8")
        run(r, home, "cabinets", "--name", "利率", "--desc", "隔夜")
    run(a, home, "note", "--tag", "Nicole/决定", "--claim", "在 a 里她要一人一仓一库", "--human", "--quote", "每个repo 有自己的 库")
    fa = run(a, home, "note", "--tag", "利率", "--claim", "SOFR 3.65%→3.9%", "--file", "x.md", "--quote", "3.65% 跳到 3.9%")[1]["id"]
    fb = run(b, home, "note", "--tag", "利率", "--claim", "SOFR 3.65%→3.9%", "--file", "x.md", "--quote", "3.65% 跳到 3.9%")[1]["id"]
    run(a, home, "link", "--tag", "利率", "--text", "隔夜在紧", "--based-on", fa)
    run(b, home, "link", "--tag", "利率", "--text", "隔夜只是季末噪音", "--based-on", fb)
    assert run(b, home, "recall", "--tag", "Nicole")[1]["facts"] == []
    assert [l["text"] for l in run(a, home, "recall", "--tag", "利率")[1]["links_not_prior"]] == ["隔夜在紧"]
    assert [l["text"] for l in run(b, home, "recall", "--tag", "利率")[1]["links_not_prior"]] == ["隔夜只是季末噪音"]
    assert run(b, home, "link", "--tag", "利率", "--text", "x", "--based-on", fa)[1]["reason"] == "bad-based-on"


def test_superseded_link_stays_hidden_after_restart(tmp_path):
    home, a = tmp_path / "brain", repo(tmp_path / "a")
    (a / "x.md").write_text("SOFR 从 3.65% 跳到 3.9%\n", encoding="utf-8")
    run(a, home, "cabinets", "--name", "利率", "--desc", "隔夜")
    fid = run(a, home, "note", "--tag", "利率/隔夜", "--claim", "SOFR 3.65%→3.9%", "--file", "x.md", "--quote", "3.65% 跳到 3.9%")[1]["id"]
    l1 = run(a, home, "link", "--tag", "利率", "--text", "隔夜在紧", "--based-on", fid)[1]["id"]
    l2 = run(a, home, "link", "--tag", "利率", "--text", "隔夜先紧，长端后紧", "--based-on", fid, "--supersedes", l1)[1]["id"]
    body = run(a, home, "recall", "--tag", "利率")[1]
    assert [l["id"] for l in body["links_not_prior"]] == [l2]
