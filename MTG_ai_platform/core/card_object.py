from dataclasses import dataclass, field
from typing import List, Optional, Callable, Any
from enum import Enum

class CardType(Enum):
    LAND = "land"
    CREATURE = "creature"
    INSTANT = "instant"
    SORCERY = "sorcery"
    ENCHANTMENT = "enchantment"
    ARTIFACT = "artifact"
    PLANESWALKER = "planeswalker"

class Color(Enum):
    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"

@dataclass
class Card:
    name: str
    mana_cost: str  # 如 "{2}{R}"
    types: List[CardType]
    subtypes: List[str] = field(default_factory=list)
    colors: List[Color] = field(default_factory=list)
    text: str = ""  # 规则文本（仅用于展示）
    power: Optional[int] = None
    toughness: Optional[int] = None
    loyalty: Optional[int] = None
    # 效果函数：接收 (game, player, target) 返回动作列表
    effect: Optional[Callable] = None
    # 触发条件等
    abilities: List[str] = field(default_factory=list)  # 如 "flying", "haste"

    def __post_init__(self):
        # 根据类型自动添加基本异能标志（这里可扩展）
        pass