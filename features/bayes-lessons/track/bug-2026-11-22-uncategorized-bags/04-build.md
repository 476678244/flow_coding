# build · 按类展示失效，71/81 进了未分类

status: done

## red（v1 复现，脚本取自 v1 备份，仓库外的临时 git 仓库）

```
$ v1 export
[('全部', '1'), ('未分类', '1')]
```

## fix

柜子必须先登记，`note` 的标签必须落在已登记的柜里；v1 数据用映射表迁移。

## green（keep）

- `test_note_needs_known_cabinet`
- `test_export_page_shows_cabinets_links_and_lost`

```
$ python -m pytest features/bayes-lessons -q -k ...
PASSED test_note_needs_known_cabinet
PASSED test_export_page_shows_cabinets_links_and_lost
```
