"""bayes-lessons v2 unit keep. 锁命令合同：一个人 + 一个仓库一份库；柜子、原文片段出处、认知层、元数据与数据的分界。"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "bayes-lessons" / "scripts" / "bayes.py"
SETUP = ROOT / "skills" / "bayes-lessons-setup" / "scripts" / "setup.py"
SKILL = ROOT / "skills" / "bayes-lessons" / "SKILL.md"
SETUP_SKILL = ROOT / "skills" / "bayes-lessons-setup" / "SKILL.md"


@pytest.fixture
def env(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".bayes_lessons").mkdir()
    (repo / "notes.md").write_text("# 周报\n\n- **26w40**：融资余额跌破了 8 月 3 日的最低点，只有 **25797 亿元**。\n- 26w41：英国 30 年期国债收益率上涨至 6.02%\n", encoding="utf-8")
    return {"repo": repo, "tmp": tmp_path}


def run(env, *args, cwd=None, bare=False, extra_env=None):
    args = list(args)
    if not bare and args[0] == "note" and "--when" not in args and "--human" not in args:
        args += ["--when", "26w40"]
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd or env["repo"], capture_output=True, text=True,
        env={**os.environ, **(extra_env or {})},
    )
    body = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, body


def cabinets(env):
    assert run(env, "cabinets", "--name", "A股", "--desc", "两融、国家队")[0] == 0
    assert run(env, "cabinets", "--name", "Nicole", "--desc", "她做过说过的事")[0] == 0


def note_a(env, *extra):
    return run(env, "note", "--tag", "A股/两融", "--claim", "26w40 两融余额跌破 8/3 低点，25797 亿元", "--file", "notes.md", "--quote", "融资余额跌破了 8 月 3 日的最低点，只有 25797 亿元", *extra)


def test_unknown_verb(env):
    code, body = run(env, "investigate")
    assert code == 2 and body["reason"] == "unknown-verb"


def test_recall_without_args_lists_cabinets_and_creates_nothing(env, tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    code, body = run(env, "recall", cwd=plain)
    assert code == 0 and body["cabinets"] == [] and body["repo_enabled"] is False
    assert not (plain / ".bayes_lessons").exists()


def test_note_needs_known_cabinet(env):
    code, body = note_a(env)
    assert code == 2 and body["reason"] == "unknown-cabinet" and body["cabinet"] == "A股"


def test_note_locates_quote_and_ignores_markdown(env):
    cabinets(env)
    code, body = note_a(env)
    assert code == 0 and body["store"] == "repo" and body["line"] == 3
    row = json.loads((env["repo"] / ".bayes_lessons" / "brain.jsonl").read_text(encoding="utf-8"))
    assert row["source"]["path"] == "notes.md" and row["tags"] == ["A股/两融"] and row["repo"] == "repo"


@pytest.mark.parametrize("quote,reason", [("没有这句话", "quote-not-found"), ("", "no-quote")])
def test_note_rejects_missing_quote(env, quote, reason):
    cabinets(env)
    code, body = run(env, "note", "--tag", "A股", "--claim", "x", "--file", "notes.md", "--quote", quote)
    assert code == 2 and body["reason"] == reason


@pytest.mark.parametrize("path", ["/etc/hosts", "../x.md"])
def test_note_rejects_paths_outside_repo(env, path):
    cabinets(env)
    code, body = run(env, "note", "--tag", "A股", "--claim", "x", "--file", path, "--quote", "x")
    assert code == 2 and body["reason"] == "bad-path"


@pytest.mark.parametrize("word", ["因此", "相当于", "共识", "预计", "我认为"])
def test_inference_rejected(env, word):
    cabinets(env)
    code, body = run(env, "note", "--tag", "A股", "--claim", f"两融{word}见底", "--file", "notes.md", "--quote", "25797")
    assert code == 2 and body["reason"] == "inference"
    assert not (env["repo"] / ".bayes_lessons" / "brain.jsonl").exists()


def test_bayesian_needs_overturns(env):
    cabinets(env)
    assert note_a(env, "--kind", "bayesian")[1]["reason"] == "bayesian-needs-overturns"
    code, _ = note_a(env, "--kind", "bayesian", "--overturns", "两融在 8/3 低点之上")
    assert code == 0


def test_duplicate_quote_rejected(env):
    cabinets(env)
    assert note_a(env)[0] == 0
    code, body = note_a(env)
    assert code == 2 and body["reason"] == "duplicate"


def test_human_fact_stays_in_this_repo(env):
    cabinets(env)
    code, body = run(env, "note", "--tag", "Nicole/决定", "--claim", "Nicole 定了一个人加一个仓库一份库", "--human", "--quote", "粒度是 一个人（Nicole）+ 一个repo 级别的")
    assert code == 0 and body["store"] == "repo"
    row = json.loads((env["repo"] / ".bayes_lessons" / "brain.jsonl").read_text(encoding="utf-8"))
    assert row["source"]["type"] == "human"
    meta = json.loads((env["repo"] / ".bayes_lessons" / "meta.json").read_text(encoding="utf-8"))
    assert meta["person"] == "Nicole" and meta["repo"] == "repo"


def test_there_is_no_global_scope(env):
    code, body = run(env, "cabinets", "--name", "X", "--desc", "y", "--scope", "global")
    assert code == 2 and body["reason"] == "per-repo-only"


def test_recall_by_tag_keeps_marks(env):
    cabinets(env)
    note_a(env, "--uncertain")
    run(env, "note", "--tag", "Nicole", "--claim", "Nicole 要求先看事实", "--human", "--quote", "具体例子 查看")
    code, body = run(env, "recall", "--tag", "A股", "--tag", "Nicole")
    assert code == 0
    assert [f["store"] for f in body["facts"]] == ["repo", "repo"]
    first = body["facts"][0]
    assert first["uncertain"] is True and first["kind"] == "fact" and first["source"]["line_now"] == 3


def test_recall_q_finds_paraphrase_by_words(env):
    cabinets(env)
    note_a(env)
    code, body = run(env, "recall", "--q", "两融 25797")
    assert code == 0 and len(body["facts"]) == 1
    assert run(env, "recall", "--q", "纳指")[1]["facts"] == []


def test_retract_needs_shared_cabinet(env):
    cabinets(env)
    old = note_a(env)[1]["id"]
    run(env, "note", "--tag", "Nicole", "--claim", "x", "--human", "--quote", "y")
    code, body = run(env, "note", "--tag", "Nicole", "--claim", "z", "--human", "--quote", "w", "--retracts", old)
    assert code == 2 and body["reason"] == "bad-retract"
    code, _ = run(env, "note", "--tag", "A股/两融", "--claim", "26w40 两融余额 25797 亿元", "--file", "notes.md", "--quote", "只有 25797 亿元", "--retracts", old)
    assert code == 0
    body = run(env, "recall", "--tag", "A股")[1]
    assert old not in [f["id"] for f in body["facts"]] and body["retracted_count"] == 1


def test_link_layer_is_separate_and_supersedable(env):
    cabinets(env)
    fid = note_a(env)[1]["id"]
    assert run(env, "link", "--tag", "A股", "--text", "两融在退潮", "--based-on", "f-nope")[1]["reason"] == "bad-based-on"
    l1 = run(env, "link", "--tag", "A股", "--text", "两融在退潮", "--based-on", fid)[1]["id"]
    l2 = run(env, "link", "--tag", "A股", "--text", "两融退潮先于指数", "--based-on", fid, "--supersedes", l1)[1]["id"]
    body = run(env, "recall", "--tag", "A股")[1]
    assert [l["id"] for l in body["links_not_prior"]] == [l2]
    assert all(f["id"] != l2 for f in body["facts"])


def test_link_goes_stale_when_fact_retracted(env):
    cabinets(env)
    fid = note_a(env)[1]["id"]
    run(env, "link", "--tag", "A股", "--text", "两融在退潮", "--based-on", fid)
    run(env, "note", "--tag", "A股", "--claim", "两融 25797 亿元", "--file", "notes.md", "--quote", "只有 25797 亿元", "--retracts", fid)
    link = run(env, "recall", "--tag", "A股")[1]["links_not_prior"][0]
    assert link["stale_because"] == [fid]


def test_doctor_reports_moved_and_lost(env):
    cabinets(env)
    note_a(env)
    run(env, "note", "--tag", "A股", "--claim", "英国 30 年收益率 6.02%", "--file", "notes.md", "--quote", "英国 30 年期国债收益率上涨至 6.02%")
    text = (env["repo"] / "notes.md").read_text(encoding="utf-8")
    text = text.replace("- 26w41：英国 30 年期国债收益率上涨至 6.02%\n", "")
    (env["repo"] / "notes.md").write_text("新的一周\n\n" + text, encoding="utf-8")
    body = run(env, "doctor")[1]
    assert [m["to"] for m in body["moved"]] == [5]
    assert len(body["lost"]) == 1 and "6.02%" in body["lost"][0]["claim"]


def test_review_rotates(env):
    cabinets(env)
    note_a(env)
    run(env, "note", "--tag", "A股", "--claim", "英国 6.02%", "--file", "notes.md", "--quote", "6.02%")
    a = run(env, "review", "--n", "1")[1]["review"][0]["id"]
    b = run(env, "review", "--n", "1")[1]["review"][0]["id"]
    assert a != b


def test_note_from_subdir_writes_to_toplevel(env):
    cabinets(env)
    sub = env["repo"] / "deep"
    sub.mkdir()
    code, _ = run(env, "note", "--tag", "A股", "--claim", "x 25797", "--file", "notes.md", "--quote", "25797", cwd=sub)
    assert code == 0
    assert not (sub / ".bayes_lessons").exists()
    assert (env["repo"] / ".bayes_lessons" / "brain.jsonl").is_file()


def test_repo_cabinet_needs_enabled_repo(env, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=other, check=True)
    code, body = run(env, "cabinets", "--name", "X", "--desc", "y", cwd=other)
    assert code == 2 and body["reason"] == "repo-not-enabled"
    assert not (other / ".bayes_lessons").exists()


def test_export_page_shows_cabinets_links_and_lost(env):
    cabinets(env)
    fid = note_a(env)[1]["id"]
    run(env, "link", "--tag", "A股", "--text", "两融在退潮", "--based-on", fid)
    (env["repo"] / "notes.md").write_text("空\n", encoding="utf-8")
    assert run(env, "export")[0] == 0
    page = (env["repo"] / ".bayes_lessons" / "index.html").read_text(encoding="utf-8")
    assert "贝叶斯大脑 · Nicole × repo" in page and ">A股<" in page and ">A股/两融<" in page
    assert 'data-testid="link"' in page and "不作先验" in page
    assert 'data-testid="lost"' in page
    assert "@@" not in page


def test_corrupt_log_fails_fast(env):
    cabinets(env)
    (env["repo"] / ".bayes_lessons" / "brain.jsonl").write_text("{oops\n", encoding="utf-8")
    code, body = run(env, "recall", "--tag", "A股")
    assert code == 2 and body["reason"] == "corrupt"


def test_when_orders_the_cabinet_like_one_big_table(env):
    cabinets(env)
    assert note_a(env, "--when", "上周")[1]["reason"] == "bad-when"
    late = note_a(env, "--when", "26w40")[1]["id"]
    early = run(env, "note", "--tag", "A股", "--claim", "英国 6.02%", "--file", "notes.md", "--quote", "6.02%", "--when", "2026-07-30")[1]
    assert [r["id"] for r in early["look_back"]] == [late]
    body = run(env, "recall", "--tag", "A股")[1]
    assert [f["when"] for f in body["facts"]] == ["2026-W31-4", "2026-W40"]


def test_recall_shows_colorful_turtles_and_small_sample(env):
    cabinets(env)
    note_a(env, "--kind", "difference")
    run(env, "note", "--tag", "A股", "--claim", "英国 6.02%", "--file", "notes.md", "--quote", "6.02%", "--uncertain")
    run(env, "note", "--tag", "A股", "--claim", "周报标题", "--file", "notes.md", "--quote", "# 周报")
    body = run(env, "recall", "--tag", "A股")[1]
    assert body["sample_size"] == 3 and "不要强行给权重" in body["hint"]
    assert [c["kind"] for c in body["colorful"]] == ["difference"]
    assert len(body["to_verify"]) == 1
    assert "hint_colorful" not in body
    run(env, "note", "--tag", "A股", "--claim", "26w40 两融", "--file", "notes.md", "--quote", "26w40", "--kind", "bayesian", "--overturns", "两融在低点之上")
    assert "七彩太多" in run(env, "recall", "--tag", "A股")[1]["hint_colorful"]


def test_downgrade_by_retracting_same_quote(env):
    cabinets(env)
    old = note_a(env, "--kind", "bayesian", "--overturns", "两融在 8/3 低点之上")[1]["id"]
    code, _ = note_a(env, "--retracts", old)
    assert code == 0
    assert [f["kind"] for f in run(env, "recall", "--tag", "A股")[1]["facts"]] == ["fact"]


def test_link_refuses_forced_weight_and_shows_siblings(env):
    cabinets(env)
    fid = note_a(env)[1]["id"]
    assert run(env, "link", "--tag", "A股", "--text", "两融见底的概率六成", "--based-on", fid)[1]["reason"] == "forced-weight"
    l1 = run(env, "link", "--tag", "A股", "--text", "两融在退潮", "--based-on", fid)[1]["id"]
    body = run(env, "link", "--tag", "A股/两融", "--text", "退潮先于指数", "--based-on", fid)[1]
    assert [l["id"] for l in body["other_links_same_cabinet"]] == [l1]


def test_doctor_lists_lonely_subtags(env):
    cabinets(env)
    note_a(env)
    assert run(env, "doctor")[1]["lonely_subtags"] == ["A股/两融"]


def test_export_has_colorful_and_question_lenses(env):
    cabinets(env)
    note_a(env, "--kind", "difference", "--uncertain")
    page = (env["repo"] / ".bayes_lessons" / "index.html").read_text(encoding="utf-8")
    assert ">七彩<" in page and ">问号<" in page and "格物" in page


def test_event_needs_when_but_human_defaults_to_today(env):
    cabinets(env)
    code, body = run(env, "note", "--tag", "A股", "--claim", "x", "--file", "notes.md", "--quote", "25797", bare=True)
    assert code == 2 and body["reason"] == "no-when"
    run(env, "note", "--tag", "Nicole", "--claim", "她说要事件数据", "--human", "--quote", "具体的事件数据")
    fact = run(env, "recall", "--tag", "Nicole")[1]["facts"][0]
    assert fact["when"].startswith("20")


@pytest.mark.parametrize("rel", ["skills/x/SKILL.md", "skills/x/templates/t.md", "features/_template/track/02.md", "Soul.md",
                                 "assets/sources/business_analysis_bayes/a.md", ".bayes_lessons/brain.jsonl", ".bayes_lessons/template.md"])
def test_methodology_and_meta_are_not_sources(env, rel):
    cabinets(env)
    path = env["repo"] / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("格物致知 25797\n", encoding="utf-8")
    code, body = run(env, "note", "--tag", "A股", "--claim", "讲稿里写格物", "--file", rel, "--quote", "格物致知")
    assert code == 2 and body["reason"] == "meta-source"


@pytest.mark.parametrize("rel", ["features/f/track/bug-2026-11-22-x/02-define.md", "skills/x/scripts/run.py", "features/f/test_f_regression.py"])
def test_bug_records_code_and_tests_are_data_sources(env, rel):
    cabinets(env)
    path = env["repo"] / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Symptom: recall 换个说法返回 0 条\n", encoding="utf-8")
    code, _ = run(env, "note", "--tag", "A股", "--claim", "换说法取不到", "--file", rel, "--quote", "recall 换个说法返回 0 条")
    assert code == 0


def test_commit_is_a_source(env):
    cabinets(env)
    repo = env["repo"]
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(git + ["add", "notes.md"], cwd=repo, check=True)
    subprocess.run(git + ["commit", "-q", "-m", "Fix recall: match by cabinet, not exact about"], cwd=repo, check=True)
    code, body = run(env, "note", "--tag", "A股", "--claim", "修复落地：按柜子取", "--commit", "HEAD", "--quote", "match by cabinet")
    assert code == 0
    fact = run(env, "recall", "--tag", "A股")[1]["facts"][0]
    assert fact["source"]["type"] == "commit" and len(fact["source"]["sha"]) == 40 and "lost" not in fact["source"]
    assert run(env, "note", "--tag", "A股", "--claim", "x", "--commit", "HEAD", "--quote", "没有这句")[1]["reason"] == "quote-not-found"
    assert run(env, "note", "--tag", "A股", "--claim", "x", "--commit", "deadbeef", "--quote", "x")[1]["reason"] == "bad-commit"


def test_recall_points_to_template_until_filled(env):
    body = run(env, "recall")[1]
    assert body["template"] is None and "template.md" in body["hint_template"]
    (env["repo"] / ".bayes_lessons" / "template.md").write_text("## 1\n<填：一句话>\n", encoding="utf-8")
    assert "<填>" in run(env, "recall")[1]["hint_template"]
    (env["repo"] / ".bayes_lessons" / "template.md").write_text("## 1\n市场里正在起作用的事件\n", encoding="utf-8")
    assert "hint_template" not in run(env, "recall")[1]


def co_built(env, patterns=("wiki/laolao/weekly_readings/*",)):
    meta_path = env["repo"] / ".bayes_lessons" / "meta.json"
    cabinets(env)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update({"admission": "co-built", "cobuilt": list(patterns), "aliases": ["zonghan", "laolao"]})
    meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    reading = env["repo"] / "wiki/laolao/weekly_readings/weekly-reading-26w40.md"
    reading.parent.mkdir(parents=True, exist_ok=True)
    reading.write_text("| 两融跌破 8/3 低点 | ✅ 兑现 |\n", encoding="utf-8")


def test_co_built_library_refuses_raw_material(env):
    co_built(env)
    code, body = note_a(env, "--grows", "both")
    assert code == 2 and body["reason"] == "not-co-built"


def test_co_built_accepts_cobuilt_record_human_and_discussed(env):
    co_built(env)
    code, _ = run(env, "note", "--tag", "A股", "--claim", "读前验证：两融跌破 8/3 低点兑现", "--file", "wiki/laolao/weekly_readings/weekly-reading-26w40.md", "--quote", "两融跌破 8/3 低点", "--grows", "both")
    assert code == 0
    code, _ = run(env, "note", "--tag", "Nicole/纠正", "--claim", "她纠正：素材不等于样本", "--human", "--quote", "不是所有的素材 捕捉进来的时候 都直接进 贝叶斯样本", "--grows", "agent")
    assert code == 0
    code, body = note_a(env, "--grows", "laolao", "--discussed", "这一条两融我们讨论过")
    assert code == 0
    facts = run(env, "recall", "--tag", "A股")[1]["facts"]
    assert facts[-1]["grows"] == "human" and facts[-1]["discussed"]["quote"] == "这一条两融我们讨论过"


def test_co_built_needs_grows(env):
    co_built(env)
    code, body = run(env, "note", "--tag", "Nicole", "--claim", "x", "--human", "--quote", "y")
    assert code == 2 and body["reason"] == "no-grows"
    assert run(env, "note", "--tag", "Nicole", "--claim", "x", "--human", "--quote", "y", "--grows", "maybe")[1]["reason"] == "bad-grows"


def test_balance_hint_when_one_side_lags(env):
    co_built(env)
    for i in range(5):
        run(env, "note", "--tag", "Nicole/纠正", "--claim", f"纠正 {i}", "--human", "--quote", f"原话 {i}", "--grows", "agent")
    body = run(env, "recall")[1]
    assert body["growth"]["agent"] == 5 and "agent 在长" in body["hint_balance"]
    run(env, "note", "--tag", "Nicole/看见自己", "--claim", "她看见接错层", "--human", "--quote", "我这样回复，是不是没有和他同频讨论", "--grows", "human")
    assert "hint_balance" not in run(env, "recall")[1]


def test_setup_writes_admission_into_meta(tmp_path):
    git_repo(tmp_path, "git@github.com:476678244/scratch.git")
    code, body = setup_run(tmp_path, "--admission", "co-built", "--cobuilt", "wiki/laolao/weekly_readings/*", "--alias", "laolao")
    assert code == 0
    meta = json.loads((tmp_path / ".bayes_lessons" / "meta.json").read_text(encoding="utf-8"))
    assert meta["admission"] == "co-built" and meta["cobuilt"] == ["wiki/laolao/weekly_readings/*"] and meta["aliases"] == ["laolao"]
    assert "谁都不落下" in (tmp_path / ".bayes_lessons" / "template.md").read_text(encoding="utf-8")


def test_repo_dir_can_be_a_trial_folder(env):
    trial = {"BAYES_REPO_DIR": ".bayes_lessons_template"}
    (env["repo"] / ".bayes_lessons_template").mkdir()
    assert run(env, "cabinets", "--name", "A股", "--desc", "两融", extra_env=trial)[0] == 0
    assert note_a(env)[1]["reason"] == "unknown-cabinet"
    code, _ = run(env, "note", "--tag", "A股", "--claim", "两融 25797", "--file", "notes.md", "--quote", "25797", extra_env=trial)
    assert code == 0
    assert (env["repo"] / ".bayes_lessons_template" / "brain.jsonl").is_file()
    assert not (env["repo"] / ".bayes_lessons" / "brain.jsonl").exists()


def test_skill_states_the_loop():
    text = SKILL.read_text(encoding="utf-8")
    for phrase in ("recall --tag", "--quote", "--human", "link", "links_not_prior", "不当先验", "整柜", "--overturns", "doctor", "review",
                   "格物", "致知", "七彩", "小乌龟", "flomo", "先点标签", "推送", "金字塔", "--when", "colorful", "to_verify", "lonely_subtags",
                   "具体事件数据", "meta-source", "no-when", "元数据", "template.md", "--commit", "一个人 + 一个仓库",
                   "谁都不落下", "co-built", "--grows", "--discussed", "hint_balance"):
        assert phrase in text, phrase
    setup = SETUP_SKILL.read_text(encoding="utf-8")
    for phrase in ("cabinets", "柜子", "needs_migration", "migrate_v1.py", "template.md", "元数据框架", "--admission co-built", "--cobuilt"):
        assert phrase in setup, phrase


def setup_run(path, *args):
    proc = subprocess.run([sys.executable, str(SETUP), *args], cwd=path, capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout)


def git_repo(path, origin):
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "remote", "add", "origin", origin], cwd=path, check=True)


def test_setup_refuses_unowned(tmp_path):
    git_repo(tmp_path, "git@github.com:octocat/hello.git")
    code, body = setup_run(tmp_path)
    assert code == 2 and body["reason"] == "not-owned"
    assert not (tmp_path / ".bayes_lessons").exists()


def test_setup_opens_owned_repo_and_reports_migration(tmp_path):
    git_repo(tmp_path, "git@github.com:476678244/scratch.git")
    (tmp_path / ".bayes_lessons").mkdir()
    (tmp_path / ".bayes_lessons" / "facts.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "Agents.md").write_text("# Agents\n", encoding="utf-8")
    code, body = setup_run(tmp_path)
    assert code == 0 and body["status"] == "ready" and body["needs_migration"] is True
    assert (tmp_path / ".bayes_lessons" / "cabinets.json").is_file()
    assert [c["name"] for c in json.loads((tmp_path / ".bayes_lessons" / "cabinets.json").read_text(encoding="utf-8"))] == ["Nicole"]
    frame = (tmp_path / ".bayes_lessons" / "template.md").read_text(encoding="utf-8")
    assert "Nicole × " in frame and "<填" in frame and "@@" not in frame
    assert (tmp_path / ".bayes_lessons" / "index.html").is_file()
    assert "recall --tag" in (tmp_path / "Agents.md").read_text(encoding="utf-8")
    assert "bayes-lessons v2" in (tmp_path / "Index.md").read_text(encoding="utf-8")
    code, body = setup_run(tmp_path, "--dry-run")
    assert body["would_write"] == []
