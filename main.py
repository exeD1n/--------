# main.py
from gui.app import App
from ttkthemes import ThemedTk

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = App(root)
    root.mainloop()