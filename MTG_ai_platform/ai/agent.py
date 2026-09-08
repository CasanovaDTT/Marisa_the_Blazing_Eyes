from .deepseek_client import DeepSeekClient
from core.game_engine import Game
import json

class MTGAgent:
    def __init__(self, api_key: str, player_index: int, model="deepseek-chat"):
        self.client = DeepSeekClient(api_key, model)
        self.player_index = player_index
        self.last_action = None

    def decide_action(self, game: Game) -> str:
        # 获取状态和合法动作
        state = game.get_state_for_ai(self.player_index)
        legal = game.get_legal_actions(self.player_index)
        # 构建提示词
        prompt = f"""你是一个万智牌AI玩家。当前游戏状态如下（你是玩家{self.player_index+1}）：
{json.dumps(state, indent=2)}
合法动作：{legal}
请选择最优动作，只输出动作名称（如"play Grizzly Bears"或"attack all"或"pass"）。
"""
        messages = [{"role": "system", "content": "你是一名万智牌高手。"},
                    {"role": "user", "content": prompt}]
        response = self.client.get_response(messages)
        action = response.strip()
        # 解析动作
        self.last_action = action
        return action