<div align="center">

<img src="./assets/banner.svg" width="100%" alt="OpenClaw Research Playbook" />

# OpenClaw Research Playbook（中文）

**赛博霓虹外壳 + 学术工程内核**：面向 OpenClaw 的多智能体科研/代码工作流、轻量护栏、文件记忆优先与运维模板。

[![OpenClaw](https://img.shields.io/badge/OpenClaw-playbook-8A2BE2?style=for-the-badge)](https://docs.openclaw.ai)
[![Language](https://img.shields.io/badge/Language-中文-00E5FF?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Active-FF2BD6?style=for-the-badge)](#)

</div>

---

## 目录导航

- [这是什么](#这是什么)
- [快速开始](#快速开始)
- [内容结构](#内容结构)
- [核心理念（A/B/C/Ops）](#核心理念abcops)
- [示例：可运行的 cron 工程骨架](#示例可运行的-cron-工程骨架)
- [贡献方式](#贡献方式)

---

## 这是什么

这个仓库用来沉淀一套**可复用、可审计、可迭代**的 Agentic R&D 方法论：

- **A 多智能体科研/代码工作流**：research → implement → test → review → write
- **B Discord 交互/控制台**：交互协议、状态机、失败回退
- **C 安全与权限（可控自动化）**：最小权限、二次确认、审计
- **Ops 运维**：更新策略、cron 可靠性、日志与排障

> 约束：本仓库不存任何 token/账号/隐私信息。

---

## 快速开始

### 1) 你最该先读的三份文件

- `playbooks/file_memory.md`：文件记忆优先（daily + long-term）
- `playbooks/guardrails.md`：轻量护栏（按当前策略：不含 budget fuse）
- `templates/cron_heartbeat_shell.md`：cron/heartbeat 标准壳（含 receipt）

### 2) 本地检索（推荐装 ripgrep）

```bash
brew install ripgrep
./scripts/agent_notes_scan.sh "Redundancy"
```

---

## 内容结构

```
playbooks/      # 方法论与流程（可复制）
templates/      # 模板（可直接改成你的项目）
examples/       # 最小可运行例子（骨架工程）
scripts/        # 小工具（检索/生成receipt等）
assets/         # README 的 UI 资源
```

---

## 核心理念（A/B/C/Ops）

### A) 多智能体科研/代码工作流
- 把聊天变成 **artifact 生产线**（文件、diff、可复现命令）

### B) Discord 交互/控制台
- 优先“状态机 + 协议”，UI 只是壳

### C) 安全与权限（可控自动化）
- 最小权限、危险动作二次确认、日志可审计

### Ops) 运维
- 可回滚升级、cron 稳定性、减少重复调用（Redundancy check）

---

## 示例：可运行的 cron 工程骨架

见：`examples/minimal-cron-project/`

这个骨架强调：
- receipts（小票审计）
- 去重/缓存
- 无新信号退出

---

## 贡献方式

- 欢迎 PR：把你验证有效的 guardrail、cron 模式、复现模板沉淀进来
- 请避免提交任何密钥/个人隐私（`.env` 一律不进仓库）
