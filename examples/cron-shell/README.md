# cron-shell（示例）

这是一个“可复制”的 cron 标准壳示例，用来强制落地：

- **幂等性**（state / seen IDs / outbox 思路）
- **receipt 审计小票**（输入→决策→副作用→有效性检查）
- **tiered data access**（优先本地/缓存，再 web_fetch，再 browser）
- **Redundancy check + TTL=30min**
- **No-new-signal exit**

## 文件

- `schema/state.schema.json`
- `schema/receipt.schema.json`
- `templates/prompt.stub.md`
- `state/state.json`（示例）

> 下一步：可以在此目录下再加一个 `runner.py`，把 state/receipt 写入自动化。
