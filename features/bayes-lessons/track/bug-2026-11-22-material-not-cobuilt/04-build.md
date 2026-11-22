# build · 投资库把素材当成了共建样本

status: done

## red

laolao 原话（2026-11-22）：「不是所有的素材 捕捉进来的时候 都直接进 贝叶斯样本」。当时的库：62 块石头全部出自周报总本，没有一块带她的讨论原话。

## fix

`meta.json` 的 `admission = co-built`：只收 `--human` 原话、`cobuilt` 通配里的共建记录（阅读追问、灵魂拷问、偏差卡、验证追踪），或带 `--discussed` 的材料；每块必须 `--grows agent|human|both`；recall 报 `growth` 与 `hint_balance`。原库移出仓库，存档在 `/Users/nicole/workspace/github/a476678244/_backup/investment_bayes_archives_2026-11-22/.bayes_lessons_material_trial/`；投资库根上只留一份 `.bayes_lessons/`。

## green（keep）

- `test_co_built_library_refuses_raw_material`
- `test_co_built_accepts_cobuilt_record_human_and_discussed`
- `test_co_built_needs_grows`
- `test_balance_hint_when_one_side_lags`

```
$ python -m pytest features/bayes-lessons -q -k co_built
PASSED test_co_built_library_refuses_raw_material
PASSED test_co_built_accepts_cobuilt_record_human_and_discussed
PASSED test_co_built_needs_grows
```
