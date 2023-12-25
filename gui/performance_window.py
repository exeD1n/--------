# gui/performance_window.py
import tkinter as tk
import psutil
import time

class PerformanceWindow:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback

        self.performance_window = tk.Toplevel(master)
        self.performance_window.title("Производительность ОС")
        self.performance_window.geometry("400x200")

        self.label_memory = tk.Label(self.performance_window, text="Используемая виртуальная память:")
        self.label_cpu = tk.Label(self.performance_window, text="Общая загрузка процессора:")
        self.label_available_ram = tk.Label(self.performance_window, text="Доступная ОЗУ:")
        self.label_total_ram = tk.Label(self.performance_window, text="Всего ОЗУ:")

        self.label_memory.pack()
        self.label_cpu.pack()
        self.label_available_ram.pack()
        self.label_total_ram.pack()

        self.update_performance_data()

        # Кнопка для возвращения в главное меню
        self.return_button = tk.Button(self.performance_window, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(pady=10)

    def update_performance_data(self):
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        self.label_memory.config(text=f"Используемая виртуальная память: {memory_info.used / (1024 ** 3):.2f} GB")
        self.label_cpu.config(text=f"Общая загрузка процессора: {cpu_percent}%")
        self.label_available_ram.config(text=f"Доступная ОЗУ: {memory_info.available / (1024 ** 3):.2f} GB")
        self.label_total_ram.config(text=f"Всего ОЗУ: {memory_info.total / (1024 ** 3):.2f} GB")

        # Планируем обновление данных через 1 секунду
        self.performance_window.after(1000, self.update_performance_data)

    def return_to_main_menu(self):
        self.on_close_callback()

    def destroy(self):
        self.performance_window.destroy()