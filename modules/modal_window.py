from tkinter import *
from .win_pos import window_pos
from PIL import Image
from PIL import ImageTk

class ModalWindow(object):

    def __init__(self, title='Mess', msg='', b1='OK', b2='', b3='', b4=''):
        WIDTH = 300
        HEIGHT = 120

        # Required Data of Init Function
        self.title = title      # Is title of titlebar
        self.msg = msg          # Is message to display
        self.b1 = b1            # Button 1 (outputs '1')
        self.b2 = b2            # Button 2 (outputs '2')
        self.b3 = b3            # Button 3 (outputs '3')
        self.b4 = b4            # Button 4 (outputs '4')
        self.choice = ''        # it will be the return of messagebox according to button press

        # Just the colors for my messagebox

        self.tabcolor = 'red'    # Button color for Active State
        self.bgcolor = 'blue'    # Button color for Non-Active State
        self.bgcolor2 = 'yellow' # Background color of Dialogue
        self.textcolor = 'Green' # Text color for Dialogue

        # Creating Dialogue for messagebox
        self.root = Toplevel()
        self.root.grab_set()
        self.root.grab_set_global()
    
        # Removing titlebar from the Dialogue
        self.root.overrideredirect(True)

        # Setting Geometry
        win_pos = window_pos()
        print(win_pos)
        # print(win_pos[0] + SCREEN_WIDTH / 2, win_pos[1] + SCREEN_WIDTH / 2)
        self.root.geometry(f"300x120+{win_pos[0]+200}+{win_pos[1]+200}")
    
        # Setting Background color of Dialogue
        # self.root.config(bg=self.bgcolor2)

        # img = Image.open("resource/img/background.png")
        # img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        # photoImg = ImageTk.PhotoImage(img)
        # background_label = Label(self.root, text=msg, image=photoImg, compound='center')
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Creating Label For message
        self.msg = Label(self.root,text=msg,
                        # font=("Helvetica",9),
                        # bg=self.bgcolor2,
                        # fg=self.textcolor,
                        #anchor='nw'
                        )
        self.msg.place(x=10,y=28,height=60,width=280)

        # Creating TitleBar
        self.titlebar = Label(self.root,text=self.title,
                            #  bg=self.bgcolor2,
                            #  fg=self.textcolor,
                            #  bd=0,
                             font=("Helvetica",10,'bold')
                             )
        self.titlebar.place(x=100,y=5)
    
        # Creating Close Button
        self.CloseBtn = Button(self.root,
                                text='x',
                                font=("Helvetica",12),
                                command = lambda : self.closed(),
                                bd=0,
                                activebackground='red',
                                activeforeground='white',
                                background=self.bgcolor2,
                                foreground=self.textcolor)
        self.CloseBtn.place(x=260,y=0,width=40)
 
        # Changing Close Button Color on Mouseover
        self.CloseBtn.bind("<Enter>", lambda e,: self.CloseBtn.config(bg='red',fg='white'))
        self.CloseBtn.bind("<Leave>", lambda e,: self.CloseBtn.config(bg=self.bgcolor2,fg=self.textcolor))

        # Creating B1 
        self.B1 = Button(self.root,text=self.b1,command=self.click1,
                        bd=0,
                        font=("Helvetica",10),
                        bg=self.bgcolor,
                        fg='white',
                        activebackground=self.tabcolor,
                        activeforeground=self.textcolor)
        self.B1.place(x=225,y=90,height=25,width=60)
    
        # Getting place_info of B1
        self.B1.info = self.B1.place_info()
    
        # Creating B2
        if not b2=="":
            self.B2 = Button(self.root,text=self.b2,command=self.click2,
                            bd=0,
                            font=("Helvetica",10),
                            bg=self.bgcolor,
                            fg='white',
                            activebackground=self.tabcolor,
                            activeforeground=self.textcolor)
            self.B2.place(x=int(self.B1.info['x'])-(70*1),
                          y=int(self.B1.info['y']),
                          height=int(self.B1.info['height']),
                          width=int(self.B1.info['width'])
                          )
        # Creating B3
        if not b3=='':
            self.B3 = Button(self.root,text=self.b3,command=self.click3,
                            bd=0,
                            font=("Helvetica",10),
                            bg=self.bgcolor,
                            fg='white',
                            activebackground=self.tabcolor,
                            activeforeground=self.textcolor)
            self.B3.place(x=int(self.B1.info['x'])-(70*2),
                          y=int(self.B1.info['y']),
                          height=int(self.B1.info['height']),
                          width=int(self.B1.info['width'])
                          )
        # Creating B4
        if not b4=='':
            self.B4 = Button(self.root,text=self.b4,command=self.click4,
                            bd=0,
                            font=("Helvetica",10),
                            bg=self.bgcolor,
                            fg='white',
                            activebackground=self.tabcolor,
                            activeforeground=self.textcolor)
            self.B4.place(x=int(self.B1.info['x'])-(70*3),
                          y=int(self.B1.info['y']),
                          height=int(self.B1.info['height']),
                          width=int(self.B1.info['width'])
                          )

        # Making MessageBox Visible
        self.root.wait_window()

    # Function on Closeing MessageBox
    def closed(self):
        self.root.destroy() # Destroying Dialogue
        self.choice='closed'#Assigning Value
        
    # Function on pressing B1
    def click1(self):
        self.root.destroy() # Destroying Dialogue
        self.choice='1'     # Assigning Value

    # Function on pressing B2
    def click2(self):
        self.root.destroy() # Destroying Dialogue
        self.choice='2'     # Assigning Value

    # Function on pressing B3
    def click3(self):
        self.root.destroy() #Destroying Dialogue
        self.choice='3'     # Assigning Value

    # Function on pressing B4
    def click4(self):
        self.root.destroy() #Destroying Dialogue
        self.choice='4'     #Assigning Value

