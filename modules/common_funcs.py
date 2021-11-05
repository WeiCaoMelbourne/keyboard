import pygame

dialogr_bg_img = None
dialogl_bg_img = None
font_name = None
selector_bg_img = None
face_img_dict = {
    
}

def draw_text(screen, text, size, color, x, y):
    global font_name
    if font_name == None:
        font_name = 'resource/font/FangZhengShuSong-GBK-1.ttf'
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)

def prepare_dialog(speaker, x, y):
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
    if speaker not in face_img_dict:
        face_img_dict[speaker] = pygame.image.load(f'resource/face/{speaker}.bmp').convert()
    return (x, y)

def drawr_dialog(screen, title, speaker, text, x, y):
    (x, y) = prepare_dialog(speaker, x, y)
    screen.blit(dialogr_bg_img, (x, y))
    screen.blit(face_img_dict[speaker], (x + 360, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 20, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 30, y + 30 + i * 18)

def drawl_dialog(screen, title, speaker, text, x, y):
    (x, y) = prepare_dialog(speaker, x, y)
    screen.blit(dialogl_bg_img, (x, y))
    screen.blit(face_img_dict[speaker], (x + 10, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 100, y + 5)
    texts = text.split("\n")
    for i, t in enumerate(texts):
        draw_text(screen, t, 16, (0, 0, 0), x + 110, y + 30 + i * 18)

def draw_dialog(screen, title, speaker, text, x, y, direct="left"):
    if direct == "left":
        drawl_dialog(screen, title, speaker, text, x, y)
    else:
        drawr_dialog(screen, title, speaker, text, x, y)

def drawe_selecter(screen, title, options):
    global selector_bg_img
    if selector_bg_img == None:
        selector_bg_img = pygame.image.load('resource/mark/select_dialog_bg.png').convert()
    w, h = pygame.display.get_surface().get_size()
    dialog_img_rect = selector_bg_img.get_rect()
    x = (w - dialog_img_rect.width) // 2
    y = (h - dialog_img_rect.height) // 2
    screen.blit(dialogl_bg_img, (x, y))