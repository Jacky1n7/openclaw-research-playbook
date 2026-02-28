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

## 运行

```bash
cd examples/cron-shell
python3 runner.py
# 或指定社区
python3 runner.py --communities openclaw-explorers,agentautomation,agent-ops
```

产物：
- `artifacts/results/<run_id>.json`
- `artifacts/receipts/<run_id>.json`
- `artifacts/digest.md`
- `state/state.json`
- `outbox/queue.json`（副作用/后续动作队列：可重试、可审计）

> 说明：未登录情况下只能抓社区页预览链接；若要深入摘要，需要登录后获取帖子正文。
