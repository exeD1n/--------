# gui/channel_info_app.py
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

        for process in self.processes_info:
            button_text = f"PID: {process['pid']}, Имя: {process['name']}"
            button = tk.Button(self.master, text=button_text, command=lambda info=process['pid']: self.show_connection_info(info))
            button.pack()

        # Кнопка для возвращения в главное меню
        return_button = tk.Button(self.master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        return_button.pack(pady=10, fill="both", expand=True)

    def get_os_channels(self):
        # Получаем информацию о процессах и их каналах через subprocess
        try:
            result = subprocess.run(["netstat", "-ano"], stdout=subprocess.PIPE, text=True, check=True)
            processes_info = self.parse_netstat_output(result.stdout)
            return processes_info
        except subprocess.CalledProcessError as e:
            print(f"Error executing netstat: {e}")
            return []

    def parse_netstat_output(self, netstat_output):
        # Парсим вывод netstat и формируем структуру данных
        processes_info = []
        lines = netstat_output.splitlines()
        for line in lines[4:]:  # Skip the first 4 lines as they are headers
            parts = line.split()
            if len(parts) >= 5:
                pid = int(parts[-1])
                name = "Unknown"
                connections = [
                    {"type": parts[0], "laddr": parts[1], "raddr": parts[2]}
                ]
                processes_info.append({"pid": pid, "name": name, "connections": connections})
        return processes_info

    def show_connection_info(self, pid):
        # Дополнительная информация о каналах для выбранного процесса
        try:
            result = subprocess.run(["netstat", "-ano"], stdout=subprocess.PIPE, text=True, check=True)
            connection_info = self.parse_process_connections(result.stdout, pid)
            self.show_connection_window(connection_info)
        except subprocess.CalledProcessError as e:
            print(f"Error executing netstat: {e}")

    def parse_process_connections(self, netstat_output, pid):
        # Парсим вывод netstat и получаем информацию о каналах для конкретного процесса
        connection_info = []
        lines = netstat_output.splitlines()
        for line in lines[4:]:  # Skip the first 4 lines as they are headers
            parts = line.split()
            if len(parts) >= 5:
                current_pid = int(parts[-1])
                if current_pid == pid:
                    connection_info.append({"type": parts[0], "laddr": parts[1], "raddr": parts[2]})
        return connection_info

    def show_connection_window(self, connection_info):
        # Отображаем окно с информацией о каналах
        connection_window = tk.Toplevel(self.master)
        connection_window.title("Дополнительная информация о каналах")

        for connection in connection_info:
            label_text = f"Тип: {connection['type']}, Локальный адрес: {connection['laddr']}, Удаленный адрес: {connection['raddr']}"
            label = tk.Label(connection_window, text=label_text)
            label.pack()

    def return_to_main_menu(self):
        self.master.destroy()