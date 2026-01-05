import tkinter as tk
from tkinter import ttk

from importlib import resources

import tomatoclock
from tomatoclock.storage import load_settings, save_settings
from tomatoclock.settings import SettingsDialog


class TomatoClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("番茄时钟")
        self.geometry("300x220")
        self.resizable(False, False)

        # Load settings
        self.work_time, self.break_time = load_settings()
        self.remaining_time = self.work_time
        self.is_working = True
        self.is_running = False

        self.setup_ui()
        self.update_display()

        # Timer
        self.after_id = None

    def setup_ui(self):
        # Time display
        self.time_label = tk.Label(self, text="25:00", font=("Helvetica", 48, "bold"))
        self.time_label.pack(pady=(20, 5))

        # Status label
        self.status_label = tk.Label(self, text="专注时间", font=("Helvetica", 16))
        self.status_label.pack(pady=(0, 15))

        # Buttons frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="开始", command=self.toggle_timer)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.reset_btn = ttk.Button(btn_frame, text="重置", command=self.reset_timer)
        self.reset_btn.grid(row=1, padx=5)

        self.settings_btn = ttk.Button(
            btn_frame, text="设置", command=self.open_settings
        )
        self.settings_btn.grid(row=0, column=2, padx=5)

    def open_settings(self):
        current_work_min = self.work_time // 60
        current_break_min = self.break_time // 60
        dialog = SettingsDialog(self, current_work_min, current_break_min)
        self.wait_window(dialog)

        if dialog.result:
            new_work, new_break = dialog.result
            self.work_time = new_work
            self.break_time = new_break

            # Update current period if not running
            if not self.is_running:
                if self.is_working:
                    self.remaining_time = new_work
                else:
                    self.remaining_time = new_break
                self.update_display()

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.start_btn.configure(text="暂停" if self.is_running else "继续")

        if self.is_running:
            self.tick()
        else:
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None

    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.switch_period()
        self.update_display()
        self.after_id = self.after(1000, self.tick)

    def switch_period(self):
        self.play_notice_sound()
        self.is_working = not self.is_working
        self.remaining_time = self.break_time if not self.is_working else self.work_time
        self.update_display()

    def reset_timer(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.is_running = False
        self.is_working = True
        self.remaining_time = self.work_time
        self.start_btn.configure(text="开始")
        self.update_display()

    def update_display(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
        self.status_label.config(text="专注时间" if self.is_working else "休息时间")

    def play_notice_sound(self):
        self.bell()

    def closeEvent(self, event=None):
        # Save settings on close
        save_settings(self.work_time, self.break_time)
        self.destroy()

    def destroy(self):
        # Override to ensure settings are saved
        save_settings(self.work_time, self.break_time)
        super().destroy()


if __name__ == "__main__":
    icon_path = resources.files(tomatoclock) / "tomato.ico"

    app = TomatoClock()
    app.iconbitmap(icon_path)
    app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()
