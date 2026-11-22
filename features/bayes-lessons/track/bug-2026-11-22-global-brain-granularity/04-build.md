# build · 大脑放全局，Nicole 在不同仓库的认知被混在一起

status: done

## red（v1 复现，脚本取自 v1 备份，仓库外的临时 git 仓库）

```
Nicole 原话：我希望的是 每个repo 有自己的 库。 未来 我们会进行 贝叶斯认知与 事实在 不同库 之间的 碰撞。
```

## fix

去掉全局存放；每个仓库根 `.bayes_lessons/` 一份库，meta.json 写 person 和 repo；全局 4 条移回学到它们的仓库，原目录改名存档。

## green（keep）

- `test_each_repo_keeps_its_own_nicole_and_its_own_cognition`
- `test_there_is_no_global_scope`

```
$ python -m pytest features/bayes-lessons -q -k ...
PASSED test_each_repo_keeps_its_own_nicole_and_its_own_cognition
PASSED test_there_is_no_global_scope
```
