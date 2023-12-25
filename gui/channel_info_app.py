# gui/channel_info_app.py
import platform
import subprocess
import tkinter as tk
import psutil

class ChannelInfoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Информация о каналах в ОС")

        self.processes_info = self.get_os_channels()

        label = tk.Label(self.master, text="Информация о каналах в операционной системе:")
        label.pack()

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.master, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        for process in self.processes_info:
            button_text = f"PID: {process['pid']}, Имя: {process['name']}"
            button = tk.Button(self.frame, text=button_text, command=lambda info=process['pid']: self.show_connection_info(info))
            button.pack()

        # Кнопка для возвращения в главное меню
        return_button = tk.Button(self.master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        return_button.pack(pady=10, fill="both", expand=True)

    def get_os_channels(self):
        # Получаем информацию о процессах и их каналах через psutil
        processes_info = []
        for process in psutil.process_iter(['pid', 'name', 'connections']):
            process_info = {
                'pid': process.info['pid'],
                'name': process.info['name'],
                'connections': process.info['connections']
            }
            if process_info['connections']:
                processes_info.append(process_info)
        return processes_info

    def show_connection_info(self, pid):
        # Дополнительная информация о каналах для выбранного процесса
        connection_info = [conn for process in self.processes_info if process['pid'] == pid for conn in process['connections']]
        self.show_connection_window(connection_info)

    def show_connection_window(self, connection_info):
        # Отображаем окно с информацией о каналах
        connection_window = tk.Toplevel(self.master)
        connection_window.title("Дополнительная информация о каналах")

        for connection in connection_info:
            label_text = f"Тип: {connection.type}, Локальный адрес: {connection.laddr}, Удаленный адрес: {connection.raddr}"
            label = tk.Label(connection_window, text=label_text)
            label.pack()

    def return_to_main_menu(self):
        self.master.destroy()