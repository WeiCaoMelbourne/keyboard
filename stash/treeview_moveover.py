import tkinter as tk
from tkinter import ttk


def highlight_row(event):
    tree = event.widget
    item = tree.identify_row(event.y)
    tree.tk.call(tree, "tag", "remove", "highlight")
    tree.tk.call(tree, "tag", "add", "highlight", item)

root = tk.Tk()

tree = ttk.Treeview(root, style = 'W.TButton')
vsb = ttk.Scrollbar(root, command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)

tree.tag_configure('highlight', background='lightblue')
tree.bind("<Motion>", highlight_row)


for i in range(100):
    tree.insert("", "end", text=f"Item #{i+1}")
    # tree.tag_bind(i, '<Motion>', highlight_row)

root.mainloop()