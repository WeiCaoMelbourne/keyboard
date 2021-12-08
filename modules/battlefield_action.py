import pygame
from .constant import *
import logging
import json

logger = logging.getLogger('main')

def is_inrange(pos, length):
    # print("is_inrange", pos, length)
    if pos[0] < 0 or pos[1] < 0:
        return False

    if pos[0] >= length or pos[1] >= length:
        return False
    
    return True
 
def get_min_adjacent(pos, length, mp_table):
    # print("get_min_adjacent", pos, length)
    min_value = 999
    adj_pos = (pos[0] - 1, pos[1])  # up adjacent
    if is_inrange(adj_pos, length) and mp_table[adj_pos[0]][adj_pos[1]] < min_value:
        min_value = mp_table[adj_pos[0]][adj_pos[1]]
    adj_pos = (pos[0] + 1, pos[1])  # down adjacent
    if is_inrange(adj_pos, length) and mp_table[adj_pos[0]][adj_pos[1]] < min_value:
        min_value = mp_table[adj_pos[0]][adj_pos[1]]
    adj_pos = (pos[0], pos[1] - 1)  # left adjacent
    if is_inrange(adj_pos, length) and mp_table[adj_pos[0]][adj_pos[1]] < min_value:
        min_value = mp_table[adj_pos[0]][adj_pos[1]]
    adj_pos = (pos[0], pos[1] + 1)  # right adjacent
    if is_inrange(adj_pos, length) and mp_table[adj_pos[0]][adj_pos[1]] < min_value:
        min_value = mp_table[adj_pos[0]][adj_pos[1]]
    
    return min_value

def add_adjacent_to_queue(pos, side_length, visited, BSF_q, queued):
    adj_pos = (pos[0] - 1, pos[1])  # up adjacent
    if is_inrange(adj_pos, side_length) and visited[adj_pos[0]][adj_pos[1]] == 0 \
        and queued[adj_pos[0]][adj_pos[1]] == 0:
        # print("up down", adj_pos)
        queued[adj_pos[0]][adj_pos[1]] = 1
        BSF_q.append(adj_pos)
    adj_pos = (pos[0] + 1, pos[1])  # down adjacent
    if is_inrange(adj_pos, side_length) and visited[adj_pos[0]][adj_pos[1]] == 0 \
        and queued[adj_pos[0]][adj_pos[1]] == 0:
        # print("add down", adj_pos)
        queued[adj_pos[0]][adj_pos[1]] = 1
        BSF_q.append(adj_pos)
    adj_pos = (pos[0], pos[1] - 1)  # left adjacent
    if is_inrange(adj_pos, side_length) and visited[adj_pos[0]][adj_pos[1]] == 0 \
        and queued[adj_pos[0]][adj_pos[1]] == 0:
        # print("left down", adj_pos)
        queued[adj_pos[0]][adj_pos[1]] = 1
        BSF_q.append(adj_pos)
    adj_pos = (pos[0], pos[1] + 1)  # right adjacent
    if is_inrange(adj_pos, side_length) and visited[adj_pos[0]][adj_pos[1]] == 0 \
        and queued[adj_pos[0]][adj_pos[1]] == 0:
        # print("right down", adj_pos)
        queued[adj_pos[0]][adj_pos[1]] = 1
        BSF_q.append(adj_pos)

# For all the enemies, up/down/left/right are speicals. can stay in it, but cannot cross it
def pre_enemies(instance, side_length, center, mp_table, visited, all_characters, groups):
    for row in range(0, side_length):
        for col in range(0, side_length):
            if row == center and col == center:
                continue

            for name, c in all_characters.items():
                if c.row == instance.row + (row - center) and c.col == instance.col + (col - center):
                    if instance.group in groups[c.group]['敌军'] or c.group in groups[instance.group]['敌军']:   # From different side
                        mp_table[row][col] = 999
                        visited[row][col] = 1
                        if row > 0:
                            mp_table[row - 1][col] = 999
                            visited[row - 1][col] = 1
                        if col > 0:
                            mp_table[row][col - 1] = 999
                            visited[row][col - 1] = 1
                        if row + 1 < len(mp_table):
                            mp_table[row + 1][col] = 999
                            visited[row + 1][col] = 1
                        if col + 1 < len(mp_table[0]):
                            mp_table[row][col + 1] = 999
                            visited[row][col + 1] = 1

def post_enemies(instance, side_length, center, mp_table, terrain_details, mblocks_info):
    for radius in range(instance.move_power, 0, -1):
        for row in range(0, side_length):
            for col in range(0, side_length):
                if abs(row - center) != radius and abs(col - center) != radius:
                    continue

                if row == center and col == center:
                    continue
                
                if  mp_table[row][col] == 999:
                    mbtype = mblocks_info[instance.row + (row - center)][instance.col + (col - center)]
                    current_mp = terrain_details[mbtype]['移动效果'][instance.category]
                    mp_table[row][col] = current_mp + get_min_adjacent((row, col), side_length, mp_table)

    # for row in range(0, side_length):
    #     for col in range(0, side_length):
    #         if row == center and col == center:
    #             continue
            
    #         if  mp_table[row][col] == 999:
    #             mbtype = mblocks_info[instance.row + (row - center)][instance.col + (col - center)]
    #             current_mp = terrain_details[mbtype]['移动效果'][instance.category]
    #             mp_table[row][col] = current_mp + get_min_adjacent((row, col), side_length, mp_table)

            # for name, c in all_characters.items():
            #     if c.row == instance.row + (row - center) and c.col == instance.col + (col - center):
            #         # print("Found", name)
            #         # print(c.row, c.col, row, col)
            #         if c.group != instance.group:   # From different side
            #             if row > 0:
            #                 mp_table[row - 1][col] = 999
            #             if col > 0:
            #                 mp_table[row][col - 1] = 999
            #             if row + 1 < len(mp_table):
            #                 mp_table[row + 1][col] = 999
            #             if col + 1 < len(mp_table[0]):
            #                 mp_table[row][col + 1] = 999
                        

def make_movearea(instance, terrain_details, mblocks_info, all_characters):
    logger.debug(f"make_movearea start. instance name: {instance.name}")
    with open('data/story/b1-groups.json', 'rb') as f:
        groups = json.load(f)

    side_length = instance.move_power * 2 + 1 
    mp_table = [[99 for x in range(side_length)] for y in range(side_length)]  # For every block, move power needed
    center = instance.move_power
    visited = [[0 for x in range(side_length)] for y in range(side_length)]
    queued = [[0 for x in range(side_length)] for y in range(side_length)]
    queued[center][center] = 1
    
    pre_enemies(instance, side_length, center, mp_table, visited, all_characters, groups)
    mp_table[center][center] = 0
    visited[center][center] = 1     
    
    # print(mp_table)
    BSF_q = []
    BSF_q.append((center - 1, center))  # (row, col)
    BSF_q.append((center + 1, center))
    BSF_q.append((center, center - 1))
    BSF_q.append((center, center + 1))

    while len(BSF_q) > 0:
        current = BSF_q.pop(0)
        if instance.row + (current[0] - center) < len(mblocks_info) and \
            instance.col + (current[1] - center) < len(mblocks_info[0]):
            mbtype = mblocks_info[instance.row + (current[0] - center)][instance.col + (current[1] - center)]
            current_mp = terrain_details[mbtype]['移动效果'][instance.category]
            mp_table[current[0]][current[1]] = current_mp + get_min_adjacent(current, side_length, mp_table)
        add_adjacent_to_queue(current, side_length, visited, BSF_q, queued)
        visited[current[0]][current[1]] = 1
    # print(mp_table)

    # after while loop, do another loop to cover the blocks that cannot be correctly
    # handled in while
    for radius in range(instance.move_power, 0, -1):
        for row in range(0, side_length):
            for col in range(0, side_length):
                if abs(row - center) != radius and abs(col - center) != radius:
                    continue

                if row == center and col == center:
                    continue

                occupied = False
                for name, c in all_characters.items():
                    if c.row == instance.row + (row - center) and c.col == instance.col + (col - center):
                        if instance.group in groups[c.group]['敌军'] or c.group in groups[instance.group]['敌军']:   # From different side
                            mp_table[row][col] = 99
                            occupied = True

                if occupied:
                    continue

                if mp_table[row][col] == 999:
                    continue

                if instance.row + (row - center) < len(mblocks_info) and \
                    instance.col + (col - center) < len(mblocks_info[0]):
                    mbtype = mblocks_info[instance.row + (row - center)][instance.col + (col - center)]
                    current_mp = terrain_details[mbtype]['移动效果'][instance.category]
                    mp_table[row][col] = current_mp + get_min_adjacent((row, col), side_length, mp_table)
    # print(mp_table)
    post_enemies(instance, side_length, center, mp_table, terrain_details, mblocks_info)
    # print(mp_table)
    return mp_table

def draw_movearea(screen, instance, shift, mp_table):
    # with codecs.open('data/troop-category-levels.csv', "r", "utf-8") as csvfile:
    #     categorylevel_info = list(csv.reader(csvfile, delimiter=','))

    # print(categorylevel_info)
    # print(subcategoy_info)
    # print(instance.x, instance.y)

    # rows = move_power // 2
    # cols = move_power - rows
    side_length = len(mp_table)
    center = side_length // 2
    for row in range(0, side_length):
        for col in  range(0, side_length):
            if mp_table[row][col] > instance.move_power or mp_table[row][col] <= 0:
                continue
            
            s = pygame.Surface((FIELD_UNIT_SIZE, FIELD_UNIT_SIZE), pygame.SRCALPHA) 
            s.fill(MOVE_BG_COLOR)
            screen.blit(s, ((instance.col - center + col)* FIELD_UNIT_SIZE + shift[0], (instance.row - center + row) * FIELD_UNIT_SIZE + shift[1]))


hitsqure_img = None
def draw_hitsqure(screen, pos):
    global hitsqure_img
    if hitsqure_img == None:
        hitsqure_img = pygame.image.load(f'resource/hitarea/square.png').convert()
    # tmp_img.set_colorkey(COLOR_KEY)
    screen.blit(hitsqure_img, pos)

def draw_attack(screen, instance, shift):
    # s = pygame.Surface((FIELD_UNIT_SIZE, FIELD_UNIT_SIZE), pygame.SRCALPHA) 
    # s.fill(HITAREA_BG_COLOR)
    # screen.blit(s, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
    # rect = pygame.Rect((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1], FIELD_UNIT_SIZE, FIELD_UNIT_SIZE)
    # pygame.draw.rect(screen, HITAREA_BG_COLOR, rect, 10)

    # pygame.draw.line(screen, HITAREA_BG_COLOR, 
    #     ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]), 
    #     ((instance.col + 2)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))

    # tmp_img = pygame.image.load(f'resource/hitarea/square.png').convert()
    # # tmp_img.set_colorkey(COLOR_KEY)
    # screen.blit(tmp_img, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
    if instance.hit_area == 'A':
        draw_hitsqure(screen, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col - 1)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row - 1) * FIELD_UNIT_SIZE + shift[1]))
    elif instance.hit_area == 'B':
        draw_hitsqure(screen, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col + 1)* FIELD_UNIT_SIZE + shift[0], (instance.row - 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row - 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col - 1)* FIELD_UNIT_SIZE + shift[0], (instance.row + 1) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col - 1)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col - 1)* FIELD_UNIT_SIZE + shift[0], (instance.row - 1) * FIELD_UNIT_SIZE + shift[1]))
    elif instance.hit_area == 'E':
        draw_hitsqure(screen, ((instance.col + 2)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col - 2)* FIELD_UNIT_SIZE + shift[0], (instance.row) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row + 2) * FIELD_UNIT_SIZE + shift[1]))
        draw_hitsqure(screen, ((instance.col)* FIELD_UNIT_SIZE + shift[0], (instance.row - 2) * FIELD_UNIT_SIZE + shift[1]))

# convert a (row, col) on map to (row, col) in a array centered instance,
# array size is instance.move_power * 2 + 1
def convert_mappos_to_centralpos(instance, map_pos):
    center = instance.move_power
    row_central = center + map_pos[0] - instance.row 
    col_central = center + map_pos[1] - instance.col
    return (row_central, col_central)

def convert_centralpos_to_mappos(instance, central_pos):
    center = instance.move_power
    row_map = instance.row  + central_pos[0] - center
    col_map = instance.col  + central_pos[1] - center
    return (row_map, col_map)

def find_prev_step(pos, side_length, moveable_area):
    adj_pos = (pos[0] - 1, pos[1])  # up adjacent
    min_gap = 999
    if is_inrange(adj_pos, side_length) and moveable_area[adj_pos[0]][adj_pos[1]] < moveable_area[pos[0]][pos[1]] \
        and moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]] < min_gap:
        min_gap = moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]]
        next_step = adj_pos
    
    adj_pos = (pos[0] + 1, pos[1])  # down adjacent
    if is_inrange(adj_pos, side_length) and moveable_area[adj_pos[0]][adj_pos[1]] < moveable_area[pos[0]][pos[1]] \
        and moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]] < min_gap:
        min_gap = moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]]
        next_step = adj_pos

    adj_pos = (pos[0], pos[1] - 1)  # left adjacent
    if is_inrange(adj_pos, side_length) and moveable_area[adj_pos[0]][adj_pos[1]] < moveable_area[pos[0]][pos[1]] \
        and moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]] < min_gap:
        min_gap = moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]]
        next_step = adj_pos

    adj_pos = (pos[0], pos[1] + 1)  # right adjacent
    if is_inrange(adj_pos, side_length) and moveable_area[adj_pos[0]][adj_pos[1]] < moveable_area[pos[0]][pos[1]] \
        and moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]] < min_gap:
        min_gap = moveable_area[pos[0]][pos[1]] - moveable_area[adj_pos[0]][adj_pos[1]]
        next_step = adj_pos

    return next_step
    

def findpath(instance, target, moveable_area):
    logger.debug(f"{__name__} start")

    path = []
    step = target
    path.append(step)
    side_length = instance.move_power * 2 + 1 
    while step[0] != instance.row or step[1] != instance.col:
        central_pos = convert_mappos_to_centralpos(instance, step)
        next_central = find_prev_step(central_pos, side_length, moveable_area)
        step = convert_centralpos_to_mappos(instance, next_central)
        path.append(step)

    # print(path)
    path.reverse()
    # print(path)
    return path

    # # Depth-first 
    # stack = []
    # links = {}
    # stack.append((instance.row, instance.col))
    # side_length = instance.move_power * 2 + 1 
    # visited = [[0 for x in range(side_length)] for y in range(side_length)]
    # center = instance.move_power
    # visited[center][center] = 1

    # while len(stack) > 0:
    #     cur_pos = stack.pop()
    #     if cur_pos[0] == target[0] and cur_pos[1] == target[1]:
    #         print("Found")
    #         break

    #     if cur_pos[0] == 11 and cur_pos[1] == 8:
    #         print("handling 11, 8")
    #     visited[center + cur_pos[0] - instance.row][center + cur_pos[1] - instance.col] = 1
        
    #     # up
    #     tmp_pos = (cur_pos[0] - 1, cur_pos[1])
    #     row_in_ma = center + tmp_pos[0] - instance.row 
    #     col_in_ma = center + tmp_pos[1] - instance.col
    #     if is_inrange((row_in_ma, col_in_ma), side_length) and visited[row_in_ma][col_in_ma] == 0 and \
    #         moveable_area[row_in_ma][col_in_ma] < instance.move_power:
    #         # visited[row_in_ma][col_in_ma] = 1
    #         stack.append(tmp_pos)
    #         links[(tmp_pos[0], tmp_pos[1])] = (cur_pos[0], cur_pos[1])
    #         if cur_pos[0] == 11 and cur_pos[1] == 8:
    #             print("add up")
        
    #     # down
    #     tmp_pos = (cur_pos[0] + 1, cur_pos[1])
    #     row_in_ma = center + tmp_pos[0] - instance.row 
    #     col_in_ma = center + tmp_pos[1] - instance.col
    #     if is_inrange((row_in_ma, col_in_ma), side_length) and visited[row_in_ma][col_in_ma] == 0 and \
    #         moveable_area[row_in_ma][col_in_ma] < instance.move_power:
    #         # visited[row_in_ma][col_in_ma] = 1
    #         stack.append(tmp_pos)
    #         links[(tmp_pos[0], tmp_pos[1])] = (cur_pos[0], cur_pos[1])
    #         if cur_pos[0] == 11 and cur_pos[1] == 8:
    #             print("add down")

    #     # left
    #     tmp_pos = (cur_pos[0], cur_pos[1] - 1)
    #     row_in_ma = center + tmp_pos[0] - instance.row 
    #     col_in_ma = center + tmp_pos[1] - instance.col
    #     if is_inrange((row_in_ma, col_in_ma), side_length) and visited[row_in_ma][col_in_ma] == 0 and \
    #         moveable_area[row_in_ma][col_in_ma] < instance.move_power:
    #         # visited[row_in_ma][col_in_ma] = 1
    #         stack.append(tmp_pos)
    #         links[(tmp_pos[0], tmp_pos[1])] = (cur_pos[0], cur_pos[1])
    #         if cur_pos[0] == 11 and cur_pos[1] == 8:
    #             print("add left")

    #     # right
    #     tmp_pos = (cur_pos[0], cur_pos[1] + 1)
    #     row_in_ma = center + tmp_pos[0] - instance.row 
    #     col_in_ma = center + tmp_pos[1] - instance.col
    #     if is_inrange((row_in_ma, col_in_ma), side_length) and visited[row_in_ma][col_in_ma] == 0 and \
    #         moveable_area[row_in_ma][col_in_ma] < instance.move_power:
    #         # visited[row_in_ma][col_in_ma] = 1
    #         stack.append(tmp_pos)
    #         links[(tmp_pos[0], tmp_pos[1])] = (cur_pos[0], cur_pos[1])
    #         if cur_pos[0] == 11 and cur_pos[1] == 8:
    #             print("add right")

    # path = []
    # path.append(target)
    # temp_pos = target
    # while True:
    #     # print("temp_pos", temp_pos)
    #     prev = links[temp_pos]
    #     # print("prev", prev)
    #     path.append(prev)
    #     if prev[0] == instance.row and prev[1] == instance.col:
    #         break
    #     temp_pos = prev

    # print(path)
    # path.reverse()
    # print(path)
    # return path