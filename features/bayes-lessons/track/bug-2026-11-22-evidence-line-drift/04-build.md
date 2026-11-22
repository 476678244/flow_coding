# build · 出处行号漂移，没人发现

status: done

## red（v1 复现，脚本取自 v1 备份，仓库外的临时 git 仓库）

```
$ v1 recall --about "美股指数怎么走？"  (after weekly.md got two new weeks on top)
{"about": "美股指数怎么走？", "observations": [{"id": "f-fc2a", "claim": "指数本周大跌 5%，跌破 200 天线", "evidence": "weekly.md:1"}]}
$ sed -n 1p weekly.md
- 26w43：新的一周
```

## fix

`--quote` 原文片段作出处，脚本算行号；recall / doctor 重新定位，多处匹配取离旧行最近的一处。

## green（keep）

- `test_fact_survives_restart_and_weekly_rewrite`
- `test_doctor_reports_moved_and_lost`

```
$ python -m pytest features/bayes-lessons -q -k ...
PASSED test_fact_survives_restart_and_weekly_rewrite
PASSED test_doctor_reports_moved_and_lost
```
