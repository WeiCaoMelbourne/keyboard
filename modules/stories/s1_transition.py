import pygame
from ..constant import *

def s1_transition(parent_root, parent_screen, global_state, exit_func):
    
    global_state["story"] = "f1"
    background_img = pygame.image.load('resource/img/transition_grey.bmp').convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    parent_screen.blit(background_img, (0, 0))

    font = pygame.font.Font('resource/font/FangZhengShuSong-GBK-1.ttf', 80)
    # font = pygame.font.SysFont('arial', 15)
    text_surface = font.render("颖川之战", True, COLOR_WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = SCREEN_WIDTH // 2 - text_rect.width // 2
    text_rect.top = SCREEN_HEIGHT // 2 - text_rect.height // 2
    parent_screen.blit(text_surface, text_rect)

    pygame.display.update()
    parent_root.update()

    parent_root.after(1000, exit_func)

