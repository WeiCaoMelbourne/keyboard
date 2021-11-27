import pygame
from .constant import *

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
def pre_enemies(instance, side_length, center, mp_table, visited, all_characters):
    for row in range(0, side_length):
        for col in range(0, side_length):
            if row == center and col == center:
                continue

            for name, c in all_characters.items():
                if c.row == instance.row + (row - center) and c.col == instance.col + (col - center):
                    if c.troop_group != instance.troop_group:   # From different side
                        # print("Found", name)
                        # print(c.row, c.col, row, col)
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
    side_length = instance.move_power * 2 + 1 
    mp_table = [[99 for x in range(side_length)] for y in range(side_length)]  # For every block, move power needed
    center = instance.move_power
    visited = [[0 for x in range(side_length)] for y in range(side_length)]
    queued = [[0 for x in range(side_length)] for y in range(side_length)]
    queued[center][center] = 1
    
    pre_enemies(instance, side_length, center, mp_table, visited, all_characters)
    mp_table[center][center] = 0
    visited[center][center] = 1     
    
    print(mp_table)
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
    print(mp_table)

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
                        # if c.troop_group == instance.troop_group:   # Friends
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
    print(mp_table)
    post_enemies(instance, side_length, center, mp_table, terrain_details, mblocks_info)
    print(mp_table)
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