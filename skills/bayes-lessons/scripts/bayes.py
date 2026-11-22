#!/usr/bin/env python3
"""bayes-lessons v2：agent 的贝叶斯大脑。

第一性原理：Nicole（zonghan / laolao）与 AI Agent 共同成长，成长的路上谁都不落下。
粒度是「一个人 + 一个仓库」：每个仓库根 .bayes_lessons/ 是 Nicole 在这个仓库里和 agent 共建的一份库，
事件、关于她的事、认知都只在这一份里；同一个人在不同仓库可以有不同的认知，库与库之间不自动混。
admission=co-built 的库只收两人一起经历过的：她的原话、共建记录里的行、或带着她讨论原话的材料。
每块石头写明是谁在长（--grows agent|human|both），recall 会提醒哪一边落下了。
石头（note）按柜子（标签）收，出处靠原文片段定位；认知（link）单独一层，不当先验。
"""

import fnmatch
import html
import json
import os
import random
import re
import secrets
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ENTITIES_PATH = SKILL_DIR / "entities.json"
EXPORT_TEMPLATE = SKILL_DIR / "templates" / "export.html"
VERBS = ("recall", "note", "link", "review", "cabinets", "doctor", "export", "entities")
INFERENCE = (
    "因此", "所以", "这说明", "说明了", "意味着", "我认为", "我觉得", "应该", "概率",
    "相当于", "共识", "预计", "或将", "有望", "可能会", "大概率", "估计",
)
KINDS = ("fact", "difference", "bayesian")
LINK_BANNED = ("概率", "百分之", "主要矛盾")
META_DIRS = (".devin/", ".cursor/", ".claude/", ".agents/",
             "assets/sources/business_analysis_bayes/", "raw/business_analysis_bayes/")
META_FILES = ("skill.md", "agents.md", "soul.md", "index.md", "readme.md", "readme_zh.md", "entities.json")


def meta_source(rel):
    """贝叶斯思维的元数据不是数据：方法（六讲讲稿）、规则（SKILL / 三件套 / README / entities）、
    模板（templates/、_template/）、大脑自己的文件（.bayes_lessons*）。
    代码、测试、bug 记录（features/*/track/bug-*）、日志、运行输出是数据的出处。"""
    parts = Path(rel).parts
    return (rel.startswith(META_DIRS) or parts[0].startswith(".bayes_lessons")
            or any(p in ("templates", "_template") for p in parts) or Path(rel).name.lower() in META_FILES)


def repo_dir_name():
    name = os.environ.get("BAYES_REPO_DIR", ".bayes_lessons")
    return name if re.fullmatch(r"\.bayes_lessons[\w-]*", name) else ".bayes_lessons"


GROWS = ("agent", "human", "both")
GROWS_LABEL = {"agent": "agent 在长", "human": "人在长", "both": "一起长"}
BALANCE_WINDOW = 5


def parse_grows(value, meta):
    """agent / human / both；人的名字和别名（Nicole、zonghan、laolao）都算 human。"""
    value = (value or "").strip()
    names = {meta.get("person", "Nicole"), *meta.get("aliases", [])}
    if value in names:
        return "human"
    return value if value in GROWS else None


def cobuilt_ok(source, patterns):
    kind = source.get("type")
    if kind == "human":
        return True
    if kind == "file":
        return any(fnmatch.fnmatch(source.get("path", ""), p) for p in patterns)
    return kind in patterns


def growth(rows):
    counts = {g: 0 for g in GROWS}
    for r in rows:
        if r.get("grows") in counts:
            counts[r["grows"]] += 1
    return counts


def balance_hint(rows, meta):
    """谁都不落下：最近几块都只是一边在长时提醒。"""
    recent = [r for r in sorted(rows, key=lambda r: r.get("ts", "")) if r.get("grows")][-BALANCE_WINDOW:]
    if len(recent) < BALANCE_WINDOW:
        return None
    sides = {r["grows"] for r in recent}
    person = meta.get("person", "Nicole")
    if sides == {"agent"}:
        return f"最近 {BALANCE_WINDOW} 块都是 agent 在长：问问 {person} 这次学到、改变了什么"
    if sides == {"human"}:
        return f"最近 {BALANCE_WINDOW} 块都是 {person} 在长：agent 这次被纠正了什么、学到了什么"
    return None


SMALL_SAMPLE = 5
PUNCT = set("？?。！!，,；;：:、")
MARKUP = set("<>\"'\\&")
SCHEMA = 2


# ---------- 入口与参数 ----------

def main(argv=None, cwd=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in VERBS:
        return reject("unknown-verb", verbs=list(VERBS))
    verb, opts = argv[0], parse_opts(argv[1:])
    ctx = Context(Path(cwd or Path.cwd()).resolve())
    return globals()["cmd_" + verb](ctx, opts)


def parse_opts(args):
    opts, i = {}, 0
    while i < len(args):
        token = args[i]
        if not token.startswith("--"):
            i += 1
            continue
        key = token[2:]
        if i + 1 < len(args) and not args[i + 1].startswith("--"):
            value, i = args[i + 1], i + 2
        else:
            value, i = "", i + 1
        if key == "tag":
            opts.setdefault(key, []).append(value)
        elif key == "based-on":
            opts.setdefault(key, []).extend(v.strip() for v in value.split(",") if v.strip())
        else:
            opts[key] = value
    return opts


def out(body, code=0):
    print(json.dumps(body, ensure_ascii=False))
    return code


def reject(reason, **extra):
    return out({"error": "rejected", "reason": reason, **extra}, 2)


def now():
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


# ---------- 存放 ----------

class Store:
    def __init__(self, scope, folder, root=None):
        self.scope, self.folder, self.root = scope, folder, root

    @property
    def log(self):
        return self.folder / "brain.jsonl"

    @property
    def cabinets_path(self):
        return self.folder / "cabinets.json"

    def exists(self):
        return self.folder.is_dir()

    def meta(self):
        path = self.folder / "meta.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        except json.JSONDecodeError:
            data = {}
        return data

    def ensure(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        data = self.meta()
        want = {"schema": SCHEMA, "person": data.get("person") or os.environ.get("BAYES_PERSON", "Nicole"),
                "repo": data.get("repo") or (self.root.name if self.root else "")}
        if data != {**data, **want} or not data:
            (self.folder / "meta.json").write_text(json.dumps({**data, **want}, ensure_ascii=False) + "\n", encoding="utf-8")
        if not self.cabinets_path.exists():
            self.cabinets_path.write_text("[]\n", encoding="utf-8")

    def rows(self):
        if not self.log.exists():
            return []
        rows = []
        for n, line in enumerate(self.log.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise Corrupt(f"{self.log}:{n}") from exc
                row["_store"] = self.scope
                rows.append(row)
        return rows

    def cabinets(self):
        if not self.cabinets_path.exists():
            return []
        try:
            data = json.loads(self.cabinets_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise Corrupt(str(self.cabinets_path)) from exc
        return [dict(c, scope=self.scope) for c in data if isinstance(c, dict) and c.get("name")]

    def append(self, record):
        self.ensure()
        with self.log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


class Corrupt(Exception):
    pass


class Context:
    def __init__(self, cwd):
        self.cwd = cwd
        root = git_toplevel(cwd)
        self.root = root
        self.repo_store = Store("repo", root / repo_dir_name(), root) if root else None

    def stores(self):
        return [self.repo_store] if self.repo_store and self.repo_store.exists() else []

    def store(self, scope="repo"):
        if self.repo_store and self.repo_store.exists():
            return self.repo_store
        return None

    def all_rows(self):
        return [row for store in self.stores() for row in store.rows()]

    def all_cabinets(self):
        return [c for store in self.stores() for c in store.cabinets()]


def git_out(root, *args):
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    except OSError:
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def git_toplevel(start):
    try:
        proc = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    except OSError:
        return None
    text = proc.stdout.strip()
    return Path(text).resolve() if proc.returncode == 0 and text else None


# ---------- 标签与柜子 ----------

def tag_ok(tag):
    if not isinstance(tag, str) or not tag or any(ch.isspace() for ch in tag):
        return False
    if any(ch in PUNCT or ch in MARKUP for ch in tag) or tag.endswith(("吗", "呢")):
        return False
    parts = tag.split("/")
    return len(parts) <= 2 and all(0 < len(p) <= 20 for p in parts)


def cabinet_of(tag):
    return tag.split("/", 1)[0]


def tag_matches(wanted, tags):
    return any(t == wanted or ("/" not in wanted and t.startswith(wanted + "/")) for t in tags)


# ---------- 格物：事件时间 ----------

def parse_when(text):
    """26w40 / 2026w40 → 2026-W40；2026-11-08 → 2026-W45-7。认不出返回 None。"""
    text = (text or "").strip()
    m = re.fullmatch(r"(\d{2}|\d{4})w(\d{1,2})", text)
    if m:
        year = int(m.group(1)) + (2000 if len(m.group(1)) == 2 else 0)
        week = int(m.group(2))
        return f"{year:04d}-W{week:02d}" if 1 <= week <= 53 else None
    try:
        d = date.fromisoformat(text)
    except ValueError:
        return None
    y, w, wd = d.isocalendar()
    return f"{y:04d}-W{w:02d}-{wd}"


def when_key(row):
    if row.get("when"):
        return row["when"]
    try:
        return parse_when(row.get("ts", "")[:10]) or ""
    except ValueError:
        return ""


def order(rows):
    return sorted(rows, key=lambda r: (when_key(r), r.get("ts", "")))


# ---------- 出处：原文片段 ----------

def norm(text):
    text = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return re.sub(r"\s+", "", text)


_FILE_CACHE = {}


def locate(path, quote, hint=None):
    """返回原文片段当前所在的行号（1 起）；有多处时取离 hint 最近的那处；找不到返回 None。"""
    if not path.is_file():
        return None
    key = (path, path.stat().st_mtime_ns)
    if key not in _FILE_CACHE:
        try:
            _FILE_CACHE[key] = [norm(line) for line in path.read_text(encoding="utf-8").splitlines()]
        except (OSError, UnicodeDecodeError):
            return None
    lines, needle = _FILE_CACHE[key], norm(quote)
    if not needle:
        return None
    hits = [i + 1 for i, line in enumerate(lines) if needle in line]
    for width in range(2, 6):
        if hits:
            break
        hits = [i + 1 for i in range(len(lines) - width + 1) if needle in "".join(lines[i:i + width])]
    if not hits:
        return None
    return min(hits, key=lambda n: abs(n - hint)) if hint else hits[0]


def resolve_source_path(source):
    base = source.get("root")
    if not base or not source.get("path"):
        return None
    return Path(base) / source["path"]


def source_status(source):
    """出处现在的样子：file 型重新定位，commit 型确认还在，其它型原样。"""
    if source.get("type") == "commit":
        alive = git_out(source.get("root", "."), "cat-file", "-e", source.get("sha", "") + "^{commit}") is not None
        return {} if alive else {"lost": True}
    if source.get("type") != "file":
        return {}
    path = resolve_source_path(source)
    line = locate(path, source.get("quote", ""), source.get("line")) if path else None
    if line is None:
        return {"line_now": None, "lost": True}
    return {"line_now": line, "moved": line != source.get("line")}


def build_source(ctx, opts):
    quote = opts.get("quote", "").strip()
    if not quote:
        return None, "no-quote"
    if len(quote) > 400:
        return None, "quote-too-long"
    if "human" in opts:
        return {"type": "human", "quote": quote, "date": now()[:10]}, None
    if opts.get("commit"):
        if ctx.root is None:
            return None, "no-repo"
        sha = git_out(ctx.root, "rev-parse", "--verify", "--quiet", opts["commit"] + "^{commit}")
        if not sha:
            return None, "bad-commit"
        if norm(quote) not in norm(git_out(ctx.root, "show", "--format=%B", sha) or ""):
            return None, "quote-not-found"
        return {"type": "commit", "root": str(ctx.root), "sha": sha, "quote": quote}, None
    if opts.get("url"):
        if not re.match(r"https?://", opts["url"]):
            return None, "bad-url"
        return {"type": "web", "url": opts["url"], "quote": quote}, None
    rel = opts.get("file", "")
    if not rel:
        return None, "no-source"
    if ctx.root is None:
        return None, "no-repo"
    if rel.startswith("/") or "\\" in rel or ".." in Path(rel).parts:
        return None, "bad-path"
    if meta_source(rel):
        return None, "meta-source"
    path = (ctx.root / rel).resolve()
    try:
        path.relative_to(ctx.root)
    except ValueError:
        return None, "bad-path"
    line = locate(path, quote)
    if line is None:
        return None, "quote-not-found"
    return {"type": "file", "root": str(ctx.root), "path": rel, "line": line, "quote": quote}, None


def source_label(source):
    kind = source.get("type")
    if kind == "file":
        return f"{Path(source.get('root', '')).name}/{source.get('path')}:{source.get('line')}"
    if kind == "web":
        return source.get("url", "")
    if kind == "commit":
        return f"{Path(source.get('root', '')).name}@{source.get('sha', '')[:10]}"
    if kind == "human":
        return f"人说 {source.get('date', '')}"
    return source.get("ref", "")


# ---------- 读出活着的条目 ----------

def live_state(rows):
    retracted = {r["retracts"] for r in rows if r.get("retracts")}
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    notes = [r for r in rows if r.get("op") == "note"]
    links = [r for r in rows if r.get("op") == "link"]
    return notes, links, retracted, superseded


def present_note(row, retracted):
    item = {k: row[k] for k in ("id", "ts", "claim", "kind", "tags") if k in row}
    item["when"] = when_key(row)
    for key in ("grows", "discussed", "uncertain", "overturns", "migrated_from"):
        if row.get(key):
            item[key] = row[key]
    source = dict(row.get("source") or {})
    source.update(source_status(source))
    source.pop("root", None)
    item["source"] = source
    item["store"] = row["_store"]
    if row["id"] in retracted:
        item["retracted"] = True
    return item


def present_link(row, notes_by_id, retracted):
    item = {k: row[k] for k in ("id", "ts", "text", "tags", "based_on", "grows") if k in row}
    item["store"] = row["_store"]
    stale = []
    for fid in row.get("based_on", []):
        base = notes_by_id.get(fid)
        if base is None or fid in retracted or source_status(base.get("source") or {}).get("lost"):
            stale.append(fid)
    if stale:
        item["stale_because"] = stale
    return item


# ---------- 命令 ----------

def cmd_entities(ctx, opts):
    rows = json.loads(ENTITIES_PATH.read_text(encoding="utf-8"))
    return out({"entities": rows})


def cmd_cabinets(ctx, opts):
    try:
        if "name" not in opts:
            notes, _, retracted, _ = live_state(ctx.all_rows())
            live = [r for r in notes if r["id"] not in retracted]
            cabs = []
            for c in ctx.all_cabinets():
                inside = [r for r in live if r["_store"] == c["scope"] and tag_matches(c["name"], r.get("tags", []))]
                subs = sorted({t for r in inside for t in r.get("tags", []) if "/" in t and cabinet_of(t) == c["name"]})
                cabs.append({**c, "count": len(inside), "subtags": subs})
            store = ctx.store()
            library = {**store.meta(), "dir": str(store.folder)} if store else None
            body = {"library": library, "cabinets": cabs, "repo_enabled": bool(store)}
            if store:
                _, live_links, _, superseded = live_state(ctx.all_rows())
                grown = live + [r for r in live_links if r["id"] not in superseded]
                body["growth"] = growth(grown)
                hint = balance_hint(grown, store.meta())
                if hint:
                    body["hint_balance"] = hint
                frame = store.folder / "template.md"
                body["template"] = str(frame) if frame.is_file() else None
                if not frame.is_file():
                    body["hint_template"] = "缺 template.md（本库的元数据框架）：先跑 /bayes-lessons-setup"
                elif "<填" in frame.read_text(encoding="utf-8"):
                    body["hint_template"] = "template.md 还有 <填>：先把本库的元数据框架填完，再记数据"
            return out(body)
        name, desc = opts["name"], opts.get("desc", "").strip()
        if not tag_ok(name) or "/" in name:
            return reject("bad-cabinet")
        if not desc:
            return reject("no-desc")
        if opts.get("scope") not in (None, "repo"):
            return reject("per-repo-only", hint="一个人 + 一个仓库一份库；没有全局库")
        store = ctx.store()
        if store is None:
            return reject("repo-not-enabled")
        if any(c["name"] == name for c in ctx.all_cabinets()):
            return reject("cabinet-exists")
        store.ensure()
        data = [{k: v for k, v in c.items() if k != "scope"} for c in store.cabinets()]
        data.append({"name": name, "desc": desc, "ts": now()})
        store.cabinets_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        export_store(ctx, store)
        return out({"status": "stored", "cabinet": name, "scope": store.scope})
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def pick_store(ctx, tags):
    cabs = {c["name"]: c["scope"] for c in ctx.all_cabinets()}
    scopes = []
    for tag in tags:
        if cabinet_of(tag) not in cabs:
            return None, ("unknown-cabinet", cabinet_of(tag))
        scopes.append(cabs[cabinet_of(tag)])
    store = ctx.store(scopes[0])
    return (store, None) if store else (None, ("repo-not-enabled", ""))


def check_tags(opts):
    tags = []
    for tag in opts.get("tag", []):
        if not tag_ok(tag):
            return None, tag
        if tag not in tags:
            tags.append(tag)
    return tags, None


def cmd_note(ctx, opts):
    try:
        claim = opts.get("claim", "").strip()
        if not claim:
            return reject("no-claim")
        hit = next((w for w in INFERENCE if w in claim), None)
        if hit:
            return reject("inference", word=hit)
        kind = opts.get("kind") or "fact"
        if kind not in KINDS:
            return reject("not-a-fact", kinds=list(KINDS))
        if kind == "bayesian" and not opts.get("overturns", "").strip():
            return reject("bayesian-needs-overturns")
        if not opts.get("when") and "human" in opts:
            opts["when"] = now()[:10]
        if not opts.get("when"):
            return reject("no-when", hint="事件哪一周、哪一天发生的：26w40、2026w40 或 2026-11-08")
        when = parse_when(opts["when"])
        if when is None:
            return reject("bad-when", hint="26w40、2026w40 或 2026-11-08")
        tags, bad = check_tags(opts)
        if bad is not None:
            return reject("bad-tag", tag=bad)
        if not tags:
            return reject("no-tag")
        store, err = pick_store(ctx, tags)
        if err:
            return reject(err[0], cabinet=err[1])
        source, err = build_source(ctx, opts)
        if err:
            return reject(err)
        meta = store.meta()
        grows = parse_grows(opts.get("grows"), meta) if opts.get("grows") else None
        if opts.get("grows") and grows is None:
            return reject("bad-grows", grows=list(GROWS))
        discussed = opts.get("discussed", "").strip()
        if meta.get("admission") == "co-built":
            if not (cobuilt_ok(source, meta.get("cobuilt", [])) or discussed):
                return reject("not-co-built", hint=f"只收 {meta.get('person', 'Nicole')} 和 agent 一起经历过的：--human 原话、共建记录里的行，或加 --discussed \"她讨论时的原话\"")
            if grows is None:
                return reject("no-grows", hint="谁在长：--grows agent|human|both")
        rows = ctx.all_rows()
        notes, _, retracted, _ = live_state(rows)
        same = [r for r in notes if r["id"] not in retracted and any(tag_matches(cabinet_of(t), r.get("tags", [])) for t in tags)]
        retracts = opts.get("retracts")
        if any(r["id"] != retracts and norm((r.get("source") or {}).get("quote", "")) == norm(source["quote"]) and (r.get("source") or {}).get("path") == source.get("path") for r in same):
            return reject("duplicate")
        if retracts:
            old = next((r for r in notes if r["id"] == retracts), None)
            if old is None or retracts in retracted or not set(map(cabinet_of, old.get("tags", []))) & set(map(cabinet_of, tags)):
                return reject("bad-retract")
        record = {"op": "note", "id": new_id("f", rows), "ts": now(), "tags": tags, "claim": claim, "kind": kind, "source": source}
        record["when"] = when
        if grows:
            record["grows"] = grows
        if discussed:
            record["discussed"] = {"quote": discussed, "date": now()[:10]}
        if ctx.root:
            record["repo"] = ctx.root.name
        if "uncertain" in opts:
            record["uncertain"] = True
        if kind == "bayesian":
            record["overturns"] = opts["overturns"].strip()
        if retracts:
            record["retracts"] = retracts
        store.append(record)
        export_store(ctx, store)
        return out({
            "id": record["id"], "status": "stored", "store": store.scope, "line": source.get("line"),
            "look_back": [{"id": r["id"], "when": when_key(r), "claim": r["claim"]} for r in order(same)[-5:]],
        })
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def cmd_link(ctx, opts):
    try:
        text = opts.get("text", "").strip()
        if not text:
            return reject("no-text")
        hit = next((w for w in LINK_BANNED if w in text), None)
        if hit:
            return reject("forced-weight", word=hit)
        tags, bad = check_tags(opts)
        if bad is not None:
            return reject("bad-tag", tag=bad)
        if not tags:
            return reject("no-tag")
        store, err = pick_store(ctx, tags)
        if err:
            return reject(err[0], cabinet=err[1])
        rows = ctx.all_rows()
        notes, links, retracted, superseded = live_state(rows)
        live_ids = {r["id"] for r in notes if r["id"] not in retracted}
        based = opts.get("based-on", [])
        if not based or any(fid not in live_ids for fid in based):
            return reject("bad-based-on")
        sup = opts.get("supersedes")
        if sup and (sup in superseded or not any(r["id"] == sup for r in links)):
            return reject("bad-supersedes")
        grows = parse_grows(opts.get("grows"), store.meta()) if opts.get("grows") else None
        if opts.get("grows") and grows is None:
            return reject("bad-grows", grows=list(GROWS))
        record = {"op": "link", "id": new_id("l", rows), "ts": now(), "tags": tags, "text": text, "based_on": based}
        if grows:
            record["grows"] = grows
        if sup:
            record["supersedes"] = sup
        store.append(record)
        export_store(ctx, store)
        older = [r for r in links if r["id"] not in superseded and r["id"] != sup and set(map(cabinet_of, r.get("tags", []))) & set(map(cabinet_of, tags))]
        return out({"id": record["id"], "status": "stored", "store": store.scope,
                    "other_links_same_cabinet": [{"id": r["id"], "text": r["text"]} for r in older]})
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def new_id(prefix, rows):
    taken = {r.get("id") for r in rows}
    while True:
        ident = f"{prefix}-{secrets.token_hex(3)}"
        if ident not in taken:
            return ident


def cmd_recall(ctx, opts):
    try:
        rows = ctx.all_rows()
        notes, links, retracted, superseded = live_state(rows)
        wanted = opts.get("tag", [])
        query = (opts.get("q") or opts.get("about") or "").strip()
        if not wanted and not query:
            return cmd_cabinets(ctx, {})
        def hit(row):
            if wanted and any(tag_matches(w, row.get("tags", [])) for w in wanted):
                return True
            if query:
                hay = " ".join([row.get("claim", ""), row.get("text", ""), (row.get("source") or {}).get("quote", ""), *row.get("tags", [])])
                return all(part in hay for part in query.split())
            return False
        facts = [r for r in notes if r["id"] not in retracted and hit(r)]
        facts = order(facts)
        by_id = {r["id"]: r for r in notes}
        live_links = [r for r in links if r["id"] not in superseded and hit(r)]
        body = {
            "tags": wanted, "q": query,
            "sample_size": len(facts),
            "growth": growth(facts + live_links),
            "colorful": [{"id": r["id"], "kind": r["kind"], "claim": r["claim"]} for r in facts if r.get("kind") in ("difference", "bayesian")],
            "to_verify": [{"id": r["id"], "claim": r["claim"]} for r in facts if r.get("uncertain")],
            "facts": [present_note(r, retracted) for r in facts],
            "links_not_prior": [present_link(r, by_id, retracted) for r in live_links],
            "retracted_count": sum(1 for r in notes if r["id"] in retracted and hit(r)),
        }
        if len(facts) < SMALL_SAMPLE:
            body["hint"] = "样本还小：模糊的正确就够，不要强行给权重"
        if len(facts) >= 3 and len(body["colorful"]) * 3 > len(facts):
            body["hint_colorful"] = "七彩太多就不显眼了：普通石头才是底色。重看哪些其实只是 fact，用 --retracts 换成 fact"
        return out(body)
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def cmd_review(ctx, opts):
    try:
        rows = ctx.all_rows()
        notes, links, retracted, superseded = live_state(rows)
        wanted = opts.get("tag", [])
        pool = [r for r in notes if r["id"] not in retracted] + [r for r in links if r["id"] not in superseded]
        if wanted:
            pool = [r for r in pool if any(tag_matches(w, r.get("tags", [])) for w in wanted)]
        store = ctx.store()
        if store is None:
            return out({"review": []})
        state_path = store.folder / "review_state.json"
        seen = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        n = int(opts.get("n") or 3)
        pool.sort(key=lambda r: (seen.get(r["id"], ""), not r.get("uncertain"), random.random()))
        picked = pool[:n]
        if picked:
            store.ensure()
            stamp = now()
            seen.update({r["id"]: stamp for r in picked})
            state_path.write_text(json.dumps(seen, ensure_ascii=False) + "\n", encoding="utf-8")
        by_id = {r["id"]: r for r in notes}
        return out({"review": [present_note(r, retracted) if r["op"] == "note" else present_link(r, by_id, retracted) for r in picked]})
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def cmd_doctor(ctx, opts):
    try:
        rows = ctx.all_rows()
        notes, links, retracted, superseded = live_state(rows)
        moved, lost = [], []
        for r in notes:
            if r["id"] in retracted:
                continue
            st = source_status(r.get("source") or {})
            if st.get("lost"):
                lost.append({"id": r["id"], "claim": r["claim"], "source": source_label(r["source"])})
            elif st.get("moved"):
                moved.append({"id": r["id"], "from": r["source"].get("line"), "to": st["line_now"], "path": r["source"].get("path")})
        by_id = {r["id"]: r for r in notes}
        stale = [present_link(r, by_id, retracted) for r in links if r["id"] not in superseded]
        stale = [s for s in stale if s.get("stale_because")]
        counts = {}
        for r in notes:
            if r["id"] not in retracted:
                for t in r.get("tags", []):
                    if "/" in t:
                        counts[t] = counts.get(t, 0) + 1
        lonely = sorted(t for t, n in counts.items() if n == 1)
        return out({"checked": len(notes) - len(retracted & set(by_id)), "moved": moved, "lost": lost,
                    "stale_links": stale, "lonely_subtags": lonely})
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


def cmd_export(ctx, opts):
    try:
        paths = [str(export_store(ctx, store)) for store in ctx.stores() if store.exists()]
        return out({"status": "exported", "paths": paths})
    except Corrupt as exc:
        return reject("corrupt", at=str(exc))


# ---------- 导出页面 ----------

def export_store(ctx, store):
    store.ensure()
    rows = store.rows()
    page = store.folder / "index.html"
    meta = store.meta()
    title = f"贝叶斯大脑 · {meta.get('person', 'Nicole')} × {meta.get('repo') or store.root.name}"
    page.write_text(render_html(rows, store.cabinets(), title), encoding="utf-8")
    return page


def evidence_html(source, status):
    label = html.escape(source_label(source))
    if status.get("lost"):
        label += ' <b class="lost" data-testid="lost">原文已找不到</b>'
    elif status.get("moved"):
        label += f' <span class="moved">→ 现在第 {status["line_now"]} 行</span>'
    if source.get("type") == "file":
        href = Path(source["root"]) / source["path"]
        return f'<a class="evidence" data-testid="evidence" href="file://{html.escape(str(href), quote=True)}">{label}</a>'
    if source.get("type") == "web":
        return f'<a class="evidence" data-testid="evidence" href="{html.escape(source["url"], quote=True)}">{label}</a>'
    return f'<span class="evidence" data-testid="evidence">{label}</span>'


def label_hit(label, row):
    if label == "七彩":
        return row.get("op") == "note" and row.get("kind") in ("difference", "bayesian")
    if label == "问号":
        return bool(row.get("uncertain"))
    return tag_matches(label, row.get("tags", []))


def render_html(rows, cabinets, title):
    notes, links, retracted, superseded = live_state(rows)
    by_id = {r["id"]: r for r in notes}
    items = []
    for r in notes:
        source = r.get("source") or {}
        status = source_status(source)
        kind = html.escape(r.get("kind") or "fact")
        qmark = '<span class="qmark" data-testid="uncertain">?</span>' if r.get("uncertain") else ""
        quote = html.escape(source.get("quote", ""))
        over = f'<p class="over">改掉：{html.escape(r["overturns"])}</p>' if r.get("overturns") else ""
        if r.get("discussed"):
            over += f'<p class="over">讨论时：{html.escape(r["discussed"].get("quote", ""))}</p>'
        state = "retracted" if r["id"] in retracted else "open"
        body = (
            f'<article data-testid="fact" data-kind="{kind}" data-state="{state}" data-tags="{html.escape(" ".join(r.get("tags", [])), quote=True)}">'
            f'<p class="meta"><span class="kind" data-testid="kind">{kind}{qmark}</span><span class="fid">{html.escape(when_key(r))}<br>{html.escape(r["id"])}</span></p>'
            f'<h3 data-testid="claim">{html.escape(r.get("claim", ""))}</h3>'
            f'<blockquote>{quote}</blockquote>{evidence_html(source, status)}'
            f'<p class="rowtags" data-testid="tags">{html.escape(" · ".join(r.get("tags", []) + [GROWS_LABEL.get(r.get("grows"), "")]).strip(" ·"))}</p>{over}'
            + ('<p class="withdrawn" data-testid="withdrawn">已撤回</p>' if state == "retracted" else "")
            + "</article>"
        )
        items.append((r, body))
    for r in links:
        if r["id"] in superseded:
            continue
        info = present_link(r, by_id, retracted)
        stale = '<p class="withdrawn">依据的事实已撤回或丢失，需重算</p>' if info.get("stale_because") else ""
        body = (
            f'<article data-testid="link" data-kind="link" data-state="open" data-tags="{html.escape(" ".join(r.get("tags", [])), quote=True)}">'
            f'<p class="meta"><span class="kind">link</span><span class="fid">{html.escape(when_key(r))}<br>{html.escape(r["id"])}</span></p>'
            f'<h3>{html.escape(r.get("text", ""))}</h3>'
            f'<p class="rowtags">依据 {html.escape(", ".join(r.get("based_on", [])))} · 不作先验</p>{stale}</article>'
        )
        items.append((r, body))
    items.sort(key=lambda pair: (when_key(pair[0]), pair[0].get("ts", "")))
    labels = [("七彩", "difference 与 bayesian：同柜里不一样的那几块"), ("问号", "吃不准的石头，可能是小乌龟，等同柜下一条来验")]
    for c in cabinets:
        labels.append((c["name"], c.get("desc", "")))
        subs = sorted({t for r, _ in items for t in r.get("tags", []) if "/" in t and cabinet_of(t) == c["name"]})
        labels.extend((s, "") for s in subs)
    nav, rules, picks = [f'<a class="all" href="#top"><span class="qlabel">全部</span><span class="qcount">{len(items)}</span></a>'], [], []
    for i, (label, desc) in enumerate(labels):
        anchor = f"q-{i}"
        count = sum(1 for r, _ in items if label_hit(label, r))
        css = "tag lens" if label in ("七彩", "问号") else "tag child" if "/" in label else "tag"
        nav.append(f'<a class="{css}" href="#{anchor}" title="{html.escape(desc, quote=True)}"><span class="qlabel">{html.escape(label)}</span><span class="qcount">{count}</span></a>')
        picks.append(f'<span id="{anchor}" class="pick"></span>')
        rules.append(f'body:has(#{anchor}:target) .taglist a[href="#{anchor}"]{{font-weight:700;box-shadow:inset 2px 0 0 #141414;padding-left:0.45rem;}}')
        shown = [idx for idx, (r, _) in enumerate(items) if label_hit(label, r)]
        for idx in shown:
            rules.append(f'body:has(#{anchor}:target) #bags article[data-i="{idx}"]{{display:grid;}}')
    bodies = [body.replace("<article ", f'<article data-i="{idx}" ', 1) for idx, (_, body) in enumerate(items)]
    bags = "".join(picks) + '<div class="questions">' + "".join(bodies) + "</div>" if items else '<p class="empty" data-testid="empty-library">还没有事实。</p>'
    slots = {
        "TITLE": html.escape(title), "LAYOUT": "" if items else " single",
        "NAV": '<nav class="taglist" aria-label="柜子">' + "".join(nav) + "</nav>" if items else "",
        "BAGS": bags, "RULES": "\n".join(rules),
    }
    page = EXPORT_TEMPLATE.read_text(encoding="utf-8")
    for key, value in slots.items():
        token = f"@@{key}@@"
        if token not in page:
            raise RuntimeError(f"export template missing {token}")
        page = page.replace(token, value)
    return page


if __name__ == "__main__":
    sys.exit(main())
