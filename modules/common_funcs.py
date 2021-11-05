import pygame

dialogr_bg_img = None
dialogl_bg_img = None
font_name = None
face_img_dict = {
    
}

def draw_text(screen, text, size, color, x, y):
    print("draw_text start", text)
    global font_name
    if font_name == None:
        font_name = 'resource/font/FangZhengShuSong-GBK-1.ttf'
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)

def drawr_dialog(screen, title, speaker, text, x, y):
    global dialogr_bg_img, dialogl_bg_img, font_name
    if dialogr_bg_img == None:
        dialogr_bg_img = pygame.image.load('resource/mark/dialogr_bg.png').convert()
    if dialogl_bg_img == None:
        dialogl_bg_img = pygame.image.load('resource/mark/dialogl_bg.png').convert()
    screen.blit(dialogr_bg_img, (x, y))
    if speaker not in face_img_dict:
        face_img_dict[speaker] = pygame.image.load(f'resource/face/{speaker}.bmp').convert()
    screen.blit(face_img_dict[speaker], (x + 360, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 20, y + 5)
    draw_text(screen, text, 16, (0, 0, 0), x + 30, y + 30)

def drawl_dialog(screen, title, speaker, text, x, y):
    global dialogr_bg_img, dialogl_bg_img, font_name
    if dialogr_bg_img == None:
        dialogr_bg_img = pygame.image.load('resource/mark/dialogr_bg.png').convert()
    if dialogl_bg_img == None:
        dialogl_bg_img = pygame.image.load('resource/mark/dialogl_bg.png').convert()
    screen.blit(dialogl_bg_img, (x, y))
    if speaker not in face_img_dict:
        face_img_dict[speaker] = pygame.image.load(f'resource/face/{speaker}.bmp').convert()
    screen.blit(face_img_dict[speaker], (x + 10, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 100, y + 5)
    draw_text(screen, text, 16, (0, 0, 0), x + 110, y + 30)