import pygame
from ..common_funcs import draw_dialog, draw_selecter
import json
from ..constant import *
# from ..toolbar import move_redblue

root = None
screen = None
background_img = None
cursor_img = None
tool_bar = None
click_img = None
act = 0
s1_story = None
option_rects = []

def s1_main():
    global act, option_rects
    for event in pygame.event.get():
        print("evnet in s1_entrance", event, pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.ACTIVEEVENT:
            print(event)
            if event.gain == 0:
                root.config(cursor="arrow")
            else:
                root.config(cursor="none")
            # if event.state & pygame.APPMOUSEFOCUS == pygame.APPMOUSEFOCUS:
            #     print ('mouse focus ' + ('gained' if event.gain else 'lost'))
            # if event.state & pygame.APPINPUTFOCUS == pygame.APPINPUTFOCUS:
            #     print ('input focus ' + ('gained' if event.gain else 'lost'))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if option_rects:
                mouse_pos = pygame.mouse.get_pos()
                selection = -1
                for i, rect in enumerate(option_rects):
                    # print(rect)
                    if rect.collidepoint(mouse_pos):
                        print("selected is ", i)
                        selection = i
                if selection == 0:
                    tool_bar.increase_red()
                elif selection == 1:
                    tool_bar.increase_blue()
            else:
                act += 1

    screen.blit(background_img, (0, 0))

    if act > 0 and act < len(s1_story["对话"]) - 1:
        x, y = s1_story["对话"][act+1]['coordinates'].split()
        x = int(x)
        y = int(y)
        draw_dialog(screen, s1_story["对话"][act+1]['speaker'], s1_story["对话"][act+1]['speaker'], 
            s1_story["对话"][act+1]['content'], x, y)
    elif act >= len(s1_story["对话"]) - 1:
        mouse_pos = pygame.mouse.get_pos()
        options = s1_story["选择"]['选项'].split("\n")
        selected = False
        if option_rects:
            for i, rect in enumerate(option_rects):
                # print(rect)
                if rect.collidepoint(mouse_pos):
                    # print("mouse is in ", rect)
                    draw_selecter(screen, s1_story["选择"]['人物'], options, selected=i)
                    selected = True
        if not selected:
            temp = draw_selecter(screen, s1_story["选择"]['人物'], options)
            if len(option_rects) == 0:
                option_rects = temp

    
    cursor_img_rect = cursor_img.get_rect()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor_img_rect.x = mouse_x
    cursor_img_rect.y = mouse_y
    # print(mouse_pos)
    # if act > 0 and act < len(s1_story["对话"]) - 1:
    #     screen.blit(click_img, cursor_img_rect)
    # else:
    #     screen.blit(cursor_img, cursor_img_rect)
    screen.blit(cursor_img, cursor_img_rect)
    
    pygame.display.update()
    root.update()
    root.after(1000 // FPS, s1_main)

def s1_entrance(parent_root, parent_screen, parent_cur, parent_tool_bar):
    print("In s1_1")
    
    global root, screen, background_img, cursor_img, s1_story, click_img, tool_bar
    with open('data/story/s1.json', 'rb') as f:
        s1_story = json.load(f)
    # tk_root = shared['root']
    print(s1_story)
    root = parent_root
    screen = parent_screen
    cursor_img = parent_cur
    tool_bar = parent_tool_bar
    background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()
    # click_img = pygame.image.load('resource/cursor/click.png').convert()

    pygame.display.update()
    parent_root.update()

    parent_root.after(1000 // FPS, s1_main)

