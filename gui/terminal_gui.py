# gui/terminal_gui.py
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import platform

class TerminalGUI:
    def __init__(self, master):
        self.master = master
        master.title("Графический терминал")

        # Создаем текстовое поле для вывода результатов
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Создаем поле для ввода команд
        self.input_entry = tk.Entry(master, width=50)
        self.input_entry.pack(expand=True, fill=tk.BOTH)

        # Создаем кнопку для выполнения команды
        self.run_button = tk.Button(master, text="Выполнить", command=self.execute_command)
        self.run_button.pack(expand=True, fill=tk.BOTH)

        # Создаем кнопку для возврата в главное меню
        self.return_button = tk.Button(master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(expand=True, fill=tk.BOTH)

    def execute_command(self):
        # Получаем команду из поля ввода
        command = self.input_entry.get()

        # Очищаем текстовое поле вывода
        self.output_text.delete(1.0, tk.END)

        try:
            # Проверяем платформу для корректного запуска команд
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True
                )
            else:
                # For Linux, split the command into a list for proper execution
                process = subprocess.Popen(
                    command.split(), shell=False, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True
                )

            # Получаем результат выполнения команды
            output, error = process.communicate()

            # Выводим результат в текстовое поле
            self.output_text.insert(tk.END, output)
            self.output_text.insert(tk.END, error)

        except Exception as e:
            # Handle exceptions and display the error message
            self.output_text.insert(tk.END, f"Error: {str(e)}")
    
    def return_to_main_menu(self):
        self.master.destroy()