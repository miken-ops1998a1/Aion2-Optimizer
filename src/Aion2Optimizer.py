import os
import sys
import json
import time
import ctypes
import psutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from utils.network import NetworkOptimizer
from utils.process import ProcessOptimizer
from utils.logger import Logger

class Aion2Optimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Aion2 Optimizer v1.0.0")
        self.root.geometry("620x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#0D1117")

        self.logger = Logger()
        self.net = NetworkOptimizer()
        self.proc = ProcessOptimizer()
        self.optimized = False

        self.build_ui()
        self.check_admin()

    def check_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showwarning("Aion2 Optimizer",
                                   "Запустите программу от имени администратора!")
            sys.exit(1)

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#0D1117")
        header.pack(pady=15)
        tk.Label(header, text="⚔️ Aion2 Optimizer", font=("Segoe UI", 22, "bold"),
                 fg="#FFD700", bg="#0D1117").pack()
        tk.Label(header, text="Network & Frame Stabilizer for AION 2",
                 font=("Segoe UI", 10), fg="#8B949E", bg="#0D1117").pack()

        # Status Card
        card = tk.Frame(self.root, bg="#161B22", bd=0, highlightthickness=1,
                        highlightbackground="#30363D")
        card.pack(fill="x", padx=30, pady=10)

        self.status_var = tk.StringVar(value="● Не оптимизировано")
        tk.Label(card, textvariable=self.status_var, font=("Segoe UI", 12, "bold"),
                 fg="#FF6B6B", bg="#161B22").pack(pady=8)

        self.ping_var = tk.StringVar(value="Ping: — ms")
        self.fps_var = tk.StringVar(value="FPS: —")
        stats = tk.Frame(card, bg="#161B22")
        stats.pack(pady=5)
        tk.Label(stats, textvariable=self.ping_var, font=("Consolas", 10),
                 fg="#58A6FF", bg="#161B22").pack(side=tk.LEFT, padx=15)
        tk.Label(stats, textvariable=self.fps_var, font=("Consolas", 10),
                 fg="#3FB950", bg="#161B22").pack(side=tk.LEFT, padx=15)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0D1117")
        btn_frame.pack(pady=10)

        self.btn_opt = tk.Button(btn_frame, text="🚀 OPTIMIZE", command=self.optimize,
                                 bg="#238636", fg="white", font=("Segoe UI", 12, "bold"),
                                 width=16, height=2, relief="flat", cursor="hand2")
        self.btn_opt.grid(row=0, column=0, padx=8)

        self.btn_restore = tk.Button(btn_frame, text="♻️ RESTORE", command=self.restore,
                                     bg="#DA3633", fg="white", font=("Segoe UI", 12, "bold"),
                                     width=16, height=2, relief="flat", cursor="hand2")
        self.btn_restore.grid(row=0, column=1, padx=8)

        # Log
        tk.Label(self.root, text="Log:", font=("Segoe UI", 10, "bold"),
                 fg="#8B949E", bg="#0D1117").pack(anchor="w", padx=35)
        self.log_box = tk.Text(self.root, height=14, width=72, bg="#0D1117",
                               fg="#3FB950", font=("Consolas", 9),
                               insertbackground="white", relief="flat")
        self.log_box.pack(padx=35, pady=5)

    def log(self, msg):
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see(tk.END)
        self.root.update()

    def optimize(self):
        self.status_var.set("● Оптимизация...")
        self.log("=" * 50)
        self.log("Запуск оптимизации для AION 2")

        try:
            self.net.optimize(self.log)
            self.proc.optimize(self.log)

            self.optimized = True
            self.status_var.set("● Оптимизировано ✓")
            self.log("✅ Готово! Запускайте AION 2.")
            messagebox.showinfo("Aion2 Optimizer", "Оптимизация завершена!")
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
            self.status_var.set("● Ошибка")

    def restore(self):
        self.log("=" * 50)
        self.log("Восстановление настроек...")
        self.net.restore(self.log)
        self.proc.restore(self.log)
        self.optimized = False
        self.status_var.set("● Не оптимизировано")
        self.log("♻️ Настройки восстановлены.")
        messagebox.showinfo("Aion2 Optimizer", "Восстановлено!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aion2Optimizer(root)
    root.mainloop()