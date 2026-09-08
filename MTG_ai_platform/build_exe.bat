@echo off
python m- pyinstaller --onefile --windowed --add-data "config.json;." --add-data "cache;cache" main.py
pause