import pygame
from ..common_funcs import draw_dialog, draw_selecter, drawr_talkbubble, drawl_talkbubble
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
all_sprites = None
all_characters = {}
timeline = 0
selection = -1
select_time = None
parent_func = None

# Character on map
class Character(pygame.sprite.Sprite):
    def  __init__(self, name):
        initial_data = s1_story["人物"][name]
        self.name = name
        pygame.sprite.Sprite.__init__(self)

        if 'left-down-face' in s1_story["人物"][name]:
            self.leftdown_img = pygame.image.load(s1_story["人物"][name]['left-down-face']).convert()
        if 'right-up-face' in s1_story["人物"][name]:
            self.rightup_img = pygame.image.load(s1_story["人物"][name]['right-up-face']).convert()
        
        if 'main-face' in s1_story["人物"][name] and s1_story["人物"][name]['main-face'] == "right-up-face":
            self.main_image = self.rightup_img
        else:
            self.main_image = self.leftdown_img
        
        # print(name, self.leftdown_img, self.rightup_img)
        self.image = self.main_image.subsurface(0, 0, 48, 64)
        self.image.set_colorkey(COLOR_KEY)
        self.rect = pygame.Rect(0, 0, 48, 64)
        self.rect.width = 48
        self.rect.height = 64
        self.rect.x = initial_data['startx']
        self.rect.y = initial_data['starty']

        self.prev_tick = pygame.time.get_ticks()
        self.cur_pic = 0
        self.pic_direct = 1

    def move(self):
        global timeline

        # if no endx and no endy, do not touch this character
        if self.name not in s1_story["时间轴"][str(timeline)]:
            return

        h_direct = 'left'
        if 'h-direct' in s1_story["时间轴"][str(timeline)][self.name]:
            h_direct = s1_story["时间轴"][str(timeline)][self.name]['h-direct']
        v_direct = 'down'
        if 'v-direct' in s1_story["时间轴"][str(timeline)][self.name]:
            v_direct = s1_story["时间轴"][str(timeline)][self.name]['v-direct']
        
        if 'benchmark' in s1_story["时间轴"][str(timeline)] and self.name == s1_story["时间轴"][str(timeline)]["benchmark"] :
            end_pivot = 'endx'
            if 'end-pivot' in s1_story["时间轴"][str(timeline)][self.name]:
                end_pivot = s1_story["时间轴"][str(timeline)][self.name]['end-pivot']

            if end_pivot == 'endx':
                if h_direct == 'left':
                    if self.rect.x < s1_story["时间轴"][str(timeline)][self.name]['endx']:
                        timeline += 1
                        return
                else:
                    if self.rect.x > s1_story["时间轴"][str(timeline)][self.name]['endx']:
                        timeline += 1
                        
            else:
                if v_direct == 'up':
                    if self.rect.y < s1_story["时间轴"][str(timeline)][self.name]['endy']:
                        timeline += 1
                        return
                else:
                    if self.rect.y > s1_story["时间轴"][str(timeline)][self.name]['endy']:
                        timeline += 1
                        return    
        
        # by default, h direct is left, v direct is down
        if h_direct == 'left':
            self.rect.x -= s1_story["时间轴"][str(timeline)][self.name]['speedx']
        else:
            self.rect.x += s1_story["时间轴"][str(timeline)][self.name]['speedx']
        
        if v_direct == 'up':
            self.rect.y -= s1_story["时间轴"][str(timeline)][self.name]['speedy']
        else:
            self.rect.y += s1_story["时间轴"][str(timeline)][self.name]['speedy']
        
        now = pygame.time.get_ticks()
        # print(now, self.prev_tick)
        if now - self.prev_tick > 70:
            if self.cur_pic >= 2:
                self.pic_direct *= -1
            self.cur_pic += self.pic_direct
            if self.cur_pic <= 0:
                self.pic_direct *= -1
            
            self.prev_tick = now

        self.image = self.main_image.subsurface(0, 64 * self.cur_pic, 48, 64)
        # Looks like if it is PNG file, do not need to call set_colorkey every time; but for BMP, it does
        self.image.set_colorkey(COLOR_KEY)

    def update(self):
        global timeline
        if s1_story["时间轴"][str(timeline)]["类型"] == '结束':
             return

        if s1_story["时间轴"][str(timeline)]["类型"] == "移动":
            self.move()
        elif s1_story["时间轴"][str(timeline)]["类型"] == "对话":
            for name in all_characters:
                if name in s1_story["时间轴"][str(timeline)] and name == self.name:
                    frame = 1
                    if 'frame' in s1_story["时间轴"][str(timeline)][name]:
                        frame = s1_story["时间轴"][str(timeline)][name]['frame']
                    if s1_story["时间轴"][str(timeline)][name]['direction'] == 'right-up':
                        self.image = self.rightup_img.subsurface(0, 64 * (frame - 1), 48, 64)
                        self.image.set_colorkey(COLOR_KEY)
                    elif s1_story["时间轴"][str(timeline)][name]['direction'] == 'left-up':
                        self.image = self.rightup_img.subsurface(0, 64 * (frame - 1), 48, 64)
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image.set_colorkey(COLOR_KEY)
                    elif s1_story["时间轴"][str(timeline)][name]['direction'] == 'right-down':
                        self.image = self.leftdown_img.subsurface(0, 64 * (frame - 1), 48, 64)
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image.set_colorkey(COLOR_KEY)
                    elif s1_story["时间轴"][str(timeline)][name]['direction'] == 'left-down':
                        self.image = self.leftdown_img.subsurface(0, 64 * (frame - 1), 48, 64)
                        self.image.set_colorkey(COLOR_KEY)


def s1_main():
    global act, option_rects, timeline, selection, select_time

    if s1_story["时间轴"][str(timeline)]["类型"] == '结束':
        all_sprites.empty()
        root.after(1000 // FPS, parent_func)
        return

    for event in pygame.event.get():
        # print("evnet in s1_entrance", event, pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.ACTIVEEVENT:
            # print(event)
            if event.gain == 0:
                root.config(cursor="arrow")
            else:
                root.config(cursor="none")
            # if event.state & pygame.APPMOUSEFOCUS == pygame.APPMOUSEFOCUS:
            #     print ('mouse focus ' + ('gained' if event.gain else 'lost'))
            # if event.state & pygame.APPINPUTFOCUS == pygame.APPINPUTFOCUS:
            #     print ('input focus ' + ('gained' if event.gain else 'lost'))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("cliecked, ", timeline, s1_story["时间轴"][str(timeline)]["类型"])
            if option_rects and s1_story["时间轴"][str(timeline)]["类型"] == "选择" and selection < 0:
                print("there are still option dialog")
                mouse_pos = pygame.mouse.get_pos()
                selection = -1
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selection = i
                if selection == 0:
                    select_time = pygame.time.get_ticks()
                    option_rects = []
                    tool_bar.increase_red()
                elif selection == 1:
                    select_time = pygame.time.get_ticks()
                    option_rects = []
                    tool_bar.increase_blue()
            elif s1_story["时间轴"][str(timeline)]["类型"] == "对话":
                print("clicked")
                timeline += 1

    screen.blit(background_img, (0, 0))
    # print(timeline)
    # Use this logic to display next dialog after increase_red/increase_blue finishes
    if select_time:
        now = pygame.time.get_ticks()
        if now - select_time > 1000:
            if selection == 0:
                timeline = 101  # 选择奸雄
            elif selection == 1:
                timeline = 21   # 忠臣
            select_time = None

    all_sprites.update()
    all_sprites.draw(screen)

    # draw dialog must be under all_sprites.draw to be above them all
    if s1_story["时间轴"][str(timeline)]["类型"] == "对话":
        x, y = s1_story["时间轴"][str(timeline)]["发言"]['coordinates'].split()
        x = int(x)
        y = int(y)
        draw_dialog(screen, s1_story["时间轴"][str(timeline)]["发言"]['face'], s1_story["时间轴"][str(timeline)]["发言"]['face'], 
            s1_story["时间轴"][str(timeline)]["发言"]['content'], x, y)
        if '人物' in s1_story["时间轴"][str(timeline)]["发言"]:
            if "bubble" in s1_story["时间轴"][str(timeline)]["发言"] and \
                s1_story["时间轴"][str(timeline)]["发言"]["bubble"] == "left":
                drawl_talkbubble(screen, all_characters[s1_story["时间轴"][str(timeline)]["发言"]['人物']].rect)
            else:
                drawr_talkbubble(screen, all_characters[s1_story["时间轴"][str(timeline)]["发言"]['人物']].rect)
    elif s1_story["时间轴"][str(timeline)]["类型"] == "选择":
        mouse_pos = pygame.mouse.get_pos()
        options = s1_story["时间轴"][str(timeline)]['选项'].split("\n")
        selected = False
        if option_rects:
            for i, rect in enumerate(option_rects):
                # print(rect)
                if rect.collidepoint(mouse_pos):
                    # print("mouse is in ", rect)
                    draw_selecter(screen, s1_story["时间轴"][str(timeline)]['人物'], options, hoveron=i)
                    selected = True
        if not selected:
            temp = draw_selecter(screen, s1_story["时间轴"][str(timeline)]['人物'], options)
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

def s1_entrance(parent_root, parent_screen, parent_cur, parent_tool_bar, global_state, exit_func):
    global_state['story'] = "s1-transition"
    # return
    
    global root, screen, background_img, cursor_img, s1_story, click_img, tool_bar, all_sprites, timeline, parent_func
    with open('data/story/s1.json', 'rb') as f:
        s1_story = json.load(f)
    
    # print(s1_story)
    root = parent_root
    screen = parent_screen
    cursor_img = parent_cur
    tool_bar = parent_tool_bar
    parent_func = exit_func
    background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()
    # click_img = pygame.image.load('resource/cursor/click.png').convert()

    all_sprites = pygame.sprite.Group()
    for name in s1_story['人物']:
        all_characters[name] =  Character(name=name)
        all_sprites.add(all_characters[name])

    # change timeline to 1
    timeline = 0

    pygame.display.update()
    parent_root.update()

    parent_root.after(1000 // FPS, exit_func)

