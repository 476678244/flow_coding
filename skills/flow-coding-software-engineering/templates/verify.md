# verify · __feature_id__

正式跟踪用 [track/05-verify.md](track/05-verify.md)。先跑 **keep**，对不上号再用 **once** 三角定位。

```bash
.venv/bin/python -m pytest features/__feature_id__ -v --tb=short
```
