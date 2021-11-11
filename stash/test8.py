from tkinter import ttk
from tkinter import *

def t():
    style = ttk.Style()
    style.theme_use("default")
    print(style.layout("Treeview.Item"))
    # style.map('Treeview', foreground=[('selected', 'black')], background=[ ('selected', '')])
    # style.layout("Treeview.Item",
    #     [('Treeitem.padding', {'sticky': 'nswe', 'children': 
    #         [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
    #         ('Treeitem.image', {'side': 'left', 'sticky': ''}),
    #         #('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
    #             ('Treeitem.text', {'side': 'left', 'sticky': ''}),
    #         #]})
    #         ],
    #     })]
    #     )
    # style.map("Treeview", background=[('disabled', 'SystemButtonFace'), ('selected', 'invalid')])
    s = ttk.Treeview(columns=('#1', '#2'))
    s.heading('#0', text='Country')
    s.heading('#1', text='Ip')
    s.heading('#2', text='Port')
    global v
    v = PhotoImage(file='resource/icon/abc.gif')
    s.insert('', 1, text="Hello", values = ('127.0.0.1', '8888'), image=v)
    s.insert('', 2, values = ('127.0.0.2', 'ddd'), image=v)
    s.insert('', 3, values = ('127.0.0.3', ''), image=v)
    s.pack()

    # columns = ('#1', '#2', '#3')
    # tree = ttk.Treeview(columns=columns, height=13)
    # tree.tag_configure('odd', background='gainsboro')
    # tree.heading('#3', text='Pic')
    # tree.heading('#1', text='名称')
    # tree.heading('#2', text='持有者')

    # tree.insert('', 2, values = ('1', '2', '3'))
    # tree.pack()

root = Tk()
t()
root.mainloop()