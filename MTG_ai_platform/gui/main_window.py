import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import json
import os
from core.game_engine import Game
from core.card_library import PRESET_CARDS
from data.deck_manager import DeckManager
from ai.agent import MTGAgent
from utils.logger import BattleLogger
import time

class MTGGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MTG AI 对战平台")
        self.root.geometry("1000x700")

        # 加载配置
        self.config = self.load_config()
        self.api_key = self.config.get("deepseek_api_key", "")

        # 初始化组件
        self.deck_manager = DeckManager("decks")
        self.logger = BattleLogger("logs")
        self.game = None
        self.agent1 = None
        self.agent2 = None
        self.running = False
        self.auto_mode = False  # AI自对弈

        self.setup_ui()

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        else:
            default = {"deepseek_api_key": "", "db_path": "cache/db/oracle-cards.sqlite", "image_cache_dir": "cache/images", "log_dir": "logs"}
            with open("config.json", "w") as f:
                json.dump(default, f, indent=2)
            return default

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=2)

    def setup_ui(self):
        # 菜单栏
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="设置API Key", command=self.set_api_key)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        self.root.config(menu=menubar)

        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部控制区
        control_frame = ttk.LabelFrame(main_frame, text="对战控制", padding="5")
        control_frame.pack(fill=tk.X, pady=5)

        # 模式选择
        ttk.Label(control_frame, text="模式:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="人机对战")
        mode_combo = ttk.Combobox(control_frame, textvariable=self.mode_var, values=["人机对战", "AI自对弈"], state="readonly", width=12)
        mode_combo.grid(row=0, column=1, padx=5)

        # 套牌选择
        ttk.Label(control_frame, text="你的套牌:").grid(row=0, column=2, padx=5)
        self.deck1_var = tk.StringVar()
        deck1_combo = ttk.Combobox(control_frame, textvariable=self.deck1_var, values=self.deck_manager.list_decks(), state="readonly", width=15)
        deck1_combo.grid(row=0, column=3, padx=5)

        ttk.Label(control_frame, text="AI套牌:").grid(row=0, column=4, padx=5)
        self.deck2_var = tk.StringVar()
        deck2_combo = ttk.Combobox(control_frame, textvariable=self.deck2_var, values=self.deck_manager.list_decks(), state="readonly", width=15)
        deck2_combo.grid(row=0, column=5, padx=5)

        # 按钮
        self.start_btn = ttk.Button(control_frame, text="开始对战", command=self.start_game)
        self.start_btn.grid(row=0, column=6, padx=5)
        self.pause_btn = ttk.Button(control_frame, text="暂停", command=self.pause_game, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=7, padx=5)
        self.stop_btn = ttk.Button(control_frame, text="终止", command=self.stop_game, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=8, padx=5)

        # 状态信息
        self.status_label = ttk.Label(control_frame, text="就绪")
        self.status_label.grid(row=0, column=9, padx=10)

        # 战场显示（简化：使用文本区域）
        battle_frame = ttk.LabelFrame(main_frame, text="战场与日志", padding="5")
        battle_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 左侧战场信息（可扩展为图形，这里用文本树）
        info_frame = ttk.Frame(battle_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.battle_text = scrolledtext.ScrolledText(info_frame, height=15, width=50)
        self.battle_text.pack(fill=tk.BOTH, expand=True)

        # 右侧日志
        log_frame = ttk.Frame(battle_frame)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(log_frame, text="战斗日志").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=50, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 底部交互输入（人机模式）
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.send_btn = ttk.Button(input_frame, text="发送指令", command=self.send_command)
        self.send_btn.pack(side=tk.RIGHT, padx=5)

        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_api_key(self):
        # 弹窗输入API Key
        api_key = tk.simpledialog.askstring("设置DeepSeek API Key", "请输入你的API Key:", parent=self.root)
        if api_key:
            self.api_key = api_key
            self.config["deepseek_api_key"] = api_key
            self.save_config()
            messagebox.showinfo("成功", "API Key已保存")

    def start_game(self):
        # 加载套牌
        deck1_name = self.deck1_var.get()
        deck2_name = self.deck2_var.get()
        if not deck1_name or not deck2_name:
            messagebox.showerror("错误", "请选择两个套牌")
            return
        deck1 = self.deck_manager.load_deck(deck1_name)
        deck2 = self.deck_manager.load_deck(deck2_name)
        if not deck1 or not deck2:
            messagebox.showerror("错误", "套牌加载失败，请检查套牌文件")
            return

        # 创建AI代理（根据模式）
        if self.mode_var.get() == "人机对战":
            self.agent1 = None  # 人类控制
            if self.api_key:
                self.agent2 = MTGAgent(self.api_key, 1)
            else:
                messagebox.showerror("错误", "人机对战需要设置API Key")
                return
        else:  # AI自对弈
            if not self.api_key:
                messagebox.showerror("错误", "AI自对弈需要设置API Key")
                return
            self.agent1 = MTGAgent(self.api_key, 0)
            self.agent2 = MTGAgent(self.api_key, 1)

        # 初始化游戏
        self.game = Game(deck1, deck2, self.agent1, self.agent2)
        self.logger.start_new_log()
        self.running = True
        self.auto_mode = (self.mode_var.get() == "AI自对弈")
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)

        # 更新界面状态
        self.update_battlefield()
        self.log_message("对局开始！")

        # 启动游戏循环（在后台线程）
        threading.Thread(target=self.game_loop, daemon=True).start()

    def game_loop(self):
        while self.running and not self.game.game_over:
            # 执行一个回合或一个动作
            self.step_game()
            # 更新GUI（通过after）
            self.root.after(0, self.update_battlefield)
            # 延时
            time.sleep(0.5)  # 可调
        self.root.after(0, self.on_game_end)

    def step_game(self):
        # 判断当前玩家是否需要AI决策
        player = self.game.get_current_player()
        idx = self.game.current_player_index
        agent = self.game.ai_agents[idx] if idx < len(self.game.ai_agents) else None

        # 简化：在每个主阶段让AI或人类选择动作
        if self.game.phase in ["main1", "main2"]:
            if agent:
                # AI决策
                action = agent.decide_action(self.game)
                self.log_message(f"AI {player.name} 选择动作: {action}")
                self.execute_action(action, idx)
            else:
                # 人类决策（通过输入框交互）
                # 这里需要等待人类输入，但我们用信号量？为了简化，我们让人类在输入框输入指令后触发
                # 这里我们设置一个标志，当有输入时执行
                pass
        elif self.game.phase == "combat":
            # 自动战斗处理（已在引擎中实现）
            pass

        # 如果人类模式，等待人类输入；但当前线程不能阻塞，所以我们将人类输入放在主线程通过事件触发
        # 为了简单，在人类模式下我们不自动推进，而是由用户点击“发送指令”来推进
        if not self.auto_mode:
            # 如果当前玩家是人类（即玩家1），我们需要等待命令
            if idx == 0:
                # 等待用户通过输入框发送指令，我们通过一个队列来实现
                # 这里用简单方法：在send_command中设置一个动作变量，然后在此处检查
                # 但为了不阻塞，我们在这里循环检查，但会占用CPU
                # 更好的方式：使用 threading.Event
                # 我们简单实现：在send_command中直接执行动作，并更新状态
                # 我们修改策略：在人类模式下，我们只在主线程通过按钮触发动作，不在此循环中自动推进
                # 所以这里我们跳过，让用户通过send_command推进游戏
                pass
        else:
            # AI自对弈，自动推进
            # 如果当前玩家是AI，但决策已在上面的agent处理，我们只需推进回合
            pass

        # 如果回合结束，推进到下一阶段
        # 这里我们用简单方式：直接执行整个回合流程（由引擎处理）
        # 但为了避免复杂，我们在主循环中调用game.advance_turn()并检查状态
        # 但由于advance_turn()包含攻击等，我们可以直接调用
        if not self.game.game_over:
            self.game.advance_turn()
            self.log_message(f"进入第{self.game.turn_number}回合，{self.game.get_current_player().name}的回合")

    def execute_action(self, action: str, player_idx: int):
        # 根据动作字符串执行操作
        if action.startswith("play "):
            card_name = action[5:].strip()
            player = self.game.players[player_idx]
            # 从手牌中找出该卡牌
            for card in player.hand:
                if card.name == card_name:
                    # 简化：直接施放（忽略费用）
                    player.hand.remove(card)
                    player.battlefield.append(card)
                    self.log_message(f"{player.name} 施放 {card_name}")
                    # 触发卡牌效果
                    if card.effect:
                        card.effect(self.game, player, None)
                    break
        elif action == "attack all":
            # 由引擎处理
            pass
        elif action == "pass":
            # 无操作
            pass

    def send_command(self):
        # 人类玩家输入指令
        if not self.game or self.game.game_over:
            return
        cmd = self.input_entry.get().strip()
        if not cmd:
            return
        self.input_entry.delete(0, tk.END)
        # 执行指令（假设当前玩家是人类）
        self.execute_action(cmd, 0)
        self.update_battlefield()

    def update_battlefield(self):
        if not self.game:
            return
        # 更新战场文本
        text = ""
        for i, p in enumerate(self.game.players):
            text += f"=== {p.name} ===\n"
            text += f"生命: {p.life}\n"
            text += f"手牌: {len(p.hand)} 张\n"
            text += f"战场生物: {[c.name for c in p.battlefield if hasattr(c, 'types') and 'creature' in str(c.types)]}\n"
            text += f"坟场: {[c.name for c in p.graveyard]}\n\n"
        self.battle_text.delete(1.0, tk.END)
        self.battle_text.insert(tk.END, text)

        # 更新状态栏
        self.status_bar.config(text=f"回合 {self.game.turn_number} | 阶段 {self.game.phase} | 当前玩家 {self.game.get_current_player().name}")

    def log_message(self, msg: str):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.logger.log(msg)

    def on_game_end(self):
        self.log_message("对局结束！")
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        # 关闭日志文件
        if self.logger.logger:
            for handler in self.logger.logger.handlers[:]:
                handler.close()
                self.logger.logger.removeHandler(handler)
        messagebox.showinfo("对局结束", f"胜利者: {self.game.winner.name if self.game.winner else '无'}")

    def pause_game(self):
        self.running = False
        self.status_label.config(text="已暂停")

    def stop_game(self):
        self.running = False
        self.game.game_over = True
        self.on_game_end()