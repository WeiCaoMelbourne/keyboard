import tkinter as tk
from .win_pos import window_pos
from PIL import Image
from PIL import ImageTk
from tkinter.constants import RAISED

class ModalWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        WIDTH = 600
        HEIGHT = 400

        tk.Toplevel.__init__(self, *args, **kwargs)

        # Removing titlebar from the Dialogue
        self.overrideredirect(True)

        self.config(border=3, relief=RAISED)

        win_pos = window_pos()
        self.geometry(f"{WIDTH}x{HEIGHT}+{win_pos[0]+100}+{win_pos[1]+100}")

        okBtn = tk.Button(self, text='确定', command=lambda:self.ok(), width=8)
        # self.CloseBtn.place(x=WIDTH/2-70, y=HEIGHT-50)
        okBtn.pack(side=tk.RIGHT, padx=10, pady=10)

    # Function on Closeing MessageBox

    # Function on pressing B1
    def ok(self):
        self.destroy() # Destroying Dialogue
        self.choice='ok'     # Assigning Value


