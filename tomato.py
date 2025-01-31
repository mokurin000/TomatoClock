import os
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QSpinBox,
    QDialogButtonBox,
)
from PySide6.QtCore import QTimer, Qt, QSettings
from typing import Self


class TomatoStorage:
    def __init__(self):
        self._settings = QSettings("mokurin000", "TomatoClock", None)
        self.work_time = None
        self.break_time = None

    def __enter__(self) -> Self:
        self.work_time = self._settings.value("work-time") or 25 * 60
        self.break_time = self._settings.value("break-time") or 5 * 60
        return self

    def __exit__(self, _type, _value, _traceback):
        self._settings.setValue("work-time", self.work_time)
        self._settings.setValue("break-time", self.break_time)


class SettingsDialog(QDialog):
    def __init__(self, parent=None, work_time=25, break_time=5):
        super().__init__(parent)
        self.setWindowTitle("设置")
        layout = QVBoxLayout()

        # 工作时间设置
        work_layout = QHBoxLayout()
        work_label = QLabel("工作时间（分钟）:")
        self.work_spin = QSpinBox()
        self.work_spin.setRange(1, 60)
        self.work_spin.setValue(work_time)
        work_layout.addWidget(work_label)
        work_layout.addWidget(self.work_spin)

        # 休息时间设置
        break_layout = QHBoxLayout()
        break_label = QLabel("休息时间（分钟）:")
        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 60)
        self.break_spin.setValue(break_time)
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_spin)

        # 按钮组
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(work_layout)
        layout.addLayout(break_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)


class TomatoClock(QWidget):
    def __init__(self):
        super().__init__()

        with TomatoStorage() as storage:
            self.work_time = storage.work_time
            self.break_time = storage.break_time

        self.remaining_time = self.work_time
        self.is_working = True
        self.is_running = False

        self.init_ui()
        self.update_display()

    def init_ui(self):
        self.setWindowTitle("番茄时钟")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # 时间显示
        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")

        # 状态显示
        self.status_label = QLabel("专注时间")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px;")

        # 控制按钮
        self.start_btn = QPushButton("开始")
        self.start_btn.clicked.connect(self.toggle_timer)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_timer)

        self.settings_btn = QPushButton("设置")
        self.settings_btn.clicked.connect(self.open_settings)

        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.settings_btn)

        # 定时器设置
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.setLayout(layout)

    def open_settings(self):
        current_work = self.work_time // 60
        current_break = self.break_time // 60
        dialog = SettingsDialog(self, current_work, current_break)

        if dialog.exec() == QDialog.Accepted:
            # 更新时间段设置
            new_work = dialog.work_spin.value() * 60
            new_break = dialog.break_spin.value() * 60
            self.work_time = new_work
            self.break_time = new_break

            # 如果计时器未运行，立即更新显示
            if not self.is_running:
                if self.is_working:
                    self.remaining_time = new_work
                else:
                    self.remaining_time = new_break
                self.update_display()

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.start_btn.setText("暂停" if self.is_running else "继续")
        if self.is_running:
            self.timer.start(1000)
        else:
            self.timer.stop()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.switch_period()
        self.update_display()

    def switch_period(self):
        self.play_notice_sound()
        self.is_working = not self.is_working
        self.remaining_time = self.break_time if not self.is_working else self.work_time
        self.update_display()

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.is_working = True
        self.remaining_time = self.work_time
        self.start_btn.setText("开始")
        self.update_display()

    def update_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        self.status_label.setText("专注时间" if self.is_working else "休息时间")

    @staticmethod
    def play_notice_sound():
        match os.name:
            case "nt":
                import winsound

                winsound.PlaySound("*", winsound.SND_ALIAS | winsound.SND_ASYNC)
            case _:
                QApplication.beep()

    def closeEvent(self, event):
        with TomatoStorage() as storage:
            storage.work_time = self.work_time
            storage.break_time = self.break_time

        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoClock()
    window.show()
    sys.exit(app.exec())
