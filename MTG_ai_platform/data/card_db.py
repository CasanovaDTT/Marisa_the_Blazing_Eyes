import sqlite3
import json
import requests
import os
from typing import List, Dict, Optional

class CardDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cards
                     (id TEXT PRIMARY KEY,
                      name TEXT,
                      mana_cost TEXT,
                      type_line TEXT,
                      oracle_text TEXT,
                      power TEXT,
                      toughness TEXT,
                      colors TEXT,
                      rarity TEXT,
                      image_uris TEXT)''')
        conn.commit()
        conn.close()

    def import_from_scryfall(self, bulk_url="https://api.scryfall.com/bulk-data/oracle-cards"):
        # 下载Scryfall Oracle卡牌数据并导入
        resp = requests.get(bulk_url)
        data = resp.json()
        # 实际需要获取下载链接，这里简化：直接使用全量数据（可能很大）
        # 更稳健：使用 https://api.scryfall.com/bulk-data 获取最新的oracle-cards json文件
        # 演示仅做示意
        print("需要实现完整导入功能，建议先从Scryfall下载oracle-cards.json导入。")
        pass

    def get_card(self, name: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM cards WHERE name=?", (name,))
        row = c.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "mana_cost": row[2], "type_line": row[3],
                    "oracle_text": row[4], "power": row[5], "toughness": row[6],
                    "colors": row[7].split(',') if row[7] else [], "rarity": row[8],
                    "image_uris": json.loads(row[9]) if row[9] else {}}
        return None

    def save_card(self, card_data: Dict):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO cards VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (card_data.get('id'), card_data.get('name'), card_data.get('mana_cost'),
                   card_data.get('type_line'), card_data.get('oracle_text'),
                   card_data.get('power'), card_data.get('toughness'),
                   ','.join(card_data.get('colors', [])), card_data.get('rarity'),
                   json.dumps(card_data.get('image_uris', {}))))
        conn.commit()
        conn.close()