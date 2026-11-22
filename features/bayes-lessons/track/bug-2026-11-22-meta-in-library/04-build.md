# build · 库里存的是元数据，不是事件

status: done

## red（v1 复现，脚本取自 v1 备份，仓库外的临时 git 仓库）

```
$ v1 note --about "这个仓库是什么？" --claim "Soul 写本仓启用了 bayes-lessons" --evidence Soul.md:2
{"id": "f-5e38", "status": "stored"}
```

## fix

`meta-source` 拒绝方法 / 规则 / 模板 / `.bayes_lessons*` 出处；`--when` 必填；bug 记录、代码、测试、commit 是数据出处。

## green（keep）

- `test_methodology_and_meta_are_not_sources`
- `test_event_needs_when_but_human_defaults_to_today`
- `test_bug_records_code_and_tests_are_data_sources`

```
$ python -m pytest features/bayes-lessons -q -k ...
PASSED test_methodology_and_meta_are_not_sources
PASSED test_event_needs_when_but_human_defaults_to_today
PASSED test_bug_records_code_and_tests_are_data_sources
```
