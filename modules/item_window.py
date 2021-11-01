from PIL import Image, ImageTk
import tkinter as tk
from tkinter.constants import BOTH, RAISED, SUNKEN
from tkinter import ttk
import json

class ItemWindow():
    def __init__(self, parent, **kwargs):
        with open('data/troop-categories.json', 'rb') as f:
            all_troops = json.load(f)

        WIDTH = 320
        HEIGHT = 330

        ROW1_X = 10
        COL1_Y = 10
        COL2_Y = COL1_Y + 45
        
        self.parent = parent
        self.root = tk.Toplevel(parent.root)
        
        # make it modal
        # self.root.grab_set_global()

        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{kwargs['x']}+{kwargs['y']}")

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        item = kwargs['item']
        all_items = kwargs['all_items']
        
        item_img = tk.PhotoImage(file=f"resource/items/{item}.png")
        img_label = tk.Label(self.root, image=item_img, relief=SUNKEN)
        img_label.image = item_img
        img_label.place(x=ROW1_X, y=COL1_Y)

        name_label = tk.Label(self.root, text=f"{item}")
        name_label.place(x=ROW1_X+50, y=COL1_Y)

        lv_label = tk.Label(self.root, text=f"Lv {all_items[item]['lv']}")
        lv_label.place(x=ROW1_X+50, y=COL1_Y+18)

        exp_label = tk.Label(self.root, text=f"Exp")
        exp_label.place(x=ROW1_X+85, y=COL1_Y+18)

        style = ttk.Style(self.root)
        style_name = f"{item}.LabeledProgressbar"
        style.configure(style_name, text=f"{all_items[item]['exp']}/100")
        exp = ttk.Progressbar(self.root, length=80, style=style_name, maximum=100)
        exp['value'] = all_items[item]['exp']
        exp.place(x=ROW1_X+115, y=COL1_Y+18)

        labelframe1 = tk.LabelFrame(self.root, text="", width=70, height=55)
        labelframe1.place(x=ROW1_X, y=COL2_Y+8)
        category_label = tk.Label(self.root, text=f"属性   {all_items[item]['category']}")
        category_label.place(x=ROW1_X+5, y=COL2_Y+8+5)
        price_label = tk.Label(self.root, text=f"价格   {all_items[item]['price']}")
        price_label.place(x=ROW1_X+5, y=COL2_Y+8+25)

        labelframe2 = tk.LabelFrame(self.root, text="效果", width=120, height=63)
        labelframe2.place(x=ROW1_X+75, y=COL2_Y)
        for index, effect in enumerate(all_items[item]['effects']):
            tk.Label(self.root, text=f"{effect}").place(x=ROW1_X+80+5, y=COL2_Y+8+5+index*20)

        brief_label = tk.Message(self.root, text=f"{all_items[item]['简介']}", relief=SUNKEN, width=190, bg="#e5e5e5")
        brief_label.place(x=ROW1_X, y=COL2_Y+75)

        labelframe3 = tk.LabelFrame(self.root, text="可装备的部队", width=90, height=280)
        labelframe3.place(x=ROW1_X+205, y=COL1_Y-8)
        for index, troop in enumerate(all_troops['selectable-catetories']):
            if troop in all_items[item]['equipable']:
                text_color = "black"
            else:
                text_color = "#adb5bd"
            tk.Label(self.root, fg=f"{text_color}", text=f"{troop}").place(x=ROW1_X+205+10, y=COL1_Y+8+index*17)
        
        okBtn = tk.Button(self.root, text='确定', command=self.ok, width=8)
        # self.CloseBtn.place(x=WIDTH/2-70, y=HEIGHT-50)
        okBtn.place(x=WIDTH-80, y=HEIGHT-40)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        self.root.config(cursor="fleur")

    def stop_move(self, event):
        self.x = None
        self.y = None
        self.root.config(cursor="arrow")

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def ok(self):
        self.root.destroy() 
        self.parent.item_win = None