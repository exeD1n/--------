# gui/app.py
import os
from pathlib import Path
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from gui.performance_window import PerformanceWindow
from gui.processes_window import ProcessesWindow
from gui.terminal_gui import TerminalGUI
from gui.channel_info_app import ChannelInfoApp

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x300")
        self.root.minsize(400, 300)
        self.root.set_theme("arc")

        self.performance_window = None
        self.processes_window = None
        
        
        self.file_system_window = None  # Добавьте эту строку


        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        button1 = tk.Button(container, text="Производительность ОС", command=self.show_performance)
        button2 = tk.Button(container, text="Просмотр процессов", command=self.show_processes)
        button3 = tk.Button(container, text="Встроенный терминал", command=self.open_terminal)
        button4 = tk.Button(container, text="Информация о каналах", command=self.show_channel_info)

        mainmenu = tk.Menu(self.root)
        self.root.config(menu=mainmenu)

        utilities_menu = tk.Menu(mainmenu, tearoff=0)
        utilities_menu.add_command(label="Открыть файловый менеджер", command=self.open_file_manager)
       
       
        utilities_menu.add_command(label="Открыть системный менеджер", command=self.open_system_manager)
       
       
        utilities_menu.add_command(label="Выполнить поиск", command=self.execute_search)
        utilities_menu.add_command(label="О приложении", command=self.show_about)
        utilities_menu.add_separator()

        mainmenu.add_cascade(label='Утилиты', menu=utilities_menu)
        mainmenu.add_command(label='Справка', command=self.show_help)
        mainmenu.add_command(label='Выход', command=self.on_exit)

        button1.pack(pady=10, fill="both", expand=True)
        button2.pack(pady=10, fill="both", expand=True)
        button3.pack(pady=10, fill="both", expand=True)
        button4.pack(pady=10, fill="both", expand=True)





    def open_system_manager(self):
        if self.file_system_window:
            self.file_system_window.destroy()

        # Создадим новое окно для отображения файловой системы
        self.file_system_window = tk.Toplevel(self.root)
        self.file_system_window.title("Файловый Менеджер")
        self.file_system_window.geometry("600x400")

        # Treeview для отображения файловой системы
        self.file_system_tree = ttk.Treeview(self.file_system_window)
        self.file_system_tree.pack(side="left", fill="both", expand=True)
        self.file_system_tree.heading("#0", text="Файловая Система", anchor="w")
        self.file_system_tree.bind("<Double-1>", self.on_file_system_tree_double_click)
        self.file_system_tree.bind("<ButtonRelease-1>", self.on_file_system_tree_click)

        # Полоса прокрутки для Treeview
        tree_scroll = ttk.Scrollbar(self.file_system_window, orient="vertical", command=self.file_system_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.file_system_tree.configure(yscrollcommand=tree_scroll.set)

        # Получим корневой каталог в зависимости от операционной системы
        root_dir = Path("C:\\") if platform.system() == "Windows" else Path("/")
        # Вставим корневой каталог в Treeview
        self.file_system_tree.insert("", "end", text=str(root_dir), open=True)

        # Заполним Treeview содержимым корневого каталога
        self.populate_file_system_tree(root_dir, "")

    def populate_file_system_tree(self, directory, parent_item=""):
        try:
            for item in directory.iterdir():
                is_directory = item.is_dir()
                if is_directory:
                    # Если элемент является директорией, рекурсивно заполним ее содержимым
                    item_id = self.file_system_tree.insert(parent_item, "end", text=item.stem, open=False)
                    self.populate_file_system_tree(item, item_id)
                else:
                    # Если элемент - файл, добавим его в дерево с указанием расширения
                    self.file_system_tree.insert(parent_item, "end", text=f"{item.stem}.{item.suffix}")
    
                    # Предотвратим дальнейший переход вглубь
                    self.file_system_tree.insert(parent_item, "end", text="--- Дальнейший переход невозможен ---", open=False)
    
        except Exception as e:
            print(f"Ошибка при заполнении каталога {directory}: {e}")

    def on_file_system_tree_double_click(self, event):
        selected_item = self.file_system_tree.selection()
        if selected_item:
            item_path = Path(self.file_system_tree.item(selected_item)["text"])
            if item_path.is_dir():
                self.populate_file_system_tree(item_path, selected_item)

    def on_file_system_tree_click(self, event):
        selected_item = self.file_system_tree.selection()
        if selected_item:
            print(f"Выбран элемент: {self.file_system_tree.item(selected_item)['text']}")






    def show_performance(self):
        self.root.withdraw()
        self.performance_window = PerformanceWindow(self.root, self.show_main_menu)

    def show_processes(self):
        self.root.withdraw()
        self.processes_window = ProcessesWindow(self.root, self.show_main_menu)

    def open_terminal(self):
        self.root.withdraw()
        root = tk.Tk()
        terminal_gui = TerminalGUI(root, self.show_main_menu)
        root.mainloop()

    def show_channel_info(self):
        root = tk.Tk()
        channel_info_app = ChannelInfoApp(root)
        root.mainloop()

    def open_file_manager(self):
        messagebox.showinfo("Утилиты", "Открыть файловый менеджер")

    def execute_search(self):
        messagebox.showinfo("Утилиты", "Выполнить поиск")

    def show_help(self):
        messagebox.showinfo("Справка", "Создатель: Лутаев Даниил Олегович\nГруппа: ИВТ26-у\nВерсия приложения: 1.0")

    def show_about(self):
        messagebox.showinfo("О приложении", "производительность ос:\nотображает информацию о загрузке процессора, использовании виртуальной памяти, доступной и общей оперативной памяти. обновляет данные в реальном времени.\n\nпросмотр процессов:\nпозволяет просматривать список активных процессов. дает возможность получить дополнительные сведения о выбранном процессе при двойном щелчке мыши. \n\nвстроенный терминал:\nпредоставляет интерфейс для выполнения команд в терминале. выводит результат выполнения команды в текстовое поле.\n\nинформация о каналах:\nотображает информацию о сетевых соединениях для каждого процесса.\n\nутилиты:\nоткрыть файловый менеджер: открывает файловый менеджер (проводник) на операционной системе (поддерживается как на windows, так и на linux).\nвыполнить поиск: открывает новое окно приложения, позволяя выполнить поиск по отрывку текста в файлах, отображает результаты с путями к найденным файлам.\nсправка: выводит информацию о приложении, включая создателя, группу и версию.\n\nвыход:\nзавершает выполнение приложения.")

    def show_main_menu(self):
        if self.performance_window:
            self.performance_window.destroy()
            self.performance_window = None
        if self.processes_window:
            self.processes_window.destroy()
            self.processes_window = None
        self.root.deiconify()

    def on_exit(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из приложения?"):
            self.root.destroy()
            
    def open_file_manager(self):
        if platform.system() == "Windows":
            subprocess.run(["explorer"])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", "."])
        else:
            messagebox.showinfo("Ошибка", "Не удалось определить операционную систему.")

    def execute_search(self):
        # Открываем диалоговое окно выбора директории
        directory = filedialog.askdirectory(title="Выберите директорию для поиска")

        # Если пользователь выбрал директорию, выполняем поиск
        if directory:
            # Получает ввод от пользователя (отрывок для поиска)
            search_query = simpledialog.askstring("Поиск", "Введите отрывок для поиска:")
            if search_query is not None:
                # Ищет все файлы в выбранной директории, содержащие отрывок в имени
                results = self.search_files(directory, search_query)

                # Выводит результаты в новом окне
                self.show_search_results(results)

    def search_files(self, directory, search_query):
        # Ищет все файлы в выбранной директории, содержащие отрывок в имени
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if search_query.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    results.append((file, file_path))

        return results

    def show_search_results(self, results):
        # Выводит результаты в новом окне
        if results:
            result_text = "Результаты поиска:\n\n"
            for file, file_path in results:
                result_text += f"{file} - {file_path}\n"
            messagebox.showinfo("Поиск завершен", result_text)
        else:
            messagebox.showinfo("Поиск завершен", "Ничего не найдено.")