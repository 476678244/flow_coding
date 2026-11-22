#!/usr/bin/env python3
"""把 v1 的 .bayes_lessons/facts.jsonl 迁成 v2 brain.jsonl。在仓库根运行。

只迁「稳定 about」表里的市场事实：about → 柜子/标签，claim 原文去出处文件里重新找片段。
身份、阅读顺序、refactor 这类元信息行、观点行、找不到原文的行不迁，写进 migration_v1.json。
facts.jsonl 改名为 facts.v1.jsonl 存档，不删。--dry-run 只打印报告。
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("bayes", Path(__file__).with_name("bayes.py"))
bayes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bayes)

STABLE = {
    "能源价格怎么走？": ["能源/价格"],
    "全球能源供给怎么了？": ["能源/供给"],
    "油轮运价怎么走？": ["能源/运价"],
    "曼德海峡谁在控制？": ["能源/曼德海峡"],
    "美债收益率怎么走？": ["美债/收益率"],
    "隔夜融资利率怎么走？": ["利率/隔夜"],
    "垃圾债利差怎么走？": ["信用/利差"],
    "美债谁在买？": ["美债/买家"],
    "英国长债收益率怎么走？": ["国债/英国"],
    "美股 ETF 谁在买？": ["美股/ETF"],
    "美股散户融资余额怎么走？": ["美股/融资"],
    "海外资金在买美股还是美债？": ["美股/买家", "美债/买家"],
    "美股指数怎么走？": ["美股/指数"],
    "高度依赖短期融资的 AI 股怎么了？": ["美股/AI融资"],
    "台积电业绩怎么了？": ["公司/台积电"],
    "英伟达回购怎么了？": ["公司/英伟达"],
    "SpaceX 在买什么？": ["公司/SpaceX"],
    "美国房贷利率怎么走？": ["利率/房贷"],
    "黄金价格怎么走？": ["黄金/价格"],
    "美联储利率怎么走？": ["利率/美联储"],
    "日本政策利率怎么走？": ["利率/日本"],
    "A股国家队在买什么？": ["A股/国家队"],
    "A股两融余额怎么走？": ["A股/两融"],
    "中国社融怎么走？": ["中国/社融"],
}
CABINETS = {
    "能源": "汽油柴油价格、放储、出口禁令、运价、海峡控制这些已经印出来的价格和已经做出的供给动作",
    "美债": "收益率有没有穿过已经在用的那条线；海外、中国、日本等持仓方向",
    "利率": "美联储、日本、隔夜 SOFR、30 年房贷这些已经做出或已经印出来的利率",
    "信用": "CCC 等低评级利差的宽窄",
    "国债": "美国以外的国债收益率，例如英国长端穿过的高点",
    "美股": "指数穿均线、ICI ETF 净流入、FINRA 融资余额、海外净买入",
    "公司": "已经印出来的指引、毛利率、回购授权、收购和牌照",
    "黄金": "金价有没有穿过已经在用的均线",
    "A股": "国家队申购宽基 ETF 的成交、两融余额穿过已有低点",
    "中国": "已经公布的社融、贷款、M2",
}
OPINION = {
    "f-b383": "含预测：直观还有至少五到十的空间",
    "f-843f": "含因果解释与共识：围绕悲观共识的传导",
    "f-46ab": "含网格读法：相当于向下 10% 网格买入",
    "f-bd6b": "claim 夹着批注：南添口头对这一行",
}
QUOTE = {
    "f-4179": "从 3.65% 附近跳升接近 3.9%",
    "f-d82f": "Sep-26 | 1,480,054",
    "f-131e": "海外资金净买入美股 9420 亿美元",
    "f-2d00": "胡塞武装现已控制了曼德海峡",
    "f-19c0": "本周 #美联储 #降息 25bp",
    "f-2e39": "跌破 1y（年线）后持续阴跌",
    "f-dc76": "原值是278.24亿，修正后是345.79亿",
    "f-ed31": "纳指目前处于27%的速度线、SOXX目前处于44%速度线",
}
WEEK = re.compile(r"^(估值（[^）]*）：|\d{2}w\d{2}(~\d{2}w\d{2})?：|\d{4} 年第 \d+ 周：|\d+/\d+ )")


def find_when(root, rel, line, claim, ts):
    texts = [claim]
    try:
        texts.append((root / rel).read_text(encoding="utf-8").splitlines()[line - 1])
    except (OSError, IndexError):
        pass
    for text in texts:
        m = re.search(r"(\d{2})w(\d{2})", text)
        if m:
            return bayes.parse_when(m.group(0))
        m = re.search(r"(\d{4}) 年第 (\d+) 周", text)
        if m:
            return bayes.parse_when(f"{m.group(1)}w{m.group(2)}")
    m = re.match(r"(?:截至 )?(\d{1,2})/(\d{1,2})\D", claim)
    if m:
        return bayes.parse_when(f"{ts[:4]}-{int(m.group(1)):02d}-{int(m.group(2)):02d}")
    return None


def find_quote(root, evidence, claim, fid=None):
    path = root / evidence.rpartition(":")[0]
    hint = int(evidence.rpartition(":")[2].split("-")[0])
    stripped = WEEK.sub("", claim).strip()
    candidates = [QUOTE[fid]] if fid in QUOTE else [stripped, claim]
    pieces = sorted((p.strip() for p in re.split(r"[，；。]", stripped)), key=len, reverse=True)
    candidates += [p for p in pieces if len(p) >= 8 and fid not in QUOTE]
    for quote in candidates:
        line = bayes.locate(path, quote, hint)
        if line:
            return quote, line
    return None, None


def main(argv):
    dry = "--dry-run" in argv
    root = bayes.git_toplevel(Path.cwd())
    if root is None:
        print(json.dumps({"error": "rejected", "reason": "no-repo"}))
        return 2
    folder = root / ".bayes_lessons"
    old = folder / "facts.jsonl"
    if not old.is_file():
        print(json.dumps({"error": "rejected", "reason": "no-v1-log"}))
        return 2
    if (folder / "brain.jsonl").exists():
        print(json.dumps({"error": "rejected", "reason": "brain-exists"}))
        return 2
    rows = [json.loads(line) for line in old.read_text(encoding="utf-8").splitlines() if line.strip()]
    retracted = {r["retracts"] for r in rows if r.get("retracts")}
    migrated, skipped, used = [], [], set()
    for r in rows:
        why = None
        if r["id"] in retracted or r.get("retracts"):
            why = "撤回链上的行"
        elif r["id"] in OPINION:
            why = OPINION[r["id"]]
        elif r.get("about") not in STABLE:
            why = "元信息（身份、阅读顺序、启用、refactor），不是这库要认识的事"
        if why:
            skipped.append({"id": r["id"], "about": r.get("about"), "claim": r["claim"], "why": why})
            continue
        quote, line = find_quote(root, r["evidence"], r["claim"], r["id"])
        if quote is None:
            skipped.append({"id": r["id"], "about": r["about"], "claim": r["claim"], "why": f"原文已在 {r['evidence']} 附近找不到"})
            continue
        tags = r.get("tags") or STABLE[r["about"]]
        new = {
            "op": "note", "id": bayes.new_id("f", [{"id": i} for i in used]), "ts": r["ts"],
            "tags": tags, "claim": r["claim"], "kind": r.get("kind") or "fact",
            "source": {"type": "file", "root": str(root), "path": r["evidence"].rpartition(":")[0], "line": line, "quote": quote},
            "repo": root.name, "migrated_from": r["id"],
        }
        when = find_when(root, new["source"]["path"], line, r["claim"], r["ts"])
        if when:
            new["when"] = when
        if r.get("uncertain"):
            new["uncertain"] = True
        used.add(new["id"])
        migrated.append(new)
    report = {"root": str(root), "migrated": len(migrated), "skipped": skipped}
    if not dry:
        store = bayes.Store("repo", folder, root)
        store.ensure()
        names = {c["name"] for c in store.cabinets()}
        cabs = [{k: v for k, v in c.items() if k != "scope"} for c in store.cabinets()]
        for tag in {bayes.cabinet_of(t) for m in migrated for t in m["tags"]}:
            if tag not in names:
                cabs.append({"name": tag, "desc": CABINETS.get(tag, ""), "ts": bayes.now()})
        store.cabinets_path.write_text(json.dumps(cabs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for m in migrated:
            store.append(m)
        old.rename(folder / "facts.v1.jsonl")
        (folder / "migration_v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        bayes.export_store(bayes.Context(root), store)
    print(json.dumps({**report, "skipped": len(skipped), "dry_run": dry}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
