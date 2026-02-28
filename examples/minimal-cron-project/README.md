# minimal-cron-project

一个最小工程骨架，用来演示：

- artifacts 输出目录
- receipts（审计小票）
- 去重/缓存
- 无新信号退出（连续两步无新证据就停并提示人类）

## 目录

```
examples/minimal-cron-project/
  artifacts/
    receipts/
    results/
    cache/
  notes/
```

## 推荐落地方式

1. 先定义 sources（URL/feed/repo/path）
2. 写一个 collect 脚本把 raw 结果落到 `artifacts/results/`
3. 让 agent 做摘要/提炼，把结论落到 `artifacts/digest.md`
4. 每轮写 receipt 到 `artifacts/receipts/`，便于审计与复现
