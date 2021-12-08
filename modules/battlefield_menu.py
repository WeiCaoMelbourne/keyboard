import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, RAISED, SUNKEN
from PIL import Image, ImageTk
from .constant import *

class BattlefieldMenu():
    def __init__(self, parent, instance, **kwargs):
        WIDTH = 100
        HEIGHT = 144

        self.parent = parent
        self.choice = None

        self.root = tk.Toplevel(parent)

        self.root.bind('<Button-3>', self.rightclicked)

        # self.icon1 = tk.PhotoImage(file='resource/mark/Cmdicon_100.bmp')
        # self.icon1 = tk.PhotoImage(file='resource/icon/exit.png')
        # self.icon1 = ImageTk.PhotoImage(file='resource/mark/Cmdicon_100.bmp')

        # messagebox.showinfo(title="Hello", message="What is it")
        # win_pos = window_pos()
        # print(win_pos)
        # print(win_pos[0] + SCREEN_WIDTH / 2, win_pos[1] + SCREEN_WIDTH / 2)
        # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, 200, 0)
        # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, win_pos[1] + SCREEN_HEIGHT // 2, 0)

        self.root.geometry(f"{WIDTH}x{HEIGHT}+{kwargs['x']}+{kwargs['y']}")
        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.grab_set_global()
        

        # bt1 = tk.Button(self.root, text='攻击', command=self.new_game)
        # bt1.image = self.icon1
        # bt1.pack(fill=tk.X, padx=20, ipady=2)
        # sub_frame2 = tk.Frame(self.root, height=100, relief=RAISED, bd=2, background='red')
        # sub_frame2.pack(fill=tk.X, pady=5, padx=5)
        # item_img3 = tk.PhotoImage(file="resource/mark/Cmdicon_100.png")
        # img_label = tk.Label(sub_frame2, image=item_img3)
        # # img_label.image = item_img
        # img_label.pack(side=tk.LEFT)
        # label_area = tk.Label(sub_frame2, text="攻击范围", width=12)
        # label_area.pack(side=tk.LEFT)
        

        # sub_frame3 = tk.Frame(self.root, height=100, relief=RAISED)
        # sub_frame3.pack(fill=tk.X, pady=5, padx=5)

        # item_img = tk.PhotoImage(file="resource/mark/Cmdicon_100.png")
        # img_label2 = tk.Label(sub_frame3, image=item_img)
        # # img_label.image = item_img
        # img_label2.pack(side=tk.LEFT)
        # label_area2 = tk.Label(sub_frame3, text="攻击范围2", width=12)
        # label_area2.pack(side=tk.LEFT)

        # item_img = tk.PhotoImage(file="resource/mark/Cmdicon_100.png")
        # bt1 = tk.Button(self.root, text='攻击', image=item_img, compound=tk.LEFT, 
        #     padx=20, command=self.new_game)
        # bt1.pack(fill=tk.X, padx=20, ipady=2)
        item_img = tk.PhotoImage(file="resource/mark/Cmdicon_100.png")
        bt1 = tk.Button(self.root, text='攻击', image=item_img, compound=tk.LEFT, height=14,
            padx=20, command=self.new_game)
        bt1.pack(fill=tk.X, ipady=2)

        item_img2 = tk.PhotoImage(file="resource/mark/Cmdicon_101.png")
        bt2 = tk.Button(self.root, text='策略', image=item_img2, compound=tk.LEFT, height=14,
            padx=20, command=self.mp)
        if instance.magic_powers == None:
            bt2['state'] = tk.DISABLED
        bt2.pack(fill=tk.X, ipady=2)

        item_img3 = tk.PhotoImage(file="resource/mark/Cmdicon_102.png")
        bt3 = tk.Button(self.root, text='道具', image=item_img3, compound=tk.LEFT, height=14,
            padx=20, command=self.new_game)
        bt3.pack(fill=tk.X, ipady=2)

        item_img4 = tk.PhotoImage(file="resource/mark/Cmdicon_103.png")
        bt4 = tk.Button(self.root, text='待命', image=item_img4, compound=tk.LEFT, height=14,
            padx=20, command=self.ok)
        bt4.pack(fill=tk.X, ipady=2)

        item_img5 = tk.PhotoImage(file="resource/mark/Cmdicon_104.png")
        okBtn = tk.Button(self.root, text='取消', image=item_img5, compound=tk.LEFT, height=14,
            padx=20, command=self.cancel)
        okBtn.pack(fill=tk.X, ipady=2, pady=4)
        
        parent.wait_window(self.root)

    def rightclicked(self, event):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "quit"

    def ok(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "待命"

    def cancel(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "quit"

    def mp(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "策略"

    def new_game(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "new"
    
class MPSelector():
    def __init__(self, parent, instance, **kwargs):
        WIDTH = 210
        HEIGHT = 245

        self.parent = parent
        self.choice = None

        self.root = tk.Toplevel(parent)
        self.root.bind('<Button-3>', self.rightclicked)

        # self.icon1 = tk.PhotoImage(file='resource/mark/Cmdicon_100.bmp')
        # self.icon1 = tk.PhotoImage(file='resource/icon/exit.png')
        # self.icon1 = ImageTk.PhotoImage(file='resource/mark/Cmdicon_100.bmp')

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

        # bt1 = tk.Button(self.root, text='攻击', command=self.new_game)
        # bt1.image = self.icon1
        # bt1.pack(fill=tk.X, padx=20, ipady=2)
        sub_frame2 = tk.Frame(self.root, relief=RAISED)
        sub_frame2.pack(fill=tk.X, pady=2, padx=5)
        # item_img3 = tk.PhotoImage(file="resource/mark/Cmdicon_100.png")
        # img_label = tk.Label(sub_frame2, image=item_img3)
        # # img_label.image = item_img
        # img_label.pack(side=tk.LEFT)
        label_area = tk.Label(sub_frame2, text=f"{instance.name}", width=4)
        label_area.pack(side=tk.LEFT, padx=4)
        label_area = tk.Label(sub_frame2, text="MP", width=4)
        label_area.pack(side=tk.LEFT, padx=2)
        
        style = ttk.Style(self.root)
        style.layout("MPProgressbar",
                [('MPProgressbar.trough',
                {'children': [('MPProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("MPProgressbar.label",   # label inside the bar
                                {"sticky": "w"})],
                'sticky': 'nswe'})])
        style.configure("MPProgressbar", background=MP_BAR_COLOR)
        style.configure("MPProgressbar", text=f"{instance.MP}/{instance.full_MP}")
        mp_bar = ttk.Progressbar(sub_frame2, style='MPProgressbar', maximum=100)
        mp_bar['value'] = 50
        mp_bar.pack(side=tk.LEFT)
    
        # list view of MP
        style.theme_use("default")
        style.map("Treeview", background=[('disabled', 'SystemButtonFace'), ('selected', 'SystemHighlight')])
        # Using .layout(), you can retrieve the layout specifications of each style
        # print(style.layout("Treeview.Item"))
        # If you comment "Treeitem.focus" out when overwriting the layout, the focus drawing behavior (and the dashed line) will disappear
        style.layout("Treeview.Item",
            [(
                'Treeitem.padding', 
                {
                    'sticky': 'nswe', 
                    'children': [
                        ('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                        ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                        #('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [('Treeitem.text', {'side': 'left', 'sticky': ''}), ]})
                        ],
                }
            )]
            )
        columns = ('#1', '#2')
        style.configure('Treeview.Item', indicatorsize=-4)
        self.mptree = ttk.Treeview(self.root, columns=columns, height=8)
        # self.mptree = ttk.Treeview(frame5, columns=columns, height=13, padding=[-15,0,0,0])
        self.mptree.tag_configure('odd', background='gainsboro')
        self.mptree.heading('#0', text='')
        self.mptree.heading('#1', text='策略名')
        self.mptree.heading('#2', text='MP')
        self.mptree.column("#0", width=20, stretch=False)
        self.mptree.column("#1", width=90, stretch=False)
        self.mptree.column("#2", width=50, stretch=False)

        self.mptree.bind('<Button-1>', self.treeview_mousedown)
        self.mptree.bind("<ButtonPress-1>", self.treeview_clicked)
        self.mptree.bind("<Motion>", lambda e: "break")   # Do not change cursor when it moves to separator
        
        sb = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        sb.config(command=self.mptree.yview)
        self.mptree.config(yscrollcommand=sb.set)
        
        values_list = [(key, value) for key, value in instance.magic_powers.items()]
        for index, values in enumerate(values_list):
            mp_img = ImageTk.PhotoImage(file=f'resource/mp/{values[0]}.bmp')
            # use setattr to make this img variable last
            setattr(self, 'mp_img' + str(index), mp_img)
            if index % 2 == 0:
                self.mptree.insert('', tk.END, values=values, image=mp_img)
            else:
                self.mptree.insert('', tk.END, values=values, image=mp_img, tags=('odd',))
        self.mptree.pack(padx=5)
        
        item_img5 = tk.PhotoImage(file="resource/mark/Cmdicon_104.png")
        okBtn = tk.Button(self.root, text='取消', image=item_img5, compound=tk.LEFT, height=14,
            padx=10, command=self.ok)
        okBtn.pack(side=tk.BOTTOM, ipady=2, pady=2, anchor=tk.SE)
        
        parent.wait_window(self.root)

    def rightclicked(self, event):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "quit"

    def ok(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "quit"

    def mp(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "策略"

    def new_game(self):
        # self.state['starting'] = False
        self.root.destroy()
        self.choice = "new"

    # Do not allow column resize
    def treeview_mousedown(self, event):
        if self.mptree.identify_region(event.x, event.y) == "separator":
            # must return "break", otherwise it won't work
            return "break"

    def treeview_clicked(self, event):
        item = self.mptree.identify('item', event.x, event.y)
        char_info = self.mptree.item(item, "value")
        print(char_info)
        if not char_info:
            #In this case, it it clicking header to sort, so do not display window
            return


        # # print("you clicked on", char_info)
        # if self.childWin:
        #     self.childWin.root.lift()
        #     print("Already exists")
        #     pass
        # else:
        #     self.childWin = CharacterWindow(parent=self, 
        #         x=self.root.winfo_x() + self.root.winfo_width(), y=self.root.winfo_y(), brief=char_info)
        #     self.childWin.root.lift()
        #     self.childWin.root.attributes('-topmost',True)
        #     self.childWin.root.after_idle(self.childWin.root.attributes, '-topmost', False)