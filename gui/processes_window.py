# gui/processes_window.py
import os
import tkinter as tk
import psutil
import time
from tkinter import messagebox

class ProcessesWindow:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback

        self.processes_window = tk.Toplevel(master)
        self.processes_window.title("Просмотр процессов")
        self.processes_window.geometry("500x300")

        self.process_listbox = tk.Listbox(self.processes_window, selectmode=tk.SINGLE, exportselection=False)
        self.process_listbox.pack(expand=True, fill=tk.BOTH)

        self.process_listbox.bind("<Double-Button-1>", self.on_double_click)

        # Кнопка для обновления данных
        self.refresh_button = tk.Button(self.processes_window, text="Обновить", command=self.update_processes_data)
        self.refresh_button.pack(pady=10)

        # Кнопка для возвращения в главное меню
        self.return_button = tk.Button(self.processes_window, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(pady=10)

        self.update_processes_data()

    def update_processes_data(self):
        self.process_listbox.delete(0, tk.END)

        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            if process.info['name'] != 'python.exe' and process.info['pid'] != os.getpid():
                process_name = process.info['name']
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(process.info['create_time']))
                item_text = f"{process_name} (PID: {process.info['pid']}, Запущен: {create_time})"
                self.process_listbox.insert(tk.END, item_text)

    def on_double_click(self, event):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            selected_process_info = self.process_listbox.get(selected_index)
            messagebox.showinfo("Детали процесса", selected_process_info)

    def return_to_main_menu(self):
        self.on_close_callback()

    def destroy(self):
        self.processes_window.destroy()