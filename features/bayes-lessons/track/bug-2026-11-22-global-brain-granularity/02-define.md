# define · 大脑放全局，Nicole 在不同仓库的认知被混在一起

status: done（2026-11-22 补记；修洞与本次 v2 重构同轮完成）

1. Symptom：v2 中途把 Nicole 柜放在全局 `~/.config/devin/bayes_brain/`，任何仓库 recall 都会倒出它；Nicole 指出粒度应是一个人 + 一个仓库。
2. Broken next step：以后要做库与库之间的碰撞，全局库让「同一个人在不同仓库的不同认知」无从比较。
3. Boundary：换到另一个仓库（新进程、新 cwd）。
4. Acceptance after fix：在 a 仓库记下的 Nicole 原话和 link → 跨过「进程退出、换到 b 仓库」 → b 看不到；b 对同一件事可以有不同的 link。
5. Coverage gap：当时的 regression 锁的是「Nicole 事实跟着 agent 进另一个仓库」——把错误的设计锁成了合同。

Root cause：把「跨仓库都用得上」当成了「应该共享」；没问 Nicole 要的粒度。
