# MEMORY.md (Long-term)

> 长期记忆（精选）。不写 token/密码等敏感信息。

## OpenClaw 运维与工作方式

- 更新/重启会短暂断线：任何重启操作应先通知，再执行，再验收。
- Discord Components v2：当前 message.edit 对带 components 的消息不稳定；已向上游提 PR 修复 interaction 数据解析兼容（#29013）。
- 学习与交流：计划每天 08:00 / 13:00 / 18:00 在 Moltbook 学习交流并回报。

## 协作护栏（不含 Budget fuse）

- Redundancy check：相似 tool call 优先复用缓存/TTL，减少重复与网络坑。
- No-new-signal exit：连续两步无新证据/无新产出就停并向人类提问。
