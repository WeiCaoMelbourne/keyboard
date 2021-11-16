import pygame
from ..common_funcs import draw_dialog, draw_selecter, bdraw_dialog, draw_mousebox, draw_mbinfo
import json
from ..constant import *
from ..win_pos import window_pos
import csv
import codecs
# from ..toolbar import move_redblue

FIELD_SCREEN_WIDTH = 960
FIELD_SCREEN_HEIGHT = 800

FIELD_WIDTH = 960
FIELD_HEIGHT = 960

LEFTTOP_X = 0
LEFTTOP_Y = FIELD_UNIT_SIZE * -3    # Because the first dialog is at bottom, so make screen lower

root = None
screen = None
background_img = None
cursor_img = None
tool_bar = None
# click_img = None
act = 0
s1_story = None
option_rects = []
all_sprites = None
all_characters = {}
timeline = 0
selection = -1
select_time = None
parent_func = None
unit_imgs = []
atk_imgs = []
prev_update = None
troop_details = None
terrain_details = None
mbinfo_switch = False
mbinfo_pos = None

# Character on map
class Character(pygame.sprite.Sprite):
    def  __init__(self, name):
        initial_data = s1_story["人物"][name]
        self.name = name
        pygame.sprite.Sprite.__init__(self)

        if isinstance(s1_story["人物"][name]['unit_img'], int):
            self.unit_img = unit_imgs[s1_story["人物"][name]['unit_img']]
        else:
            self.unit_img = pygame.image.load(s1_story["人物"][name]['unit_img']).convert()
            
        if 'atk_img' in s1_story["人物"][name]:
            if isinstance(s1_story["人物"][name]['atk_img'], int):
                self.atk_img = atk_imgs[s1_story["人物"][name]['atk_img']]
            else:
                self.atk_img = pygame.image.load(s1_story["人物"][name]['atk_img']).convert()
        
        if 'spc_img' in s1_story["人物"][name]:
            self.spc_img = pygame.image.load(s1_story["人物"][name]['spc_img']).convert()
        
        if 'direction' in s1_story["人物"][name]:
            if s1_story["人物"][name]['direction'] == 'right':
                self.image = self.unit_img.subsurface(0, UNIT_MOV_LEFT_FRAME * FIELD_UNIT_SIZE, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
                self.image = pygame.transform.flip(self.image, True, False)
            elif s1_story["人物"][name]['direction'] == 'left':
                self.image = self.unit_img.subsurface(0, UNIT_MOV_LEFT_FRAME * FIELD_UNIT_SIZE, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
            elif s1_story["人物"][name]['direction'] == 'up':
                self.image = self.unit_img.subsurface(0, UNIT_MOV_UP_FRAME * FIELD_UNIT_SIZE, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
            else:
                self.image = self.unit_img.subsurface(0, UNIT_MOV_DOWN_FRAME, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
        else:
            # print(name, self.leftdown_img, self.rightup_img)
            self.image = self.unit_img.subsurface(0, UNIT_MOV_DOWN_FRAME, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
        
        if 'frame' in s1_story["人物"][name]:
            frame = s1_story["人物"][name]['frame'] - 1
            self.image = self.unit_img.subsurface(0, frame * FIELD_UNIT_SIZE, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)

        self.image.set_colorkey(COLOR_KEY)
        self.rect = pygame.Rect(0, 0, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
        self.rect.width = FIELD_UNIT_SIZE
        self.rect.height = FIELD_UNIT_SIZE
        self.rect.x = initial_data['startx'] * FIELD_UNIT_SIZE
        self.rect.y = initial_data['starty'] * FIELD_UNIT_SIZE
        self.original_x = self.rect.x
        self.original_y = self.rect.y

        self.prev_tick = pygame.time.get_ticks()
        self.cur_pic = 0
        self.pic_direct = 1
        self.act = -1
        self.actframe_last = FIELD_ACT_FRAME_LAST
        self.die_flick = 0

    def play(self):
        global timeline

        # if no endx and no endy, do not touch this character
        if self.name not in s1_story["时间轴"][str(timeline)]:
            return

        now = pygame.time.get_ticks()
        # print(now, self.prev_tick)
        if now - self.prev_tick > self.actframe_last:
            self.act += 1
            if self.act >= len(s1_story["时间轴"][str(timeline)][self.name]):
                self.act = 0
                if 'benchmark' in s1_story["时间轴"][str(timeline)] and self.name == s1_story["时间轴"][str(timeline)]["benchmark"]:
                    timeline += 1
                return

            self.act_frame = 0
            if 'frame' in s1_story["时间轴"][str(timeline)][self.name][self.act]:
                self.act_frame = s1_story["时间轴"][str(timeline)][self.name][self.act]['frame'] - 1
            if 'last' in s1_story["时间轴"][str(timeline)][self.name][self.act]:
                self.actframe_last = s1_story["时间轴"][str(timeline)][self.name][self.act]['last']
            else:
                self.actframe_last = FIELD_ACT_FRAME_LAST
            self.prev_tick = now
            
        if s1_story["时间轴"][str(timeline)][self.name][self.act]['img'] == 'atk_img':
            self.image = self.atk_img.subsurface(0, FIELD_ATK_UNIT_SIZE * self.act_frame, FIELD_ATK_UNIT_SIZE, FIELD_ATK_UNIT_SIZE)
        elif s1_story["时间轴"][str(timeline)][self.name][self.act]['img'] == 'spc_img':
            self.image = self.spc_img.subsurface(0, FIELD_UNIT_SIZE * self.act_frame, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
        else:
            self.image = self.unit_img.subsurface(0, FIELD_UNIT_SIZE * self.act_frame, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)

        if 'flip' in s1_story["时间轴"][str(timeline)][self.name][self.act] and \
            s1_story["时间轴"][str(timeline)][self.name][self.act]['flip']:
            self.image = pygame.transform.flip(self.image, True, False)
        # Looks like if it is PNG file, do not need to call set_colorkey every time; but for BMP, it does
        self.image.set_colorkey(COLOR_KEY)

    def die(self):
        global timeline, all_sprites
        
        if self.name != s1_story["时间轴"][str(timeline)]['人物']:
            return

        now = pygame.time.get_ticks()
        if now - self.prev_tick > FIELD_DIE_FLICK_LAST:
            self.prev_tick = now
            self.die_flick += 1
            if self.die_flick >= 5:
                all_sprites.remove(self)
                del all_characters[self.name]
                timeline += 1
                return

            frame = 0
            if 'frame' in s1_story["时间轴"][str(timeline)]:
                frame = s1_story["时间轴"][str(timeline)]['frame'] - 1

            if self.die_flick % 2 == 0:
                self.image = self.unit_img.subsurface(0, FIELD_UNIT_SIZE * frame, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
                self.image.set_colorkey(COLOR_KEY)
            else:
                self.image = pygame.Surface((FIELD_UNIT_SIZE, FIELD_UNIT_SIZE))
                self.image.set_colorkey(COLOR_BLACK)

    def move(self):
        # print("move", self.name)
        global timeline

        if self.name != s1_story["时间轴"][str(timeline)]['人物']:
            return
        
        s = pygame.Surface((FIELD_UNIT_SIZE, FIELD_UNIT_SIZE), pygame.SRCALPHA) 
        s.fill(MOVE_BG_COLOR)    
        screen.blit(s, (self.rect.x - FIELD_UNIT_SIZE, self.rect.y - FIELD_UNIT_SIZE))

        # h_direct = 'left'
        # if 'h-direct' in s1_story["时间轴"][str(timeline)][self.name]:
        #     h_direct = s1_story["时间轴"][str(timeline)][self.name]['h-direct']
        # v_direct = 'down'
        # if 'v-direct' in s1_story["时间轴"][str(timeline)][self.name]:
        #     v_direct = s1_story["时间轴"][str(timeline)][self.name]['v-direct']
        
        # if 'benchmark' in s1_story["时间轴"][str(timeline)] and self.name == s1_story["时间轴"][str(timeline)]["benchmark"] :
        #     end_pivot = 'endx'
        #     if 'end-pivot' in s1_story["时间轴"][str(timeline)][self.name]:
        #         end_pivot = s1_story["时间轴"][str(timeline)][self.name]['end-pivot']

        #     if end_pivot == 'endx':
        #         if h_direct == 'left':
        #             if self.rect.x < s1_story["时间轴"][str(timeline)][self.name]['endx']:
        #                 timeline += 1
        #                 return
        #         else:
        #             if self.rect.x > s1_story["时间轴"][str(timeline)][self.name]['endx']:
        #                 timeline += 1
                        
        #     else:
        #         if v_direct == 'up':
        #             if self.rect.y < s1_story["时间轴"][str(timeline)][self.name]['endy']:
        #                 timeline += 1
        #                 return
        #         else:
        #             if self.rect.y > s1_story["时间轴"][str(timeline)][self.name]['endy']:
        #                 timeline += 1
        #                 return    
        
        # # by default, h direct is left, v direct is down
        # if h_direct == 'left':
        #     self.rect.x -= s1_story["时间轴"][str(timeline)][self.name]['speedx']
        # else:
        #     self.rect.x += s1_story["时间轴"][str(timeline)][self.name]['speedx']
        
        # if v_direct == 'up':
        #     self.rect.y -= s1_story["时间轴"][str(timeline)][self.name]['speedy']
        # else:
        #     self.rect.y += s1_story["时间轴"][str(timeline)][self.name]['speedy']
        
        # now = pygame.time.get_ticks()
        # # print(now, self.prev_tick)
        # if now - self.prev_tick > 70:
        #     if self.cur_pic >= 2:
        #         self.pic_direct *= -1
        #     self.cur_pic += self.pic_direct
        #     if self.cur_pic <= 0:
        #         self.pic_direct *= -1
            
        #     self.prev_tick = now

        # self.image = self.main_image.subsurface(0, 64 * self.cur_pic, 48, 64)
        # # Looks like if it is PNG file, do not need to call set_colorkey every time; but for BMP, it does
        # self.image.set_colorkey(COLOR_KEY)

    def update(self):
        global timeline
        if s1_story["时间轴"][str(timeline)]["类型"] == '结束':
             return

        if s1_story["时间轴"][str(timeline)]["类型"] == "移动":
            self.move()
        elif s1_story["时间轴"][str(timeline)]["类型"] == "动画":
            self.play()
        elif s1_story["时间轴"][str(timeline)]["类型"] == "死亡":
            self.die()
        # elif s1_story["时间轴"][str(timeline)]["类型"] == "对话":
        else:
            for name in all_characters:
                if name in s1_story["时间轴"][str(timeline)] and name == self.name:
                    frame = 1
                    if 'frame' in s1_story["时间轴"][str(timeline)][name]:
                        frame = s1_story["时间轴"][str(timeline)][name]['frame']
                    self.image = self.unit_img.subsurface(0, FIELD_UNIT_SIZE * (frame - 1), FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
                    if 'img' in s1_story["时间轴"][str(timeline)][name]:
                        if s1_story["时间轴"][str(timeline)][name]['img'] == 'atk_img':
                            self.image = self.atk_img.subsurface(0, FIELD_ATK_UNIT_SIZE * (frame - 1), FIELD_ATK_UNIT_SIZE, FIELD_ATK_UNIT_SIZE)
                        elif s1_story["时间轴"][str(timeline)][name]['img'] == 'spc_img':
                            self.image = self.spc_img.subsurface(0, FIELD_UNIT_SIZE * (frame - 1), FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
                    if 'flip' in s1_story["时间轴"][str(timeline)][name] and s1_story["时间轴"][str(timeline)][name]['flip']:
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.image.set_colorkey(COLOR_KEY)

def b1_main():
    global act, option_rects, timeline, selection, select_time, LEFTTOP_Y, mbinfo_switch, mbinfo_pos, mb_type

    # if s1_story["时间轴"][str(timeline)]["类型"] == '结束':
    #     all_sprites.empty()
    #     root.after(1000 // FPS, parent_func)
    #     return

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
            mouse_pos = pygame.mouse.get_pos()
            if option_rects and s1_story["时间轴"][str(timeline)]["类型"] == "选择" and selection < 0:
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
                timeline += 1
            else:   #display map block info
                mbinfo_switch = not mbinfo_switch
                mbinfo_pos = (mouse_pos[0] - FIELD_UNIT_SIZE, mouse_pos[1] - FIELD_UNIT_SIZE)
                # global mblocks_info
                # print(mblocks_info)
                # print(mouse_pos, (mouse_pos[0] - LEFTTOP_X) // FIELD_UNIT_SIZE, (mouse_pos[1] - LEFTTOP_Y) // FIELD_UNIT_SIZE)
                mb_type = mblocks_info[(mouse_pos[1] - LEFTTOP_Y) // FIELD_UNIT_SIZE][(mouse_pos[0] - LEFTTOP_X) // FIELD_UNIT_SIZE]
    # background_img.scroll(30, 30)
    mouse_pos = pygame.mouse.get_pos()
    # print(mouse_pos)
    if mouse_pos[1] >= FIELD_SCREEN_HEIGHT - MOVE_UNIT and LEFTTOP_Y * -1 + FIELD_SCREEN_HEIGHT + MOVE_UNIT < FIELD_HEIGHT:
        LEFTTOP_Y -= MOVE_UNIT
    elif mouse_pos[1] < MOVE_UNIT and LEFTTOP_Y < 0:
        LEFTTOP_Y += MOVE_UNIT
        # screen.blit(vertical_cursor, cursor_img_rect)

    screen.blit(background_img, (LEFTTOP_X, LEFTTOP_Y))
        # draw_mbinfo(screen, adjusted_pos, mb_type, terrain_details)
        # s = pygame.Surface((FIELD_UNIT_SIZE, FIELD_UNIT_SIZE), pygame.SRCALPHA) 
        # s.fill(MOVE_BG_COLOR)    
        # screen.blit(s, mbinfo_pos)

    # screen.blit(background_img, (LEFTTOP_X, LEFTTOP_Y), pygame.Rect(0, 0, FIELD_SCREEN_WIDTH, FIELD_SCREEN_HEIGHT))
    # print(timeline)
    # Use this logic to display next dialog after increase_red/increase_blue finishes
    # if select_time:
    #     now = pygame.time.get_ticks()
    #     if now - select_time > 1000:
    #         if selection == 0:
    #             timeline = 101  # 选择奸雄
    #         elif selection == 1:
    #             timeline = 21   # 忠臣
    #         select_time = None

    for sprite in all_sprites:
        sprite.rect.y = sprite.original_y + LEFTTOP_Y
        # print(sprite.original_y, LEFTTOP_Y)
        
    all_sprites.update()
    all_sprites.draw(screen)

    draw_mousebox(screen, mouse_pos)
    if mbinfo_switch:
        draw_mbinfo(screen, mbinfo_pos, mb_type, terrain_details)
    
    # draw dialog must be under all_sprites.draw to be above them all
    if s1_story["时间轴"][str(timeline)]["类型"] == "对话":
        # x, y = s1_story["时间轴"][str(timeline)]["发言"]['coordinates'].split()
        # x = int(x)
        # y = int(y)
        # print()
        rect = all_characters[s1_story["时间轴"][str(timeline)]["发言"]['人物']].rect
        face = s1_story["时间轴"][str(timeline)]["发言"]['face']
        speaker = face
        content = s1_story["时间轴"][str(timeline)]["发言"]['content']
        if 'speaker' in s1_story["时间轴"][str(timeline)]["发言"]:
            speaker = s1_story["时间轴"][str(timeline)]["发言"]['speaker']
        bdraw_dialog(screen, speaker, face, content, rect.x, rect.y)
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
    elif s1_story["时间轴"][str(timeline)]["类型"] == "通知":
        global prev_update
        if prev_update == None:
            prev_update = pygame.time.get_ticks()
        font_name = FONT_SONGTI
        font = pygame.font.Font(font_name, 46)
        text_surface = font.render(s1_story["时间轴"][str(timeline)]["content"], True, COLOR_WHITE)
        # print(text_surface.get_size())
        text_rect = text_surface.get_rect()
        w, h = pygame.display.get_surface().get_size()
        text_rect.left = (w - text_rect.width) // 2
        text_rect.top = (h - text_rect.height) // 2
        screen.blit(text_surface, text_rect)
        now = pygame.time.get_ticks()
        if now - prev_update > s1_story["时间轴"][str(timeline)]["last"]:
            timeline += 1
            prev_update = None

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

    root.after(1000 // FPS, b1_main)

def b1_entrance(parent_root, parent_screen, parent_cur, parent_tool_bar, global_state, exit_func):
    print("In b1_entrance", global_state)
    global_state['story'] = "s1-transition"
    # return
    
    global root, screen, background_img, cursor_img, s1_story, tool_bar, all_sprites, timeline, parent_func
    global troop_details, terrain_details, mblocks_info
    global unit_imgs, atk_imgs
    with open('data/story/b1.json', 'rb') as f:
        s1_story = json.load(f)
                    
    with open('data/troop-details.json', 'rb') as f:
        troop_details = json.load(f)

    with open('data/terrain-details.json', 'rb') as f:
        terrain_details = json.load(f)

    with codecs.open('data/story/b1-mblock.csv', "r", "utf-8") as csvfile:
        mblocks_info = list(csv.reader(csvfile, delimiter=','))
    # print(data)
    # if data[0][0] == '平原':
    #     print("correct")
    # else:
    #     print("incorrect")
    # tk_root = shared['root']
    
    root = parent_root
    screen = parent_screen
    cursor_img = parent_cur
    tool_bar = parent_tool_bar
    parent_func = exit_func

    # load all unit images
    for pic in s1_story['unit_imgs']:
        tmp_img = pygame.image.load(pic).convert()
        unit_imgs.append(tmp_img)

    # load all attack images
    for pic in s1_story['atk_imgs']:
        tmp_img = pygame.image.load(pic).convert()
        atk_imgs.append(tmp_img)

    background_img = pygame.image.load(s1_story['背景图']).convert()
    # click_img = pygame.image.load('resource/cursor/click.png').convert()

    all_sprites = pygame.sprite.Group()
    for name in s1_story['人物']:
        all_characters[name] =  Character(name=name)
        all_sprites.add(all_characters[name])

    # print(all_characters["曹操"].rect)

    # change timeline to 1
    timeline = 0

    # Initial screen
    for sprite in all_sprites:
        sprite.rect.y = sprite.original_y + LEFTTOP_Y
    screen.blit(background_img, (LEFTTOP_X, LEFTTOP_Y))
    all_sprites.draw(screen)

    pygame.display.update()
    parent_root.update()
    # in_pos = window_pos()
    # win_x = (parent_root.winfo_screenwidth() - parent_root.winfo_width()) // 2
    # win_y = (parent_root.winfo_screenheight() - parent_root.winfo_height()) // 2
    # parent_root.geometry(f"+{win_x}+{win_y}")
    parent_root.eval('tk::PlaceWindow . center')

    parent_root.after(500, b1_main)
    # parent_root.after(1000 // FPS, b1_main)

