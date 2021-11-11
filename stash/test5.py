from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style(root)

# custom indicator images
im_open = Image.new('RGBA', (15, 15), '#00000000')
im_empty = Image.new('RGBA', (15, 15), '#00000000')
draw = ImageDraw.Draw(im_open)
draw.polygon([(0, 4), (14, 4), (7, 11)], fill = 'yellow', outline = 'black')
im_close = im_open.rotate(90)

img_open = ImageTk.PhotoImage(im_open, name = 'img_open', master = root)
img_close = ImageTk.PhotoImage(im_close, name = 'img_close', master = root)
img_empty = ImageTk.PhotoImage(im_empty, name = 'img_empty', master = root)

# custom indicator
style.element_create('Treeitem.myindicator',
   'image', 'img_close', ('user1', '!user2', 'img_open'), ('user2', 'img_empty'),
   sticky = '', width = 15)
# replace Treeitem.indicator by custom one
style.layout('Treeview.Item',
   [('Treeitem.padding', {
      'sticky': 'nswe',
      'children': [('Treeitem.myindicator', {
            'side': 'left',
            'sticky': ''
         }),
         ('Treeitem.image', {
            'side': 'left',
            'sticky': ''
         }),
         ('Treeitem.focus', {
            'side': 'left',
            'sticky': '',
            'children': [('Treeitem.text', {
               'side': 'left',
               'sticky': ''
            })]
         })
      ]
   })]
)
style.configure('Treeview', indent=-100)

columns = ('#1', '#2')
tree = ttk.Treeview(root, columns=columns, padding=[-15,0,0,0])
tree.pack()
tree.insert('', 0, text = 'item 1', open = True)
tree.insert('', 0, text = 'item 2')
# tree.insert('I001', 'end', text = 'item 11', open = False)
# tree.insert('I001', 'end', text = 'item 12', open = False)
# tree.insert('I004', 'end', text = 'item 121', open = False)

root.mainloop()