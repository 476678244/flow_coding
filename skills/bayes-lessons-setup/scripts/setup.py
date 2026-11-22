#!/usr/bin/env python3
"""打开一个 Nicole 自己的仓库：仓库根 .bayes_lessons/（meta、cabinets、页面），加上页面目录上的启用说明。

不写 brain.jsonl，不定柜子。不是自己的仓库时拒绝，不创建目录。
旧版 facts.jsonl 在、brain.jsonl 不在时，报告 needs_migration。
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

OWNER = "476678244"
LOCAL_ROOT = Path("/Users/nicole/workspace/github/a476678244")
BAYES_PY = Path(__file__).resolve().parent.parent.parent / "bayes-lessons" / "scripts" / "bayes.py"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "template.md"
LIBRARY_AGENTS = Path(__file__).resolve().parent.parent / "templates" / "library-agents.md"

MARK = "bayes-lessons v2"

PAGE_NOTE = (
    f"<!-- {MARK} --> 本仓已启用 `/bayes-lessons`：根上 `.bayes_lessons/` 是 Nicole 在这个仓库里的一份库"
    "（事件、关于她的事、认知都在这里，不和别的仓库混）。"
    "开工先 `recall` 看柜子、倒出相关的柜，收工把确认的事实 `note` 回去（原文片段作出处），"
    "想过的一句写成 `link`，不当先验。\n"
)

SOUL_NOTE = (
    f"\n<!-- {MARK} --> 本仓已启用 `/bayes-lessons`。认识这库，靠柜子里还活着的事实，每次整柜倒出来重算；"
    "上次的结论不当输入。\n"
)

HELP = """\
用法：
  python3 setup.py [--root 目录] [--dry-run]
                   [--admission co-built|open] [--cobuilt 路径通配 ...] [--alias 别名 ...]
  python3 setup.py --help

--admission co-built：本库只收人和 agent 一起经历过的（--human 原话、--cobuilt 列出的共建记录、
或 note 时带 --discussed "她讨论时的原话"），并要求每块写 --grows agent|human|both。
--cobuilt 可重复，fnmatch 通配，如 "wiki/laolao/weekly_readings/*"；写 commit / web 表示允许这两类出处。
--alias 可重复：人的别名，如 zonghan、laolao。

在自己的 git 仓库根打开 .bayes_lessons/（meta.json、cabinets.json，尚无页面时再导出 index.html），
并在根上的页面目录写下启用说明。已有 index.md 或 Index.md 就改那一份，不另建一份。
仓库根取 git toplevel。--root 可以是仓库里的子目录。

接受：origin 指向 github 用户 476678244，或没有 origin 且仓库根在
/Users/nicole/workspace/github/a476678244/ 下面。
其它路径拒绝，不创建 .bayes_lessons。

--dry-run 只打印将要写的相对路径。
脚本不写 brain.jsonl，不定柜子。柜子用 bayes.py cabinets --name 名 --desc 比什么。
"""


def main(argv=None, cwd=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    opts = parse_args(argv)
    if opts is None:
        return reject("unknown-arg")
    if opts["help"]:
        print(HELP, end="")
        return 0
    if not BAYES_PY.is_file():
        return reject("missing-script")
    start = Path(opts["root"] or (cwd or Path.cwd())).expanduser()
    if not start.exists() or not start.is_dir():
        return reject("not-a-repo", start=str(start))
    start = start.resolve()
    root = git_toplevel(start)
    if root is None:
        return reject("not-a-repo", start=str(start))
    origin = origin_url(root)
    if not owned(root, origin):
        return reject("not-owned", root=str(root), origin=origin or "")
    plan = build_plan(root)
    if opts["dry_run"]:
        print(json.dumps({"status": "dry-run", "root": str(root), "origin": origin or "", **plan}, ensure_ascii=False))
        return 0
    wrote, err = apply_plan(root, plan)
    if err:
        print(err)
        return 2
    if write_admission(root / repo_dir_name(), opts):
        wrote.append(f"{repo_dir_name()}/meta.json")
    registry = register_instance(root, root / repo_dir_name())
    print(json.dumps({"status": "ready", "root": str(root), "origin": origin or "", "wrote": wrote, "needs_migration": plan["needs_migration"], "registered": registry}, ensure_ascii=False))
    return 0


def parse_args(argv):
    opts = {"root": None, "dry_run": False, "help": False, "admission": None, "cobuilt": [], "alias": []}
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in ("-h", "--help"):
            opts["help"] = True
            i += 1
            continue
        if token == "--dry-run":
            opts["dry_run"] = True
            i += 1
            continue
        if token in ("--root", "--admission", "--cobuilt", "--alias"):
            if i + 1 >= len(argv):
                return None
            key, value = token[2:], argv[i + 1]
            if key in ("cobuilt", "alias"):
                opts[key].append(value)
            else:
                opts[key] = value
            i += 2
            continue
        return None
    if opts["admission"] not in (None, "co-built", "open"):
        return None
    return opts


SETUP_SKILL = Path(__file__).resolve().parent.parent / "SKILL.md"
BAYES_SKILL = BAYES_PY.parent.parent / "SKILL.md"


def fill_template(text, person, repo):
    for key, value in {"@@PERSON@@": person, "@@REPO@@": repo, "@@SETUP_SKILL@@": str(SETUP_SKILL),
                       "@@SKELETON@@": str(TEMPLATE), "@@BAYES_SKILL@@": str(BAYES_SKILL), "@@BAYES_PY@@": str(BAYES_PY)}.items():
        text = text.replace(key, value)
    return text


def instances_path():
    """技能这一侧的回链：它生成过哪些库。测试用 BAYES_INSTANCES 指到别处。"""
    override = os.environ.get("BAYES_INSTANCES")
    return Path(override) if override else Path(__file__).resolve().parent.parent / "instances.json"


def register_instance(root, bayes):
    path = instances_path()
    rows = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    meta = json.loads((bayes / "meta.json").read_text(encoding="utf-8")) if (bayes / "meta.json").is_file() else {}
    row = {"repo": root.name, "root": str(root), "library": str(bayes), "template": str(bayes / "template.md"),
           "person": meta.get("person", "Nicole"), "admission": meta.get("admission", "open"),
           "generated": (meta.get("template_from") or {}).get("generated") or (meta.get("template_from") or {}).get("backfilled", ""),
           "locked": bool(meta.get("template_sha256"))}
    rows = [r for r in rows if r.get("library") != row["library"]] + [row]
    rows.sort(key=lambda r: r["library"])
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [
        "# bayes-lessons-setup · 生成过的库（回链）",
        "",
        "> 由 `scripts/setup.py` 自动维护，不手改。每次 setup 跑完都会更新这一张表。",
        "> 每一份 `template.md` 开头的 🧬 出处链到本技能；本表从技能这一侧链回每一份库。",
        "",
        "| 仓库 | 人 | 门槛 | 元数据框架 | 上锁 | 生成 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(f"| {r['repo']} | {r['person']} | {r['admission']} | [template.md](file://{r['template']}) | {'是' if r['locked'] else '否'} | {r['generated']} |")
    path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path.with_suffix(".md"))


def template_from():
    import hashlib
    return {"skill": str(SETUP_SKILL), "skeleton": str(TEMPLATE),
            "skeleton_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(), "generated": __import__("datetime").date.today().isoformat()}


def write_admission(bayes, opts):
    """入库门槛写进 meta.json：co-built = 只收人和 agent 一起经历过的。"""
    if not (opts["admission"] or opts["cobuilt"] or opts["alias"]):
        return False
    meta_path = bayes / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    if opts["admission"]:
        meta["admission"] = opts["admission"]
    for key in ("cobuilt", "alias"):
        field = "aliases" if key == "alias" else key
        merged = list(meta.get(field, []))
        merged += [v for v in opts[key] if v not in merged]
        if merged:
            meta[field] = merged
    meta_path.write_text(json.dumps(meta, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def reject(reason, **extra):
    body = {"error": "rejected", "reason": reason, **extra}
    print(json.dumps(body, ensure_ascii=False))
    return 2


def repo_dir_name():
    name = os.environ.get("BAYES_REPO_DIR", ".bayes_lessons")
    return name if re.fullmatch(r"\.bayes_lessons[\w-]*", name) else ".bayes_lessons"


def git_toplevel(start):
    proc = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    text = proc.stdout.strip()
    if not text:
        return None
    return Path(text).resolve()


def origin_url(root):
    proc = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    text = proc.stdout.strip()
    return text or None


def owned(root, origin):
    if origin and f"/{OWNER}/" not in origin and f":{OWNER}/" not in origin:
        return False
    if origin:
        return f"/{OWNER}/" in origin or f":{OWNER}/" in origin
    try:
        root.resolve().relative_to(LOCAL_ROOT.resolve())
    except ValueError:
        return False
    return True


def enabled(text):
    return MARK in text


def files_named(root, lower):
    return sorted(
        (path for path in root.iterdir() if path.is_file() and path.name.lower() == lower),
        key=lambda path: path.name,
    )


def build_plan(root):
    pages = files_named(root, "index.md")
    souls = files_named(root, "soul.md")
    agents = files_named(root, "agents.md")
    bayes = root / repo_dir_name()
    meta = bayes / "meta.json"
    html = bayes / "index.html"
    would = []
    if not meta.is_file():
        would.append(f"{bayes.name}/meta.json")
    if not html.is_file():
        would.append(f"{bayes.name}/index.html")
    if not (bayes / "cabinets.json").is_file():
        would.append(f"{bayes.name}/cabinets.json")
    if not (bayes / "template.md").is_file():
        would.append(f"{bayes.name}/template.md")
    if not (bayes / "Agents.md").is_file():
        would.append(f"{bayes.name}/Agents.md")
    page_actions = []
    if not pages:
        page_actions.append({"path": "Index.md", "action": "create"})
        would.append("Index.md")
    else:
        for page in pages:
            action = "keep" if enabled(page.read_text(encoding="utf-8")) else "patch"
            page_actions.append({"path": page.name, "action": action})
            if action == "patch":
                would.append(page.name)
    extras = []
    for path in souls + agents:
        action = "keep" if enabled(path.read_text(encoding="utf-8")) else "patch"
        extras.append({"path": path.name, "action": action})
        if action == "patch":
            would.append(path.name)
    return {
        "page": page_actions,
        "charter": extras,
        "would_write": would,
        "needs_migration": (bayes / "facts.jsonl").is_file() and not (bayes / "brain.jsonl").is_file(),
    }


def insert_page_note(text):
    if text.startswith("---\n"):
        close = text.find("\n---", 4)
        if close != -1:
            head = text[: close + 4]
            rest = text[close + 4 :]
            rest = rest.lstrip("\n")
            return head + "\n\n" + PAGE_NOTE + "\n" + rest
    if text.strip() == "":
        return "# Index\n\n" + PAGE_NOTE
    return PAGE_NOTE + "\n" + text


def agents_note():
    return (
        f"\n## Bayes lessons（已启用）\n\n<!-- {MARK} -->\n"
        "本仓已启用 `/bayes-lessons`。做法以技能为准，每一轮：\n\n"
        "1. 开工：`recall` 列出柜子；倒出和任务相关的柜，以及本仓的 `Nicole` 柜。\n"
        "2. 只用倒出来的事实在对话里重算；`links_not_prior` 只回看，不当输入。\n"
        "3. 收工：确认的事实 `note`（原文片段作出处）；人的决定和纠正用 `--human`；想过的一句写 `link`。\n\n"
        "```bash\n"
        f"python3 {BAYES_PY} recall\n"
        f"python3 {BAYES_PY} recall --tag 柜子\n"
        f"python3 {BAYES_PY} note --tag 柜子/小类 --claim \"发生了什么\" --file 相对路径 --quote \"原文片段\"\n"
        f"python3 {BAYES_PY} note --tag Nicole/决定 --claim \"她做了什么\" --human --quote \"她的原话\"\n"
        f"python3 {BAYES_PY} link --tag 柜子 --text \"想过的一句\" --based-on f-xxxx,f-yyyy\n"
        "```\n"
    )


def apply_plan(root, plan):
    wrote = []
    bayes = root / repo_dir_name()
    html = bayes / "index.html"
    meta = bayes / "meta.json"
    if not html.is_file():
        missing_meta = not meta.is_file()
        bayes.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(
            [sys.executable, str(BAYES_PY), "export"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return None, proc.stdout or json.dumps({"error": "rejected", "reason": "export-failed"}, ensure_ascii=False)
        wrote.append(f"{bayes.name}/index.html")
        if missing_meta:
            wrote.append(f"{bayes.name}/meta.json")
    elif not meta.is_file() or not (bayes / "cabinets.json").is_file():
        proc = subprocess.run([sys.executable, str(BAYES_PY), "export"], cwd=root, capture_output=True, text=True)
        if proc.returncode != 0:
            return None, proc.stdout
        wrote.append(f"{bayes.name}/meta.json")
    frame = bayes / "template.md"
    if not frame.is_file():
        person = os.environ.get("BAYES_PERSON", "Nicole")
        text = fill_template(TEMPLATE.read_text(encoding="utf-8"), person, root.name)
        bayes.mkdir(parents=True, exist_ok=True)
        frame.write_text(text, encoding="utf-8")
        wrote.append(f"{bayes.name}/template.md")
        meta_path = bayes / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        meta_path.write_text(json.dumps({**meta, "template_from": template_from()}, ensure_ascii=False) + "\n", encoding="utf-8")
    guide = bayes / "Agents.md"
    meta_path = bayes / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    person = meta.get("person") or os.environ.get("BAYES_PERSON", "Nicole")
    if not guide.is_file():
        guide.write_text(fill_template(LIBRARY_AGENTS.read_text(encoding="utf-8"), person, root.name), encoding="utf-8")
        wrote.append(f"{bayes.name}/Agents.md")
    skills = {"daily": str(BAYES_SKILL), "setup": str(SETUP_SKILL), "script": str(BAYES_PY)}
    if meta.get("skills") != skills:
        meta_path.write_text(json.dumps({**meta, "skills": skills}, ensure_ascii=False) + "\n", encoding="utf-8")
    cabs = bayes / "cabinets.json"
    if not cabs.is_file() or json.loads(cabs.read_text(encoding="utf-8") or "[]") == []:
        proc = subprocess.run(
            [sys.executable, str(BAYES_PY), "cabinets", "--name", "Nicole",
             "--desc", f"Nicole 在 {root.name} 里做过、说过的事：决定、纠正、否掉、坚持，以及原话"],
            cwd=root, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            return None, proc.stdout
        wrote.append(f"{bayes.name}/cabinets.json")
    for item in plan["page"]:
        path = root / item["path"]
        if item["action"] == "create":
            path.write_text("# Index\n\n" + PAGE_NOTE, encoding="utf-8")
            wrote.append(item["path"])
        elif item["action"] == "patch":
            path.write_text(insert_page_note(path.read_text(encoding="utf-8")), encoding="utf-8")
            wrote.append(item["path"])
    for item in plan["charter"]:
        if item["action"] != "patch":
            continue
        path = root / item["path"]
        extra = agents_note() if path.name.lower() == "agents.md" else SOUL_NOTE
        path.write_text(path.read_text(encoding="utf-8").rstrip() + "\n" + extra, encoding="utf-8")
        wrote.append(item["path"])
    return wrote, None


if __name__ == "__main__":
    sys.exit(main())
