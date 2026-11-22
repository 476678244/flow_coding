# acceptance-report · bayes-lessons

2026-11-10，对照 `acceptance.md` 与当次 pytest。先记后勾。九条都有对应用例，且已绿，所以勾选。

| keep | 用例 | 结果 |
| --- | --- | --- |
| 技能两段顺序，`investigate` 不是命令 | `test_skill_states_daily_path_and_investigate` | 绿 |
| 空仓库 `recall` 只建 `meta.json` | `test_recall_on_empty_repo_opens_dir_without_facts` | 绿 |
| 无证据不改 `facts.jsonl` | `test_note_without_evidence_leaves_facts_untouched` | 绿 |
| 推论词拒绝 | `test_inference_words_rejected` 五条 | 绿 |
| 第三动词拒绝 | `test_investigate_is_not_a_verb` | 绿 |
| 成功追加 | `test_note_appends_one_line` | 绿 |
| 未知问题得到 `[]` | `test_recall_unknown_about_is_empty_list` | 绿 |
| 新进程仍能调出 | `test_recall_survives_new_process` | 绿 |
| 撤回后新进程不再返回旧 id | `test_retract_survives_new_process` | 绿 |
| 绝对路径拒绝 | `test_absolute_evidence_rejected` | 绿 |
| 撤回不存在的 id | `test_bad_retract_does_not_append` | 绿 |

未做：浏览器。无 DOM，不假装做过。
