import pygame
from .constant import *

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
        font_name = FONT_NAME_CHN
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
    print("drawl_talkbubble here", x, y)
    
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