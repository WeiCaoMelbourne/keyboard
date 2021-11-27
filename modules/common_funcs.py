import pygame
from .constant import *
import codecs
import csv

dialogr_bg_img = None
dialogl_bg_img = None
bdialogl_bg_img = None
bdialogr_bg_img = None
font_name = None
selector_bg_img = None
speakbubble_l_img = None
speakbubble_r_img = None
face_img_dict = {
    
}

def draw_text(screen, text, size, color, x, y, fill=False):
    # print("draw_text", text, fill)
    global font_name
    if font_name == None:
        font_name = FONT_SONGTI
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    # print(text_surface.get_size())
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    if fill:
        screen.fill(COLOR_BLUE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect

def prepare_dialog(face, x, y):
    global dialogr_bg_img, dialogl_bg_img, font_name
    if dialogr_bg_img == None:
        dialogr_bg_img = pygame.image.load('resource/mark/dialogr_bg.png').convert()
    if dialogl_bg_img == None:
        dialogl_bg_img = pygame.image.load('resource/mark/dialogl_bg.png').convert()
    if x < 0 or y < 0:
        w, h = pygame.display.get_surface().get_size()
        if x < 0:
            dialog_img_rect = dialogr_bg_img.get_rect()
            x = w + x - dialog_img_rect.width
        if y < 0:
            dialog_img_rect = dialogr_bg_img.get_rect()
            y = h + y - dialog_img_rect.height
    if face not in face_img_dict:
        face_img_dict[face] = pygame.image.load(f'resource/face/{face}.bmp').convert()
    return (x, y)

def drawr_dialog(screen, title, face, text, x, y):
    (x, y) = prepare_dialog(face, x, y)
    screen.blit(dialogr_bg_img, (x, y))
    screen.blit(face_img_dict[face], (x + 360, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 20, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 30, y + 30 + i * 18)

def drawl_dialog(screen, title, face, text, x, y):
    (x, y) = prepare_dialog(face, x, y)
    
    screen.blit(dialogl_bg_img, (x, y))
    screen.blit(face_img_dict[face], (x + 10, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 100, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 110, y + 30 + i * 18)

def draw_dialog(screen, title, face, text, x, y, direct="left"):
    if direct == "left":
        drawl_dialog(screen, title, face, text, x, y)
    else:
        drawr_dialog(screen, title, face, text, x, y)

def draw_selecter(screen, face, options, hoveron=None):
    # print("draw_selecter", hoveron)
    global selector_bg_img
    if selector_bg_img == None:
        selector_bg_img = pygame.image.load('resource/mark/select_dialog_bg.png').convert()
    w, h = pygame.display.get_surface().get_size()
    dialog_img_rect = selector_bg_img.get_rect()
    x = (w - dialog_img_rect.width) // 2
    y = (h - dialog_img_rect.height) // 2
    screen.blit(selector_bg_img, (x, y))
    screen.blit(face_img_dict[face], (x + 10, y + 10))
    option_rects = []
    for i, t in enumerate(options):
        if hoveron == i:
            draw_text(screen, t, 16, (0, 0, 0), x + 110, y + 30 + i * 18, fill=True)
        else:
            rect = draw_text(screen, t, 16, (0, 0, 0), x + 110, y + 30 + i * 18)
            option_rects.append(rect)

    return option_rects

def drawr_talkbubble(screen, rect):
    global speakbubble_r_img
    if speakbubble_r_img == None:
        speakbubble_r_img = pygame.image.load('resource/mark/speakbubble_right.bmp').convert()
        speakbubble_r_img.set_colorkey(COLOR_KEY)
    screen.blit(speakbubble_r_img, (rect.x + rect.width - 5, rect.y - 20))

def drawl_talkbubble(screen, rect):
    global speakbubble_r_img
    if speakbubble_r_img == None:
        speakbubble_r_img = pygame.image.load('resource/mark/speakbubble_left.bmp').convert()
        speakbubble_r_img.set_colorkey(COLOR_KEY)
    screen.blit(speakbubble_r_img, (rect.x - 20, rect.y - 20))

def drawl_talkbubble(screen, rect):
    global speakbubble_l_img
    if speakbubble_l_img == None:
        speakbubble_l_img = pygame.image.load('resource/mark/speakbubble_left.bmp').convert()
        speakbubble_l_img.set_colorkey(COLOR_KEY)
    screen.blit(speakbubble_l_img, (rect.x - 20, rect.y - 20))
    # screen.blit(face_img_dict[face], (x + 10, y + 10))

def prepare_bdialog(face, x, y):
    global bdialogr_bg_img, bdialogl_bg_img, font_name
    if bdialogr_bg_img == None:
        bdialogr_bg_img = pygame.image.load('resource/mark/bdialogr_bg.png').convert()
    if bdialogl_bg_img == None:
        bdialogl_bg_img = pygame.image.load('resource/mark/bdialogl_bg.png').convert()
    if face not in face_img_dict:
        face_img_dict[face] = pygame.image.load(f'resource/face/{face}.bmp').convert()
    
    dialog_img_rect = bdialogr_bg_img.get_rect()
    return (x - dialog_img_rect.width // 2 + FIELD_UNIT_SIZE // 2, y - dialog_img_rect.height)

def bdrawr_dialog(screen, title, face, text, x, y):
    (x, y) = prepare_bdialog(face, x, y)
    screen.blit(bdialogr_bg_img, (x, y))
    screen.blit(face_img_dict[face], (x + 360, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 20, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 30, y + 30 + i * 18)

def bdrawl_dialog(screen, title, face, text, x, y):
    (x, y) = prepare_bdialog(face, x, y)
    screen.blit(bdialogl_bg_img, (x, y))
    screen.blit(face_img_dict[face], (x + 10, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 100, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 110, y + 30 + i * 18)

# battle field dialog
def bdraw_dialog(screen, title, face, text, x, y, direct="left"):
    if direct == "left":
        bdrawl_dialog(screen, title, face, text, x, y)
    else:
        bdrawr_dialog(screen, title, face, text, x, y)

def draw_mousebox(screen, pos):
    # print("draw_mousebox", pos)
    x = FIELD_UNIT_SIZE * (pos[0] // FIELD_UNIT_SIZE)
    y = FIELD_UNIT_SIZE * (pos[1] // FIELD_UNIT_SIZE)
    # x = FIELD_UNIT_SIZE * ((pos[0] - FIELD_UNIT_SIZE / 2) // FIELD_UNIT_SIZE)
    # y = FIELD_UNIT_SIZE * ((pos[1] - FIELD_UNIT_SIZE / 2) // FIELD_UNIT_SIZE)
    # print(x, y)
    outline_rect = pygame.Rect(x, y, FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
    pygame.draw.rect(screen, COLOR_WHITE, outline_rect, 2)

def draw_miinfo(screen, pos, character, block_type, effect):
    s = pygame.Surface((MIINFO_DIALOG_WIDTH, MIINFO_DIALOG_HEIGHT), pygame.SRCALPHA) 
    # s.fill(COLOR_BLACK)    
    s.fill(MBINFO_BG_COLOR)    
    # outline_rect = pygame.Rect(0, 0, 150, 100)
    # pygame.draw.rect(s, COLOR_SILVER, outline_rect, 1)
    pygame.draw.line(s, COLOR_SILVER, (0, 0), (MIINFO_DIALOG_WIDTH, 0), 1)
    pygame.draw.line(s, COLOR_SILVER, (0, 0), (0, MIINFO_DIALOG_HEIGHT), 1)
    pygame.draw.line(s, COLOR_BLACK, (0, MIINFO_DIALOG_HEIGHT - 1), (MIINFO_DIALOG_WIDTH, MIINFO_DIALOG_HEIGHT - 1), 1)
    pygame.draw.line(s, COLOR_BLACK, (MIINFO_DIALOG_WIDTH - 1, 0), (MIINFO_DIALOG_WIDTH - 1, MIINFO_DIALOG_HEIGHT), 1)

    font = pygame.font.Font(FONT_HEITI, 17)
    font_song = pygame.font.Font(FONT_SONGTI, 17)
    font_jersey = pygame.font.Font(FONT_JERSEY, 17)
    font_sys = pygame.font.SysFont("Arial", 17, bold=True)
    text_surface = font.render(character.display_name, True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 5
    text_rect.top = 5
    s.blit(text_surface, text_rect)

    text_surface = font.render(f"{character.category_level}  等级", True, COLOR_WHITE_OPAQUE)
    text_rect2 = text_surface.get_rect()
    text_rect2.left = 85
    text_rect2.top = 5
    s.blit(text_surface, text_rect2)
    text_surface = font_sys.render(f"{character.level}", True, COLOR_WHITE_OPAQUE)
    text_rect3 = text_surface.get_rect()
    text_rect3.left = text_rect2.left + text_rect2.width + 5
    text_rect3.top = text_rect2.top
    s.blit(text_surface, text_rect3)

    tmp_img = pygame.image.load(f'resource/mark/HP.bmp').convert()
    tmp_img.set_colorkey(COLOR_KEY)
    s.blit(tmp_img, (20, 30))
    tmp_img = pygame.image.load(f'resource/mark/HP_bar.bmp').convert()
    tmp_img = pygame.transform.scale(tmp_img, (136, 8))
    tmp_img.set_colorkey(COLOR_KEY)
    s.blit(tmp_img, (50, 40))
    text_surface = font_sys.render(f"{character.HP}", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 110 - text_rect.width - 5
    text_rect.top = 30
    s.blit(text_surface, text_rect)
    text_surface = font_sys.render(f"/ {character.full_HP}", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 110
    text_rect.top = 30
    s.blit(text_surface, text_rect)
    # text_surface = font_sys.render("130 / 130", True, COLOR_WHITE)
    # text_rect = text_surface.get_rect()
    # text_rect.left = 79
    # text_rect.top = 29
    # s.blit(text_surface, text_rect)

    tmp_img = pygame.image.load(f'resource/mark/MP.bmp').convert()
    tmp_img.set_colorkey(COLOR_KEY)
    s.blit(tmp_img, (20, 55))
    tmp_img = pygame.image.load(f'resource/mark/MP_bar.bmp').convert()
    tmp_img = pygame.transform.scale(tmp_img, (136, 8))
    tmp_img.set_colorkey(COLOR_KEY)
    s.blit(tmp_img, (50, 65))
    text_surface = font_sys.render(f"{character.MP}", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 110 - text_rect.width - 5
    text_rect.top = 55
    s.blit(text_surface, text_rect)
    text_surface = font_sys.render(f"/ {character.full_MP}", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 110
    text_rect.top = 55
    s.blit(text_surface, text_rect)
    # text_surface = font_sys.render("36 / 36", True, COLOR_WHITE)
    # text_rect = text_surface.get_rect()
    # text_rect.left = 79
    # text_rect.top = 54
    # s.blit(text_surface, text_rect)


    # text_surface = font.render("7", True, COLOR_WHITE_OPAQUE)
    # text_rect = text_surface.get_rect()
    # text_rect.left = 135
    # text_rect.top = 5
    # s.blit(text_surface, text_rect)

    if character.group == 0:
        text_surface = font.render("我军", True, COLOR_ORINGE)
    elif character.group == 1:
        text_surface = font.render("敌军", True, COLOR_LIGHTBLUE)
    elif character.group == 2:
        text_surface = font.render("友军", True, COLOR_ORINGE)
    text_rect = text_surface.get_rect()
    text_rect.left = 20
    text_rect.top = 80
    s.blit(text_surface, text_rect)

    text_surface = font.render(f"{block_type}", True, COLOR_FONT_GREEN)
    text_rect = text_surface.get_rect()
    text_rect.left = 100
    text_rect.top = 80
    s.blit(text_surface, text_rect)

    text_surface = font_sys.render(f"{effect}%", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = 150
    text_rect.top = 80
    s.blit(text_surface, text_rect)

    screen_rect = screen.get_rect()
    start_x = pos[0]
    start_y = pos[1]
    if start_x < screen_rect.width // 2:
        start_x += FIELD_UNIT_SIZE * 1
    else:
        start_x -= MBINFO_DIALOG_WIDTH
    # if start_x + MBINFO_DIALOG_WIDTH + 50 > screen_rect.width:
    #     start_x = screen_rect.width - MBINFO_DIALOG_WIDTH - 50
    # elif start_x <= FIELD_UNIT_SIZE:
    #     start_x = FIELD_UNIT_SIZE

    if start_y <= FIELD_UNIT_SIZE:
        start_y = FIELD_UNIT_SIZE
    elif start_y + MIINFO_DIALOG_HEIGHT + 200 > screen_rect.height:
        start_y -= MIINFO_DIALOG_HEIGHT - FIELD_UNIT_SIZE

    # if start_y <= FIELD_UNIT_SIZE:
    #     start_y = FIELD_UNIT_SIZE
    # elif start_y + MBINFO_DIALOG_HEIGHT + 200 > screen_rect.height:
    #     start_y = screen_rect.height - MBINFO_DIALOG_HEIGHT - 200
    screen.blit(s, (start_x, start_y))


mb_type = None
buff_str = None
debuff_str = None
buff_str2 = None
debuff_str2 = None
block_img = None
firemp_img = None
watermp_img = None
earthmp_img = None
windmp_img = None
powerup_img = None
powerdown_img = None
powerup2_img = None
powerdown2_img = None
def draw_mbinfo(screen, pos, type, terrain_details):
    if type == None:
        print("Invalid type in draw_mbinfo")
        return

    global mb_type, buff_str, debuff_str, buff_str2, debuff_str2, block_img
    if mb_type != type:
        print("Refresh mbtype")
        mb_type = type
        buffs = {"+20": [], "+10": []}
        debufs = {"-20": [], "-10": []}
        for key, value in terrain_details[type]['能力效果'].items():
            # print(key, value)
            if value > 100:
                if value == 120:
                    buffs['+20'].append(key)
                elif value == 110:
                    buffs['+10'].append(key)
                # buffs.append({key: value})
            elif value < 100:
                if value == 80:
                    debufs['-20'].append(key)
                elif value == 90:
                    debufs['-10'].append(key)

        buff_str = ""
        # buff_str = "+20%"
        buff_str2 = ""
        # buff_str2 = "+10%"
        if len(buffs['+20']) > 0:
            if len(buffs['+20']) == TROOP_TYPE_NUM:
                buff_str += " 全体"
            elif len(buffs['+20']) >= 5:
                buff_str += " " + ",".join(buffs['+20'][0:5]) + "等"
            else:
                buff_str += " " + ",".join(buffs['+20'])
        if len(buffs['+10']) > 0:
            if len(buffs['+10']) == TROOP_TYPE_NUM:
                buff_str2 += " 全体"
            elif len(buffs['+10']) >= 5:
                buff_str2 += " " + ",".join(buffs['+10'][0:5]) + "等"
            else:
                buff_str2 += " " + ",".join(buffs['+10'])
        # if len(buffs['+20']) <= 0 and len(buffs['+10']) <= 0:
        #     buff_str += "无"
        debuff_str = ""
        # debuff_str = "-20%"
        debuff_str2 = ""
        # debuff_str2 = "-10%"
        if len(debufs['-20']) > 0:
            if len(debufs['-20']) == TROOP_TYPE_NUM:
                debuff_str += " 全体"
            elif len(debufs['-20']) >= 5:
                debuff_str += " " + ",".join(debufs['-20'][0:5]) + "等"
            else:
                debuff_str += " " + ",".join(debufs['-20'])
        if len(debufs['-10']) > 0:
            if len(debufs['-10']) == TROOP_TYPE_NUM:
                debuff_str2 += " 全体"
            elif len(debufs['-10']) >= 5:
                debuff_str2 += " " + ",".join(debufs['-10'][0:5]) + "等"
            else:
                debuff_str2 += " " + ",".join(debufs['-10'])
        # if len(debufs['-20']) <= 0 and len(debufs['-10']) <= 0:
        #     debuff_str += "无"
        # print(debuff_str)

        block_img = pygame.image.load(f'resource/mblock/{type}.bmp').convert()
    
        # print(buffs, debufs)
    # print(terrain_details)
    # s = pygame.Surface((150, 100)) 
    s = pygame.Surface((MBINFO_DIALOG_WIDTH, MBINFO_DIALOG_HEIGHT), pygame.SRCALPHA) 
    s.fill(MBINFO_BG_COLOR)    
    # outline_rect = pygame.Rect(0, 0, 150, 100)
    # pygame.draw.rect(s, COLOR_SILVER, outline_rect, 1)
    pygame.draw.line(s, COLOR_SILVER, (0, 0), (MBINFO_DIALOG_WIDTH, 0), 1)
    pygame.draw.line(s, COLOR_SILVER, (0, 0), (0, MBINFO_DIALOG_HEIGHT), 1)
    pygame.draw.line(s, COLOR_BLACK, (0, MBINFO_DIALOG_HEIGHT - 1), (MBINFO_DIALOG_WIDTH, MBINFO_DIALOG_HEIGHT - 1), 1)
    pygame.draw.line(s, COLOR_BLACK, (MBINFO_DIALOG_WIDTH - 1, 0), (MBINFO_DIALOG_WIDTH - 1, MBINFO_DIALOG_HEIGHT), 1)

    # global font_name
    # if font_name == None:
    #     print("")
    #     font_name = FONT_HEITI
    font = pygame.font.Font(FONT_HEITI, 17)
    text_surface = font.render(type, True, COLOR_WHITE_OPAQUE)
    text_rect = text_surface.get_rect()
    text_rect.left = 60
    text_rect.top = 5
    s.blit(text_surface, text_rect)

    font2 = pygame.font.Font(FONT_HEITI, 14)
    # print(buff_str)
    buftext_surface = font2.render(buff_str, True, COLOR_WHITE_OPAQUE)
    text_rect = text_surface.get_rect()
    text_rect.left = 25
    text_rect.top = 60
    s.blit(buftext_surface, text_rect)

    buftext_surface2 = font2.render(buff_str2, True, COLOR_WHITE_OPAQUE)
    text_rect = text_surface.get_rect()
    text_rect.left = 25
    text_rect.top = 80
    s.blit(buftext_surface2, text_rect)

    debuftext_surface = font2.render(debuff_str, True, COLOR_WHITE_OPAQUE)
    text_rect = debuftext_surface.get_rect()
    text_rect.left = 25
    text_rect.top = 100
    s.blit(debuftext_surface, text_rect)

    debuftext_surface2 = font2.render(debuff_str2, True, COLOR_WHITE_OPAQUE)
    text_rect = debuftext_surface.get_rect()
    text_rect.left = 25
    text_rect.top = 120
    s.blit(debuftext_surface2, text_rect)
    # Find buff and debuff
    
    # print(text_surface.get_size())
    s.blit(block_img, (5, 5))
    
    global firemp_img, watermp_img, earthmp_img, windmp_img, powerup_img, powerdown_img, powerup2_img, powerdown2_img
    if firemp_img == None:
        if '火系' in terrain_details[type]['适用法术']:
            firemp_img = pygame.image.load(f'resource/mp/火系.bmp').convert()
        else:
            firemp_img = pygame.image.load(f'resource/mp/火系2.bmp').convert()
    if watermp_img == None:
        if '水系' in terrain_details[type]['适用法术']:
            watermp_img = pygame.image.load(f'resource/mp/水系.bmp').convert()
        else:
            watermp_img = pygame.image.load(f'resource/mp/水系2.bmp').convert()
    if earthmp_img == None:
        if '土系' in terrain_details[type]['适用法术']:
            earthmp_img = pygame.image.load(f'resource/mp/土系.bmp').convert()
        else:
            earthmp_img = pygame.image.load(f'resource/mp/土系2.bmp').convert()
    if windmp_img == None:
        if '风系' in terrain_details[type]['适用法术']:
            windmp_img = pygame.image.load(f'resource/mp/风系.bmp').convert()
        else:
            windmp_img = pygame.image.load(f'resource/mp/风系2.bmp').convert()
    if powerup_img == None:
        powerup_img = pygame.image.load(f'resource/mp/powerup.bmp').convert()
    if powerup2_img == None:
        powerup2_img = pygame.image.load(f'resource/mp/powerup2.bmp').convert()
    if powerdown_img == None:
        powerdown_img = pygame.image.load(f'resource/mp/powerdown.bmp').convert()
    if powerdown2_img == None:
        powerdown2_img = pygame.image.load(f'resource/mp/powerdown2.bmp').convert()
    # print(buffs)
    s.blit(firemp_img, (60, 35))
    s.blit(watermp_img, (60 + 30, 35))
    s.blit(earthmp_img, (60 + 60, 35))
    s.blit(windmp_img, (60 + 90, 35))
    s.blit(powerup_img, (5, 60))
    s.blit(powerup2_img, (5, 80))
    s.blit(powerdown_img, (5, 100))
    s.blit(powerdown2_img, (5, 120))

    screen_rect = screen.get_rect()
    start_x = pos[0]
    start_y = pos[1]
    if start_x < screen_rect.width // 2:
        start_x += FIELD_UNIT_SIZE * 2
    else:
        start_x -= MBINFO_DIALOG_WIDTH - FIELD_UNIT_SIZE
    # if start_x + MBINFO_DIALOG_WIDTH + 50 > screen_rect.width:
    #     start_x = screen_rect.width - MBINFO_DIALOG_WIDTH - 50
    # elif start_x <= FIELD_UNIT_SIZE:
    #     start_x = FIELD_UNIT_SIZE

    if start_y <= FIELD_UNIT_SIZE:
        start_y = FIELD_UNIT_SIZE
    elif start_y + MBINFO_DIALOG_HEIGHT + 200 > screen_rect.height:
        start_y -= MBINFO_DIALOG_HEIGHT - 2 * FIELD_UNIT_SIZE
    else:
        start_y += FIELD_UNIT_SIZE

    # if start_y <= FIELD_UNIT_SIZE:
    #     start_y = FIELD_UNIT_SIZE
    # elif start_y + MBINFO_DIALOG_HEIGHT + 200 > screen_rect.height:
    #     start_y = screen_rect.height - MBINFO_DIALOG_HEIGHT - 200
    screen.blit(s, (start_x, start_y))
