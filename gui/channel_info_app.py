# gui/channel_info_app.py
import tkinter as tk
import psutil

class ChannelInfoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Информация о каналах в ОС")

        self.processes_info = self.get_os_channels()

        label = tk.Label(self.master, text="Информация о каналах в операционной системе:")
        label.pack()

        for process in self.processes_info:
            button_text = f"PID: {process['pid']}, Имя: {process['name']}"
            connection_info = process['connections']

            if connection_info:
                button = tk.Button(self.master, text=button_text, command=lambda info=connection_info: self.show_connection_info(info))
                button.pack()

        # Кнопка для возвращения в главное меню
        return_button = tk.Button(self.master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        return_button.pack(pady=10, fill="both", expand=True)

    def get_os_channels(self):
        # Получаем информацию о процессах и их каналах
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

    def show_connection_info(self, connection_info):
        connection_window = tk.Toplevel(self.master)
        connection_window.title("Дополнительная информация о каналах")

        for connection in connection_info:
            label_text = f"Тип: {connection.type}, Локальный адрес: {connection.laddr}, Удаленный адрес: {connection.raddr}"
            label = tk.Label(connection_window, text=label_text)
            label.pack()

    def return_to_main_menu(self):
        self.master.destroy()