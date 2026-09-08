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
## 📦 项目结构
```bash
MTG_AI_Platform/
│
├── main.py                 # 程序入口
├── config.json             # 配置文件（API Key 等）
├── requirements.txt        # 依赖列表
├── build_exe.bat           # PyInstaller 打包脚本
│
├── core/                   # 核心引擎
│   ├── __init__.py
│   ├── game_engine.py      # 游戏主循环、状态管理、回合流程
│   ├── card_object.py      # 卡牌对象定义
│   ├── card_library.py     # 预置卡牌效果库
│   └── game_state.py       # 状态序列化（供 AI 读取）
│
├── ai/                     # AI 模块
│   ├── __init__.py
│   ├── deepseek_client.py  # DeepSeek API 客户端
│   └── agent.py            # AI 决策代理（状态→提示词→动作解析）
│
├── data/                   # 数据管理
│   ├── __init__.py
│   ├── card_db.py          # SQLite 卡牌库操作（导入/查询）
│   ├── deck_manager.py     # 套牌导入/存储
│   └── image_cache.py      # 图片下载与缓存
│
├── gui/                    # 图形界面
│   ├── __init__.py
│   └── main_window.py      # Tkinter 主窗口（含设置、对战、日志）
│
├── utils/                  # 工具
│   ├── __init__.py
│   ├── logger.py           # 战斗日志记录
│   └── deck_parser.py      # 套牌解析辅助
│
├── decks/                  # 用户套牌存放目录（自动创建）
│   └── example_deck.txt    # 示例套牌
│
├── logs/                   # 对局日志存储（自动生成）
│
└── cache/                  # 运行时缓存
    ├── db/                 # 卡牌 SQLite 数据库
    └── images/             # 卡牌图片缓存
```

---

## 🚀 快速开始（从零到运行）

### 1. 环境准备
- **Python 3.8+**：确保已安装，可在终端输入 `python --version` 检查。
- **网络**：用于调用 DeepSeek API。

### 2. 获取代码：直接下载 ZIP
在 GitHub 仓库页面点击 Code → Download ZIP，解压到本地。

### 3. 安装依赖
`pip install -r requirements.txt`

### 4. 获取 DeepSeek API Key
访问 DeepSeek 平台 注册并获取 API Key（免费额度足够测试）。

### 5. 运行程序
python main.py
首次运行会自动在根目录生成 config.json 和必要的文件夹（cache/、logs/ 等）。

### 6. 设置 API Key
在程序界面中点击菜单栏 文件 → 设置API Key，粘贴你的 API Key。

### 7. 准备套牌
在 decks/ 目录下创建套牌文件（如 my_deck.txt），每行一张卡牌（或「数量 名称」），例如：
`4 Forest
4 Mountain
4 Grizzly Bears
4 Lightning Bolt
2 Counterspell`
支持的卡牌名称见 core/card_library.py 中的 PRESET_CARDS

### 8. 开始对战
#### ·选择对战模式（人机对战 / AI自对弈）。

#### ·选择你的套牌和 AI 套牌。

#### ·点击「开始对战」，享受游戏！

## 🧠 AI 决策机制
### AI 通过 DeepSeek API 进行决策，流程如下：

#### ·引擎将当前游戏状态（生命值、手牌、战场、阶段、合法动作等）序列化为 JSON。

#### ·构建提示词，包含状态描述和可选择的动作列表。

#### ·调用 DeepSeek API，获取模型返回的动作。

#### ·解析动作并执行（如施放卡牌、攻击等）。

### 提示词示例：

`你是一个万智牌AI玩家。当前游戏状态如下（你是玩家1）：
{...状态JSON...}
合法动作：["play Grizzly Bears", "attack all", "pass"]
请选择最优动作，只输出动作名称。`
## 🛠️ 自定义与扩展指南
### 添加新卡牌
### 在 core/card_library.py 中定义卡牌效果函数，并添加到 PRESET_CARDS 字典。例如：
`def effect_giant_growth(game, player, targets=None):
    # 对目标生物 +3/+3 直到回合结束
    if targets:
        target = targets[0]
        target.power += 3
        target.toughness += 3
    return True`

`PRESET_CARDS["Giant Growth"] = Card(
    name="Giant Growth",
    mana_cost="{G}",
    types=[CardType.INSTANT],
    colors=[Color.GREEN],
    text="Target creature gets +3/+3 until end of turn.",
    effect=effect_giant_growth
)`
## 完善卡牌数据库
### data/card_db.py 提供了从 Scryfall 导入数据的骨架，你可以实现 import_from_scryfall() 方法以自动下载并存储完整卡牌数据。

## 替换为完整规则引擎
### 本项目中的 game_engine.py 为演示版。若需完整规则支持，可考虑集成 XMage（通过 Jython 桥接）或 Forge，替换核心引擎模块。

## 🤝 贡献指南
### 欢迎提交 Issue 和 Pull Request！

### 若发现规则 Bug，请附上对局日志和复现步骤。

### 新增卡牌效果或引擎特性时，请确保添加相应测试（若可能）。

#### 代码风格请遵循 PEP 8。

## 📄 许可证
### 本项目采用 MIT 许可证，详情见 LICENSE 文件。

## 🙏 致谢
### DeepSeek 提供强大的 AI 模型 API。

### Scryfall 提供卡牌数据 API。

### 所有万智牌玩家和开源社区贡献者。

## Enjoy the game! 🎴

### 本程序仅为学习与娱乐用途，不侵犯任何版权。万智牌是 Wizards of the Coast 的注册商标。


