import tkinter as tk
from tkinter import ttk

# def createTreeView(frame, columns, height=15):
#     tree = ttk.Treeview(frame, columns=columns, show='headings', height=height)
#     tree.tag_configure('odd', background='gainsboro')

#     tree.heading('#1', text='武将名')
#     tree.heading('#2', text='部队属性')
#     tree.heading('#3', text='Lv', command=lambda:self.treeview_sort_column(tree, '#3', False))

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda:treeview_sort_column(tv, col, not reverse))