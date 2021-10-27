import tkinter as tk
from PIL import Image, ImageTk
from .win_pos import window_pos
from tkinter.constants import BOTTOM, LEFT, RAISED
import json

class MsgBoxWindow():
    def __init__(self, title='Mess', msg='', b1='OK', b2='', b3='', b4=''):
        with open('data/about/about.json', 'rb') as f:
            about_info = json.load(f)
            # about_info = f.readlines()
            print(about_info)

        WIDTH = 300
        HEIGHT = 150

        # Creating Dialogue for messagebox
        self.root = tk.Toplevel()
        # self.root.grab_set()
        self.root.grab_set_global()
        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)
        win_pos = window_pos()
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{win_pos[0]+200}+{win_pos[1]+200}")
        
        info_frame = tk.Frame(self.root)
        info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # signup_canvas = tk.Canvas(self.root, height=HEIGHT, width=WIDTH)
        img = Image.open('resource/img/game_main.png')
        img = img.resize((70, 70), Image.ANTIALIAS)
        game_img = ImageTk.PhotoImage(img)
        icon_label = tk.Label(info_frame, image=game_img)
        icon_label.image = game_img
        icon_label.grid(row=0, rowspan=2, column=0)
        # icon_label.pack(side=LEFT)

        txt_label = tk.Label(info_frame, text=about_info['info'], font=("Arial", 10))
        txt_label.grid(row=0, rowspan=1, column=1, columnspan=2, padx=20)
        # txt_label.pack(side=LEFT, expand=True, padx=10)

        txt_label2 = tk.Label(info_frame, text=about_info['copyright'], font=("Arial", 10))
        txt_label2.grid(row=1, rowspan=1, column=1, columnspan=2, padx=20)
        # txt_label2.pack(side=BOTTOM, expand=True, padx=10)
        # icon_label.place(x=0, y=0)
        # img = Image.open('resource/img/game_30_30.png')
        # img = img.resize((200, 200), Image.ANTIALIAS)
        # im1 = ImageTk.PhotoImage(img)

        # # Add the image in the label widget
        # image1 = tk.Label(self.root, image=im1)
        # image1.image = im1
        # image1.place(x=0, y=0, relwidth=1)


        # Creating Close Button
        okBtn = tk.Button(self.root, text=' 确定 ', command=lambda:self.ok(), width=8)
        # self.CloseBtn.place(x=WIDTH/2-70, y=HEIGHT-50)
        okBtn.pack(side=tk.BOTTOM, padx=20, pady=10)

        self.root.wait_window()
    
    def closed(self):
        self.root.destroy()
        self.choice = 'closed'

    def ok(self):
        self.root.destroy() 
        self.choice = 'ok'     

    def cancel(self):
        self.root.destroy() 
        self.choice = 'cancel'