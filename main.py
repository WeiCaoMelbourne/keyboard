import pygame
import os
# import pygame_menu
# import pygamepopup
# from pygamepopup.menu_manager import MenuManager

import tkinter as tk
import tkinter.messagebox as messagebox

from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT
from modules.main_menu import *
from modules.toolbar import *
from modules.win_pos import *
from modules.start_window import StartMainmenu
from modules.stories.s1_1 import s1_entrance
from modules.shared_variables import shared

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
UNIT_SIZE = 50
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
FPS = 100

global_state = {
    "starting": True,
    "section": 1
}

char_img = pygame.image.load('resource/img/t1.png')

root = tk.Tk()

#pictures must be a global variable, otherwise it won't work
# exit_btn = None
# exit_btn = tk.PhotoImage(file='resource/icon/exit.png')

embed = tk.Frame(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT) #creates embed frame for pygame window
config_menu(root)
config_toolbar(root)

embed.pack()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# center main window. It must be called after packing all elements of this window
root.eval('tk::PlaceWindow . center')

running = True
# def quit_callback():
#     global running
#     running = False

# root.wm_withdraw() #to hide the main window
# root.protocol("WM_DELETE_WINDOW", quit_callback)
# main_dialog =  tk.Frame(root)
# main_dialog.pack()

# def menu_cmd():
#     print("Cut clicked")
#     return 

# Menu
# L = tk.Label(root, text ="Right-click to display menu", width = 40, height = 20)
# L.pack()

def show_mainmenu():
    # messagebox.showinfo(title="Hello", message="What is it")
    win_pos = window_pos()
    print(win_pos)
    print(win_pos[0] + SCREEN_WIDTH / 2, win_pos[1] + SCREEN_WIDTH / 2)
    # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, 200, 0)
    # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, win_pos[1] + SCREEN_HEIGHT // 2, 0)

    top = tk.Toplevel()
    # print(win_pos[0] + mouse_pos[0], win_pos[1] + mouse_pos[1])
    top.geometry(f"+{win_pos[0] + SCREEN_WIDTH // 2}+{win_pos[1] + SCREEN_HEIGHT // 2}")
    # print(top)
    bt1 = tk.Button(top, text='New Game')
    bt1.pack()

    bt2 = tk.Button(top, text='Load Game')
    bt2.pack()
    top.focus_force()
    top.lift()
    top.grab_set()
    # top.grab_set_global()
    root.wait_window(top)

    # mySubmitButton = tk.Button(top, text='Submit', command=self.send)
    # mySubmitButton.pack()

    # main_manu = tk.Menu(None, tearoff = 0)
    # main_manu.add_command(label ="新的游戏")
    # main_manu.add_command(label ="Copy")
    # main_manu.add_command(label ="Paste")
    # main_manu.add_command(label ="Reload")
    # main_manu.add_separator()
    # main_manu.add_command(label ="Rename")

    # win_pos = window_pos()
    # print(win_pos)
    # print(win_pos[0] + SCREEN_WIDTH / 2, win_pos[1] + SCREEN_WIDTH / 2)
    # # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, 200, 0)
    # main_manu.tk_popup(win_pos[0] + SCREEN_WIDTH // 2, win_pos[1] + SCREEN_HEIGHT // 2, 0)

class MyMenu:
    def __init__(self, parent, win_pos, mouse_pos):
        self.m = tk.Menu(parent, tearoff = 0)
        self.m.add_command(label ="Cut", command=self.test)
        self.m.add_command(label ="Copy")
        self.m.add_command(label ="Paste")
        self.m.add_command(label ="Reload")
        self.m.add_separator()
        self.m.add_command(label ="Rename")

        print("do_popup")
        try:
            self.m.tk_popup(win_pos[0] + mouse_pos[0], win_pos[1] + mouse_pos[1], 0)
            # m.tk_popup(event.x_root, event.y_root)
        finally:
            print("Error")
            # self.m.grab_release()

    def test(self):
        print("cut clicked from MyMenu")

# def do_popup(win_pos, mouse_pos):
#     print("do_popup")
#     try:
#         m.tk_popup(win_pos[0] + mouse_pos[0], win_pos[1] + mouse_pos[1], 1)
#         # m.tk_popup(event.x_root, event.y_root)
#     finally:
#         print("Error")
#         # self.m.grab_release()
    

class MyDialog:
    def __init__(self, parent, win_pos, mouse_pos):
        # print(tk.Toplevel(parent))
        # tk.Toplevel(parent)
        top = self.top = tk.Toplevel()
        print(win_pos[0] + mouse_pos[0], win_pos[1] + mouse_pos[1])
        top.geometry(f"+{win_pos[0] + mouse_pos[0]}+{win_pos[1] + mouse_pos[1]}")
        # print(top)
        self.myLabel = tk.Label(top, text='Enter your username below')
        self.myLabel.pack()

        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        global username
        username = self.myEntryBox.get()
        self.top.destroy()


class Char(pygame.sprite.Sprite):
    def  __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(char_img, (UNIT_SIZE, UNIT_SIZE))
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.width = UNIT_SIZE
        self.rect.height = UNIT_SIZE
        self.rect.x = UNIT_SIZE * ((SCREEN_WIDTH / 2) // UNIT_SIZE)
        self.rect.y = UNIT_SIZE * ((SCREEN_HEIGHT / 2) // UNIT_SIZE)

    def update(self):
        pass

class MouseRec(pygame.sprite.Sprite):
    def  __init__(self, screen, pos):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 0, 0))
        # self.rect = self.image.get_rect()
        # self.rect.center = (pos[0], pos[1])
        self.rect = pygame.Rect(pos.x, pos.y, 50, 50)

    def update(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

def draw_mousebox(screen, pos):
    # print("draw_mousebox", pos)
    WIDTH = 50
    HEIGHT = 50
    x = UNIT_SIZE * ((pos[0] - WIDTH / 2) // UNIT_SIZE)
    y = UNIT_SIZE * ((pos[1] - HEIGHT / 2) // UNIT_SIZE)
    # print(x, y)
    outline_rect = pygame.Rect(x, y, WIDTH, HEIGHT)
    pygame.draw.rect(screen, COLOR_WHITE, outline_rect, 2)

    
pygame.display.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# screen.fill((0, 0, 0))

all_sprites = pygame.sprite.Group()
c = Char()
all_sprites.add(c)

fpsClock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background.fill(pygame.Color('#456000'))

background_img = pygame.image.load('resource/mmap/start.png').convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_img = pygame.image.load('resource/mmap/end.png').convert()
end_img = pygame.transform.scale(end_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
caocao_img = pygame.image.load('resource/pmap/曹操.png').convert()

cursor_img = pygame.image.load('resource/cursor/arrow.png')
horizontal_cursor = pygame.image.load('resource/cursor/arrow.png')
vertical_cursor = pygame.image.load('resource/cursor/arrow.png')
pygame.mouse.set_visible(False)
cursor_img_rect = cursor_img.get_rect()

# class Story:
#     pass

# story_object = Story()

class CaoCao(pygame.sprite.Sprite):
    def  __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = caocao_img
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 255, 255))
        self.rect = pygame.Rect(0, 0, 48, 64)
        self.rect.width = 48
        self.rect.height = 64
        self.rect.x = 100
        self.rect.y = 100
        

    def update(self):
        pass

# main loop here
def game():
    global running, background_img
    if running == False:
        root.quit()

    # start menu. It needs to be after root.update to get correct window pos
    if global_state['starting']:
        # background.blit(background_img, pygame.Rect((0,0),(10, 10)))
        screen.blit(background_img, (0, 0))
        pygame.display.update()
        start_win = StartMainmenu(root, 
            x=root.winfo_x()+root.winfo_width()//2-50, y=root.winfo_y()+root.winfo_height()//2, state=global_state)
        
        if start_win.choice == 'quit':
            print("Quite")
            screen.fill(COLOR_BLACK)
            screen.blit(end_img, (0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
            root.quit()

    # if global_state['section'] == 1:
    #     # background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()
    #     # background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    #     # a = CaoCao()
    #     # all_sprites.add(a)
    #     # global FPS
    #     shared["root"] = root
    #     # # shared['FPS'] = FPS
    #     # shared['running'] = running
    #     # shared['test'] = "hello"
    #     # shared['count'] = 1
    #     # print("before")
    #     # # root.after(1000 // FPS, s1_1)
    #     # s1_1()
        # print("back now")
        # FPS = shared['FPS']
        # print("getting here ")

        # screen.fill(COLOR_BLACK)
        # screen.blit(story_object.background_img, (0, 0))

            
    # print(pygame.time.get_ticks())
    # last_update = pygame.time.get_ticks()
    for event in pygame.event.get():
        print("evnet", event)
        if event.type == pygame.QUIT:
            running = False

            # start_win.root.lift()
            # start_win.attributes('-topmost',True)
            # start_win.after_idle(self.item_win.root.attributes, '-topmost', False)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("mouse clicked")
        #     show_mainmenu()

            # mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            # hwnd = pygame.display.get_wm_info()["window"]
            # prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
            # paramflags = (1, "hwnd"), (2, "lprect")
            # GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
            # # finally get our data!
            # rect = GetWindowRect(hwnd)
            
            # for item in all_sprites.sprites():
            #     if item.rect.collidepoint(mouse_pos):
            #         print("detected")
            #         if event.button == 1:
            #             print("left button clicked")
            #             inputDialog = MyDialog(root, (rect.left, rect.top), mouse_pos)
            #             root.wait_window(inputDialog.top)
            #             break
            #         elif event.button == 3:
            #             print("right button clicked")
            #             menu = MyMenu(root, (rect.left, rect.top), mouse_pos) 
            #             # do_popup((rect.left, rect.top), mouse_pos)
                        
            #             # inputDialog = MyDialog(root, (rect.left, rect.top), mouse_pos)
            #             # root.wait_window(inputDialog.top)
            #             break
            


    
    # # inputDialog = MyDialog(root)
    # # root.wait_window(inputDialog.top)
    # # ret = messagebox.askquestion ('Continue','OK')
    # # print(ret)

    
    # # Update sprits
    all_sprites.update()
    # main_dialog.update()

    # # main_dialog.update()

    # # Display screen
    # # screen.fill((0, 0, 0))
    # screen.blit(background, (0, 0))
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    
    mouse_pos = pygame.mouse.get_pos()
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    # print(mouse_pos)
    if mouse_pos[0] >= SCREEN_WIDTH - UNIT_SIZE / 2 or mouse_pos[0] < UNIT_SIZE / 2:
        screen.blit(horizontal_cursor, cursor_img_rect)
    elif mouse_pos[1] >= SCREEN_HEIGHT - UNIT_SIZE / 2 or mouse_pos[1] < UNIT_SIZE / 2:
        screen.blit(vertical_cursor, cursor_img_rect)
    else:
        screen.blit(cursor_img, cursor_img_rect)

    draw_mousebox(screen, mouse_pos)

    pygame.display.update()
    root.update()
    print("before root.after")
    if global_state['section'] == 1:
        # shared["root"] = root
        # root.after(1000 // FPS, s1_1)
        s1_entrance(root, screen, FPS, background_img, cursor_img)
    else:    
        root.after(1000 // FPS, game)
    print("after root.after")

if __name__ == "__main__":
    root.config(cursor="none")
    root.update()   # call this update to display background before showing main menu
    root.after(0, game)
    print("here it is...........................")
    root.mainloop()
    pygame.quit()