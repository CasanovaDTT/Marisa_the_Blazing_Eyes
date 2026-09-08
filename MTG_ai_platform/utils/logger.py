import logging
import os
from datetime import datetime

class BattleLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.filename = None
        self.logger = None

    def start_new_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.log_dir, f"battle_{timestamp}.log")
        self.logger = logging.getLogger('battle')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.filename, encoding='utf-8')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.info("=== Battle Log Started ===")

    def log(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    def get_log_file(self):
        return self.filename