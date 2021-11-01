from PIL import Image, ImageTk
import tkinter as tk
from tkinter.constants import BOTH, RAISED, SUNKEN
from tkinter import ttk
import json

class CharacterWindow():
    def __init__(self, parent, **kwargs):
        with open('data/items.json', 'rb') as f:
            all_items = json.load(f)

        WIDTH = 400
        HEIGHT = 400
        LEFTFRAME_WIDTH = WIDTH/2-20
        MAINFRAME_HEIGHT = HEIGHT-90

        self.parent = parent
        self.item_win = None
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

        main_frame = tk.Frame(self.root, height=MAINFRAME_HEIGHT)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH)

        left_frame = tk.Frame(main_frame, width=LEFTFRAME_WIDTH, height=MAINFRAME_HEIGHT)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        # avator_file = ;
        lefttop_frame = tk.Frame(left_frame, width=WIDTH/2-20)
        lefttop_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=5)

        all_chars = {}
        with open('data/characters.json', 'rb') as f:
            all_chars = json.load(f)
            # about_info = f.readlines()

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
        frame1 = tk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame1.pack(fill=tk.BOTH, expand=True)
        basics_frame = tk.LabelFrame(frame1, text="部队属性", height=70, width=150)
        basics_frame.pack(fill=tk.X, padx=10, pady=5)
        # basics_frame.columnconfigure(tuple(range(2)), weight=1)
        # basics_frame.columnconfigure(0, weight=1)
        attack_label = tk.Label(basics_frame, text=f"武力 {char_info['武力']}", width=12)
        attack_label.grid(row=0, column=0, sticky="news", padx=5, pady=1)
        agile_label = tk.Label(basics_frame, text=f"武力 {char_info['敏捷']}", width=12)
        agile_label.grid(row=0, column=1, sticky="news", padx=5, pady=1)
        mind_label = tk.Label(basics_frame, text=f"武力 {char_info['智力']}", width=12)
        mind_label.grid(row=1, column=0, sticky="news", padx=5, pady=1)
        luck_label = tk.Label(basics_frame, text=f"武力 {char_info['运气']}", width=12)
        luck_label.grid(row=1, column=1, sticky="news", padx=5, pady=1)
        leadship_label = tk.Label(basics_frame, text=f"武力 {char_info['统率']}", width=12)
        leadship_label.grid(row=3, column=0, sticky="news", padx=5, pady=1)
        
        # brief_label = tk.Label(frame1, text=f"{char_info['列传']}", relief=SUNKEN, wraplength=160, width=23, height=10, anchor="nw")
        brief_label = tk.Message(frame1, text=f"{char_info['列传']}", relief=SUNKEN, width=180, bg="#e5e5e5")
        brief_label.pack(padx=10, pady=5)

        total = tk.Frame(frame1, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        total.pack(fill=tk.BOTH, expand=True)
        totalleft_label = tk.Label(total, text=f"出阵数 15", width=10)
        totalleft_label.pack(side=tk.LEFT, padx=10, pady=5)
        totalright_label = tk.Label(total, text=f"撤退数 0", width=10)
        totalright_label.pack(side=tk.RIGHT, padx=10, pady=5)

        notebook.add(frame1, text='武将列传')

        frame2 = tk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame2.pack(fill=tk.BOTH, expand=True)
        notebook.add(frame2, text='部队特性')

        frame3 = tk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame3.pack(fill=tk.BOTH, expand=True)
        attack_frame = tk.LabelFrame(frame3, text="攻击力", height=130, width=130)
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

        attack_frame = tk.LabelFrame(frame3, text="精神力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("1.AbilityProgressbar", text="90")
        mind_bar = ttk.Progressbar(attack_frame, style='1.AbilityProgressbar', maximum=100)
        mind_bar['value'] = 50
        mind_bar.pack(pady=1)

        attack_frame = tk.LabelFrame(frame3, text="防御力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("2.AbilityProgressbar", text="146")
        defense_bar = ttk.Progressbar(attack_frame, style='2.AbilityProgressbar', maximum=100)
        defense_bar['value'] = 60
        defense_bar.pack(pady=1)

        attack_frame = tk.LabelFrame(frame3, text="爆发力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("4.AbilityProgressbar", text="83")
        bar4 = ttk.Progressbar(attack_frame, style='4.AbilityProgressbar', maximum=100)
        bar4['value'] = 70
        bar4.pack(pady=1)

        attack_frame = tk.LabelFrame(frame3, text="士气", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        style.configure("5.AbilityProgressbar", text="86")
        bar5 = ttk.Progressbar(attack_frame, style='5.AbilityProgressbar', maximum=100)
        bar5['value'] = 50
        bar5.pack(pady=1)
        notebook.add(frame3, text='能力')

        attack_frame = tk.LabelFrame(frame3, text="移动力", height=130, width=130)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        move_label = tk.Label(attack_frame, text='6')
        move_label.pack(pady=1)
        notebook.add(frame3, text='能力')

        frame4 = tk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
        frame4.pack(fill=tk.BOTH, expand=True)
        weapen_frame = tk.LabelFrame(frame4, text="武器", height=85)
        weapen_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(weapen_frame, all_items, char_info['武器'])
        # weapen_label = tk.Label(weapen_frame, text=f"{char_info['武器']}", anchor='w')
        # weapen_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        # weapen_img = tk.PhotoImage(file=f"resource/items/{char_info['武器']}.png")
        # img_label = tk.Label(weapen_frame, image=weapen_img, relief=SUNKEN)
        # img_label.image = weapen_img
        # img_label.grid(row=1, rowspan=2, column=0, padx=10, sticky=tk.W)
        # lv_label = tk.Label(weapen_frame, text="Lv 10")
        # lv_label.grid(row=1, column=1, padx=5, sticky=tk.W)
        # exp_label = tk.Label(weapen_frame, text="Exp 10/100")
        # exp_label.grid(row=2, column=1, padx=5, sticky=tk.W)
        # addon_label = tk.Label(weapen_frame, text="攻击力", anchor='w')
        # addon_label.grid(row=3, column=0, padx=10, sticky=tk.W)

        armor_frame = tk.LabelFrame(frame4, text="护具", height=85)
        armor_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(armor_frame, all_items, char_info['护具'])
        
        treasure_frame = tk.LabelFrame(frame4, text="辅助", height=85)
        treasure_frame.pack(fill=tk.X, padx=5, pady=2)
        self.item_display(treasure_frame, all_items, char_info['辅助'])
        notebook.add(frame4, text='装备')

        frame5 = tk.Frame(notebook, width=LEFTFRAME_WIDTH, height=TAB_HEIGHT)
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
            itemname_label = tk.Label(weapen_frame, text="无", anchor='w')
        else:
            itemname_label = tk.Label(weapen_frame, text=f"{item}", anchor='w')
            
        itemname_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        if item == None or item == '':
            item_img = tk.PhotoImage(file=f"resource/items/blank.png")
        else:
            item_img = tk.PhotoImage(file=f"resource/items/{item}.png")
        img_label = tk.Label(weapen_frame, image=item_img, relief=SUNKEN)
        img_label.image = item_img
        img_label.grid(row=1, rowspan=2, column=0, padx=10, sticky=tk.W)

        img_label.bind("<ButtonPress-1>", lambda event, item=item: self.item_clicked(event, all_items, item))
        # img_label.bind("<ButtonPress-1>", lambda:self.item_clicked(item, event, ))
        
        if not (item == None or item == ''):
            lv_label = tk.Label(weapen_frame, text="Lv")
            lv_label.grid(row=1, column=1, padx=5, sticky=tk.W)
            lv2_label = tk.Label(weapen_frame, text=f"{all_items[item]['lv']}")
            lv2_label.grid(row=1, column=2, sticky=tk.W)

            exp_label = tk.Label(weapen_frame, text="Exp")
            exp_label.grid(row=2, column=1, padx=5, sticky=tk.W)
            style = ttk.Style(self.root)
            style_name = f"{item}.LabeledProgressbar"
            style.configure(style_name, text=f"{all_items[item]['exp']}/100")
            exp = ttk.Progressbar(weapen_frame, length=80, style=style_name, maximum=100)
            exp['value'] = all_items[item]['exp']
            exp.grid(row=2, column=2, sticky=tk.W)
        
        if not (item == None or item == ''):
            addon_label = tk.Label(weapen_frame, text=f"{all_items[item]['main_effect']['main']}", anchor='w')
            addon_label.grid(row=3, column=0, padx=10, sticky=tk.W)

            addon2_label = tk.Label(weapen_frame, text=f"{all_items[item]['main_effect']['effect']}", anchor='w')
            addon2_label.grid(row=3, column=1, padx=5, sticky=tk.W)

    def item_clicked(self, event, all_items, item):
        if not item:
            return

        if self.item_win:
            self.item_win.root.lift()
            print("Already exists")
            pass
        else:
            self.item_win = ItemWindow(parent=self, 
                x=self.root.winfo_x()-200, y=self.root.winfo_y(), all_items=all_items, item=item)
            self.item_win.root.lift()
            self.item_win.root.attributes('-topmost',True)
            self.item_win.root.after_idle(self.item_win.root.attributes, '-topmost', False)

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