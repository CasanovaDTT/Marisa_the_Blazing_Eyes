import random
from typing import List, Optional, Dict, Any, Tuple
from .card_object import Card, CardType
from .card_library import PRESET_CARDS
import copy

class Player:
    def __init__(self, name: str, deck: List[Card]):
        self.name = name
        self.life = 20
        self.deck = deck[:]
        self.hand: List[Card] = []
        self.battlefield: List[Card] = []
        self.graveyard: List[Card] = []
        self.exile: List[Card] = []
        self.mana_pool: Dict[str, int] = {'W':0,'U':0,'B':0,'R':0,'G':0,'C':0}
        self.lands_tapped_this_turn = False
        self.has_attacked = False
        self.creatures_attacked: List[Card] = []
        self.creatures_blocked: Dict[Card, List[Card]] = {}  # attacker -> blockers

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw(self, n=1):
        drawn = []
        for _ in range(n):
            if self.deck:
                card = self.deck.pop()
                self.hand.append(card)
                drawn.append(card)
        return drawn

    def untap_all(self):
        # 简化：所有永久物重置（这里只重置地标记）
        self.lands_tapped_this_turn = False
        # 重置生物攻击标记
        for card in self.battlefield:
            if CardType.CREATURE in card.types:
                card.tapped = False
                card.attacking = False
                card.blocking = False

    def take_damage(self, amount: int):
        self.life -= amount

class Game:
    def __init__(self, player1_deck: List[Card], player2_deck: List[Card], ai_agent1=None, ai_agent2=None):
        self.players = [Player("Player1", player1_deck), Player("Player2", player2_deck)]
        self.current_player_index = 0
        self.turn_number = 1
        self.phase = "beginning"  # beginning, draw, main1, combat, main2, end, cleanup
        self.stack: List[Any] = []  # 堆叠（存卡牌或动作）
        self.priority_player = 0  # 当前有优先权的玩家
        self.game_over = False
        self.winner = None
        self.log = []
        self.ai_agents = [ai_agent1, ai_agent2]  # AI代理列表，可None表示人类

        # 为每个玩家洗牌
        for p in self.players:
            p.shuffle_deck()
            # 初始手牌7张
            p.draw(7)

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_opponent(self, player: Player) -> Player:
        return self.players[1 - self.players.index(player)]

    def advance_turn(self):
        # 简单回合流程
        player = self.get_current_player()
        opponent = self.get_opponent(player)
        # 开始阶段
        self.phase = "beginning"
        # 重置生物状态
        player.untap_all()
        opponent.untap_all()
        # 抓牌阶段
        self.phase = "draw"
        player.draw(1)
        self.log_event(f"{player.name} draws a card.")
        # 主阶段一
        self.phase = "main1"
        # 战斗阶段
        self.phase = "combat"
        # 简化战斗：玩家宣告攻击者（由AI或人类决策）
        self.declare_attackers(player)
        # 防御方宣告阻挡者
        self.declare_blockers(opponent)
        # 战斗伤害
        self.deal_combat_damage()
        # 主阶段二
        self.phase = "main2"
        # 结束阶段
        self.phase = "end"
        # 清理（手牌上限等）
        self.phase = "cleanup"
        # 检查胜利条件
        if self.check_win_condition():
            return
        # 切换玩家
        self.current_player_index = 1 - self.current_player_index
        self.turn_number += 1

    def declare_attackers(self, player: Player):
        # 需要AI或用户选择攻击生物
        # 这里先使用AI决策，若没有AI则跳过
        # 简化：若有AI，让AI选择；否则自动选择所有未横置且具有攻击能力的生物
        attackers = []
        for card in player.battlefield:
            if CardType.CREATURE in card.types and not getattr(card, 'tapped', False):
                # 若AI存在，调用AI选择攻击者
                # 否则默认全部攻击
                attackers.append(card)
        # 标记攻击
        for card in attackers:
            card.tapped = True
            card.attacking = True
            player.creatures_attacked.append(card)
        self.log_event(f"{player.name} attacks with {len(attackers)} creatures.")

    def declare_blockers(self, player: Player):
        # 防御方选择阻挡（简化：AI或自动阻挡）
        blockers = {}
        # 自动匹配：每个攻击者被第一个未横置生物阻挡（演示）
        attacker_list = self.get_current_player().creatures_attacked
        for att in attacker_list:
            for blocker in player.battlefield:
                if CardType.CREATURE in blocker.types and not getattr(blocker, 'tapped', False):
                    blockers.setdefault(att, []).append(blocker)
                    blocker.tapped = True
                    break
        # 记录阻挡
        self.get_current_player().creatures_blocked = blockers
        self.log_event(f"{player.name} blocks with {sum(len(v) for v in blockers.values())} creatures.")

    def deal_combat_damage(self):
        # 计算伤害
        # 攻击者与阻挡者交换伤害
        current = self.get_current_player()
        opponent = self.get_opponent(current)
        for attacker, blockers in current.creatures_blocked.items():
            if blockers:
                # 分配伤害：简化，每个阻挡者受到攻击者力量伤害
                for blocker in blockers:
                    blocker.toughness -= attacker.power  # 简化为减少韧性
                    attacker.toughness -= blocker.power  # 互相伤害
                # 如果阻挡者都死了，攻击者可能对牌手造成伤害（本简化版忽略践踏等）
            else:
                # 无阻挡，对牌手造成伤害
                opponent.life -= attacker.power
                self.log_event(f"{attacker.name} deals {attacker.power} damage to {opponent.name}.")
        # 清空记录
        current.creatures_attacked = []
        current.creatures_blocked = {}

    def check_win_condition(self):
        for p in self.players:
            if p.life <= 0:
                self.game_over = True
                self.winner = self.get_opponent(p)
                self.log_event(f"{self.winner.name} wins!")
                return True
        return False

    def log_event(self, msg: str):
        self.log.append(msg)
        # 同时写入日志文件（由外部处理）

    def get_state_for_ai(self, player_index: int) -> Dict:
        # 序列化状态供AI使用
        player = self.players[player_index]
        opponent = self.players[1-player_index]
        state = {
            "player": {
                "life": player.life,
                "hand": [c.name for c in player.hand],
                "battlefield": [{"name": c.name, "power": c.power, "toughness": c.toughness} for c in player.battlefield if CardType.CREATURE in c.types],
                "mana_pool": player.mana_pool,
            },
            "opponent": {
                "life": opponent.life,
                "hand_count": len(opponent.hand),
                "battlefield": [{"name": c.name} for c in opponent.battlefield],
            },
            "phase": self.phase,
            "turn": self.turn_number,
            "stack": [str(item) for item in self.stack],
        }
        return state

    def get_legal_actions(self, player_index: int) -> List[str]:
        # 返回当前可执行的动作列表（简化）
        # 实际需根据阶段返回不同动作
        actions = ["pass"]
        if self.phase in ["main1", "main2"]:
            # 施放手牌
            player = self.players[player_index]
            for card in player.hand:
                actions.append(f"play {card.name}")
        if self.phase == "combat" and player_index == self.current_player_index:
            # 攻击宣言
            actions.append("attack all")
        return actions