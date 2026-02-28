# Cron/Heartbeat 标准壳（不含 Budget fuse）

用途：把周期性任务做成“可复现、可审计、不会乱跑”的稳定循环。

## 结构

- 输入：固定的 sources（URL/feed/repo/path）
- 过程：收集 → 去重 → 摘要 → 写入 artifacts
- 输出：一条简短通知（可点开看 artifacts）

## 必备件

### 1) Idempotency key（避免重复副作用）
- 规则：每次运行生成 `run_id`，对每个 item 生成 `item_key`
- 若 `item_key` 已处理：跳过

### 2) Receipt（审计小票）
每次运行在 `artifacts/receipts/YYYY-MM-DD/<run_id>.json` 记录：
- 输入 sources
- 工具调用列表（tool, params, time）
- 产出文件路径
- 停止原因（正常结束/无新信号退出/错误）

### 3) Redundancy check + TTL 缓存
- 同轮/跨轮复用

### 4) No-new-signal exit
- 两步无新证据：停并问人类

## 产物目录建议

```
project/
  artifacts/
    receipts/
    results/
    digest.md
    todo.md
```

## 通知模板（Discord）
- 今日新增：N 条
- 关键要点：3 条
- TODO：1 条
- artifacts 链接/路径
