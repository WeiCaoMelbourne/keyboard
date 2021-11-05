import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, RAISED, SUNKEN
from PIL import Image, ImageTk
from .win_pos import window_pos
from .tv_funcs import treeview_sort_column
from .msg_box import MsgBoxWindow
from .modal_window import ModalWindow
import json
from .character_window import CharacterWindow

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
        frame1 = tk.Frame(notebook, width=WIDTH-30, height=HEIGHT-320)
        frame2 = tk.Frame(notebook, width=WIDTH-30, height=HEIGHT-320)
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

class CharactersWindow():
    def __init__(self):
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

        # print("you clicked on", char_info)
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
    global exit_img, save_img, setup_img, char_img, tool_img, load_img
    exit_img = tk.PhotoImage(file='resource/icon/exit.png')
    exit_button= tk.Button(toolbar, image=exit_img, command=lambda: exit(root=root), width=25, height=25)
    exit_button.pack(side=tk.LEFT)
    CreateToolTip(exit_button, "结束游戏")

    save_img = tk.PhotoImage(file='resource/icon/save.png')
    save_button= tk.Button(toolbar, image=save_img, command=lambda: save(root=root), width=25, height=25)
    save_button.pack(side=tk.LEFT)
    CreateToolTip(save_button, "保存游戏")

    load_img = tk.PhotoImage(file='resource/icon/load.png')
    load_button= tk.Button(toolbar, image=load_img, command=lambda: save(root=root), width=25, height=25)
    load_button.pack(side=tk.LEFT)
    CreateToolTip(load_button, "读取游戏")

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