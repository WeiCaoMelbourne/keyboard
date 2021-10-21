import pygame
# import pygamepopup
# from pygamepopup.menu_manager import MenuManager

import tkinter as tk
import tkinter.messagebox as messagebox

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

root = tk.Tk()
root.wm_withdraw() #to hide the main window

class MyDialog:
    def __init__(self, parent):
        # print(tk.Toplevel(parent))
        # tk.Toplevel(parent)
        top = self.top = tk.Toplevel()
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
                # pos = pygame.mouse.get_pos()
                # print(pos)
                inputDialog = MyDialog(root)
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