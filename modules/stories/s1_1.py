import pygame
from ..shared_variables import shared

root = None
screen = None
background_img = None
cursor_img = None
FPS = None

print("Inside s1_1.py")

# s1_bg_img = pygame.image.load('resource/mmap/1-1.bmp').convert()

def s1_main():
    print("In s1_main")
    for event in pygame.event.get():
        print("evnet in s1_entrance", event)
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_img, (0, 0))
    # all_sprites.draw(screen)
    
    mouse_pos = pygame.mouse.get_pos()
    cursor_img_rect = cursor_img.get_rect()
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    # print(mouse_pos)
    screen.blit(cursor_img, cursor_img_rect)

    pygame.display.update()
    root.update()
    root.after(1000 // FPS, s1_main)

def s1_entrance(parent_root, parent_screen, parent_fps, parent_img, parent_cur):
    print("In s1_1")
    global root, screen, background_img, cursor_img, FPS
    # tk_root = shared['root']
    root = parent_root
    screen = parent_screen
    cursor_img = parent_cur
    FPS = parent_fps
    background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()

    pygame.display.update()
    parent_root.update()

    parent_root.after(1000 // FPS, s1_main)
    # root.after(1000, s1_1)
    # shared['FPS'] = 10
    # shared['test'] = "hello back"
    # shared['new'] = 'new'
    # shared['count'] = 2
    # print("inside", shared)

