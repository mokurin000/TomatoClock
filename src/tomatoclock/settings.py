from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpinBox,
    QDialogButtonBox,
    QDialog,
    QVBoxLayout,
    QLabel,
)


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
