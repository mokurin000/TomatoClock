# storage.py
import json
import os
from typing import Tuple

SETTINGS_FILE = os.path.expanduser("~/.tomatoclock_settings.json")

DEFAULT_WORK = 25 * 60
DEFAULT_BREAK = 5 * 60


def load_settings() -> Tuple[int, int]:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                work = int(data.get("work_time", DEFAULT_WORK))
                break_ = int(data.get("break_time", DEFAULT_BREAK))
                return work, break_
        except Exception:
            pass
    return DEFAULT_WORK, DEFAULT_BREAK


def save_settings(work_time: int, break_time: int) -> None:
    data = {"work_time": work_time, "break_time": break_time}
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
