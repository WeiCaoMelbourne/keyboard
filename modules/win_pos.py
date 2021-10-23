import pygame
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

def window_pos():
    hwnd = pygame.display.get_wm_info()["window"]
    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")
    GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
    # finally get our data!
    rect = GetWindowRect(hwnd)
    return (rect.left, rect.top)

