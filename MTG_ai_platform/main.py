import tkinter as tk
from gui.main_window import MTGGUI
import os

if __name__ == "__main__":
    # 创建必要的目录
    os.makedirs("decks", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("cache/db", exist_ok=True)
    os.makedirs("cache/images", exist_ok=True)

    root = tk.Tk()
    app = MTGGUI(root)
    root.mainloop()