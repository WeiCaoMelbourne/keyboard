

import tkinter as tk
root = tk.Tk()

tiles_letter = ['a', 'b', 'c', 'd', 'e']

def add_letter():
    print("before")
    root.after(5000, add_letter)
    print("after")
    print("keep going ")


root.after(0, add_letter)  # add_letter will run as soon as the mainloop starts.
root.mainloop()