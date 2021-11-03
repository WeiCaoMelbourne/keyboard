import tkinter as tk
from tkinter.constants import BOTH, RAISED, SUNKEN
import json

class StartMainmenu():
    def __init__(self, parent, **kwargs):
        with open('data/config.json', 'rb') as f:
            config = json.load(f)

        WIDTH = 200
        HEIGHT = 170

        self.parent = parent
        self.state = kwargs['state']
        self.root = tk.Toplevel(parent)

        # messagebox.showinfo(title="Hello", message="What is it")
        # win_pos = window_pos()
        # print(win_pos)
        # print(win_pos[0] + SCREEN_WIDTH / 2, win_pos[1] + SCREEN_WIDTH / 2)
        # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, 200, 0)
        # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, win_pos[1] + SCREEN_HEIGHT // 2, 0)

        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.grab_set_global()
        
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{kwargs['x']}+{kwargs['y']}")

        titlebar = tk.Label(self.root, text=f"{config['title']}", anchor="center")
        titlebar.pack(fill=tk.X, padx=15, pady=5)

        bt1 = tk.Button(self.root, text='开始新游戏')
        bt1.pack(fill=tk.X, padx=20, ipady=2)
        bt2 = tk.Button(self.root, text='读取保存进度')
        bt2.pack(fill=tk.X, padx=20, ipady=2)
        bt3 = tk.Button(self.root, text='环境设定')
        bt3.pack(fill=tk.X, padx=20, ipady=2)
        okBtn = tk.Button(self.root, text='结束游戏', command=self.ok)
        okBtn.pack(fill=tk.X, padx=20, ipady=2)

        parent.wait_window(self.root)

    def ok(self):
        self.state['starting'] = False
        self.root.destroy()
    