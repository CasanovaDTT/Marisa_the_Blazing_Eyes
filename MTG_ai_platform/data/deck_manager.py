import json
import os
from typing import List
from core.card_object import Card
from core.card_library import PRESET_CARDS

class DeckManager:
    def __init__(self, deck_dir="decks"):
        self.deck_dir = deck_dir
        os.makedirs(deck_dir, exist_ok=True)

    def load_deck(self, filename: str) -> List[Card]:
        # 支持 .dek (MTGO) 和 .txt (每行数量+名称)
        path = os.path.join(self.deck_dir, filename)
        cards = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if parts[0].isdigit():
                    count = int(parts[0])
                    name = ' '.join(parts[1:])
                else:
                    count = 1
                    name = line
                for _ in range(count):
                    card = PRESET_CARDS.get(name)
                    if card:
                        cards.append(card)
                    else:
                        # 尝试从数据库获取（未实现）
                        print(f"卡牌 {name} 未预置，跳过。")
        return cards

    def list_decks(self) -> List[str]:
        return [f for f in os.listdir(self.deck_dir) if f.endswith(('.dek', '.txt'))]