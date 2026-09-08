# 🧙 MTG AI Battle Platform

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DeepSeek API](https://img.shields.io/badge/DeepSeek-API-green)](https://deepseek.com/)

> 基于 **DeepSeek 大语言模型** 的万智牌（Magic: The Gathering）AI 对战平台 —— 核心演示版

---

## 📖 简介

**MTG AI Battle Platform** 是一个用 Python 编写的桌面应用程序，允许你与 AI 进行万智牌对战，或让两个 AI 通过 DeepSeek API 自动对弈。  
本项目以 **核心规则演示** 为目的，提供了一个完整的对战框架（游戏循环、卡牌效果、回合流程、战斗阶段），并集成了 **DeepSeek API** 实现智能决策。

> ⚠️ **当前版本为「核心演示版」**，实现了万智牌基本规则（地、生物、法术、瞬间等），但尚未覆盖全部规则细节（如堆叠顺序、触发式异能、完整费用支付等）。代码结构清晰，易于扩展，欢迎贡献！

---

## ✨ 功能特性

- 🤖 **AI 对战**：支持 **人机对战**（人类 vs AI）和 **AI 自对弈**（两个 DeepSeek 模型互搏）
- 🃏 **卡牌系统**：内置常见卡牌（地、灰棕熊、闪电击、反击咒语等），可通过 `card_library.py` 轻松添加新卡牌
- 🧠 **DeepSeek 集成**：通过 API 获取 AI 决策，提示词包含当前游戏状态和合法动作
- 🎮 **图形界面**：基于 Tkinter 的图形界面，包含战场显示、实时日志、套牌选择和交互输入
- 📁 **套牌管理**：支持 `.txt` / `.dek` 格式套牌导入，预置示例套牌
- 📜 **战斗日志**：自动记录每场对局，保存为 `logs/battle_时间戳.log`
- 🖼️ **图片缓存**（骨架）：支持卡牌图片下载与本地缓存（需进一步集成 Scryfall）
- 💾 **卡牌数据库**（骨架）：支持从 Scryfall 导入 SQLite 卡牌库（待完善）

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 网络连接（用于调用 DeepSeek API）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/你的用户名/mtg-ai-platform.git
   cd mtg-ai-platform
