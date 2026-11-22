# build · recall 换个说法就取不到

status: done

## red（v1 复现，脚本取自 v1 备份，仓库外的临时 git 仓库）

```
$ v1 recall --about "美股指数怎么走"
{"about": "美股指数怎么走", "observations": []}
```

## fix

`recall --tag` 按柜子（大类含小类）取；`--q` 词都出现即命中；返回全部字段。

## green（keep）

- `test_recall_by_tag_keeps_marks`
- `test_recall_q_finds_paraphrase_by_words`

```
$ python -m pytest features/bayes-lessons -q -k ...
PASSED test_recall_by_tag_keeps_marks
PASSED test_recall_q_finds_paraphrase_by_words
```
