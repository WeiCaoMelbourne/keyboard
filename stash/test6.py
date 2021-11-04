import pygame
pygame.init()

screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True

background_img = pygame.image.load('resource/mmap/1-1.bmp').convert()
caocao_img = pygame.image.load('resource/pmap/曹操.png').convert()

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

while run:
    pygame.time.delay(10) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
    # clock.tick(60)
    # print(pygame.time.get_ticks())
    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop

    # screen.blit(background_img, (100, 100), pygame.Rect(0, 0, 48, 64))

    screen.blit(background_img, (0, 0))

    # Move 曹操
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.update()

    

pygame.quit()  # If we exit the loop this will execute and close our game