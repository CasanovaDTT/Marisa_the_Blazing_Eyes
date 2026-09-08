from .card_object import Card, CardType, Color
from .game_engine import Game, Player

# 预置常用卡牌效果函数
def effect_forest(game: Game, player: Player, targets=None):
    # 横置产生 {G}
    if not player.lands_tapped_this_turn:
        player.mana_pool['G'] += 1
        return True
    return False

def effect_mountain(game: Game, player: Player, targets=None):
    if not player.lands_tapped_this_turn:
        player.mana_pool['R'] += 1
        return True
    return False

def effect_plains(game: Game, player: Player, targets=None):
    if not player.lands_tapped_this_turn:
        player.mana_pool['W'] += 1
        return True
    return False

def effect_island(game: Game, player: Player, targets=None):
    if not player.lands_tapped_this_turn:
        player.mana_pool['U'] += 1
        return True
    return False

def effect_swamp(game: Game, player: Player, targets=None):
    if not player.lands_tapped_this_turn:
        player.mana_pool['B'] += 1
        return True
    return False

def effect_grizzly_bears(game: Game, player: Player, targets=None):
    # 生物卡本身已经在施放时进入战场，无需额外效果
    return True

def effect_lightning_bolt(game: Game, player: Player, targets=None):
    # 对目标造成3点伤害（目标由玩家选择）
    if targets:
        target = targets[0]
        if target in game.players:
            target.life -= 3
        elif target in game.battlefield:  # 可能是生物
            # 简化为对生物造成伤害（需要处理生物伤害标记）
            target.damage += 3
        return True
    return False

def effect_counterspell(game: Game, player: Player, targets=None):
    # 反击目标咒语（在堆叠中）
    if targets:
        stack_item = targets[0]
        if stack_item in game.stack:
            game.stack.remove(stack_item)
            return True
    return False

# 预置卡牌字典（名称 -> Card对象）
PRESET_CARDS = {
    "Forest": Card("Forest", "", [CardType.LAND], subtypes=["Forest"], colors=[Color.GREEN], text="", effect=effect_forest),
    "Mountain": Card("Mountain", "", [CardType.LAND], subtypes=["Mountain"], colors=[Color.RED], text="", effect=effect_mountain),
    "Plains": Card("Plains", "", [CardType.LAND], subtypes=["Plains"], colors=[Color.WHITE], text="", effect=effect_plains),
    "Island": Card("Island", "", [CardType.LAND], subtypes=["Island"], colors=[Color.BLUE], text="", effect=effect_island),
    "Swamp": Card("Swamp", "", [CardType.LAND], subtypes=["Swamp"], colors=[Color.BLACK], text="", effect=effect_swamp),
    "Grizzly Bears": Card("Grizzly Bears", "{1}{G}", [CardType.CREATURE], subtypes=["Bear"], colors=[Color.GREEN], text="", power=2, toughness=2, effect=effect_grizzly_bears),
    "Lightning Bolt": Card("Lightning Bolt", "{R}", [CardType.INSTANT], colors=[Color.RED], text="Lightning Bolt deals 3 damage to any target.", effect=effect_lightning_bolt),
    "Counterspell": Card("Counterspell", "{U}{U}", [CardType.INSTANT], colors=[Color.BLUE], text="Counter target spell.", effect=effect_counterspell),
}