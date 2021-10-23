
import tkinter as tk
from .modal_window import ModalWindow
# Menu
# L = tk.Label(root, text ="Right-click to display menu", width = 40, height = 20)
# L.pack()

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
    a = ModalWindow(msg='Hello I m your multiline message',
                    title='Hello World',
                    b1='Button 1',
                    b2='Button 2',
                    )
    print(a.choice)

def config_toolbar(root):
    toolbar = tk.Frame(root, height=30)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    
    # Images must be declared as global, otherwise imega won't work
    global exit_img, save_img, setup_img
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