# Guardrails（轻量护栏）

> 本版按用户要求：**不启用 Budget fuse**；启用去重/缓存与无新信号退出。

## 1) Redundancy Check（去重 / 缓存）

### 目的
避免同一轮/跨轮重复调用相同工具（尤其是网络搜索、状态检查、版本检查）。

### 执行规则
- **同一轮内**：相同输入+相同工具调用 => 不重复跑，复用上一次结果
- **跨轮**：对“低风险高频”调用设 TTL（默认 10–30 分钟）

### 建议缓存键（idempotency key）
`<tool>:<normalized_input>:<major_options>`

示例：
- `tavily_search:openclaw+components+v2:max=5:depth=advanced`
- `openclaw_status:deep=false`

### 不应缓存的例外（默认）
- 重启/更新/安装前的状态检查（要实时）
- 涉及资金/支付/删除的操作前确认（要实时）

## 2) No-new-signal Exit（无新信号就停）

### 目的
防止 agent 在不增加证据/不产出新工件的情况下循环。

### 判定
连续两步满足以下任一：
- 没有新增来源/证据
- 没有新增 artifact 文件
- 没有推进状态（plan/outline/draft/review）

=> 停止，并明确向人类提出 1 个澄清问题。

### 输出格式（固定）
- 我尝试了什么
- 我得到什么（新/旧）
- 我为什么停
- 你需要我下一步选哪条路（给 2–3 个选项）
