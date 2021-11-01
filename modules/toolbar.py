import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, RAISED, SUNKEN
from PIL import Image, ImageTk
from .win_pos import window_pos
from .tv_funcs import treeview_sort_column
from .msg_box import MsgBoxWindow
from .modal_window import ModalWindow
import json

# Menu
# L = tk.Label(root, text ="Right-click to display menu", width = 40, height = 20)
# L.pack()

class SetupWindow():
    def __init__(self, title='Mess', msg='', b1='OK', b2='', b3='', b4=''):
        WIDTH = 300
        HEIGHT = 420

        # Creating Dialogue for messagebox
        self.root = tk.Toplevel()
        # self.root.grab_set()
        self.root.grab_set_global()

        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)

        self.root.config(border=3, relief=RAISED)

        win_pos = window_pos()
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{win_pos[0]+200}+{win_pos[1]+200}")

        self.titlebar = tk.Label(self.root, text="环境设定")
        # self.titlebar.place(x=5, y=5)
        self.titlebar.pack(fill=tk.BOTH, padx=5, pady=5)

        # button_frame = tk.Frame(self.root, height=40)
        # button_frame.pack(side=tk.TOP, fill=tk.X)
        labelframe1 = tk.LabelFrame(self.root, text="讯息显示速度", width=WIDTH-40, height=90)
        # labelframe1.place(x=20, y=HEIGHT-250)
        labelframe1.pack(expand=1, fill=tk.BOTH, padx=20, pady=10)

        self.v = tk.StringVar()
        r1 = tk.Radiobutton(labelframe1, text="慢", variable=self.v, value="slow")
        r1.pack(side=tk.LEFT, padx=20)
        r2 = tk.Radiobutton(labelframe1, text="普通", variable=self.v, value="normal")
        r2.pack(side=tk.LEFT, padx=20)
        r3 = tk.Radiobutton(labelframe1, text="快", variable=self.v, value="fast")
        r3.pack(side=tk.LEFT, padx=20)

        labelframe2 = tk.LabelFrame(self.root, text="武将移动速度", width=WIDTH-40, height=90)
        # self.labelframe.place(x=20, y=HEIGHT-150)
        labelframe2.pack(expand=1, fill=tk.BOTH, padx=20, pady=0)

        # Creating Close Button
        okBtn = tk.Button(self.root, text='确定', command=lambda:self.ok(), width=8)
        # self.CloseBtn.place(x=WIDTH/2-70, y=HEIGHT-50)
        okBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10)

        cancleBtn = tk.Button(self.root, text='取消', command=lambda:self.cancel(), width=8)
        # self.CloseBtn.place(x=WIDTH/2+20, y=HEIGHT-50)
        cancleBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10)

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

class ToolsWindow():
    def __init__(self, title='Mess', msg='', b1='OK', b2='', b3='', b4=''):
        WIDTH = 600
        HEIGHT = 400

        # Creating Dialogue for messagebox
        self.root = tk.Toplevel()
        self.root.grab_set_global()
        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)

        win_pos = window_pos()
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{win_pos[0]+100}+{win_pos[1]+100}")
        self.titlebar = tk.Label(self.root, text="道具一览")
        self.titlebar.pack(fill=tk.BOTH, padx=5, pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True)

        # create frames
        frame1 = ttk.Frame(notebook, width=WIDTH-30, height=HEIGHT-320)
        frame2 = ttk.Frame(notebook, width=WIDTH-30, height=HEIGHT-320)
        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)

        style = ttk.Style()
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
        
        columns = ('#1', '#2', '#3')
        tree = ttk.Treeview(frame1, columns=columns, height=13)
        tree.tag_configure('odd', background='gainsboro')
        tree.heading('#0', text='Pic')
        tree.heading('#1', text='名称')
        tree.heading('#2', text='持有者')
        tree.heading('#3', text='属性', command=lambda:treeview_sort_column(tree, '#3', False))

        sb = tk.Scrollbar(frame1, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        sb.config(command=tree.yview)
        tree.config(yscrollcommand=sb.set)
        
        # self.spear_img = tk.PhotoImage(file="resource/icon/spear.png")
        img = Image.open('resource/icon/spear.png')
        img = img.resize((25, 25), Image.ANTIALIAS)
        self.spear_img = ImageTk.PhotoImage(img)

        # values_list = [("曹操", "群雄", 14), ] * 25
        values_list = [("布衣", "仓库", "衣服"), ("短剑", "仓库", "剑"), ("短枪", "仓库", "枪")]
        # tree.insert('', tk.END, values=("布衣", "仓库", "衣服"), image=self.spear_img)
        for index, values in enumerate(values_list):
            if index % 2 == 0:
                tree.insert('', tk.END, values=values)
            else:
                tree.insert('', tk.END, values=values, image=self.spear_img, tags=('odd',))
        tree.pack()

        # treeview 2
        columns = ('#1', '#2', '#3')
        tree2 = ttk.Treeview(frame2, columns=columns, show='headings', height=13)
        tree2.tag_configure('odd', background='gainsboro')
        tree2.heading('#1', text='名称')
        tree2.heading('#2', text='库存')
        tree2.heading('#3', text='功效', command=lambda:treeview_sort_column(tree, '#3', False))

        sb2 = tk.Scrollbar(frame2, orient=tk.VERTICAL)
        sb2.pack(side=tk.RIGHT, fill=tk.Y)

        sb2.config(command=tree.yview)
        tree2.config(yscrollcommand=sb.set)
        
        # values_list = [("曹操", "群雄", 14), ] * 25
        values_list2 = [("米", 14, "恢复HP"), ("豆", 10, "恢复HP")]
        for index, values in enumerate(values_list2):
            if index % 2 == 0:
                tree2.insert('', tk.END, values=values)
            else:
                tree2.insert('', tk.END, values=values, tags=('odd',))
        tree2.pack()

        notebook.add(frame1, text='武器')
        notebook.add(frame2, text='道具')

        okBtn = tk.Button(self.root, text='确定', command=lambda:self.ok(), width=8)
        okBtn.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        self.root.wait_window()

    def ok(self):
        self.root.destroy() 
        self.choice = 'ok'   

class CharacterWindow():
    def __init__(self, parent, **kwargs):
        with open('data/items.json', 'rb') as f:
            all_items = json.load(f)
            # about_info = f.readlines()
            print(all_items)

        WIDTH = 400
        HEIGHT = 400
        LEFTFRAME_WIDTH = WIDTH/2-20
        MAINFRAME_HEIGHT = HEIGHT-90

        for key, value in kwargs.items():
            print("{} is {}".format(key,value))

        self.parent = parent
        self.root = tk.Toplevel(parent.root)
        # self.root.grab_set()
        # self.root.grab_set_global()

        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)
        self.root.config(border=3, relief=RAISED)
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{kwargs['x']}+{kwargs['y']}")

        titlebar = tk.Label(self.root, text="武将情报", anchor="w")
        # self.titlebar.place(x=5, y=5)
        titlebar.bind("<ButtonPress-1>", self.start_move)
        titlebar.bind("<ButtonRelease-1>", self.stop_move)
        titlebar.bind("<B1-Motion>", self.do_move)
        titlebar.pack(fill=tk.Y, padx=5, pady=5)

        main_frame = tk.Frame(self.root, height=MAINFRAME_HEIGHT, background="red")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH)

        left_frame = tk.Frame(main_frame, width=LEFTFRAME_WIDTH, height=MAINFRAME_HEIGHT, background="blue")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        # avator_file = ;
        lefttop_frame = tk.Frame(left_frame, width=WIDTH/2-20, background="yellow")
        lefttop_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=5)

        all_chars = {}
        with open('data/characters.json', 'rb') as f:
            all_chars = json.load(f)
            # about_info = f.readlines()
            print(all_chars)
        char_info = all_chars[kwargs['brief'][0]]
        print(char_info)
        img = Image.open(char_info['pic'])
        img = img.resize((70, 70), Image.ANTIALIAS)
        game_img = ImageTk.PhotoImage(img)
        icon_label = tk.Label(lefttop_frame, image=game_img)
        icon_label.image = game_img
        icon_label.grid(row=0, rowspan=2, column=0)

        name_label = tk.Label(lefttop_frame, text=kwargs['brief'][0])
        name_label.grid(row=0, rowspan=1, column=1)

        money_frame = tk.LabelFrame(lefttop_frame, text="现金", width=80, height=40)
        money_frame.grid(row=1, rowspan=1, column=1, padx=10)
        name_label = tk.Label(money_frame, text='2000')
        name_label.pack()

        troop_frame = tk.LabelFrame(left_frame, text="部队属性", height=70, width=150)
        troop_frame.pack(fill=tk.X, padx=5, pady=5)
        troop_label = tk.Label(troop_frame, text='群雄')
        troop_label.grid(row=0, rowspan=1, column=0, columnspan=1)
        troop_label2 = tk.Label(troop_frame, text='Lv 14')
        troop_label2.grid(row=1, rowspan=1, column=0, columnspan=1)
        troop_label3 = tk.Label(troop_frame, text='Exp')
        troop_label3.grid(row=1, rowspan=1, column=1, columnspan=1, sticky=tk.E, padx=2)
        # troop_frame.grid_columnconfigure(1, minsize=50)

        style = ttk.Style(self.root)
        style.layout("LabeledProgressbar",
                [('LabeledProgressbar.trough',
                {'children': [('LabeledProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("LabeledProgressbar.label",   # label inside the bar
                                {"sticky": "w"})],
                'sticky': 'nswe'})])
        style.configure("LabeledProgressbar", background='#9d4edd')
        style.configure("LabeledProgressbar", text="40/100")
        exp = ttk.Progressbar(troop_frame, length=80, style='LabeledProgressbar', maximum=100)
        # exp = ttk.Progressbar(troop_frame, length=60, maximum=100)
        exp['value'] = 90
        exp.grid(row=1, rowspan=1, column=2, columnspan=1, padx=3)

        status_frame = tk.LabelFrame(left_frame, text="状态", height=130, width=130)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        hp_label = tk.Label(status_frame, text='HP')
        hp_label.grid(row=0, column=0)
        style.layout("HPProgressbar",
                [('HPProgressbar.trough',
                {'children': [('HPProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("HPProgressbar.label",   # label inside the bar
                                {"sticky": "w"})],
                'sticky': 'nswe'})])
        style.configure("HPProgressbar", background='#83c5be')
        style.configure("HPProgressbar", text="30/100")
        hp_bar = ttk.Progressbar(status_frame, style='HPProgressbar', maximum=100)
        hp_bar['value'] = 40
        hp_bar.grid(row=0, column=1, columnspan=3, padx=3)
        mp_label = tk.Label(status_frame, text='MP')
        mp_label.grid(row=1, column=0)
        style.layout("MPProgressbar",
                [('MPProgressbar.trough',
                {'children': [('MPProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("MPProgressbar.label",   # label inside the bar
                                {"sticky": "w"})],
                'sticky': 'nswe'})])
        style.configure("MPProgressbar", background='#ccd5ae')
        style.configure("MPProgressbar", text="20/100")
        mp_bar = ttk.Progressbar(status_frame, style='MPProgressbar', maximum=100)
        mp_bar['value'] = 50
        mp_bar.grid(row=1, column=1, columnspan=3, padx=3)

        # status_label = tk.Message(status_frame, text='正常', relief=SUNKEN, width=LEFTFRAME_WIDTH)
        # status_label.grid(row=2, rowspan=2, column=0, columnspan=4)
        # status_label.pack(fill=BOTH)
        status_label = tk.Label(status_frame, text=char_info['status'], relief=SUNKEN, width=18, height=4, anchor="nw")
        status_label.grid(row=2, rowspan=2, column=0, columnspan=4, padx=5, pady=10)
        
        right_frame = tk.Frame(main_frame, width=LEFTFRAME_WIDTH, height=MAINFRAME_HEIGHT, background="green")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)

        TAB_HEIGHT = MAINFRAME_HEIGHT - 30
        notebook = ttk.Notebook(right_frame)
        notebook.pack(expand=True)
        frame1 = ttk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame1.pack(fill=tk.BOTH, expand=True)
        basics_frame = ttk.LabelFrame(frame1, text="部队属性", height=70, width=150)
        basics_frame.pack(fill=tk.X, padx=10, pady=5)
        # basics_frame.columnconfigure(tuple(range(2)), weight=1)
        # basics_frame.columnconfigure(0, weight=1)
        attack_label = ttk.Label(basics_frame, text=f"武力 {char_info['武力']}", width=12)
        attack_label.grid(row=0, column=0, sticky="news", padx=5, pady=1)
        agile_label = ttk.Label(basics_frame, text=f"武力 {char_info['敏捷']}", width=12)
        agile_label.grid(row=0, column=1, sticky="news", padx=5, pady=1)
        mind_label = ttk.Label(basics_frame, text=f"武力 {char_info['智力']}", width=12)
        mind_label.grid(row=1, column=0, sticky="news", padx=5, pady=1)
        luck_label = ttk.Label(basics_frame, text=f"武力 {char_info['运气']}", width=12)
        luck_label.grid(row=1, column=1, sticky="news", padx=5, pady=1)
        leadship_label = ttk.Label(basics_frame, text=f"武力 {char_info['统率']}", width=12)
        leadship_label.grid(row=3, column=0, sticky="news", padx=5, pady=1)
        
        # brief_label = tk.Label(frame1, text=f"{char_info['列传']}", relief=SUNKEN, wraplength=160, width=23, height=10, anchor="nw")
        brief_label = tk.Message(frame1, text=f"{char_info['列传']}", relief=SUNKEN, width=180, bg="#e5e5e5")
        brief_label.pack(padx=10, pady=5)

        total = ttk.Frame(frame1, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        total.pack(fill=tk.BOTH, expand=True)
        totalleft_label = ttk.Label(total, text=f"出阵数 15", width=10)
        totalleft_label.pack(side=tk.LEFT, padx=10, pady=5)
        totalright_label = ttk.Label(total, text=f"撤退数 0", width=10)
        totalright_label.pack(side=tk.RIGHT, padx=10, pady=5)

        notebook.add(frame1, text='武将列传')

        frame2 = ttk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame2.pack(fill=tk.BOTH, expand=True)
        notebook.add(frame2, text='部队特性')

        frame3 = ttk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame3.pack(fill=tk.BOTH, expand=True)
        attack_frame = ttk.LabelFrame(frame3, text="攻击力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.layout("AbilityProgressbar",
                [('AbilityProgressbar.trough',
                {'children': [('AbilityProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("AbilityProgressbar.label",   # label inside the bar
                                {"sticky": "e"})],
                'sticky': 'nswe'})])
        style.configure("AbilityProgressbar", background='#4895ef')
        style.configure("AbilityProgressbar", text="111")
        attack_bar = ttk.Progressbar(attack_frame, style='AbilityProgressbar', maximum=100)
        attack_bar['value'] = 40
        attack_bar.pack(pady=1)

        attack_frame = ttk.LabelFrame(frame3, text="精神力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("1.AbilityProgressbar", text="90")
        mind_bar = ttk.Progressbar(attack_frame, style='1.AbilityProgressbar', maximum=100)
        mind_bar['value'] = 50
        mind_bar.pack(pady=1)

        attack_frame = ttk.LabelFrame(frame3, text="防御力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("2.AbilityProgressbar", text="146")
        defense_bar = ttk.Progressbar(attack_frame, style='2.AbilityProgressbar', maximum=100)
        defense_bar['value'] = 60
        defense_bar.pack(pady=1)

        attack_frame = ttk.LabelFrame(frame3, text="爆发力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("4.AbilityProgressbar", text="83")
        bar4 = ttk.Progressbar(attack_frame, style='4.AbilityProgressbar', maximum=100)
        bar4['value'] = 70
        bar4.pack(pady=1)

        attack_frame = ttk.LabelFrame(frame3, text="士气", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("5.AbilityProgressbar", text="86")
        bar5 = ttk.Progressbar(attack_frame, style='5.AbilityProgressbar', maximum=100)
        bar5['value'] = 50
        bar5.pack(pady=1)
        notebook.add(frame3, text='能力')

        attack_frame = ttk.LabelFrame(frame3, text="移动力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        move_label = ttk.Label(attack_frame, text='6')
        move_label.pack(pady=1)
        notebook.add(frame3, text='能力')

        frame4 = ttk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame4.pack(fill=tk.BOTH, expand=True)
        weapen_frame = ttk.LabelFrame(frame4, text="武器", height=85)
        weapen_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(weapen_frame, all_items, char_info['武器'])
        # weapen_label = ttk.Label(weapen_frame, text=f"{char_info['武器']}", background='red', anchor='w')
        # weapen_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        # weapen_img = tk.PhotoImage(file=f"resource/items/{char_info['武器']}.png")
        # img_label = ttk.Label(weapen_frame, image=weapen_img, relief=SUNKEN)
        # img_label.image = weapen_img
        # img_label.grid(row=1, rowspan=2, column=0, padx=10, sticky=tk.W)
        # lv_label = ttk.Label(weapen_frame, text="Lv 10", background='red')
        # lv_label.grid(row=1, column=1, padx=5, sticky=tk.W)
        # exp_label = ttk.Label(weapen_frame, text="Exp 10/100", background='red')
        # exp_label.grid(row=2, column=1, padx=5, sticky=tk.W)
        # addon_label = ttk.Label(weapen_frame, text="攻击力", background='red', anchor='w')
        # addon_label.grid(row=3, column=0, padx=10, sticky=tk.W)

        armor_frame = ttk.LabelFrame(frame4, text="护具", height=85)
        armor_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(armor_frame, all_items, char_info['护具'])
        
        treasure_frame = ttk.LabelFrame(frame4, text="辅助", height=85)
        treasure_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(treasure_frame, all_items, char_info['辅助'])
        notebook.add(frame4, text='装备')

        frame5 = ttk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame5.pack(fill=tk.BOTH, expand=True)
        notebook.add(frame5, text='策略')

        okBtn = tk.Button(self.root, text='确定', command=lambda:self.ok(), width=8)
        # self.CloseBtn.place(x=WIDTH/2-70, y=HEIGHT-50)
        okBtn.pack(side=tk.BOTTOM, padx=10, pady=10)

        # cancleBtn = tk.Button(self.root, text='取消', command=lambda:self.cancel(), width=8)
        # # self.CloseBtn.place(x=WIDTH/2+20, y=HEIGHT-50)
        # cancleBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10)

        # self.root.wait_window()
        self.choice = None

    def item_display(self, weapen_frame, all_items, item):
        if item == None or item == '':
            itemname_label = ttk.Label(weapen_frame, text="无", background='red', anchor='w')
        else:
            itemname_label = ttk.Label(weapen_frame, text=f"{item}", background='red', anchor='w')
            
        itemname_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        if item == None or item == '':
            item_img = tk.PhotoImage(file=f"resource/items/blank.png")
        else:
            item_img = tk.PhotoImage(file=f"resource/items/{item}.png")
        img_label = ttk.Label(weapen_frame, image=item_img, relief=SUNKEN)
        img_label.image = item_img
        img_label.grid(row=1, rowspan=2, column=0, padx=10, sticky=tk.W)

        img_label.bind("<ButtonPress-1>", lambda event, item=item: self.item_clicked(event, item))
        # img_label.bind("<ButtonPress-1>", lambda:self.item_clicked(item, event, ))
        
        if not (item == None or item == ''):
            lv_label = ttk.Label(weapen_frame, text="Lv", background='red')
            lv_label.grid(row=1, column=1, padx=5, sticky=tk.W)
            lv2_label = ttk.Label(weapen_frame, text=f"{all_items[item]['lv']}", background='red')
            lv2_label.grid(row=1, column=2, sticky=tk.W)

            exp_label = ttk.Label(weapen_frame, text="Exp", background='red')
            exp_label.grid(row=2, column=1, padx=5, sticky=tk.W)
            style = ttk.Style(self.root)
            style_name = f"{item}.LabeledProgressbar"
            style.configure(style_name, text=f"{all_items[item]['exp']}/100")
            exp = ttk.Progressbar(weapen_frame, length=80, style=style_name, maximum=100)
            exp['value'] = all_items[item]['exp']
            exp.grid(row=2, column=2, sticky=tk.W)
        
        if not (item == None or item == ''):
            addon_label = ttk.Label(weapen_frame, text=f"{all_items[item]['main_effect']['main']}", background='red', anchor='w')
            addon_label.grid(row=3, column=0, padx=10, sticky=tk.W)

            addon2_label = ttk.Label(weapen_frame, text=f"{all_items[item]['main_effect']['effect']}", background='red', anchor='w')
            addon2_label.grid(row=3, column=1, padx=5, sticky=tk.W)

    def item_clicked(self, event, item):
        print(item)

    def ok(self):
        self.root.destroy() 
        self.parent.childWin = None
        # self.choice = 'ok' 

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

class CharactersWindow():
    def __init__(self, title='Mess', msg='', b1='OK', b2='', b3='', b4=''):
        WIDTH = 600
        HEIGHT = 400

        self.childWin = None

        # Creating Dialogue for messagebox
        self.root = tk.Toplevel()
        # self.root.grab_set()
        self.root.grab_set_global()

        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)

        self.root.config(border=3, relief=RAISED)

        win_pos = window_pos()
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{win_pos[0]+100}+{win_pos[1]+100}")

        
        self.titlebar = tk.Label(self.root, text="部队情报一览")
        # self.titlebar.place(x=5, y=5)
        self.titlebar.bind("<ButtonPress-1>", self.start_move)
        self.titlebar.bind("<ButtonRelease-1>", self.stop_move)
        self.titlebar.bind("<B1-Motion>", self.do_move)
        self.titlebar.pack(fill=tk.BOTH, padx=5, pady=5)

        box_frame = tk.Frame(self.root, height=30)
        box_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10)

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview", background=[('disabled', 'SystemButtonFace'), ('selected', 'SystemHighlight')])
        # tree.config(style="black.Treeview")
        # style.configure("Treeview", background="#383838", foreground="white")
        
        columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(box_frame, columns=columns, show='headings', height=15)
        self.tree.tag_configure('odd', background='gainsboro')
        # tree.tag_configure('even', background='lightgreen')
        self.tree.heading('#1', text='武将名')
        self.tree.heading('#2', text='部队属性')
        self.tree.heading('#3', text='Lv', command=lambda:self.treeview_sort_column(self.tree, '#3', False))
        # tree['selectmode'] = "extended"

        sb = tk.Scrollbar(box_frame, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        sb.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=sb.set)
        
        # values_list = [("曹操", "群雄", 14), ] * 25
        values_list = [("曹操", "群雄", 14), ("于禁", "弓兵", 10), ("郭嘉", "法师", 11)]
        for index, values in enumerate(values_list):
            if index % 2 == 0:
                self.tree.insert('', tk.END, values=values)
            else:
                self.tree.insert('', tk.END, values=values, tags=('odd',))
        # tree.tag_configure('oddrow', background='orange')
        self.tree.bind("<ButtonPress-1>", self.treeview_clicked)
        self.tree.pack()

        okBtn = tk.Button(self.root, text='确定', command=lambda:self.ok(), width=8)
        okBtn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.wait_window()

    def treeview_clicked(self, event):
        item = self.tree.identify('item', event.x, event.y)
        char_info = self.tree.item(item, "value")
        if not char_info:
            #In this case, it it clicking header to sort, so do not display window
            return

        print("you clicked on", char_info)
        if self.childWin:
            self.childWin.root.lift()
            print("Already exists")
            pass
        else:
            self.childWin = CharacterWindow(parent=self, 
                x=self.root.winfo_x() + self.root.winfo_width(), y=self.root.winfo_y(), brief=char_info)
            self.childWin.root.lift()
            self.childWin.root.attributes('-topmost',True)
            self.childWin.root.after_idle(self.childWin.root.attributes, '-topmost', False)
            # print(self.childWin.choice)
            # if self.childWin.choice == 'ok':
            #     self.childWin = None

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda:self.treeview_sort_column(tv, col, not reverse))
    
    def closed(self):
        self.root.destroy()
        self.choice = 'closed'

    def ok(self):
        self.root.destroy() 
        self.choice = 'ok'     

    def cancel(self):
        self.root.destroy() 
        self.choice = 'cancel'

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def exit(root):
    root.quit()

def save(root):
    print("save")

def setup(root):
    a = SetupWindow()
    # print(a.choice)

def characters(root):
    a = CharactersWindow()
    # print(a.choice)

def tools(root):
    a = ToolsWindow()
    # print(a.choice)

def about(root):
    a = MsgBoxWindow()
    # a = ModalWindow()
    # print(a.choice)

def config_toolbar(root):
    toolbar = tk.Frame(root, height=30)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    
    # Images must be declared as global, otherwise imega won't work
    global exit_img, save_img, setup_img, char_img, tool_img
    exit_img = tk.PhotoImage(file='resource/icon/exit.png')
    exit_button= tk.Button(toolbar, image=exit_img, command=lambda: exit(root=root), width=25, height=25)
    exit_button.pack(side=tk.LEFT)
    CreateToolTip(exit_button, "结束游戏")

    save_img = tk.PhotoImage(file='resource/icon/save.png')
    save_button= tk.Button(toolbar, image=save_img, command=lambda: save(root=root), width=25, height=25)
    save_button.pack(side=tk.LEFT)
    CreateToolTip(save_button, "保存游戏")

    setup_img = tk.PhotoImage(file='resource/icon/setup.png')
    setup_button= tk.Button(toolbar, image=setup_img, command=lambda: setup(root=root), width=25, height=25)
    setup_button.pack(side=tk.LEFT)
    CreateToolTip(setup_button, "设置")

    # char_img = tk.PhotoImage(file='resource/icon/characters.png')
    # char_button= tk.Button(toolbar, image=char_img, command=lambda: characters(root=root), width=25, height=25)
    # char_button.pack(side=tk.LEFT)
    # CreateToolTip(setup_button, "武将一览")

    toolbar2 = tk.Frame(toolbar)
    toolbar2.pack(side=tk.LEFT, padx=5)
    char_img = tk.PhotoImage(file='resource/icon/characters.png')
    char_button= tk.Button(toolbar2, image=char_img, command=lambda: characters(root=root), width=25, height=25)
    char_button.pack(side=tk.LEFT)
    CreateToolTip(setup_button, "武将一览")

    tool_img = tk.PhotoImage(file='resource/icon/tools.png')
    tool_button= tk.Button(toolbar2, image=tool_img, command=lambda: tools(root=root), width=25, height=25)
    tool_button.pack(side=tk.LEFT)
    CreateToolTip(tool_button, "持有道具一览")

    # about_img = tk.PhotoImage(file='resource/icon/about.png')
    global about_img
    img = Image.open('resource/icon/about.png')
    img = img.resize((25, 25), Image.ANTIALIAS)
    about_img = ImageTk.PhotoImage(img)
    about_button= tk.Button(toolbar2, image=about_img, command=lambda: about(root=root), width=25, height=25)
    about_button.pack(side=tk.LEFT)
    CreateToolTip(about_button, "关于")