# main.py
import os
from gui.app import App
from ttkthemes import ThemedTk

if __name__ == "__main__":
    if os.geteuid() != 0:
        # Если не является, запускаем программу с sudo
        os.system("sudo python3 main.py")
    else:
        # Если уже root, создаем ThemedTk и запускаем программу
        root = ThemedTk(theme="arc")
        app = App(root)
        root.mainloop()