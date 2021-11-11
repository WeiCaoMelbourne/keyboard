

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

