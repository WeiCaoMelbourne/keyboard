import pygame
import os
# import pygamepopup
# from pygamepopup.menu_manager import MenuManager

import tkinter as tk
import tkinter.messagebox as messagebox

from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

root = tk.Tk()
root.wm_withdraw() #to hide the main window

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
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def update(self):
        pass

# window = tk.Tk()
# window.mainloop()
def main():
    pygame.init()
    # pygamepopup.init()

    pygame.display.set_caption('Quick Start')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    all_sprites = pygame.sprite.Group()
    c = Char()
    all_sprites.add(c)
    # menu_manager = MenuManager(screen)

    # from pygamepopup.components import Button, InfoBox

    # my_custom_menu = InfoBox(
    #     "Title of the Menu",
    #     [
    #         Button(
    #             title="Hello World!",
    #             callback=lambda: None
    #         )
    #     ]
    # )

    # menu_manager.open(my_custom_menu)

    fpsClock = pygame.time.Clock()

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(pygame.Color('#456000'))

    running = True

    while running:
        # fpsClock.tick(30)

        # print(pygame.time.get_ticks())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse clicked")
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)

                hwnd = pygame.display.get_wm_info()["window"]
                prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
                paramflags = (1, "hwnd"), (2, "lprect")
                GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
                # finally get our data!
                rect = GetWindowRect(hwnd)
                # print(rect.top, rect.left, rect.bottom, rect.right)
                
                inputDialog = MyDialog(root, (rect.left, rect.top), mouse_pos)
                root.wait_window(inputDialog.top)

        
        # inputDialog = MyDialog(root)
        # root.wait_window(inputDialog.top)
        # ret = messagebox.askquestion ('Continue','OK')
        # print(ret)

        # Update sprits
        all_sprites.update()

        # Display screen
        # screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()