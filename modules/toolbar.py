import tkinter as tk
from tkinter import ttk
from tkinter.constants import RAISED, W
from .win_pos import window_pos
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

class CharactersWindow():
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

        self.titlebar = tk.Label(self.root, text="部队情报一览")
        # self.titlebar.place(x=5, y=5)
        self.titlebar.pack(fill=tk.BOTH, padx=5, pady=5)

        columns = ('#1', '#2', '#3')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.heading('#1', text='First Name')
        tree.heading('#2', text='Last Name')
        tree.heading('#3', text='Email')
        contacts = []
        for n in range(1, 10):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))
                # adding data to the treeview
        for contact in contacts:
            tree.insert('', tk.END, values=contact)
        tree.pack()
        # tree.grid(row=0, column=0, sticky='nsew')
        # scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        # tree.configure(yscroll=scrollbar.set)
        # scrollbar.grid(row=0, column=1, sticky='ns')
        
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

    tool_img = tk.PhotoImage(file='resource/icon/characters.png')
    tool_button= tk.Button(toolbar2, image=tool_img, command=lambda: setup(root=root), width=25, height=25)
    tool_button.pack(side=tk.LEFT)
    CreateToolTip(setup_button, "持有道具一览")