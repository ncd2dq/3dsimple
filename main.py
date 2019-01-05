#Microsoft Visual C/C++ Runtime
import msvcrt
import os
import time
import sys
import math
from transpose import transposer


def get_keys():
    '''
    Asynchronous callback if key is pressed
    '''
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'H':
            return 'UP'
        elif key == b'M':
            return 'RIGHT'
        elif key == b'P':
            return 'DOWN'
        elif key == b'K':
            return 'LEFT'
        elif key == b'q':
            return 'QUIT'
        else:
            return False
    return False


def test_performance(env):
    import numpy as np
    #print string vs print array
    chars = ''.join(env)
    chars = bytes(chars, 'utf-8')
    a_chars = env
    np_chars = np.array(env)

    str_total = 0
    a_total = 0
    np_total = 0

    trials = 1000

    for i in range(trials):
        print('\rFull String------', end='')
        before = time.time()
        #os.system('cls')
        #print(chars, end='\r')
        sys.stdout.buffer.write(chars)
        after = time.time()
        str_total += after - before

        '''
        print('\rBoring Array------', end='')
        before = time.time()
        #os.system('cls')
        print(a_chars, end='')
        after = time.time()
        a_total += after - before

        print('\rNumpy Array------')
        before = time.time()
        #os.system('cls')
        print(np_chars, end='')
        after = time.time()
        np_total += after - before
        '''

    str_total /= trials
    a_total /= trials
    np_total /= trials

    print(str_total)
    print(a_total)
    print(np_total)

    #Best performance was python array, string/numpy are relatively close
    #os.system('cls') reduces run time to 0.02 (50fps) for all versions


def create_env():
    '''
    Create blueprint floorplan of environment
    '''
    env_array = [
            '############',
            '#..........#',
            '#..........#',
            '#..........#',
            '#..........#',
            '#..........#',
            '#...########',
            '##.......###',
            '##..##....##',
            '######...###',
            '######.....#',
            '######...###',
            '#..........#',
            '###..###..##',
            '##...#######',
            '##.........#',
            '##.........#',
            '############',
    ]

    env_string = '\n'.join(env_array)

    return env_array, env_string


def create_textures():
    '''
    Transform unicode string literals into byte code: b'\xe2\x96\x93' that can be read by the stdout buffer
    '''
    texture_byte_map = {
        'light_shade': bytes('░','utf-8'),
        'medium_shade': bytes('▒','utf-8'),
        'dark_shade': bytes('▓','utf-8'),
        'full_shade': bytes('█', 'utf-8'),
        'floor_close': bytes('▃', 'utf-8'),
        'floor_medium': bytes('▂', 'utf-8'),
        'floor_far': bytes('▁', 'utf-8'),
        'ceiling_close': bytes('#', 'utf-8'),
        'ceiling_medium': bytes('x', 'utf-8'),
        'ceiling_far': bytes('.', 'utf-8'),
    }

    texture_byte_map = {
        'light_shade': '░',
        'medium_shade': '▒',
        'dark_shade': '▓',
        'full_shade': '█',
        'floor_close': '▃',
        'floor_medium': '▂',
        'floor_far': '▁',
        'ceiling_close': '#',
        'ceiling_medium': 'x',
        'ceiling_far': '.', \
        'level0': '██████████████████████████████',
        'level1': '#████████████████████████████=',
        'level2': '##-▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓===',
        'level3': '##--▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓====',
        'level4': '##--.▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒_====',
        'level5': '##--..▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒__====',
        'level6': '##--...▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒___====',
        'level7': '##--....░░░░░░░░░░░░░░____====',
        'level8': '##--.....░░░░░░░░░░░░-____====',
        'level9': '##--......░░░░░░░░░░--____====',
        'level10': '##--......░░░░░░░░░---____====',
        'level11': '##--.......░░░░░░░░---____====',
    }

    return texture_byte_map


def generate_player_vision(distances, texture_map, max_distance, screen_height_res, screen_height):
    '''
    @param distances:: Python array of floating point distances between rays and walls

    Generate a string that represents the players vision. Note, each element in the array
    represents a column on the screen.

    Legal:
    a = b'xxxxx---...' + bytes('▓', 'utf-8')
    '''
    to_transpose = ''

    column_increment_heights = 2

    #{2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24}

    # NEED TO GENERATE OUTPUT AND TRANSPOSE COLUMNS
    for distance in distances:
        if distance // column_increment_heights == 0:
            to_transpose += texture_map['level0']
        elif distance // column_increment_heights == 1:
            to_transpose += texture_map['level1']
        elif distance // column_increment_heights == 2:
            to_transpose += texture_map['level2']
        elif distance // column_increment_heights == 3:
            to_transpose += texture_map['level3']
        elif distance // column_increment_heights == 4:
            to_transpose += texture_map['level4']
        elif distance // column_increment_heights == 5:
            to_transpose += texture_map['level5']
        elif distance // column_increment_heights == 6:
            to_transpose += texture_map['level6']
        elif distance // column_increment_heights == 7:
            to_transpose += texture_map['level7']
        elif distance // column_increment_heights == 8:
            to_transpose += texture_map['level8']
        elif distance // column_increment_heights == 9:
            to_transpose += texture_map['level9']
        elif distance // column_increment_heights == 10:
            to_transpose += texture_map['level10']
        elif distance // column_increment_heights == 11:
            to_transpose += texture_map['level11']
        to_transpose += '\n'

    # for row in range(screen_height_res):
    #     new_row = ''
    #     for distance in distances:
    #         if distance // column_increment_heights == 0:
    #             new_row += texture_map['level0'][row]
    #         elif distance // column_increment_heights == 1:
    #             new_row += texture_map['level1'][row]
    #         elif distance // column_increment_heights == 2:
    #             new_row += texture_map['level2'][row]
    #         elif distance // column_increment_heights == 3:
    #             new_row += texture_map['level3'][row]
    #         elif distance // column_increment_heights == 4:
    #             new_row += texture_map['level4'][row]
    #     new_row += '\n'
    #     to_transpose += new_row

    transposed = transposer(to_transpose)
    transposed = bytes(transposed, 'utf-8')
    return transposed


def main(env_array, env_string, texture_map, wall='#'):
    last_key = None

    # If resolution is 12, each 3D column will be 12 units long
    env_index_width = len(env_array[0])
    env_index_height = len(env_array)
    screen_width_resolution = 12
    screen_height_resolution = 12
    screen_width = env_index_width * screen_width_resolution
    screen_height = env_index_height * screen_height_resolution

    # Player Attributes (Angles in Degrees)
    player_visual_field_breadth = 90
    playerX = 24.0
    playerY = 12.0
    playerMoveSpeed = 2
    playerTurnSpeed = 5
    playerAngle = 0
    current_arrow = '>'

    while last_key != 'QUIT':
        map_env_array = env_array.copy()
        new_key = get_keys()

        #
        # PLAYER MOVEMENT
        #
        # Move player in direction they are facing
        if new_key == 'UP' or new_key == 'DOWN':
            # Determine amount of x / y component in direction player is facing
            angle_radians = math.radians(playerAngle)
            increment_x = math.cos(angle_radians) * playerMoveSpeed
            increment_y = math.sin(angle_radians) * playerMoveSpeed
            if new_key == 'UP':
                playerX += increment_x
                playerY += increment_y
            else:
                playerX -= increment_x
                playerY -= increment_y
        # Rotate characters visual field
        if new_key == 'LEFT':
            playerAngle -= playerTurnSpeed
        elif new_key == 'RIGHT':
            playerAngle += playerTurnSpeed

        if playerAngle > 0:
            arrow_angle = playerAngle % 360
        else:
            arrow_angle = playerAngle * -1
            arrow_angle = playerAngle % 360
            arrow_angle *= -1

        if arrow_angle < -45 and arrow_angle > -135:
            current_arrow = '^'
        elif arrow_angle < -135 and arrow_angle > -225:
            current_arrow = '<'
        elif arrow_angle < -225 and arrow_angle > -315:
            current_arrow = 'v'
        elif arrow_angle < -315:
            current_arrow = '>'

        elif arrow_angle > -45 and arrow_angle < 45:
            current_arrow = '>'
        elif arrow_angle > 45 and arrow_angle < 135:
            current_arrow = 'v'
        elif arrow_angle > 135 and arrow_angle < 225:
            current_arrow = '<'
        elif arrow_angle > 225:
            current_arrow = '^'

        #
        # RAY TRACING
        #
        # Determine distances to objects in player field
        # each distance until ray touched an object will determine 1 full column drawn
        distances = []
        ray_count = 140
        ray_angle_incrementation = player_visual_field_breadth / ray_count
        ray_distance_incrementation = 2
        ray_max_dist = screen_width
        for ray_num in range(ray_count):
            ray_x = playerX
            ray_y = playerY
            ray_angle = (
                            playerAngle
                            - (player_visual_field_breadth / 2)
                            + (ray_angle_incrementation * ray_num)
                        )

            # Increment the rays length until a collision
            ray_distance = 0
            while True:
                ray_index_x = int(ray_x // screen_width_resolution)
                ray_index_y = int(ray_y // screen_height_resolution)
                # If we hit a wall, determine distance we traveled

                if ray_index_x >= env_index_width:
                    ray_index_x = env_index_width - 1
                if ray_index_y >= env_index_height:
                    ray_index_y = env_index_height - 1

                if ray_distance >= ray_max_dist:
                    distances.append(ray_max_dist)
                    break
                elif env_array[ray_index_y][ray_index_x] == wall:
                    distances.append(ray_distance)
                    break
                else:
                    ray_distance += ray_distance_incrementation
                    ray_angle_radians = math.radians(ray_angle)
                    ray_x += math.cos(ray_angle_radians) * ray_distance
                    ray_y += math.sin(ray_angle_radians) * ray_distance

        #
        # SCREEN RENDERING
        #
        # Now we have an array of distances (@array distances) for each array
        # each distance in the array represents a column
        player_vision = generate_player_vision(distances, texture_map, ray_max_dist, screen_height_resolution, screen_height)
        last_key = new_key
        try:
            # Widnows
            os.system('cls')
        except Exception as e:
            # Mac
            os.system('clear')

        # Display player on map
        player_cord_x = int(playerX // screen_width_resolution)
        player_cord_y = int(playerY // screen_height_resolution)
        map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x] +
        'P' +
        map_env_array[player_cord_y][player_cord_x + 1:])

        # place directional arrow
        if current_arrow == '>':
            map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x+1] +
            current_arrow +
            map_env_array[player_cord_y][player_cord_x + 2:])
        elif current_arrow == '<':
            map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x-1] +
            current_arrow +
            map_env_array[player_cord_y][player_cord_x:])
        elif current_arrow == '^':
            map_env_array[player_cord_y-1] = (map_env_array[player_cord_y-1][:player_cord_x] +
            current_arrow +
            map_env_array[player_cord_y-1][player_cord_x + 1:])
        elif current_arrow == 'v':
            map_env_array[player_cord_y+1] = (map_env_array[player_cord_y+1][:player_cord_x] +
            current_arrow +
            map_env_array[player_cord_y+1][player_cord_x + 1:])


        map_byte = '\n'.join(map_env_array)
        map_byte = bytes(map_byte, 'utf-8')
        player_vision += map_byte
        player_vision += bytes(str(arrow_angle), 'utf-8')
        sys.stdout.buffer.write(player_vision)
        sys.stdout.flush()

if __name__ == '__main__':
    env_array, env_string = create_env()
    texture_map = create_textures()
    main(env_array, env_string, texture_map)

    # for i in range(5):
    #     vart = bytes(str(i), 'utf-8')
    #     sys.stdout.buffer.write(vart)
    #     sys.stdout.flush() # Flush forces the buffer to screen
    #     time.sleep(1)

# to_transpose = 'himynameisjohn\nhimynameismary'

# transposed = ''.join([''.join(i) for i in zip(*to_transpose.split('\n'))])
# print(transposed)
    input('Press <Enter> to quit')
