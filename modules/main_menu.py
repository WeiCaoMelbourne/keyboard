
import tkinter as tk
# Menu
# L = tk.Label(root, text ="Right-click to display menu", width = 40, height = 20)
# L.pack()

def quit_callback():
    # global running
    # running = False
    print("quit")

def config_menu(root):
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="读取")
    filemenu.add_command(label="保存")
    filemenu.add_separator()
    filemenu.add_command(label="结束游戏", command=quit_callback)
    menubar.add_cascade(label="文件", menu=filemenu)
    root.config(menu=menubar)