import pygame
from ..shared_variables import shared
from ..common_funcs import drawr_dialog, drawl_dialog
import json

root = None
screen = None
background_img = None
cursor_img = None
FPS = None
act = 0
s1_story = None
# caocao_face_img = pygame.image.load('resource/face/曹操-1.bmp').convert()

# s1_bg_img = pygame.image.load('resource/mmap/1-1.bmp').convert()

def s1_main():
    global act
    for event in pygame.event.get():
        print("evnet in s1_entrance", event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            act += 1

    screen.blit(background_img, (0, 0))
    # all_sprites.draw(screen)
    
    # mouse_pos = pygame.mouse.get_pos()
    cursor_img_rect = cursor_img.get_rect()
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    # print(mouse_pos)
    screen.blit(cursor_img, cursor_img_rect)

    if act == 1:
        drawr_dialog(screen, "曹操", "曹操", "测试一下曹操的对话1", -10, -10)
    elif act == 2:
        drawl_dialog(screen, "曹操", "曹操", "测试一下曹操的对话2", 10, -10)

    pygame.display.update()
    root.update()
    root.after(1000 // FPS, s1_main)

def s1_entrance(parent_root, parent_screen, parent_fps, parent_img, parent_cur):
    print("In s1_1")
    
    global root, screen, background_img, cursor_img, FPS, s1_story
    # with open('data/story/s1.json', 'rb') as f:
    #     s1_story = json.load(f)
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

