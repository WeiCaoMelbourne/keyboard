import pygame
pygame.init()

screen = pygame.display.set_mode((640, 400))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True

background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()
caocao_img = pygame.image.load('resource/pmap/曹操.png').convert()
dialogr_bg_img = pygame.image.load('resource/mark/dialogr_bg.png').convert()
dialogl_bg_img = pygame.image.load('resource/mark/dialogl_bg.png').convert()
dialog_face_img = pygame.image.load('resource/face/曹操-1.bmp').convert()

class CaoCao(pygame.sprite.Sprite):
    def  __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = caocao_img.subsurface(0, 0, 48, 64)
        # self.image = caocao_img.subsurface(0, 0, 48, 64)
        # print(caocao_img.get_rect())
        # self.image = caocao_img.subsurface(0, 0, 48, 64)
        # self.image = pygame.transform.chop(caocao_img, (20, 20, 48, 64))
        self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 255, 255))
        self.rect = pygame.Rect(0, 0, 48, 64)
        self.rect.width = 48
        self.rect.height = 64
        self.rect.x = 300
        self.rect.y = 150
        self.speed = 2
        self.moved = 0
        self.moveimg = 1
        self.step_length = 30

        self.prev_tick = pygame.time.get_ticks()
        self.cur_pic = 0
        self.pic_direct = 1

    def update(self):
        # print("update")
        if self.rect.x < 150:
            return
        
        self.rect.y += self.speed
        self.rect.x -= self.speed
        
        now = pygame.time.get_ticks()
        # print(now, self.prev_tick)
        if now - self.prev_tick > 50:
            if self.cur_pic >= 2:
                self.pic_direct *= -1
            self.cur_pic += self.pic_direct
            if self.cur_pic <= 0:
                self.pic_direct *= -1
            
            self.prev_tick = now

        self.image = caocao_img.subsurface(0, 64 * self.cur_pic, 48, 64)
        # self.moved += self.speed * self.moveimg
        # steps = self.moved // self.step_length
        # print(self.moved, steps)
        # if steps > 2:
        #     self.moveimg *= -1
        #     self.moved -= self.step_length
        # elif self.moved <= 0:
        #     self.moveimg *= -1
        #     self.moved += self.step_length
        # self.image = caocao_img.subsurface(0, 64 * steps, 48, 64)

all_sprites = pygame.sprite.Group()
c = CaoCao()
all_sprites.add(c)
clock = pygame.time.Clock()

# font_name = 'resource/font/FangZhengShuSong-GBK-1.ttf'
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def drawr_dialog(surf, title, text, x, y):
    if x < 0 or y < 0:
        w, h = pygame.display.get_surface().get_size()
        
        if x < 0:
            x = w - x
        if y < 0:
            y = h - y

    surf.blit(dialogr_bg_img, (x, y))
    surf.blit(dialog_face_img, (x + 360, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 20, y + 5)
    draw_text(screen, text, 16, (0, 0, 0), x + 30, y + 30)

def drawl_dialog(surf, title, text, x, y):
    if x < 0 or y < 0:
        w, h = pygame.display.get_surface().get_size()
        dialog_img_rect = dialogr_bg_img.get_rect()
        # print(w, h)
        if x < 0:
            x = w + x
        if y < 0:
            y = h + y
    print(dialog_img_rect.width)        
    surf.blit(dialogl_bg_img, (x, y))
    surf.blit(dialog_face_img, (x + 10, y + 10))
    draw_text(screen, title, 17, (0, 0, 255), x + 100, y + 5)
    draw_text(screen, text, 16, (0, 0, 0), x + 110, y + 30)

# pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
act = 0
while run:
    pygame.time.delay(10) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
    # clock.tick(60)
    # print(pygame.time.get_ticks())
    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            act += 1

    # screen.blit(background_img, (100, 100), pygame.Rect(0, 0, 48, 64))

    screen.blit(background_img, (0, 0))
    # if act == 1:
    #     drawr_dialog(screen, "曹操", "测试一下曹操的对话1", 200, 200)
    # elif act == 2:
    #     drawl_dialog(screen, "曹操", "测试一下曹操的对话2", 10, -110)
    # screen.blit(dialog_bg_img, (300, 300))
    # for y in range(0, 60, 32):
    #     for x in range(0, 120, 32):
    #         screen.blit(dialog_bg_img, (x + 400, y + 300))

    # Move 曹操
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.update()

    

pygame.quit()  # If we exit the loop this will execute and close our game