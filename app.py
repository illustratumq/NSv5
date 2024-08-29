import tkinter as tk
import subprocess
import threading
import re
from tkinter import PhotoImage
from read_write import *
import psutil

path = '/opt/NSv5'

class ConsoleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перевірка НСУ v5")

        # Завантаження іконок
        self.icon_connected = PhotoImage(file='/opt/NSv5/2.png')     # Іконка для підключеного Ethernet
        self.icon_disconnected = PhotoImage(file='/opt/NSv5/1.png')  # Іконка для не підключеного Ethernet

        # Налаштування текстового поля для виводу
        self.console = tk.Text(root, wrap=tk.WORD, height=20, width=90)
        self.console.pack(padx=10, pady=10)
        self.console.insert(tk.END, "Очікування команди...\n")
        self.console.config(state=tk.DISABLED)

        # Кнопка для запуску скрипта
        self.run_button = tk.Button(root, text="Запустити", command=self.run_script)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Іконка статусу Ethernet
        self.ethernet_icon = tk.Label(root, image=self.icon_disconnected)
        self.ethernet_icon.pack(side=tk.LEFT, padx=10, pady=10)

        # Оновлення статусу Ethernet при запуску інтерфейсу
        self.update_ethernet_status()
        self.update_interval = 500  # Оновлювати кожні 0.5 секунд
        self.refresh_ethernet_status()


    def run_script(self):
        self.clear_console()
        # Дизаблити кнопку "Запустити" під час виконання скрипта
        self.run_button.config(state=tk.DISABLED)
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, "Запуск скрипта...\n")
        self.console.config(state=tk.DISABLED)
        threading.Thread(target=self.execute_script).start()

    def execute_script(self):
        process = subprocess.Popen(['python3', '/opt/NSv5/script.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        # Видалення символів керування терміналом
        control_chars = re.compile(r'\x1b\[[0-9;]*m|\x1b\[[0-9;]*[HJKSTf]')

        for line in process.stdout:
            line = control_chars.sub('', line)  # Видалення символів керування
            self.console.config(state=tk.NORMAL)
            self.console.insert(tk.END, line)
            self.console.config(state=tk.DISABLED)
            self.console.yview(tk.END)

        stderr = process.stderr.read()
        stderr = control_chars.sub('', stderr)  # Видалення символів керування
        if stderr:
            self.console.config(state=tk.NORMAL)
            self.console.insert(tk.END, stderr)
            self.console.config(state=tk.DISABLED)
            self.console.yview(tk.END)

        # Реактивація кнопки після завершення скрипта
        self.run_button.config(state=tk.NORMAL)

    def clear_console(self):
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)

    def update_ethernet_status(self):
        try:
            addresses = []
            interfaces = psutil.net_if_addrs()
            for k, v in interfaces.items():
                addresses.append(v[0].address)
            if any(['192.168.9.' in addr for addr in addresses]):
                self.ethernet_icon.config(image=self.icon_connected)
            else:
                self.ethernet_icon.config(image=self.icon_disconnected)
        except Exception as e:
            print(f"Помилка при перевірці статусу Ethernet: {e}")
            self.ethernet_icon.config(image=self.icon_unknown)

    def refresh_ethernet_status(self):
        self.update_ethernet_status()
        self.root.after(self.update_interval, self.refresh_ethernet_status)


root = tk.Tk()
app = ConsoleApp(root)
root.mainloop()
