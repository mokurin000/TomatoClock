import tkinter as tk
from tkinter import ttk


class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, current_work_min: int, current_break_min: int):
        super().__init__(parent)
        self.title("设置")
        self.resizable(False, False)
        self.grab_set()  # modal

        self.result = None

        # Work time
        ttk.Label(self, text="工作时间（分钟）:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.work_spin = tk.Spinbox(self, from_=1, to=60, width=5)
        self.work_spin.grid(row=0, column=1, padx=10, pady=10)
        self.work_spin.delete(0, "end")
        self.work_spin.insert(0, str(current_work_min))

        # Break time
        ttk.Label(self, text="休息时间（分钟）:").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.break_spin = tk.Spinbox(self, from_=1, to=60, width=5)
        self.break_spin.grid(row=1, column=1, padx=10, pady=10)
        self.break_spin.delete(0, "end")
        self.break_spin.insert(0, str(current_break_min))

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="确定", command=self.on_ok).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="取消", command=self.on_cancel).pack(
            side="left", padx=5
        )

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_ok(self):
        self.result = (int(self.work_spin.get()) * 60, int(self.break_spin.get()) * 60)
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()
