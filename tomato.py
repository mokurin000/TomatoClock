import os
import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QTimer, Qt


class TomatoClock(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.work_time = 3  # 1分钟
        self.break_time = 5 * 60  # 5分钟
        self.remaining_time = self.work_time
        self.is_working = True
        self.is_running = False

        self.init_ui()
        self.update_display()

    def init_ui(self):
        self.setWindowTitle("番茄时钟")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")

        self.status_label = QLabel("专注时间")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px;")

        self.start_btn = QPushButton("开始")
        self.start_btn.clicked.connect(self.toggle_timer)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_timer)

        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.reset_btn)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.setLayout(layout)

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.start_btn.setText("暂停" if self.is_running else "继续")
        if self.is_running:
            self.timer.start(1000)

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.switch_period()
        self.update_display()

    def switch_period(self):
        self.play_notice_sound()
        self.is_working = not self.is_working
        self.remaining_time = self.break_time if self.is_working else self.work_time
        self.is_running = False
        self.timer.stop()
        self.start_btn.setText("开始")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoClock()
    window.show()
    sys.exit(app.exec())
