from typing import Self
from PySide6.QtCore import QSettings


class TomatoStorage:
    def __init__(self):
        self._settings = QSettings("mokurin000", "TomatoClock", None)
        self.work_time: int = None
        self.break_time: int = None

    def __enter__(self) -> Self:
        self.work_time = self._settings.value("work-time") or 25 * 60
        self.break_time = self._settings.value("break-time") or 5 * 60
        return self

    def __exit__(self, _type, _value, _traceback):
        self._settings.setValue("work-time", self.work_time)
        self._settings.setValue("break-time", self.break_time)
